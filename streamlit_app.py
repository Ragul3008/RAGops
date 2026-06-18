import streamlit as st
import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="RAGOps Local Testing Playground",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .reportview-container {
        background: #0f172a;
    }
    h1, h2, h3 {
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        transform: scale(1.02);
    }
    .context-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 10px;
        color: #e2e8f0;
    }
    .metrics-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #334155;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Helper to read local vector store
def read_local_store():
    file_path = "local_vector_store.json"
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

# Helper to write local vector store
def write_local_store(data):
    file_path = "local_vector_store.json"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Failed to write to local vector store: {e}")

st.title("🤖 RAGOps Local Testing Playground")
st.markdown("Easily ingest documents, run context-grounded queries, and manage your local vector store.")

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Configuration")
    llm_provider = st.selectbox("LLM Provider", ["gemini", "openai", "ollama"], index=0)
    prompt_version = st.selectbox("Prompt Version", ["v1", "v2"], index=0)
    
    # Embedding Provider Setup
    default_embedding_provider = os.getenv("EMBEDDING_PROVIDER", "local")
    embedding_options = ["local", "gemini", "openai"]
    if default_embedding_provider not in embedding_options:
        embedding_options.append(default_embedding_provider)
    
    embedding_provider = st.selectbox(
        "Embedding Provider",
        embedding_options,
        index=embedding_options.index(default_embedding_provider) if default_embedding_provider in embedding_options else 0
    )
    
    st.markdown("---")
    st.subheader("🚀 Advanced RAG Settings")
    multi_query = st.checkbox("Multi-Query Expansion", value=False)
    rerank = st.checkbox("Cross-Encoder Re-ranking", value=False)
    top_k = st.slider("Top K Contexts", min_value=1, max_value=10, value=5)
    score_threshold = st.slider("Similarity Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
    
    st.markdown("---")
    st.subheader("📁 Vector Store Control")
    
    # Reload button
    if st.button("🔄 Refresh Data"):
        st.rerun()

    # Clear database button
    if st.button("🗑️ Clear Vector Store", type="primary"):
        write_local_store([])
        st.success("Vector store cleared!")
        st.rerun()

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Query Playground", "📤 Ingest Document", "🔍 Vector Store Inspector"])

# Tab 1: Query Playground
with tab1:
    st.header("💬 Query & Retrieve")
    
    query_text = st.text_area(
        "Enter your query:",
        placeholder="e.g., what is ragul's education qualification from uploaded resume?",
        key="query_input"
    )
    
    if st.button("Run Pipeline"):
        if not query_text.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("Retrieving context and generating answer..."):
                try:
                    # POST request to RAG Engine
                    url = "http://127.0.0.1:8003/api/v1/query"
                    payload = {
                        "query": query_text.strip(),
                        "tenant_id": "00000000-0000-0000-0000-000000000000",
                        "llm_provider": llm_provider,
                        "prompt_version": prompt_version,
                        "embedding_provider": embedding_provider,
                        "multi_query": multi_query,
                        "rerank": rerank,
                        "top_k": top_k,
                        "score_threshold": score_threshold
                    }
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        answer = res_data.get("answer", "")
                        contexts = res_data.get("contexts", [])
                        faithful = res_data.get("faithful", True)
                        rewritten = res_data.get("rewritten_query", "")
                        route = res_data.get("route", "")
                        
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.subheader("💡 Generated Answer")
                            if answer == "I do not have the context to answer this query.":
                                st.error(answer)
                                st.info("ℹ️ Grounding Alert: The model refused to answer because the query wasn't supported by the retrieved contexts.")
                            else:
                                st.success(answer)
                                
                            st.markdown("### 📊 Metrics")
                            m_col1, m_col2 = st.columns(2)
                            with m_col1:
                                status = "✅ Faithful" if faithful else "❌ Unfaithful"
                                color = "green" if faithful else "red"
                                st.markdown(f"<div class='metrics-card'><h4>Faithfulness</h4><h2 style='color:{color}'>{status}</h2></div>", unsafe_allow_html=True)
                            with m_col2:
                                st.markdown(f"<div class='metrics-card'><h4>Router Decision</h4><h2>{route.upper()}</h2></div>", unsafe_allow_html=True)
                                
                        with col2:
                            st.subheader("📖 Retrieved Context Chunks")
                            if not contexts:
                                st.info("No context retrieved for this query.")
                                st.warning(
                                    "💡 **Troubleshooting Tip:** If you have uploaded documents but get no results, ensure that:\n"
                                    "1. The **Embedding Provider** selected in the sidebar matches the one used during document ingestion.\n"
                                    "2. The **Similarity Threshold** slider is set to a lower value (e.g., `0.4` or `0.5`)."
                                )
                            else:
                                for idx, ctx in enumerate(contexts):
                                    st.markdown(f"""
                                    <div class="context-card">
                                        <strong>Chunk #{idx+1}</strong><br/>
                                        <p style="margin-top:5px; font-size:14px; white-space: pre-wrap;">{ctx}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Failed to query RAG Engine: {e}")

# Tab 2: Ingest Document
with tab2:
    st.header("📤 Document Ingestor")
    st.markdown("Upload any document (PDF, TXT, DOCX, etc.) to clean, chunk, embed and index it in the local store.")
    
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx", "md"])
    doc_id = st.text_input("Document ID / Key", value="my_resume")
    
    chunk_size = st.number_input("Chunk Size (characters)", value=500, min_value=100, max_value=2000, step=50)
    chunk_overlap = st.number_input("Chunk Overlap (characters)", value=50, min_value=0, max_value=500, step=10)
    
    if st.button("Start Ingestion"):
        if not uploaded_file:
            st.warning("Please upload a file first.")
        else:
            with st.spinner("Parsing, embedding and storing..."):
                try:
                    url = "http://127.0.0.1:8001/api/v1/ingest-file"
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                    }
                    data = {
                        "tenant_id": "00000000-0000-0000-0000-000000000000",
                        "doc_id": doc_id,
                        "config": json.dumps({
                            "embedding_provider": embedding_provider,
                            "strategy": "recursive",
                            "chunk_size": int(chunk_size),
                            "chunk_overlap": int(chunk_overlap)
                        })
                    }
                    response = requests.post(url, files=files, data=data)
                    if response.status_code == 200:
                        st.success(f"Successfully started ingestion for document '{doc_id}'!")
                        st.info("The document is being parsed and embedded in the background. Check the 'Vector Store Inspector' tab to verify.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Failed to trigger ingestion: {e}")

# Tab 3: Vector Store Inspector
with tab3:
    st.header("🔍 Local Vector Store Inspector")
    data = read_local_store()
    
    if not data:
        st.info("The local vector store is empty.")
    else:
        # Group by document
        docs = {}
        for pt in data:
            doc_id_key = pt["payload"]["doc_id"]
            if doc_id_key not in docs:
                docs[doc_id_key] = []
            docs[doc_id_key].append(pt)
            
        st.subheader(f"Total Chunks Ingested: {len(data)}")
        
        # Display as a table/expander per doc
        for doc_id_key, chunks in docs.items():
            with st.expander(f"📄 Document: {doc_id_key} ({len(chunks)} Chunks)"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**Collection:** `{chunks[0]['collection']}`")
                with col2:
                    if st.button(f"Delete Document", key=f"del_{doc_id_key}"):
                        # Delete this doc
                        new_data = [pt for pt in data if pt["payload"]["doc_id"] != doc_id_key]
                        write_local_store(new_data)
                        st.success(f"Document '{doc_id_key}' deleted from local store!")
                        st.rerun()
                
                # Show chunk content
                for idx, chunk in enumerate(chunks):
                    st.markdown(f"**Chunk #{idx+1} (ID: `{chunk['id'][:8]}...`)**")
                    st.code(chunk["payload"]["content"], language="text")
                    st.markdown("---")
