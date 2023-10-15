import asyncio
import logging
import typing
import uuid

import fastapi
import langchain.agents
import langchain.agents.format_scratchpad
import langchain.agents.output_parsers
import langchain.chat_models
import langchain.prompts
import langchain.schema
import langchain.tools.render
import langchain.memory
import langchain.memory.chat_memory

import lib.models as models
import lib.agent.openai_functions as openai_functions
import lib.app.settings as app_settings
import lib.agent.chat_repository as _chat_repository


class AgentService:
    def __init__(
        self,
        settings: app_settings.Settings,
        tools: openai_functions.OpenAIFunctions,
        chat_repository: _chat_repository.ChatHistoryRepository,
    ) -> None:
        self.settings = settings
        self.tools = tools
        self.llm = langchain.chat_models.ChatOpenAI(
            temperature=self.settings.openai.agent_temperature,
            openai_api_key=self.settings.openai.api_key.get_secret_value()
        )
        self.chat_repository = chat_repository
        self.logger = logging.getLogger(__name__)

    async def get_chat_session_id(self, request: models.RequestLastSessionId) -> uuid.UUID:
        session_id = self.chat_repository.get_last_session_id(request)
        if not session_id:
            session_id = uuid.uuid4()
        return session_id

    async def artem_process_request(self, request: models.AgentCreateRequestModel) -> models.AgentCreateResponseModel:
        # Get session ID
        session_request = models.RequestLastSessionId(
            channel=request.channel,
            user_id=request.user_id,
            minutes_ago=3
        )
        session_id = await self.chat_repository.get_last_session_id(session_request)
        if not session_id:
            print("NO PREVIOUS CHATS")
            session_id = uuid.uuid4()
        print("FOUND CHAT:", )
        print("SID:", session_id)

        tools = [
            langchain.tools.Tool(
                name="GetMovieByDescription",
                func=self.tools.get_movie_by_description,
                coroutine=self.tools.get_movie_by_description,
                description="Get a movie by description"
            ),
        ]

        llm = langchain.chat_models.ChatOpenAI(temperature=self.settings.openai.agent_temperature, openai_api_key=self.settings.openai.api_key.get_secret_value())

        # chat_history = langchain.memory.ChatMessageHistory()
        chat_history = []
        chat_history_name = f"{chat_history=}".partition("=")[0]

        request_chat_history = models.RequestChatHistory(session_id=session_id)
        chat_history_source = await self.chat_repository.get_messages_by_sid(request_chat_history)
        chat_history.append(langchain.schema.HumanMessage(content="Hi there!"))
        for entry in chat_history_source:
            print("ENTRY: ", entry)
            if entry.content["role"] == "user":
                chat_history.append(langchain.schema.HumanMessage(content=entry.content["content"]))
            elif entry.content["role"] == "agent":
                chat_history.append(langchain.schema.AIMessage(content=entry.content["content"]))

        # memory = langchain.memory.ConversationBufferMemory(memory_key=chat_history_name,chat_memory=chat_history)

        print("CHAT HISTORY:", chat_history)

        prompt = langchain.prompts.ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Act as an advanced AI assistant with extensive capabilities, you have a vast knowledge base about movies and their related aspects. If you are asked about a movie, please use provided functions to retrive data about movies. You can receive a question in any language. Translate it into English. If you don't know the answer, just say that you don't know, don't try to make up an answer. Be concise. ",
                ),
                langchain.prompts.MessagesPlaceholder(variable_name=chat_history_name),
                ("user", "{input}"),
                langchain.prompts.MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm_with_tools = llm.bind(
            functions=[langchain.tools.render.format_tool_to_openai_function(tool) for tool in tools]
        )

        agent = (
            {
                "input": lambda _: _["input"],
                "agent_scratchpad": lambda _: langchain.agents.format_scratchpad.format_to_openai_functions(
                    _["intermediate_steps"]
                ),
                "chat_history": lambda _: _["chat_history"],
            }
            | prompt
            | llm_with_tools
            | langchain.agents.output_parsers.OpenAIFunctionsAgentOutputParser()
        )

        print("AGENT:", agent)

        agent_executor = langchain.agents.AgentExecutor(agent=agent, tools=tools, verbose=True)
        print("CH:", type(chat_history), chat_history)
        response = await agent_executor.ainvoke({"input": request.text, "chat_history": chat_history})
        print("AI RESPONSE:", response)
        user_request = models.RequestChatMessage(
            session_id=session_id,
            user_id=request.user_id,
            channel=request.channel,
            message={"role": "user", "content": request.text}
        )
        ai_response = models.RequestChatMessage(
            session_id=session_id,
            user_id=request.user_id,
            channel=request.channel,
            message={"role": "assistant", "content": response["output"]}
        )

        await self.chat_repository.add_message(user_request)
        await self.chat_repository.add_message(ai_response)

        return response


    # TODO: Добавить запрос для процессинга запроса с памятью+
    # TODO: Улучшить промпт+
    # TODO: Возможно, надо добавить Chain на перевод


    async def process_request(self, request: models.AgentCreateRequestModel) -> models.AgentCreateResponseModel:

        result = await self.tools.get_movie_by_description(request.text)

        if len(result) == 0:
            raise fastapi.HTTPException(status_code=404, detail="Movies not found")

        # llm = langchain.chat_models.ChatOpenAI(
        #     temperature=self.settings.openai.agent_temperature,
        #     openai_api_key=self.settings.openai.api_key.get_secret_value()
        # )

        content_films = "\n".join(film.get_movie_info_line() for film in result)

        system_prompt = (
            "You are a cinema expert. "
            f"Here are the movies I found for you: {content_films}"
            "Listen to the question and answer it based on the information above."
        )

        prompt = langchain.prompts.ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
            ]
        )
        chain = prompt | self.llm
        response = await chain.ainvoke({"input": request.text})
        response_model = models.AgentCreateResponseModel(text=response.content)
        return response_model


async def main():
    import lib.agent.repositories as agent_repositories
    import lib.clients as clients

    postgres_client = clients.AsyncPostgresClient(app_settings.Settings())
    embedding_repository = agent_repositories.EmbeddingRepository(app_settings.Settings())
    chat_repository = _chat_repository.ChatHistoryRepository(postgres_client.get_async_session())

    agent_service = AgentService(
        settings=app_settings.Settings(),
        tools=openai_functions.OpenAIFunctions(
            repository=embedding_repository,
            pg_async_session=postgres_client.get_async_session(),
        ),
        chat_repository=chat_repository
    )

    # question = "What is the movie about a famous country singer meet a talented singer and songwriter who works as a waitress?"
    request_1  = models.AgentCreateRequestModel(
        channel="telegram",
        user_id="123",
        text="What is the movie about a famous country singer meet a talented singer and songwriter who works as a waitress?"
    )
    request_2  = models.AgentCreateRequestModel(
        channel="telegram",
        user_id="123",
        text="So what is the rating of the movie? Do you recommend it?"
    )
    request_3  = models.AgentCreateRequestModel(
        channel="telegram",
        user_id="123",
        text="What are the similar movies?"
    )

    response = await agent_service.artem_process_request(request_1)
    response = await agent_service.artem_process_request(request_2)
    response = await agent_service.artem_process_request(request_3)




    # response = await agent_service.artem_process_request(question)
    # question = "Highly Rated Titanic Movies"
    # request = models.AgentCreateRequestModel(text=question)
    # film_results = await agent_service.process_request(request=request)

    # result = [agent_service.tools.get_movie_by_id(id=film.id) for film in film_results]

    # agent_executor = langchain.agents.AgentExecutor(agent=agent, tools=tools, verbose=True)
    #
    # # first_question = "What is the movie where halfling bring the ring to the volcano?"
    # first_question = (
    #     "What is the movie about a famous country singer meet a talented singer and songwriter who works as a waitress?"
    # )
    # second_question = "So what is the rating of the movie? Do you recommend it?"
    # third_question = "What are the similar movies?"
    # first_result = await agent_executor.ainvoke({"input": first_question, "chat_history": chat_history})
    # chat_history.append(langchain.schema.messages.HumanMessage(content=first_question))
    # chat_history.append(langchain.schema.messages.AIMessage(content=first_result["output"]))
    # second_result = await agent_executor.ainvoke({"input": second_question, "chat_history": chat_history})
    # chat_history.append(langchain.schema.messages.HumanMessage(content=second_question))
    # chat_history.append(langchain.schema.messages.AIMessage(content=second_result["output"]))
    # final_result = await agent_executor.ainvoke({"input": third_question, "chat_history": chat_history})


if __name__ == "__main__":
    asyncio.run(main())
