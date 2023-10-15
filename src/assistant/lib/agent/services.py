import logging
import uuid

import langchain.agents
import langchain.agents.format_scratchpad
import langchain.agents.output_parsers
import langchain.chat_models
import langchain.memory
import langchain.memory.chat_memory
import langchain.prompts
import langchain.schema
import langchain.tools.render

import lib.agent.repositories as lib_agent_repositories
import lib.agent.repositories.chat_repository as chat_repositories
import lib.app.settings as app_settings
import lib.models as models


class AgentService:
    def __init__(
        self,
        settings: app_settings.Settings,
        chat_repository: chat_repositories.ChatHistoryRepository,
        tools: lib_agent_repositories.OpenAIFunctions,
    ) -> None:
        self.settings = settings
        self.tools = tools
        self.chat_repository = chat_repository
        self.logger = logging.getLogger(__name__)

    async def process_request(self, request: models.AgentCreateRequestModel) -> models.AgentCreateResponseModel:
        # Get session ID
        session_request = models.RequestLastSessionId(channel=request.channel, user_id=request.user_id, minutes_ago=3)
        session_id = await self.chat_repository.get_last_session_id(session_request)
        if not session_id:
            session_id = uuid.uuid4()

        # Declare tools (OpenAI functions)
        tools = [
            langchain.tools.Tool(
                name="GetMovieByDescription",
                func=self.tools.get_movie_by_description,
                coroutine=self.tools.get_movie_by_description,
                description="Get a movie by description",
            ),
        ]

        llm = langchain.chat_models.ChatOpenAI(
            temperature=self.settings.openai.agent_temperature,
            openai_api_key=self.settings.openai.api_key.get_secret_value(),
        )

        chat_history = []
        chat_history_name = f"{chat_history=}".partition("=")[0]

        request_chat_history = models.RequestChatHistory(session_id=session_id)
        chat_history_source = await self.chat_repository.get_messages_by_sid(request_chat_history)
        if not chat_history_source:
            for entry in chat_history_source:
                if entry.role == "user":
                    chat_history.append(langchain.schema.HumanMessage(content=entry.content))
                elif entry.role == "agent":
                    chat_history.append(langchain.schema.AIMessage(content=entry.content))

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

        agent_executor = langchain.agents.AgentExecutor(agent=agent, tools=tools, verbose=False)
        chat_history = []  # temporary disable chat_history
        response = await agent_executor.ainvoke({"input": request.text, "chat_history": chat_history})

        user_request = models.RequestChatMessage(
            session_id=session_id,
            user_id=request.user_id,
            channel=request.channel,
            message={"role": "user", "content": request.text},
        )
        ai_response = models.RequestChatMessage(
            session_id=session_id,
            user_id=request.user_id,
            channel=request.channel,
            message={"role": "assistant", "content": response["output"]},
        )

        await self.chat_repository.add_message(user_request)
        await self.chat_repository.add_message(ai_response)

        print("RES:", response)

        return models.AgentCreateResponseModel(text="response")
