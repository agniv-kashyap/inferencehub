import streamlit as st
import requests
import time

# Backend URL
BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="InferenceHub",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 InferenceHub")
st.caption("High-Concurrency ML API Gateway")

st.divider()

# Sidebar
st.sidebar.title("Authentication")

api_key = st.sidebar.text_input(
    "API Key",
    type="password",
    placeholder="Paste your API key"
)

st.sidebar.markdown("---")

model = st.sidebar.selectbox(
    "Choose Model",
    [
        "basic-document-summary",
        "rag-document-analyzer",
        "contract-risk-analysis"
    ]
)

st.header("Inference Request")

prompt = st.text_area(
    "Input Text",
    height=250,
    placeholder="Enter text here..."
)

if st.button("🚀 Submit Inference", use_container_width=True):

    if api_key == "":
        st.error("Please enter API key.")
        st.stop()

    if prompt.strip() == "":
        st.error("Please enter input text.")
        st.stop()

    headers = {
        "x-api-key": api_key
    }

    payload = {
        "model": model,
        "input_text": prompt
    }

    try:

        response = requests.post(
            f"{BASE_URL}/infer",
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        task_id = response.json()["task_id"]

        st.success(f"Task Submitted!\n\nTask ID: {task_id}")

        progress = st.progress(0)

        status_placeholder = st.empty()

        while True:

            task = requests.get(
                f"{BASE_URL}/task/{task_id}",
                headers=headers
            )

            data = task.json()

            status = data["status"]

            status_placeholder.info(f"Status: {status}")

            if status == "SUCCESS":

                progress.progress(100)

                st.success("Inference Completed!")

                st.subheader("Result")

                st.json(data["result"])

                break

            elif status == "FAILURE":

                st.error("Inference Failed.")

                break

            else:

                progress.progress(30)

                time.sleep(2)

    except Exception as e:
        st.error(str(e))