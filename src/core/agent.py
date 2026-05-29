"""
src/core/agent.py
==================
SQL AI Agent using LangChain's SQLDatabaseToolkit + Claude.
Implements ReAct reasoning: Thought → Action → Observation loop.
"""

from pathlib import Path
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain.prompts import PromptTemplate


_BLOCKED_KEYWORDS = {"DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE", "CREATE"}

DB_PATH = Path(__file__).parent.parent.parent / "data" / "abs_labour.db"

SYSTEM_PROMPT = """You are an expert data analyst specialising in Australian labour market data.
You have access to a SQLite database containing ABS (Australian Bureau of Statistics) Labour Force data.

Tables available:
- labour_force: employment by quarter, state, industry (employed_thousands, unemployment_rate, participation_rate)
- wage_growth: wage price index and annual growth by quarter and industry
- state_population: population, interstate and overseas migration by state and year

Rules:
1. Always inspect the schema before writing queries.
2. Write efficient SQL — use aggregations, GROUP BY, ORDER BY appropriately.
3. When asked for comparisons or trends, use multiple queries if needed.
4. Format numbers clearly: round percentages to 1 decimal, thousands to whole numbers.
5. Always contextualise your answer — mention what the data means for Australia.
6. If a query returns no results, explain why and suggest an alternative.

{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


def build_agent(api_key: str) -> AgentExecutor:
    """
    Initialise and return a LangChain AgentExecutor connected to the ABS database.
    """
    llm = ChatAnthropic(
        model="claude-sonnet-4-5",
        anthropic_api_key=api_key,
        temperature=0,
        max_tokens=2048,
    )

    db = SQLDatabase.from_uri(
        f"sqlite:///{DB_PATH}",
        sample_rows_in_table_info=3,
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        return_intermediate_steps=True,
    )


def run_query(executor: AgentExecutor, question: str) -> dict:
    """
    Execute a natural language question against the ABS database.
    """
    try:
        result = executor.invoke({"input": question})
        return {
            "answer": result.get("output", "No answer returned."),
            "steps": result.get("intermediate_steps", []),
            "error": None,
        }
    except ValueError as e:
        return {"answer": "", "steps": [], "error": str(e)}
    except Exception as e:
        return {
            "answer": "",
            "steps": [],
            "error": f"Agent error: {str(e)}",
        }