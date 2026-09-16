import streamlit as st

from app.rag import PyTorchRAG


st.set_page_config(
    page_title="PyTorch Docs Assistant",
    page_icon="🔥"
)


@st.cache_resource
def load_rag():
    return PyTorchRAG()


st.title("PyTorch Docs Assistant")

st.write(
    "Ask questions about the official PyTorch documentation."
)


rag = load_rag()


question = st.text_input(
    "Question",
    placeholder="How does torch.compile work?"
)


if st.button("Ask") and question:

    with st.spinner("Searching documentation..."):

        result = rag.ask(question)

    st.subheader("Answer")

    st.write(
        result["answer"]
    )

    st.subheader("Sources")

    for source in result["sources"]:

        st.markdown(
            f"[{source['id']}] "
            f"[{source['section']}]"
            f"({source['url']})"
        )