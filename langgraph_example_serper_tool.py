import gradio as gr

from typing import Annotated
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from typing import TypedDict
from langchain_community.utilities import GoogleSerperAPIWrapper

from langchain.agents import Tool
from langgraph.checkpoint.memory import MemorySaver

load_dotenv(override=True)

serper = GoogleSerperAPIWrapper()
serper.run("what is the capital of france")

tool_search = Tool(
    name="search",
    func=serper.run,
    description="Used to get info from online search",
)

tool_search.invoke("What is the capital of France?")

tools = [tool_search]


class State(TypedDict):
    messages: Annotated[list, add_messages]


memory = MemorySaver()

graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    print(state)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile(checkpointer=memory)

print(graph.get_graph().draw_ascii())


config = {"configurable": {"thread_id": "1"}}


def chat(user_input: str, history):
    result = graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]}, config=config
    )
    return result["messages"][-1].content


gr.ChatInterface(chat, type="messages", theme="dark").launch(
    server_name="localhost", server_port=7860, share=True
)


graph.get_state(config)

list(graph.get_state_history(config))
