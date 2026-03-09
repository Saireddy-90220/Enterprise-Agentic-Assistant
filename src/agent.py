from typing import Annotated, TypedDict, Sequence, Literal
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

import os
from src.ingestion import get_retriever
from src.sql_agent import execute_sql_query
from src.api_agent import fetch_external_data

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: str
    analysis: str
    route: str

class RouteDecider(BaseModel):
    datasource: Literal["vectorstore", "sqldb", "api"] = Field(
        ...,
        description="Given a user question choose to route it to vectorstore (for documents/reports), sqldb (for structured financials/tables), or api (for live/external data like stock or weather)."
    )

def plan_node(state: AgentState):
    """Routes the query to the correct data source."""
    query = state["messages"][-1].content
    print(f"--- ROUTING QUERY: {query} ---")
    
    if not os.environ.get("GROQ_API_KEY"):
        return {"route": "error"}

    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    structured_llm = llm.with_structured_output(RouteDecider)
    
    system_prompt = """You are an expert router. Determine the best data source:
- 'vectorstore': for queries about reports, strategic initiatives, executive summaries, documents.
- 'sqldb': for queries requiring EXACT structured financial values from a database (e.g. Q1 revenue, departmental budgets).
- 'api': for requests needing live, external data like current stock prices, weather, or supply chain statuses."""
    
    result = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ])
    
    decision = result.datasource
    print(f"--- DECISION: Route to {decision.upper()} ---")
    return {"route": decision}

def retrieve_node(state: AgentState):
    """Retrieves context from Vector DB."""
    last_message = state["messages"][-1].content
    print("--- FETCHING FROM VECTOR STORE ---")
    retriever = get_retriever()
    docs = retriever.invoke(last_message)
    context = "\n".join([doc.page_content for doc in docs])
    return {"context": f"Source: Enterprise Documents\n====\n{context}"}

def sql_node(state: AgentState):
    """Retrieves exact numerical data via SQL."""
    query = state["messages"][-1].content
    print("--- FETCHING FROM SQL DATABASE ---")
    
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a SQLite expert. The database table `financials` has schema: id, department, q1_revenue, q2_revenue, q3_revenue, q4_revenue, annual_budget. Write ONLY a raw valid SQL query string to answer the user's question, without markdown formatting."),
        ("human", "{question}")
    ])
    chain = prompt | llm
    sql_query = chain.invoke({"question": query}).content.replace('```sql', '').replace('```', '').strip()
    
    print(f"Executing SQL: {sql_query}")
    results = execute_sql_query(sql_query)
    return {"context": f"Source: Enterprise SQL Database\n====\nSQL Executed: {sql_query}\nResults: {results}"}

def api_node(state: AgentState):
    """Fetches external live data from the API."""
    query = state["messages"][-1].content
    print("--- FETCHING FROM LIVE API ---")
    results = fetch_external_data(query)
    return {"context": f"Source: External Enterprise API\n====\n{results}"}

def analyze_node(state: AgentState):
    """Analyzes the context focusing on enterprise insights."""
    context = state.get("context", "")
    query = state["messages"][-1].content
    
    print("--- ANALYZING DATA ---")
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    
    system_prompt = """You are an expert Enterprise AI Analyst. 
Analyze the provided context against the user's query. Extract key insights.
Context:
{context}"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Analyze this context to answer: {query}")
    ])
    
    chain = prompt | llm
    analysis_res = chain.invoke({"context": context, "query": query})
    return {"analysis": analysis_res.content}

def generate_node(state: AgentState):
    """Synthesizes the final high-quality enterprise response."""
    analysis = state.get("analysis", "")
    query = state["messages"][-1].content
    
    if state.get("route") == "error":
        return {"messages": [AIMessage(content="I cannot answer this because the Groq API key is missing.")]}

    print("--- GENERATING FINAL RESPONSE ---")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
    system_prompt = """You are a highly advanced Enterprise Agentic AI Assistant.
Provide a "super", wow-factor executive response. Use formatting (markdown, lists).
Analyst Insights:
{analysis}"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "User Query: {query}\n\nProvide the final executive response.")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"analysis": analysis, "query": query})
    return {"messages": [response]}


def build_graph():
    """Compiles the full Multi-Agent routing pipeline."""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("plan", plan_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("sql", sql_node)
    workflow.add_node("api", api_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("generate", generate_node)
    
    workflow.set_entry_point("plan")
    
    def route_decision(state: AgentState):
        if state.get("route") == "error": return "generate"
        if state["route"] == "vectorstore": return "retrieve"
        if state["route"] == "sqldb": return "sql"
        if state["route"] == "api": return "api"
        return "retrieve" # Default fallback
    
    workflow.add_conditional_edges("plan", route_decision)
    workflow.add_edge("retrieve", "analyze")
    workflow.add_edge("sql", "analyze")
    workflow.add_edge("api", "analyze")
    workflow.add_edge("analyze", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()

app_graph = build_graph()
