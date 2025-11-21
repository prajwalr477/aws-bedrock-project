import streamlit as st
import boto3
from botocore.exceptions import ClientError
import json
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt

# Streamlit UI
st.title("Bedrock Chat Application")

# Sidebar for configurations
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox(
    "Select LLM Model",
    [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
    ],
)

kb_id = st.sidebar.text_input("Knowledge Base ID", "your-knowledge-base-id")
temperature = st.sidebar.select_slider(
    "Temperature", [i / 10 for i in range(0, 11)], 1.0
)
top_p = st.sidebar.select_slider(
    "Top_P", [i / 1000 for i in range(0, 1001)], 1.0
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages (scrolling history)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):

    # 1) Show and store the user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2) Build assistant message (answer + optional Source)
    assistant_text = "I'm unable to answer this, please try again"

    if valid_prompt(prompt, model_id):
        try:
            kb_results = query_knowledge_base(prompt, kb_id)
        except ClientError as e:
            kb_results = []
            print(f"Error querying Knowledge Base: {e}")

        if kb_results:
            # Optional: inspect one retrieval result in terminal
            print("One retrieval result raw structure:")
            print(json.dumps(kb_results[0], indent=2, default=str))

            # Collect PDF names from metadata / S3 URI
            sources = set()
            for result in kb_results:
                metadata = result.get("metadata", {})
                file_name = metadata.get("x-amz-bedrock-kb-file-name")

                # Fallback: derive from S3 URI if metadata is missing
                if not file_name:
                    loc = result.get("location", {}).get("s3Location", {})
                    uri = loc.get("uri")
                    if uri:
                        # e.g. s3://bucket/spec-sheets/excavator-x950-spec-sheet.pdf#page=3
                        file_name = uri.split("/")[-1].split("#")[0]

                if file_name:
                    sources.add(file_name)

            # Build context from KB chunks
            context = "\n".join(result["content"]["text"] for result in kb_results)

            # Call the LLM with context + user query
            full_prompt = f"Context: {context}\n\nUser: {prompt}\n\n"
            base_answer = generate_response(full_prompt, model_id, temperature, top_p)

            # Combine answer + Source into ONE markdown string
            if sources:
                source_list = ", ".join(sorted(sources))
                assistant_text = f"{base_answer}\n\n*Source:* {source_list}"
            else:
                assistant_text = base_answer
        else:
            assistant_text = "I'm unable to answer this, please try again"
    else:
        assistant_text = "I'm unable to answer this, please try again"

    # 3) Show and store a single assistant message for this turn
    with st.chat_message("assistant"):
        st.markdown(assistant_text)

    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
