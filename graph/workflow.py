from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import ChatState

from graph.nodes import (
    language_node,
    translate_node,
    rewrite_node,
    route_node,
    web_node,
    pdf_node,
    translate_back_node
)


def decide_route(state):
    return state["route"]


# ================= GRAPH =================

builder = StateGraph(ChatState)

# ================= NODES =================

builder.add_node(
    "language",
    language_node
)

builder.add_node(
    "translate",
    translate_node
)

builder.add_node(
    "rewrite",
    rewrite_node
)

builder.add_node(
    "route",
    route_node
)

builder.add_node(
    "web",
    web_node
)

builder.add_node(
    "pdf",
    pdf_node
)

builder.add_node(
    "translate_back",
    translate_back_node
)

# ================= ENTRY =================

builder.set_entry_point(
    "language"
)

# ================= EDGES =================

builder.add_edge(
    "language",
    "translate"
)

builder.add_edge(
    "translate",
    "rewrite"
)

builder.add_edge(
    "rewrite",
    "route"
)

# ================= CONDITIONAL ROUTING =================

builder.add_conditional_edges(
    "route",
    decide_route,
    {
        "web": "web",
        "rag": "pdf"
    }
)

# ================= FINAL FLOW =================

builder.add_edge(
    "web",
    "translate_back"
)

builder.add_edge(
    "pdf",
    "translate_back"
)

builder.add_edge(
    "translate_back",
    END
)

# ================= COMPILE =================

graph = builder.compile()