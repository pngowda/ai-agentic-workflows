# LangGraph Chatbot with Extensible Tool Integration

This project demonstrates a conversational AI chatbot using [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and [Gradio](https://gradio.app/), designed with a **generic tool integration framework**. The chatbot supports tools like Google Serper for web search and can be easily extended to integrate with services such as Jira, custom APIs, and more.

## Features

- **Conversational AI**: Powered by LangGraph and OpenAI's GPT-4o-mini (or Azure OpenAI, if configured).
- **Generic Tool Integration**: Easily plug in new tools (Google Serper, Jira, etc.) as LangChain Tools or custom interfaces.
- **Memory**: Maintains conversation history using LangGraph's `MemorySaver`.
- **Gradio UI**: Simple chat interface for easy interaction.

## Requirements

- Python 3.8+
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Gradio](https://gradio.app/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [httpx](https://www.python-httpx.org/)
- [requests](https://requests.readthedocs.io/)
- OpenAI API Key
- Optional: Google Serper API Key, Jira API credentials, etc.

## Installation

1. **Clone this repository** and navigate to the project folder.

2. **Install dependencies**:
    ```bash
    pip install langgraph langchain gradio python-dotenv httpx requests
    ```

3. **Set up environment variables**:
    - Create a `.env` file in the project root with your API keys:
      ```
      OPENAI_API_KEY=your_openai_api_key
      # Optional for search:
      SERPER_API_KEY=your_serper_api_key
      # Optional for Jira:
      JIRA_API_TOKEN=your_jira_api_token
      JIRA_BASE_URL=your_jira_url
      ```

## How it Works

- **Generic Tool Integration:**  
  Tools are defined as LangChain `Tool` instances or compatible callables. You can add any number of tools (Search, Jira, custom APIs) to the `tools` list.
- **Flexible Routing:**  
  The chatbot uses LangGraph to route user queries to the appropriate tool based on intent, or handle them directly with the language model.
- **Extensible:**  
  To add a new tool (e.g., Jira integration), simply create a new `Tool` instance and add it to the `tools` list in your script.

## Example: Adding Tools

```python
from langchain.agents import Tool

# Example: Google Serper Tool
tool_search = Tool(
    name="search",
    func=serper.run,
    description="Useful for online search"
)

# Example: Jira Tool (pseudo-code, add your own implementation)
def create_jira_ticket(query: str):
    # Your Jira integration logic here
    pass

tool_jira = Tool(
    name="jira",
    func=create_jira_ticket,
    description="Create and manage Jira tickets"
)

tools = [tool_search, tool_jira]  # Add as many tools as you need!
```

## Usage

1. **Start the chat server**:
    ```bash
    python your_script.py
    ```
2. **Access the chat UI**:
   - By default, visit [http://localhost:7860](http://localhost:7860) in your browser.
   - If `share=True`, a public Gradio link will be generated.

3. **Chat with the bot**!
   - The bot will use its model and any available tools (search, Jira, etc.) as needed.

## Customization

- **Add New Tools:**  
  Follow the [LangChain Tool documentation](https://python.langchain.com/docs/modules/agents/tools/custom_tools/) to create and register new tools (APIs, databases, etc.).
- **Change Models or Logic:**  
  Swap out the LLM, adjust the chat graph, or modify tool routing to suit your needs.

---

**References:**
- [LangGraph Documentation](https://langgraph.readthedocs.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Gradio Documentation](https://gradio.app/)
- [Google Serper API](https://serper.dev/)