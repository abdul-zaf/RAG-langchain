import streamlit as st
from src.data_loader import load_all_documents
from src.search import RAGSearch
import os

st.set_page_config(page_title="Programming Languages RAG", page_icon="📚", layout="centered")

st.title("📚 Concepts of Programming Languages")
st.caption("Ask questions about the textbook — topics include data types, variables, control flow, subprograms, OOP, concurrency, and more.")

SUGGESTED = [
    "What are the differences between call by value and call by reference?",
    "How does Ada handle concurrency and tasks?",
    "What is static vs dynamic scoping?",
    "What are the main features of object-oriented programming?",
    "How do functional languages like Scheme and Haskell differ from imperative languages?",
    "What is BNF and how is it used to describe programming language syntax?",
    "How does exception handling work in programming languages?",
    "What is the difference between static and dynamic typing?",
    "How does inheritance work in object-oriented languages?",
    "What is logic programming and how does Prolog work?",
    "What are the design criteria for evaluating programming languages?",
    "How are subprograms implemented and linked at runtime?",
]

@st.cache_resource(show_spinner="Loading RAG pipeline...")
def load_rag():
    return RAGSearch()

rag = load_rag()

st.subheader("Ask a question")

with st.expander("Suggested questions"):
    for q in SUGGESTED:
        if st.button(q, key=q):
            st.session_state.query = q

query = st.text_input(
    "Your question:",
    value=st.session_state.get("query", ""),
    placeholder="e.g. What is dynamic scoping?",
)

top_k = st.slider("Number of passages to retrieve", min_value=1, max_value=10, value=3)

if st.button("Search", type="primary") and query.strip():
    with st.spinner("Searching and summarizing..."):
        summary = rag.search_and_summarize(query.strip(), top_k=top_k)
        raw_results = rag.vectorstore.query(query.strip(), top_k=top_k)

    st.subheader("Summary")
    st.write(summary)

    with st.expander("Retrieved passages"):
        for i, r in enumerate(raw_results, 1):
            text = r["metadata"].get("text", "") if r["metadata"] else ""
            st.markdown(f"**Passage {i}** (distance: `{r['distance']:.4f}`)")
            st.text(text[:800] + ("..." if len(text) > 800 else ""))
            st.divider()

    with open("results.txt", "w") as f:
        f.write(f"Query: {query}\n\nSummary:\n{summary}\n")
    st.success("Results saved to results.txt")
