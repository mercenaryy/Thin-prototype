import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from data_loader import load_user_data, format_data_summary

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")

DATA_FILE    = "AI_model-_Raw_Data.xlsx"
user_data    = load_user_data(DATA_FILE)
data_summary = format_data_summary(user_data)

@tool
def get_user_behavioral_data() -> str:
    """Retrieve the user's full behavioral data: events, emotions, decisions,
    loops and pattern insights. Use for any question about the user's week."""
    return data_summary

@tool
def analyze_user_patterns(focus_area: str) -> str:
    """Deep-dive into one area: emotions, work, social, health, family,
    leisure, decisions, loops, insights, or all."""
    from collections import Counter
    focus     = focus_area.lower().strip()
    signals   = user_data.get("signals", [])
    loops     = user_data.get("loops", [])
    decisions = user_data.get("decisions", [])
    patterns  = user_data.get("patterns", [])
    out = []
    if focus in ("emotions","all"):
        ec = Counter(s.get("Emotion","?") for s in signals)
        out.append("EMOTIONS: " + ", ".join(f"{e}:{c}" for e,c in ec.most_common()))
    if focus in ("work","all"):
        we = [s for s in signals if s.get("Type")=="Work"]
        out.append(f"WORK ({len(we)}): " + " | ".join(
            f"[{s.get('Day')} {s.get('Time')}] {s.get('Event')} ({s.get('Emotion')})"
            for s in we))
    if focus in ("social","all"):
        se = [s for s in signals if s.get("Type")=="Social"]
        out.append(f"SOCIAL ({len(se)}): " + " | ".join(
            f"[{s.get('Day')} {s.get('Time')}] {s.get('Event')}" for s in se))
    if focus in ("health","all"):
        he = [s for s in signals if s.get("Type")=="Health"]
        out.append(f"HEALTH ({len(he)}): " + " | ".join(
            f"[{s.get('Day')} {s.get('Time')}] {s.get('Event')}" for s in he))
    if focus in ("family","all"):
        fe = [s for s in signals if s.get("Type")=="Personal"]
        out.append(f"FAMILY ({len(fe)}): " + " | ".join(
            f"[{s.get('Day')} {s.get('Time')}] {s.get('Event')} ({s.get('Emotion')})"
            for s in fe))
    if focus in ("decisions","all"):
        out.append(f"DECISIONS ({len(decisions)}): " + " | ".join(
            f"[{d.get('Time')}] {d.get('Decision')} emotion={d.get('Emotion')} conf={d.get('Confidence')}"
            for d in decisions))
    if focus in ("loops","all"):
        out.append(f"LOOPS ({len(loops)}): " + " | ".join(
            f"[{l.get('Loop ID')}] {l.get('Loop')} status={l.get('Status')}"
            for l in loops))
    if focus in ("insights","all"):
        out.append(f"INSIGHTS ({len(patterns)}): " + " | ".join(
            f"[{p.get('Pattern Type')}] {p.get('Insight')}"
            for p in patterns))
    return "\n".join(out) if out else f"Unknown focus area: {focus_area}"

TOOLS = [get_user_behavioral_data, analyze_user_patterns]

SYSTEM_PROMPT = (
    "You are a Personal Intelligence AI. Use get_user_behavioral_data or "
    "analyze_user_patterns to answer questions about the user's week, habits, "
    "emotions, decisions and loops. Be concise and warm."
)

_graph = None

def _build_graph():
    from langgraph.graph import StateGraph, START, MessagesState
    from langgraph.prebuilt import ToolNode, tools_condition
    from langchain_groq import ChatGroq

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
    )
    llm_with_tools = llm.bind_tools(TOOLS)

    def tool_calling_llm(state: MessagesState):
        msgs = ([SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
                if len(state["messages"]) <= 1 else state["messages"])
        return {"messages": [llm_with_tools.invoke(msgs)]}

    builder = StateGraph(MessagesState)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", "tool_calling_llm")
    return builder.compile()

def ask(question: str, verbose: bool = False) -> str:
    global _graph
    if _graph is None:
        _graph = _build_graph()
    result   = _graph.invoke({"messages": [HumanMessage(content=question)]})
    messages = result["messages"]
    if verbose:
        for m in messages: m.pretty_print()
        return ""
    for m in reversed(messages):
        if hasattr(m, "content") and m.content and m.type == "ai":
            return m.content
    return "No response generated."