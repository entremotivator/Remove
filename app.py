import streamlit as st
import requests
import json
import random
import string
from datetime import datetime

# Streamlit setup
st.set_page_config(page_title="KIE.AI Task Viewer", page_icon="🎬", layout="wide")

st.title("🎬 KIE.AI Task Viewer")
st.markdown("Enter a new API URL to generate and view random task information.")

# Input fields
api_url = st.text_input("Enter KIE.AI API URL", value="https://api.kie.ai/api/v1/jobs/recordInfo")
api_key = st.text_input("Enter your API Key", type="password")

# Generate random Task ID
if st.button("Generate Random Task ID"):
    random_task_id = "task_" + ''.join(random.choices(string.digits, k=8))
    st.session_state["task_id"] = random_task_id
    st.success(f"✅ Generated Task ID: {random_task_id}")

# Display current Task ID if generated
task_id = st.session_state.get("task_id", None)
if task_id:
    st.info(f"Using Task ID: **{task_id}**")

# Fetch data
if st.button("Fetch Task Info"):
    if not api_url or not api_key or not task_id:
        st.warning("Please provide API URL, API Key, and generate a Task ID first.")
    else:
        with st.spinner("Fetching task data..."):
            try:
                params = {"taskId": task_id}
                headers = {"Authorization": f"Bearer {api_key}"}

                response = requests.get(api_url, headers=headers, params=params)
                if response.status_code == 200:
                    result = response.json()

                    if result.get("code") == 200:
                        data = result["data"]

                        st.success("✅ Task Info Retrieved Successfully")

                        st.subheader("🧾 Task Details")
                        st.json({
                            "Task ID": data.get("taskId"),
                            "Model": data.get("model"),
                            "State": data.get("state"),
                            "Created": datetime.fromtimestamp(data.get("createTime")/1000).strftime("%Y-%m-%d %H:%M:%S"),
                            "Completed": datetime.fromtimestamp(data.get("completeTime")/1000).strftime("%Y-%m-%d %H:%M:%S"),
                        })

                        st.subheader("⚙️ Input Parameters")
                        param_data = json.loads(data.get("param", "{}"))
                        st.json(param_data)

                        st.subheader("🖼️ Results")
                        result_data = json.loads(data.get("resultJson", "{}"))
                        result_urls = result_data.get("resultUrls", [])
                        if result_urls:
                            for url in result_urls:
                                st.markdown(f"[View Result Image]({url})")
                                st.image(url, use_container_width=True)
                        else:
                            st.info("No result URLs found.")
                    else:
                        st.error(f"API Error: {result.get('message')}")
                else:
                    st.error(f"HTTP Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Powered by KIE.AI API | Built with Streamlit 💡")
