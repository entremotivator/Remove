import streamlit as st
import requests
import json
import time
from datetime import datetime
import plotly.graph_objects as go
from typing import Optional, Dict, List

# Page configuration
st.set_page_config(
    page_title="Sora Watermark Remover Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
        animation: gradient 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-waiting {
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
        color: white;
    }
    
    .status-success {
        background: linear-gradient(135deg, #28A745 0%, #20C997 100%);
        color: white;
    }
    
    .status-fail {
        background: linear-gradient(135deg, #DC3545 0%, #C82333 100%);
        color: white;
    }
    
    .card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.2);
    }
    
    .task-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .task-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 24px rgba(102, 126, 234, 0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.1) 0%, rgba(255, 140, 0, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #FFA500;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.1) 0%, rgba(32, 201, 151, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #28A745;
        margin: 1rem 0;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 1rem;
        border-radius: 12px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(102, 126, 234, 0.4);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .progress-ring {
        width: 120px;
        height: 120px;
        margin: 0 auto;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .timeline-item {
        position: relative;
        padding-left: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #667eea;
        border: 3px solid white;
        box-shadow: 0 0 0 2px #667eea;
    }
    
    .timeline-item::after {
        content: '';
        position: absolute;
        left: 5px;
        top: 12px;
        width: 2px;
        height: calc(100% + 1rem);
        background: linear-gradient(180deg, #667eea 0%, transparent 100%);
    }
    
    .timeline-item:last-child::after {
        display: none;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'task_history' not in st.session_state:
    st.session_state.task_history = []
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# API Configuration - Using Streamlit Secrets
try:
    API_KEY = st.secrets.get("api_key", "")
except:
    API_KEY = ""

BASE_URL = "https://api.kie.ai/api/v1/jobs"
CREATE_TASK_URL = f"{BASE_URL}/createTask"
QUERY_TASK_URL = f"{BASE_URL}/recordInfo"

def create_task(api_key: str, video_url: str, callback_url: Optional[str] = None) -> Dict:
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
        response = requests.post(CREATE_TASK_URL, headers=headers, json=payload, timeout=30)
        return response.json()
    except Exception as e:
        return {"code": 500, "msg": f"Error: {str(e)}"}

def query_task(api_key: str, task_id: str) -> Dict:
    """Query task status"""
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    params = {"taskId": task_id}
    
    try:
        response = requests.get(QUERY_TASK_URL, headers=headers, params=params, timeout=30)
        return response.json()
    except Exception as e:
        return {"code": 500, "msg": f"Error: {str(e)}"}

def format_timestamp(timestamp: Optional[int]) -> str:
    """Format timestamp to readable date"""
    if timestamp:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def get_status_emoji(state: str) -> str:
    """Get emoji for status"""
    status_map = {
        "waiting": "🟡",
        "success": "🟢",
        "fail": "🔴"
    }
    return status_map.get(state, "⚪")

def calculate_stats() -> Dict:
    """Calculate task statistics"""
    total = len(st.session_state.task_history)
    waiting = sum(1 for t in st.session_state.task_history if t.get('state') == 'waiting')
    success = sum(1 for t in st.session_state.task_history if t.get('state') == 'success')
    failed = sum(1 for t in st.session_state.task_history if t.get('state') == 'fail')
    
    return {
        'total': total,
        'waiting': waiting,
        'success': success,
        'failed': failed,
        'success_rate': (success / total * 100) if total > 0 else 0
    }

# Header Section
st.markdown('<h1 class="main-header">🎬 Sora Watermark Remover Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Watermark Removal for Professional Video Content</p>', unsafe_allow_html=True)

# Sidebar - Enhanced Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/video-editing.png", width=80)
    st.title("⚙️ Control Panel")
    
    st.markdown("---")
    
    # API Key Section
    st.subheader("🔑 API Configuration")
    
    if API_KEY:
        st.success("✅ API Key loaded from secrets")
        api_key = API_KEY
        show_key = st.checkbox("Show API Key")
        if show_key:
            st.code(api_key[:20] + "..." + api_key[-10:])
    else:
        api_key = st.text_input(
            "Enter API Key",
            type="password",
            help="Get your API key from https://kie.ai/api-key"
        )
        if api_key:
            st.info("💡 Tip: Add API key to .streamlit/secrets.toml for permanent storage")
    
    st.markdown("---")
    
    # Settings Section
    st.subheader("⚡ Settings")
    
    auto_refresh = st.checkbox(
        "Auto-refresh tasks",
        value=st.session_state.auto_refresh,
        help="Automatically refresh task status every 10 seconds"
    )
    st.session_state.auto_refresh = auto_refresh
    
    refresh_interval = st.slider(
        "Refresh interval (seconds)",
        min_value=5,
        max_value=60,
        value=10,
        disabled=not auto_refresh
    )
    
    show_advanced = st.checkbox("Show advanced options", value=False)
    
    if show_advanced:
        st.markdown("---")
        st.subheader("🔧 Advanced Options")
        max_tasks = st.number_input("Max tasks to display", min_value=5, max_value=100, value=20)
        show_json = st.checkbox("Show raw JSON responses", value=False)
    
    st.markdown("---")
    
    # Statistics Section
    st.subheader("📊 Statistics")
    stats = calculate_stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tasks", stats['total'])
        st.metric("Successful", stats['success'], delta=None)
    with col2:
        st.metric("Waiting", stats['waiting'])
        st.metric("Failed", stats['failed'])
    
    if stats['total'] > 0:
        st.progress(stats['success_rate'] / 100)
        st.caption(f"Success Rate: {stats['success_rate']:.1f}%")
    
    st.markdown("---")
    
    # Help Section
    st.subheader("ℹ️ Quick Guide")
    with st.expander("📖 How to Use"):
        st.markdown("""
        **Step 1:** Enter your API key (or add to secrets.toml)
        
        **Step 2:** Paste your Sora video URL
        
        **Step 3:** Click "Remove Watermark"
        
        **Step 4:** Monitor progress in real-time
        
        **Step 5:** Download your processed video!
        """)
    
    with st.expander("🔗 Supported URLs"):
        st.markdown("""
        - Must start with `sora.chatgpt.com`
        - Must be publicly accessible
        - Maximum length: 500 characters
        
        **Example:**
        ```
        https://sora.chatgpt.com/p/s_68e83bd7ee...
        ```
        """)
    
    with st.expander("📊 Task States"):
        st.markdown("""
        - 🟡 **Waiting**: Task is being processed
        - 🟢 **Success**: Processing completed
        - 🔴 **Fail**: An error occurred
        """)
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.tasks = []
            st.session_state.task_history = []
            st.rerun()
    
    if st.button("📥 Export History", use_container_width=True):
        if st.session_state.task_history:
            export_data = json.dumps(st.session_state.task_history, indent=2)
            st.download_button(
                label="Download JSON",
                data=export_data,
                file_name=f"task_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Footer Links
    st.markdown("""
    **📚 Resources:**
    - [API Documentation](https://kie.ai/docs)
    - [Get API Key](https://kie.ai/api-key)
    - [Support Center](https://kie.ai/support)
    """)
    
    st.caption("v2.0.0 | Made with ❤️")

# Main Content Area
if not api_key:
    # Welcome Screen
    st.markdown('<div class="card animated">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div class="feature-icon">🎯</div>
            <h3>Fast Processing</h3>
            <p>Remove watermarks in minutes with AI-powered technology</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div class="feature-icon">🔒</div>
            <h3>Secure & Private</h3>
            <p>Your videos are processed securely with encrypted connections</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <div class="feature-icon">⚡</div>
            <h3>High Quality</h3>
            <p>Maintain original video quality with advanced algorithms</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="warning-box animated">', unsafe_allow_html=True)
    st.warning("⚠️ **Getting Started:** Please enter your API Key in the sidebar to begin. Don't have one? [Get your API key here](https://kie.ai/api-key)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Setup Instructions
    st.markdown("### 🚀 Quick Setup Guide")
    
    tab1, tab2, tab3 = st.tabs(["💻 Method 1: Secrets File", "🔑 Method 2: Manual Entry", "📖 API Key Guide"])
    
    with tab1:
        st.markdown("""
        **Using Streamlit Secrets (Recommended)**
        
        1. Create a file: `.streamlit/secrets.toml`
        2. Add your API key:
        ```toml
        api_key = "your_api_key_here"
        ```
        3. Restart the application
        4. ✅ Your API key will be automatically loaded!
        """)
        
        st.code("""
# .streamlit/secrets.toml
api_key = "sk_your_actual_api_key_here"
        """, language="toml")
    
    with tab2:
        st.markdown("""
        **Manual Entry**
        
        1. Get your API key from [kie.ai/api-key](https://kie.ai/api-key)
        2. Enter it in the sidebar under "🔑 API Configuration"
        3. Start using the app immediately!
        
        ⚠️ Note: You'll need to re-enter the key each session.
        """)
    
    with tab3:
        st.markdown("""
        **How to Get Your API Key**
        
        1. Visit [https://kie.ai/api-key](https://kie.ai/api-key)
        2. Sign in or create an account
        3. Navigate to API Settings
        4. Generate a new API key
        5. Copy and save it securely
        
        🔒 **Security Tips:**
        - Never share your API key publicly
        - Use secrets.toml for production
        - Rotate keys regularly
        - Monitor usage in your dashboard
        """)

else:
    # Main Application Interface
    
    # Create Task Section
    st.markdown("### 🚀 Create New Watermark Removal Task")
    
    with st.container():
        st.markdown('<div class="card animated">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            video_url = st.text_input(
                "🎥 Sora Video URL",
                placeholder="https://sora.chatgpt.com/p/s_68e83bd7eee88191be79d2ba7158516f",
                help="Enter the complete Sora video URL from sora.chatgpt.com",
                key="video_url_input"
            )
            
            # URL Validation
            if video_url:
                if video_url.startswith("https://sora.chatgpt.com"):
                    st.success("✅ Valid Sora URL")
                else:
                    st.error("❌ Invalid URL - Must start with https://sora.chatgpt.com")
        
        with col2:
            callback_url = st.text_input(
                "🔔 Callback URL (Optional)",
                placeholder="https://your-domain.com/callback",
                help="Receive webhook notifications when task completes"
            )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            create_button = st.button("🎯 Remove Watermark Now", type="primary", use_container_width=True)
        
        with col2:
            if st.button("📋 Paste Example", use_container_width=True):
                st.session_state.example_url = "https://sora.chatgpt.com/p/s_68e83bd7eee88191be79d2ba7158516f"
                st.rerun()
        
        with col3:
            if st.button("🔄 Clear Form", use_container_width=True):
                st.rerun()
        
        if create_button:
            if not video_url:
                st.error("❌ Please enter a video URL")
            elif not video_url.startswith("https://sora.chatgpt.com"):
                st.error("❌ Invalid URL format. Must start with https://sora.chatgpt.com")
            elif len(video_url) > 500:
                st.error("❌ URL is too long (max 500 characters)")
            else:
                with st.spinner("🔄 Creating task... Please wait"):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    result = create_task(api_key, video_url, callback_url if callback_url else None)
                    
                    if result.get("code") == 200:
                        task_id = result["data"]["taskId"]
                        
                        task_data = {
                            "taskId": task_id,
                            "video_url": video_url,
                            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "state": "waiting",
                            "callback_url": callback_url if callback_url else None
                        }
                        
                        st.session_state.tasks.append(task_data)
                        st.session_state.task_history.append(task_data)
                        
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success(f"✅ Task created successfully!")
                        st.info(f"**Task ID:** `{task_id}`")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        time.sleep(1)
                        st.rerun()
                    else:
                        error_msg = result.get('msg', 'Unknown error')
                        st.error(f"❌ Failed to create task: {error_msg}")
                        
                        if result.get("code") == 401:
                            st.warning("🔑 Authentication failed. Please check your API key.")
                        elif result.get("code") == 402:
                            st.warning("💳 Insufficient account balance. Please top up your account.")
                        elif result.get("code") == 429:
                            st.warning("⏱️ Rate limit exceeded. Please wait a moment and try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Task Management Section
    st.markdown("### 📋 Task Management Dashboard")
    
    # Statistics Cards
    stats = calculate_stats()
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Tasks</div>
            <div class="metric-value">{stats['total']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);">
            <div class="metric-label">⏳ Waiting</div>
            <div class="metric-value">{stats['waiting']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #28A745 0%, #20C997 100%);">
            <div class="metric-label">✅ Success</div>
            <div class="metric-value">{stats['success']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #DC3545 0%, #C82333 100%);">
            <div class="metric-label">❌ Failed</div>
            <div class="metric-value">{stats['failed']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #17A2B8 0%, #138496 100%);">
            <div class="metric-label">Success Rate</div>
            <div class="metric-value">{stats['success_rate']:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Task Filters and Controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_status = st.selectbox(
            "🔍 Filter by Status",
            ["All", "Waiting", "Success", "Failed"],
            key="status_filter"
        )
    
    with col2:
        sort_by = st.selectbox(
            "📊 Sort by",
            ["Newest First", "Oldest First", "Status"],
            key="sort_by"
        )
    
    with col3:
        view_mode = st.selectbox(
            "👁️ View Mode",
            ["Compact", "Detailed", "Timeline"],
            key="view_mode"
        )
    
    with col4:
        st.write("")
        st.write("")
        if st.button("🔄 Refresh All Tasks", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # Task List Display
    if not st.session_state.tasks:
        st.markdown('<div class="info-box animated">', unsafe_allow_html=True)
        st.info("📭 No active tasks. Create your first task above to get started!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Filter tasks
        filtered_tasks = st.session_state.tasks.copy()
        
        if filter_status != "All":
            filtered_tasks = [t for t in filtered_tasks if t.get('state', '').lower() == filter_status.lower()]
        
        # Sort tasks
        if sort_by == "Newest First":
            filtered_tasks = list(reversed(filtered_tasks))
        elif sort_by == "Status":
            status_order = {"success": 0, "waiting": 1, "fail": 2}
            filtered_tasks.sort(key=lambda x: status_order.get(x.get('state', ''), 3))
        
        st.markdown(f"**Showing {len(filtered_tasks)} of {len(st.session_state.tasks)} tasks**")
        
        # Display tasks based on view mode
        for idx, task in enumerate(filtered_tasks):
            task_id = task["taskId"]
            
            # Query latest status
            with st.spinner(f"Loading task {idx + 1}..."):
                task_result = query_task(api_key, task_id)
            
            if task_result.get("code") == 200:
                task_data = task_result["data"]
                state = task_data.get("state", "unknown")
                
                # Update task state in session
                task['state'] = state
                
                # Display based on view mode
                if view_mode == "Timeline":
                    # Timeline View
                    st.markdown(f"""
                    <div class="timeline-item animated">
                        <strong>Task #{len(filtered_tasks) - idx}</strong> • {get_status_emoji(state)} {state.upper()}<br>
                        <small>{task['created_at']}</small><br>
                        <code>{task_id[:16]}...</code>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if state == "success" and task_data.get("resultJson"):
                        result_data = json.loads(task_data["resultJson"])
                        if "resultUrls" in result_data:
                            for url in result_data["resultUrls"]:
                                st.video(url)
                                st.markdown(f"[📥 Download Video]({url})")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                
                elif view_mode == "Compact":
                    # Compact View
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**Task #{len(filtered_tasks) - idx}**")
                        st.caption(f"`{task_id[:20]}...`")
                    
                    with col2:
                        st.markdown(f'<span class="status-badge status-{state}">{get_status_emoji(state)} {state}</span>', unsafe_allow_html=True)
                    
                    with col3:
                        st.caption(task['created_at'])
                    
                    with col4:
                        if st.button("📊", key=f"detail_{idx}"):
                            st.session_state[f"expand_{idx}"] = not st.session_state.get(f"expand_{idx}", False)
                    
                    if st.session_state.get(f"expand_{idx}", False):
                        with st.expander("Details", expanded=True):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"**Video URL:** {task['video_url'][:40]}...")
                                st.markdown(f"**Created:** {task['created_at']}")
                                st.markdown(f"**Model:** {task_data.get('model', 'N/A')}")
                            
                            with col2:
                                st.markdown(f"**Complete Time:** {format_timestamp(task_data.get('completeTime'))}")
                                cost_time = task_data.get('costTime')
                                if cost_time:
                                    st.markdown(f"**Processing Time:** {cost_time / 1000:.2f}s")
                                else:
                                    st.markdown("**Processing Time:** N/A")
                            
                            if state == "success" and task_data.get("resultJson"):
                                result_data = json.loads(task_data["resultJson"])
                                if "resultUrls" in result_data:
                                    st.success("✅ Video processed successfully!")
                                    for url in result_data["resultUrls"]:
                                        st.video(url)
                                        st.markdown(f"**📥 [Download Processed Video]({url})**")
                            
                            elif state == "fail":
                                st.error(f"❌ **Error:** {task_data.get('failMsg', 'Unknown error')}")
                                st.caption(f"Error Code: {task_data.get('failCode', 'N/A')}")
                    
                    st.markdown("---")
                
                else:
                    # Detailed View (Default)
                    st.markdown('<div class="task-card animated">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### 🎬 Task #{len(filtered_tasks) - idx}")
                        st.markdown(f"**Task ID:** `{task_id}`")
                        st.markdown(f"**Video URL:** [{task['video_url'][:50]}...]({task['video_url']})")
                        st.markdown(f"**Created:** {task['created_at']}")
                        st.markdown(f"**Model:** {task_data.get('model', 'sora-watermark-remover')}")
                    
                    with col2:
                        st.markdown(f'<div style="text-align: center;"><span class="status-badge status-{state}">{get_status_emoji(state)} {state.upper()}</span></div>', unsafe_allow_html=True)
                        
                        if state == "waiting":
                            st.markdown("""
                            <div style="text-align: center; margin-top: 1rem;">
                                <div class="spinner"></div>
                                <p style="color: #FFA500; font-weight: 600;">Processing...</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Progress Information
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("⏱️ Created At", format_timestamp(task_data.get('createTime')))
                    
                    with col2:
                        st.metric("✅ Completed At", format_timestamp(task_data.get('completeTime')))
                    
                    with col3:
                        cost_time = task_data.get('costTime')
                        if cost_time:
                            st.metric("⚡ Processing Time", f"{cost_time / 1000:.2f}s")
                        else:
                            st.metric("⚡ Processing Time", "N/A")
                    
                    # Results Section
                    if state == "success" and task_data.get("resultJson"):
                        st.markdown("---")
                        st.markdown("### 🎉 Processing Complete!")
                        
                        result_data = json.loads(task_data["resultJson"])
                        
                        if "resultUrls" in result_data:
                            st.success(f"✅ Successfully removed watermark from your video!")
                            
                            for url_idx, url in enumerate(result_data["resultUrls"]):
                                st.markdown(f"**Result Video #{url_idx + 1}:**")
                                
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.video(url)
                                
                                with col2:
                                    st.markdown(f"**[📥 Download]({url})**")
                                    
                                    if st.button(f"📋 Copy URL", key=f"copy_{idx}_{url_idx}"):
                                        st.code(url)
                                        st.success("URL ready to copy!")
                    
                    elif state == "fail":
                        st.markdown("---")
                        st.error(f"❌ **Task Failed**")
                        st.markdown(f"**Error Message:** {task_data.get('failMsg', 'Unknown error occurred')}")
                        st.markdown(f"**Error Code:** {task_data.get('failCode', 'N/A')}")
                        
                        st.markdown("""
                        **Troubleshooting Tips:**
                        - Verify the video URL is correct and accessible
                        - Check if the video is from sora.chatgpt.com
                        - Ensure you have sufficient API credits
                        - Try again in a few minutes
                        """)
                    
                    elif state == "waiting":
                        st.markdown("---")
                        st.info("⏳ Your video is being processed. This may take a few minutes...")
                        
                        progress_text = "Processing your video..."
                        progress_bar = st.progress(0, text=progress_text)
                        
                        # Simulated progress (for UX)
                        for percent in range(0, 100, 10):
                            time.sleep(0.1)
                            progress_bar.progress(percent + 10, text=progress_text)
                    
                    # Action Buttons
                    st.markdown("---")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button(f"🔄 Refresh", key=f"refresh_{idx}", use_container_width=True):
                            st.rerun()
                    
                    with col2:
                        if st.button(f"📊 View JSON", key=f"json_{idx}", use_container_width=True):
                            st.session_state[f"show_json_{idx}"] = not st.session_state.get(f"show_json_{idx}", False)
                    
                    with col3:
                        if st.button(f"🔗 Share", key=f"share_{idx}", use_container_width=True):
                            st.session_state[f"show_share_{idx}"] = not st.session_state.get(f"show_share_{idx}", False)
                    
                    with col4:
                        if st.button(f"🗑️ Remove", key=f"remove_{idx}", use_container_width=True):
                            st.session_state.tasks = [t for t in st.session_state.tasks if t['taskId'] != task_id]
                            st.rerun()
                    
                    # Show JSON if toggled
                    if st.session_state.get(f"show_json_{idx}", False):
                        with st.expander("📄 Raw JSON Response", expanded=True):
                            st.json(task_data)
                    
                    # Show share options if toggled
                    if st.session_state.get(f"show_share_{idx}", False):
                        with st.expander("🔗 Share Options", expanded=True):
                            st.code(f"Task ID: {task_id}")
                            if state == "success" and task_data.get("resultJson"):
                                result_data = json.loads(task_data["resultJson"])
                                if "resultUrls" in result_data:
                                    st.code(result_data["resultUrls"][0])
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                st.error(f"❌ Failed to query task {task_id}: {task_result.get('msg', 'Unknown error')}")
        
        # Pagination (if too many tasks)
        if len(filtered_tasks) > 10:
            st.markdown("---")
            st.info(f"📄 Showing all {len(filtered_tasks)} tasks. Consider using filters to narrow results.")

# Auto-refresh functionality
if st.session_state.auto_refresh and api_key:
    time.sleep(10)
    st.rerun()

# Footer Section
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
            padding: 3rem; 
            border-radius: 20px; 
            text-align: center;
            margin-top: 3rem;">
    <h2 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               margin-bottom: 1rem;">
        Need Help?
    </h2>
    <p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">
        Access comprehensive documentation and support resources
    </p>
    
    <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
        <a href="https://kie.ai/docs" style="text-decoration: none;">
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📚</div>
                <div style="color: #667eea; font-weight: 600;">Documentation</div>
            </div>
        </a>
        <a href="https://kie.ai/api-key" style="text-decoration: none;">
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔑</div>
                <div style="color: #667eea; font-weight: 600;">Get API Key</div>
            </div>
        </a>
        <a href="https://kie.ai/support" style="text-decoration: none;">
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💬</div>
                <div style="color: #667eea; font-weight: 600;">Support Center</div>
            </div>
        </a>
        <a href="https://kie.ai/pricing" style="text-decoration: none;">
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💳</div>
                <div style="color: #667eea; font-weight: 600;">Pricing</div>
            </div>
        </a>
    </div>
    
    <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(102, 126, 234, 0.2);">
        <p style="color: #999; font-size: 0.9rem;">
            Sora Watermark Remover Pro v2.0.0<br>
            Made with ❤️ using Streamlit | Powered by <a href="https://kie.ai" style="color: #667eea;">KIE.AI</a>
        </p>
        <p style="color: #999; font-size: 0.8rem; margin-top: 1rem;">
            © 2025 All rights reserved | <a href="#" style="color: #667eea;">Privacy Policy</a> | <a href="#" style="color: #667eea;">Terms of Service</a>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Additional CSS for spinner animation
st.markdown("""
<style>
    .spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #FFA500;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)
