import asyncio
import logging
import uuid

import fastapi
import langchain.agents
import langchain.agents.format_scratchpad
import langchain.agents.output_parsers
import langchain.chat_models
import langchain.prompts
import langchain.schema
import langchain.tools.render

import assistant.lib.models.movies as movies
import lib.agent.openai_functions as openai_functions
import lib.app.settings as app_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentService:
    def __init__(self, settings: app_settings.Settings, tools: openai_functions.OpenAIFunctions) -> None:
        self.settings = settings
        self.tools = tools

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


        return await agent_executor.ainvoke({"input": first_question, "chat_history": chat_history})


# async def main():
#     agent_executor = langchain.agents.AgentExecutor(agent=agent, tools=tools, verbose=True)

#     # first_question = "What is the movie where halfling bring the ring to the volcano?"
#     first_question = (
#         "What is the movie about a famous country singer meet a talented singer and songwriter who works as a waitress?"
#     )
#     second_question = "So what is the rating of the movie? Do you recommend it?"
#     third_question = "What are the similar movies?"
#     first_result = await agent_executor.ainvoke({"input": first_question, "chat_history": chat_history})
#     chat_history.append(langchain.schema.messages.HumanMessage(content=first_question))
#     chat_history.append(langchain.schema.messages.AIMessage(content=first_result["output"]))
#     second_result = await agent_executor.ainvoke({"input": second_question, "chat_history": chat_history})
#     chat_history.append(langchain.schema.messages.HumanMessage(content=second_question))
#     chat_history.append(langchain.schema.messages.AIMessage(content=second_result["output"]))
#     final_result = await agent_executor.ainvoke({"input": third_question, "chat_history": chat_history})


# if __name__ == "__main__":
#     asyncio.run(main())
