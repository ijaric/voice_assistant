import asyncio
import logging
import uuid

import langchain.agents
import langchain.agents.format_scratchpad
import langchain.agents.output_parsers
import langchain.chat_models
import langchain.prompts
import langchain.schema.agent
import langchain.schema.messages
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

    async def process_request(self, request: str, chat_history: list[langchain.schema.messages.Message]) -> str:
        llm = langchain.chat_models.ChatOpenAI(temperature=0.7, openai_api_key=self.settings.openai.api_key)
        tools = [self.tools.get_movie_by_description, self.tools.get_movie_by_id, self.tools.get_similar_movies]

        chat_history = []
        chat_history_name = f"{chat_history=}".partition("=")[0]
        prompt = langchain.prompts.ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are very powerful assistant. If you are asked about movies you will you provided functions.",
                ),
                langchain.prompts.MessagesPlaceholder(variable_name=chat_history_name),
                ("user", "{input}"),
                langchain.prompts.MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm_with_tools = llm.bind(
            functions=[langchain.tools.render.format_tool_to_openai_function(tool) for tool in tools]
        )

        chat_history = []

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

        agent_executor = langchain.agents.AgentExecutor(agent=agent, tools=tools, verbose=True)

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
