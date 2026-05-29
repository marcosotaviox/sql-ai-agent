# 🦘 SQL AI Agent — ABS Australian Labour Force Data

Natural language → SQL → insights. Built with LangGraph ReAct agents and Claude, querying ABS-style Australian labour market data.

## Features

- **ReAct Agent reasoning** — Thought → Action → Observation loop
- **ABS Labour Force data** — employment, wages, and population across all Australian states
- **Read-only safety** — destructive SQL operations are blocked at the agent layer
- **Schema-aware** — agent inspects the database schema automatically before querying
- **Example queries** — pre-built questions to demonstrate multi-table reasoning

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude (`claude-sonnet-4-5`) via `langchain-anthropic` |
| Agent | LangGraph `create_react_agent` + `SQLDatabaseToolkit` |
| Database | SQLite via SQLAlchemy |
| UI | Streamlit |

## Quick Start

# 1. Clone and install
    git clone https://github.com/YOUR_USERNAME/sql-ai-agent
    cd sql-ai-agent

    # 2. Create and activate virtual environment
    py -3.11 -m venv venv
    venv\Scripts\activate

    # 3. Install dependencies
    pip install -r requirements.txt

    # 4. Configure environment
    cp .env.example .env
    # Add your ANTHROPIC_API_KEY to .env

    # 5. Seed the database
    python data/seed_db.py

    # 6. Run the app
    python -m streamlit run app.py

## Project Structure

    sql-agent/
    ├── app.py                  # Streamlit entrypoint
    ├── data/
    │   ├── seed_db.py          # ABS data seeder
    │   └── abs_labour.db       # SQLite database (git-ignored)
    ├── src/
    │   ├── core/
    │   │   └── agent.py        # LangGraph agent + query runner
    │   ├── ui/
    │   │   ├── sidebar.py      # Schema + example queries
    │   │   └── chat.py         # Chat interface
    │   └── utils/
    │       └── session.py      # Streamlit session state
    └── requirements.txt

## Example Queries

- *Which state had the highest unemployment rate in 2024-Q2?*
- *Compare wage growth across industries in 2023.*
- *What are the top 3 industries by employment in Victoria?*
- *Show the unemployment trend in NSW from 2022 to 2024.*
- *Which industry had the fastest wage growth in 2023-Q4?*

## Data Source

Data is synthetically generated to reflect ABS Labour Force Survey patterns.
For production use, replace `seed_db.py` with real ABS CSV imports from [abs.gov.au](https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia).

## Author

Built by Marcos Otavio — [LinkedIn](https://www.linkedin.com/in/marcosotavio) · [GitHub](https://github.com/marcosotaviox)