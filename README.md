# Arison-X

**Agentic Financial Research Platform** using **Model Context Protocol (MCP)**, **Graph-RAG**, and **LangGraph** for automated stock analysis and backtesting.

![Arison-X Architecture](https://placehold.co/1200x400/101010/FFFFFF/png?text=Arison-X+Agentic+Architecture)
*(Note: Replace with actual architecture diagram)*

## 🚀 Overview

Arison-X is an advanced, autonomous financial research system designed to democratize high-frequency-style data analysis for retail investors. By leveraging a multi-agent architecture, it autonomously aggregates market data, performs technical and fundamental analysis, and executes backtesting strategies with minimal human intervention.

Built with a focus on **modularity** and **scalability**, Arison-X demonstrates the power of composable AI systems in financial tech.

## 🛠 Tech Stack

- **Core Logic**: Python 3.10+
- **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/) (Stateful multi-agent workflows)
- **Data Integration**: [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) (Standardized server-client tool interface)
- **Knowledge Retrieval**: Graph-RAG (Graph-based Retrieval Augmented Generation)
- **Vector Database**: ChromaDB / Pinecone (for semantic search of financial reports)
- **API Management**: FastAPI (Server)

## ✨ Key Features

- **Multi-Agent Collaboration**: Specialized agents for *Data Retrieval*, *Technical Analysis*, *Sentiment Analysis*, and *Backtesting* work in concert.
- **MCP Server Architecture**: Decoupled tools ensure that data sources (Yahoo Finance, Alpha Vantage) can be swapped without rewriting agent logic.
- **Graph-RAG Memory**: Maintains a knowledge graph of stock relationships and historical context to improve reasoning capabilities over time.
- **Automated Backtesting**: A dedicated engine simulating thousands of trading scenarios to validate agent generated strategies.

## 📂 Project Structure

```bash
Arison-X/
├── src/
│   ├── agents/          # LangGraph agent definitions
│   ├── equipment/       # Shared utilities & tools
│   ├── server.py        # Main MCP server entry point
│   ├── tools/           # Market data & analysis tools
│   └── backtest/        # Backtesting engine
├── data/                # Local data cache
├── requirements.txt     # Dependency definitions
└── README.md            # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/a-rison/Arison-X.git
   cd Arison-X
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   OPENAI_API_KEY=sk-...
   ALPHA_VANTAGE_KEY=...
   ```

### Usage

**Running the MCP Server**:
```bash
python src/server.py
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any features or bug fixes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
