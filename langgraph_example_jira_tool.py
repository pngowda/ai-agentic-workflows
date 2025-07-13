from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.checkpoint.memory import MemorySaver

import gradio as gr

# Load environment
load_dotenv(override=True)

# Set up Jira tools
jira = JiraAPIWrapper()
jira_toolkit = JiraToolkit.from_jira_api_wrapper(jira)
jira_tools = jira_toolkit.get_tools()

# Optional: Print tools for reference
for tool in jira_tools:
    print(f"{tool.name}: {tool.description}")


# LangGraph State Definition
class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

# LLM setup
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(jira_tools)


# Define chatbot node
def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


memory = MemorySaver()

# Build graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=jira_tools))
graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.set_finish_point("chatbot")

config = {"configurable": {"thread_id": "1"}}

graph = graph_builder.compile(checkpointer=memory)
print(graph.get_graph().draw_ascii())


# Gradio UI
def chat(user_input: str, history):
    result = graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]}, config=config
    )
    return result["messages"][-1].content


gr.ChatInterface(chat, type="messages", title="Jira AI Assistant").launch(
    server_name="localhost", server_port=7860, share=True
)
