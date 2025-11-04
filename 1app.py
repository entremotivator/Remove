import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Sora Watermark Remover",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .status-waiting {
        color: #FFA500;
        font-weight: bold;
    }
    .status-success {
        color: #28A745;
        font-weight: bold;
    }
    .status-fail {
        color: #DC3545;
        font-weight: bold;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# API Configuration
BASE_URL = "https://api.kie.ai/api/v1/jobs"
CREATE_TASK_URL = f"{BASE_URL}/createTask"
QUERY_TASK_URL = f"{BASE_URL}/recordInfo"

def create_task(api_key, video_url, callback_url=None):
    """Create a watermark removal task"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sora-watermark-remover",
        "input": {
            "video_url": video_url
        }
    }
    
    if callback_url:
        payload["callBackUrl"] = callback_url
    
    try:
        response = requests.post(CREATE_TASK_URL, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"code": 500, "msg": f"Error: {str(e)}"}

def query_task(api_key, task_id):
    """Query task status"""
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    params = {"taskId": task_id}
    
    try:
        response = requests.get(QUERY_TASK_URL, headers=headers, params=params)
        return response.json()
    except Exception as e:
        return {"code": 500, "msg": f"Error: {str(e)}"}

def format_timestamp(timestamp):
    """Format timestamp to readable date"""
    if timestamp:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def get_status_class(state):
    """Get CSS class for status"""
    if state == "waiting":
        return "status-waiting"
    elif state == "success":
        return "status-success"
    elif state == "fail":
        return "status-fail"
    return ""

# Header
st.markdown('<h1 class="main-header">🎬 Sora Watermark Remover</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Remove watermarks from Sora-generated videos with AI</p>', unsafe_allow_html=True)

# Sidebar - API Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input(
        "API Key",
        type="password",
        value=st.session_state.api_key,
        help="Get your API key from https://kie.ai/api-key"
    )
    st.session_state.api_key = api_key
    
    st.markdown("---")
    
    st.header("ℹ️ Information")
    st.markdown("""
    **Supported URLs:**
    - Must start with `sora.chatgpt.com`
    - Must be publicly accessible
    - Max length: 500 characters
    
    **Task States:**
    - 🟡 Waiting: Processing
    - 🟢 Success: Completed
    - 🔴 Fail: Failed
    """)
    
    st.markdown("---")
    st.markdown("**Quick Links:**")
    st.markdown("- [Get API Key](https://kie.ai/api-key)")
    st.markdown("- [API Documentation](https://kie.ai/docs)")

# Main content
if not api_key:
    st.warning("⚠️ Please enter your API Key in the sidebar to get started.")
    st.info("📝 Get your API key from: https://kie.ai/api-key")
else:
    # Create Task Section
    st.header("🚀 Create New Task")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_url = st.text_input(
            "Sora Video URL",
            placeholder="https://sora.chatgpt.com/p/s_68e83bd7eee88191be79d2ba7158516f",
            help="Enter the Sora video URL to remove watermark"
        )
    
    with col2:
        st.write("")
        st.write("")
        callback_url = st.text_input(
            "Callback URL (Optional)",
            placeholder="https://your-domain.com/callback"
        )
    
    if st.button("🎯 Remove Watermark", type="primary"):
        if not video_url:
            st.error("❌ Please enter a video URL")
        elif not video_url.startswith("https://sora.chatgpt.com"):
            st.error("❌ URL must start with https://sora.chatgpt.com")
        else:
            with st.spinner("Creating task..."):
                result = create_task(api_key, video_url, callback_url if callback_url else None)
                
                if result.get("code") == 200:
                    task_id = result["data"]["taskId"]
                    st.success(f"✅ Task created successfully! Task ID: {task_id}")
                    
                    # Add to session state
                    st.session_state.tasks.append({
                        "taskId": task_id,
                        "video_url": video_url,
                        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result.get('msg', 'Unknown error')}")
    
    st.markdown("---")
    
    # Task List Section
    st.header("📋 Task List")
    
    if not st.session_state.tasks:
        st.info("No tasks yet. Create a task above to get started!")
    else:
        # Refresh all button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("🔄 Refresh All"):
                st.rerun()
        with col2:
            if st.button("🗑️ Clear All"):
                st.session_state.tasks = []
                st.rerun()
        
        st.markdown("---")
        
        # Display tasks
        for idx, task in enumerate(reversed(st.session_state.tasks)):
            task_id = task["taskId"]
            
            # Query task status
            task_result = query_task(api_key, task_id)
            
            if task_result.get("code") == 200:
                task_data = task_result["data"]
                state = task_data.get("state", "unknown")
                
                # Task container
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Task #{len(st.session_state.tasks) - idx}**")
                        st.markdown(f"**ID:** `{task_id}`")
                        st.markdown(f"**URL:** {task['video_url'][:50]}...")
                        st.markdown(f"**Created:** {task['created_at']}")
                    
                    with col2:
                        status_class = get_status_class(state)
                        st.markdown(f'<p class="{status_class}">Status: {state.upper()}</p>', unsafe_allow_html=True)
                        
                        if st.button(f"🔍 Details", key=f"details_{idx}"):
                            st.session_state[f"show_details_{idx}"] = not st.session_state.get(f"show_details_{idx}", False)
                    
                    # Show details if toggled
                    if st.session_state.get(f"show_details_{idx}", False):
                        with st.expander("Task Details", expanded=True):
                            st.json({
                                "taskId": task_data.get("taskId"),
                                "model": task_data.get("model"),
                                "state": task_data.get("state"),
                                "createTime": format_timestamp(task_data.get("createTime")),
                                "completeTime": format_timestamp(task_data.get("completeTime")),
                                "costTime": f"{task_data.get('costTime', 0) / 1000:.2f}s" if task_data.get('costTime') else "N/A"
                            })
                            
                            if state == "success" and task_data.get("resultJson"):
                                result_data = json.loads(task_data["resultJson"])
                                if "resultUrls" in result_data:
                                    st.success("✅ Processing completed!")
                                    for url in result_data["resultUrls"]:
                                        st.markdown(f"**Download:** [{url}]({url})")
                                        st.video(url)
                            
                            elif state == "fail":
                                st.error(f"❌ Task failed: {task_data.get('failMsg', 'Unknown error')}")
                                st.markdown(f"**Error Code:** {task_data.get('failCode', 'N/A')}")
                    
                    st.markdown("---")
            else:
                st.error(f"Failed to query task {task_id}: {task_result.get('msg', 'Unknown error')}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Made with ❤️ using Streamlit | Powered by KIE.AI</p>
    <p style="font-size: 0.8rem;">For support and documentation, visit <a href="https://kie.ai">kie.ai</a></p>
</div>
""", unsafe_allow_html=True)
