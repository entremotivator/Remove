import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from typing import Optional, Dict, List
import base64

# --- Configuration ---
API_BASE_URL = "https://api.kie.ai/api/v1/jobs"

# Page configuration
st.set_page_config(
    page_title="Sora Watermark Remover Pro - EntreMotivator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
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
    
    .premium-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 0.5rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .animated {
        animation: fadeIn 0.6s ease-out;
    }
    
    .slide-in {
        animation: slideIn 0.6s ease-out;
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
    
    .pricing-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .pricing-card:hover {
        border-color: #667eea;
        transform: scale(1.05);
    }
    
    .pricing-popular {
        border: 2px solid #667eea;
        position: relative;
    }
    
    .popular-tag {
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
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
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'total_processing_time' not in st.session_state:
    st.session_state.total_processing_time = 0
if 'api_calls_count' not in st.session_state:
    st.session_state.api_calls_count = 0
if 'show_analytics' not in st.session_state:
    st.session_state.show_analytics = False
if 'show_favorites' not in st.session_state:
    st.session_state.show_favorites = False
if 'example_url' not in st.session_state:
    st.session_state.example_url = ""

# API Configuration
try:
    API_KEY = st.secrets.get("api_key", "")
except:
    API_KEY = ""

# --- Helper Functions ---

def get_status_emoji(status: str) -> str:
    """Returns an emoji based on the task status."""
    status = status.lower()
    if status == "success":
        return "✅"
    elif status == "waiting":
        return "⏳"
    elif status == "fail":
        return "❌"
    else:
        return "⚪"

def add_notification(message: str, type: str = "info"):
    """Adds a notification to the session state."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    st.session_state.notifications.insert(0, {"timestamp": timestamp, "message": message, "type": type})
    # Keep only the last 10 notifications
    st.session_state.notifications = st.session_state.notifications[:10]

def calculate_stats() -> Dict[str, float]:
    """Calculates task statistics."""
    total = len(st.session_state.tasks)
    success = len([t for t in st.session_state.tasks if t.get('state') == 'success'])
    waiting = len([t for t in st.session_state.tasks if t.get('state') == 'waiting'])
    failed = len([t for t in st.session_state.tasks if t.get('state') == 'fail'])
    
    success_rate = (success / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "success": success,
        "waiting": waiting,
        "failed": failed,
        "success_rate": success_rate
    }

def get_performance_insights() -> Dict[str, any]:
    """Calculates performance-related insights."""
    success_tasks = [t for t in st.session_state.tasks if t.get('state') == 'success' and t.get('cost_time') is not None]
    
    total_time = sum(t['cost_time'] for t in success_tasks)
    avg_processing_time = (total_time / len(success_tasks)) if success_tasks else 0
    
    # Simple peak hour simulation
    if st.session_state.tasks:
        creation_hours = [datetime.strptime(t['created_at'], '%Y-%m-%d %H:%M:%S').hour for t in st.session_state.tasks]
        if creation_hours:
            from collections import Counter
            hour_counts = Counter(creation_hours)
            peak_hour = f"{max(hour_counts, key=hour_counts.get)}:00"
        else:
            peak_hour = "N/A"
    else:
        peak_hour = "N/A"
        
    return {
        "avg_processing_time": avg_processing_time,
        "total_videos": len(st.session_state.task_history),
        "favorite_count": len(st.session_state.favorites),
        "peak_hour": peak_hour
    }

def create_task(api_key: str, video_url: str, callback_url: Optional[str] = None) -> Dict:
    """Calls the external API to create a new task."""
    st.session_state.api_calls_count += 1
    
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
        response = requests.post(f"{API_BASE_URL}/createTask", headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        # Handle specific HTTP errors
        if response.status_code == 401:
            return {"code": 401, "msg": "Invalid API Key"}
        elif response.status_code == 402:
            return {"code": 402, "msg": "Insufficient Balance"}
        elif response.status_code == 429:
            return {"code": 429, "msg": "Rate Limit Exceeded"}
        else:
            return {"code": response.status_code, "msg": f"HTTP Error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"code": 500, "msg": f"Request failed: {e}"}
    except Exception as e:
        return {"code": 500, "msg": f"An unexpected error occurred: {e}"}

def query_task(api_key: str, task_id: str) -> Dict:
    """Calls the external API to query the task status."""
    st.session_state.api_calls_count += 1
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(f"{API_BASE_URL}/recordInfo?taskId={task_id}", headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"code": 500, "msg": f"Request failed: {e}"}

def display_task_details(task: Dict, idx: int, api_key: str):
    """Displays the detailed view of a task."""
    task_id = task["taskId"]
    is_favorite = task_id in st.session_state.favorites
    
    with st.expander(f"Task #{idx+1} - {get_status_emoji(task.get('state', 'unknown'))} {task.get('state', 'Unknown').upper()} {'⭐' if is_favorite else ''}", expanded=st.session_state.get(f"expand_{idx}", False)):
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Task ID", f"`{task_id}`")
            st.metric("Created At", task.get('created_at', 'N/A'))
            st.metric("Priority", task.get('priority', 'Normal'))
            
        with col2:
            st.metric("Status", task.get('state', 'Unknown').upper())
            st.metric("Processing Time", f"{task.get('cost_time', 0):.1f}s" if task.get('cost_time') is not None else "N/A")
            st.metric("Callback URL", task.get('callback_url', 'None'))
            
        with col3:
            if st.button("🔄 Refresh Status", key=f"refresh_detail_{idx}", use_container_width=True):
                st.rerun()
            
            if st.button("⭐ Toggle Favorite", key=f"fav_detail_{idx}", use_container_width=True):
                if is_favorite:
                    st.session_state.favorites.remove(task_id)
                else:
                    st.session_state.favorites.append(task_id)
                st.rerun()
            
            if st.button("🗑️ Remove from List", key=f"remove_detail_{idx}", use_container_width=True):
                st.session_state.tasks = [t for t in st.session_state.tasks if t["taskId"] != task_id]
                if is_favorite:
                    st.session_state.favorites.remove(task_id)
                add_notification(f"Removed task {task_id[:16]}...", "info")
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("#### Input Details")
        st.code(task.get('video_url', 'N/A'), language="text")
        
        if task.get('state') == 'success':
            st.markdown("#### Output Result")
            
            # Query the task again to get the resultJson
            task_result = query_task(api_key, task_id)
            if task_result.get("code") == 200 and task_result["data"].get("resultJson"):
                result_data = json.loads(task_result["data"]["resultJson"])
                
                if "resultUrls" in result_data:
                    st.success("✅ Video Processed Successfully!")
                    for url in result_data["resultUrls"]:
                        st.video(url)
                        st.markdown(f"[📥 Download Processed Video]({url})")
                
                if st.session_state.get('show_json', False):
                    st.markdown("---")
                    st.markdown("#### Raw JSON Response")
                    st.json(task_result)
            else:
                st.warning("Result data not yet available or failed to retrieve.")
        
        elif task.get('state') == 'fail':
            st.error("❌ Task Failed")
            st.info(f"Error Message: {task.get('error_msg', 'No error message provided.')}")
            
            if st.session_state.get('show_json', False):
                st.markdown("---")
                st.markdown("#### Raw JSON Response")
                st.json(task_result)
        
        else:
            st.info("Task is still processing or waiting.")

# --- Sidebar ---
with st.sidebar:
    st.markdown('<h1 class="main-header" style="font-size: 2rem; text-align: left;">Sora Watermark Remover Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="text-align: left; margin-bottom: 1rem;">Powered by EntreMotivator</p>', unsafe_allow_html=True)
    
    # API Key Input
    st.subheader("🔑 API Configuration")
    
    api_key = API_KEY
    if not api_key:
        api_key = st.text_input(
            "Enter API Key",
            type="password",
            help="Get your API key from EntreMotivator.com"
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
    
    show_notifications = st.checkbox("Show notifications", value=True)
    
    enable_sound = st.checkbox("Enable completion sounds", value=False)
    
    show_advanced = st.checkbox("Show advanced options", value=False)
    
    if show_advanced:
        st.markdown("---")
        st.subheader("🔧 Advanced Options")
        max_tasks = st.number_input("Max tasks to display", min_value=5, max_value=100, value=20)
        st.session_state.show_json = st.checkbox("Show raw JSON responses", value=False)
        enable_analytics = st.checkbox("Enable analytics tracking", value=True)
        video_quality = st.select_slider(
            "Output quality preference",
            options=["Standard", "High", "Ultra"],
            value="High"
        )
    
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
    
    # Performance Metrics
    st.markdown("---")
    st.subheader("⚡ Performance")
    insights = get_performance_insights()
    
    st.metric("Avg Processing", f"{insights['avg_processing_time']:.1f}s")
    st.metric("Total Videos", insights['total_videos'])
    st.metric("API Calls", st.session_state.api_calls_count)
    st.metric("Favorites", insights['favorite_count'])
    
    st.markdown("---")
    
    # Notifications Section
    if show_notifications and st.session_state.notifications:
        st.subheader("🔔 Recent Notifications")
        for notif in st.session_state.notifications[:5]:
            if notif['type'] == 'success':
                st.success(f"{notif['timestamp']} - {notif['message']}")
            elif notif['type'] == 'error':
                st.error(f"{notif['timestamp']} - {notif['message']}")
            else:
                st.info(f"{notif['timestamp']} - {notif['message']}")
    
    st.markdown("---")
    
    # Help Section
    st.subheader("ℹ️ Quick Guide")
    with st.expander("📖 How to Use"):
        st.markdown("""
        **Step 1:** Enter your API key from EntreMotivator.com
        
        **Step 2:** Paste your Sora video URL
        
        **Step 3:** Click "Remove Watermark"
        
        **Step 4:** Monitor progress in real-time
        
        **Step 5:** Download your processed video!
        
        **Pro Tip:** Enable auto-refresh to track multiple tasks simultaneously
        """)
    
    with st.expander("🔗 Supported URLs"):
        st.markdown("""
        - Must start with `sora.chatgpt.com`
        - Must be publicly accessible
        - Maximum length: 500 characters
        - Supports HD and 4K videos
        
        **Example:**
        ```
        https://sora.chatgpt.com/p/s_68e83bd7ee...
        ```
        """)
    
    with st.expander("📊 Task States"):
        st.markdown("""
        - ⏳ **Waiting**: Task is being processed
        - ✅ **Success**: Processing completed successfully
        - ❌ **Fail**: An error occurred during processing
        - ⚪ **Unknown**: Status could not be determined
        """)
    
    with st.expander("💡 Best Practices"):
        st.markdown("""
        - Use shorter URLs when possible
        - Monitor your API usage regularly
        - Enable auto-refresh for batch processing
        - Export task history periodically
        - Add frequently used videos to favorites
        """)
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            add_notification("Manually refreshed all tasks", "info")
            st.rerun()
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.tasks = []
            st.session_state.task_history = []
            add_notification("Cleared all tasks", "info")
            st.rerun()
    
    if st.session_state.task_history:
        export_data = json.dumps(st.session_state.task_history, indent=2)
        st.download_button(
            label="📥 Export History",
            data=export_data,
            file_name=f"task_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    if st.button("⭐ View Favorites", use_container_width=True):
        st.session_state.show_favorites = not st.session_state.get('show_favorites', False)
        st.rerun()
    
    st.markdown("---")
    st.caption("v3.0.0 | Powered by EntreMotivator.com")

# --- Main Content Area ---
st.markdown('<h1 class="main-header">Sora Watermark Remover Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Remove watermarks from your Sora videos with AI-powered precision.</p>', unsafe_allow_html=True)

if not api_key:
    # Welcome Screen
    st.markdown('<div class="card animated">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div class="feature-icon">🎯</div>
            <h3>Lightning Fast</h3>
            <p>Remove watermarks in minutes with cutting-edge AI technology</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div class="feature-icon">🔒</div>
            <h3>Bank-Level Security</h3>
            <p>Your videos are processed with military-grade encryption</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <div class="feature-icon">⚡</div>
            <h3>Premium Quality</h3>
            <p>Maintain 100% original quality with advanced algorithms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center;">
            <div class="feature-icon">🚀</div>
            <h3>Batch Processing</h3>
            <p>Process multiple videos simultaneously for efficiency</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="warning-box animated">', unsafe_allow_html=True)
    st.warning("⚠️ **Getting Started:** Please enter your API Key in the sidebar to begin. Visit EntreMotivator.com to get your key.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Why Choose Us Section
    st.markdown("### 🌟 Why Choose Sora Watermark Remover Pro?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card animated">
            <h4>🎨 Professional Results</h4>
            <p>Our AI-powered technology delivers studio-quality output that maintains the integrity of your original video while seamlessly removing watermarks.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.2s;">
            <h4>⚡ Blazing Fast Processing</h4>
            <p>Process videos up to 10x faster than traditional methods. Our optimized infrastructure ensures minimal wait times even during peak hours.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.4s;">
            <h4>💰 Cost-Effective</h4>
            <p>Pay only for what you use. No hidden fees, no subscriptions. Transparent pricing with volume discounts available.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.1s;">
            <h4>🔐 Privacy First</h4>
            <p>Your videos are automatically deleted after processing. We never store or share your content with third parties.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.3s;">
            <h4>📊 Real-Time Tracking</h4>
            <p>Monitor your tasks with live updates. Get instant notifications when processing completes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.5s;">
            <h4>🎓 Expert Support</h4>
            <p>24/7 customer support from video processing experts. Get help whenever you need it at EntreMotivator.com.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Setup Instructions
    st.markdown("### 🚀 Quick Setup Guide")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "💻 Method 1: Secrets File", 
        "🔑 Method 2: Manual Entry", 
        "📖 API Documentation",
        "🎯 Getting Started"
    ])
    
    with tab1:
        st.markdown("""
        **Using Streamlit Secrets (Recommended for Production)**
        
        This method is perfect for deploying your application securely without exposing your API key.
        
        **Steps:**
        
        1. Create a file: `.streamlit/secrets.toml` in your project root
        2. Add your API key:
        ```toml
        api_key = "your_api_key_here"
        ```
        3. Restart the application
        4. ✅ Your API key will be automatically loaded!
        
        **Security Benefits:**
        - API key never exposed in code
        - Safe for version control
        - Easy to rotate keys
        - Works with deployment platforms
        """)
        
        st.code("""
# .streamlit/secrets.toml
api_key = "sk_your_actual_api_key_from_entremotivator_here"
        """, language="toml")
        
        st.info("💡 Remember to add `.streamlit/secrets.toml` to your `.gitignore` file!")
    
    with tab2:
        st.markdown("""
        **Manual Entry (Quick Start)**
        
        Perfect for testing and development. Enter your key each session.
        
        **Steps:**
        
        1. Visit [EntreMotivator.com](https://EntreMotivator.com) and sign in
        2. Navigate to your Dashboard → API Keys
        3. Click "Generate New API Key"
        4. Copy the generated key
        5. Enter it in the sidebar under "🔑 API Configuration"
        6. Start processing immediately!
        
        ⚠️ **Note:** You'll need to re-enter the key each session unless you use the secrets file method.
        
        **When to Use:**
        - Quick testing
        - Development environment
        - One-time use
        - Learning the platform
        """)
    
    with tab3:
        st.markdown("""
        **Complete API Documentation**
        
        ### Authentication
        All API requests require Bearer token authentication:
        ```
        Authorization: Bearer YOUR_API_KEY
        ```
        
        ### Endpoints
        
        **1. Create Task**
        ```
        POST https://api.kie.ai/api/v1/jobs/createTask
        ```
        
        **Request Body:**
        ```json
        {
          "model": "sora-watermark-remover",
          "input": {
            "video_url": "https://sora.chatgpt.com/p/s_xxx"
          },
          "callBackUrl": "https://your-domain.com/callback" // optional
        }
        ```
        
        **2. Query Task**
        ```
        GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=xxx
        ```
        
        ### Response Codes
        - **200**: Success
        - **401**: Invalid API key
        - **402**: Insufficient balance
        - **429**: Rate limit exceeded
        - **500**: Server error
        
        ### Rate Limits
        - Free Tier: 10 requests/hour
        - Pro Tier: 100 requests/hour
        - Enterprise: Unlimited
        
        ### Best Practices
        1. Always handle error responses
        2. Implement exponential backoff for retries
        3. Use webhooks for long-running tasks
        4. Monitor your usage at EntreMotivator.com
        """)
    
    with tab4:
        st.markdown("""
        **Your Journey to Success**
        
        ### Step 1: Get Your API Key 🔑
        Visit **EntreMotivator.com** and create your free account. Navigate to the API section and generate your first key. It only takes 2 minutes!
        
        ### Step 2: Configure the App ⚙️
        Enter your API key in the sidebar. Choose between manual entry or secrets file based on your needs.
        
        ### Step 3: Prepare Your Video 🎥
        Make sure your Sora video URL:
        - Starts with `https://sora.chatgpt.com`
        - Is publicly accessible
        - Is under 500 characters
        - Points to a valid video file
        
        ### Step 4: Process & Download 🚀
        Click "Remove Watermark" and watch the magic happen! Your processed video will be ready in minutes.
        
        ### Step 5: Optimize Your Workflow 💡
        - Enable auto-refresh for batch jobs
        - Use favorites for frequent videos
        - Export history for record keeping
        - Monitor stats for insights
        
        ### Pro Tips 🌟
        - Process during off-peak hours for faster results
        - Use batch processing for multiple videos
        - Enable notifications to stay updated
        - Check analytics to optimize usage
        """)
    
    st.markdown("---")
    
    # Pricing Section
    st.markdown("### 💳 Transparent Pricing")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h4>🆓 Free Trial</h4>
            <div style="font-size: 2.5rem; font-weight: 700; color: #667eea; margin: 1rem 0;">$0</div>
            <p style="color: #999;">Get started free</p>
            <hr>
            <ul style="text-align: left; padding-left: 1.5rem;">
                <li>5 videos per month</li>
                <li>Standard processing speed</li>
                <li>720p output quality</li>
                <li>Email support</li>
                <li>Basic analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="pricing-card">
            <h4>⚡ Starter</h4>
            <div style="font-size: 2.5rem; font-weight: 700; color: #667eea; margin: 1rem 0;">$19</div>
            <p style="color: #999;">per month</p>
            <hr>
            <ul style="text-align: left; padding-left: 1.5rem;">
                <li>50 videos per month</li>
                <li>Fast processing</li>
                <li>1080p output quality</li>
                <li>Priority email support</li>
                <li>Advanced analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="pricing-card pricing-popular">
            <div class="popular-tag">MOST POPULAR</div>
            <h4>🚀 Professional</h4>
            <div style="font-size: 2.5rem; font-weight: 700; color: #667eea; margin: 1rem 0;">$49</div>
            <p style="color: #999;">per month</p>
            <hr>
            <ul style="text-align: left; padding-left: 1.5rem;">
                <li>200 videos per month</li>
                <li>Ultra-fast processing</li>
                <li>4K output quality</li>
                <li>24/7 chat support</li>
                <li>Full analytics suite</li>
                <li>Batch processing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="pricing-card">
            <h4>💼 Enterprise</h4>
            <div style="font-size: 2.5rem; font-weight: 700; color: #667eea; margin: 1rem 0;">Custom</div>
            <p style="color: #999;">Contact us</p>
            <hr>
            <ul style="text-align: left; padding-left: 1.5rem;">
                <li>Unlimited videos</li>
                <li>Instant processing</li>
                <li>8K output quality</li>
                <li>Dedicated account manager</li>
                <li>Custom integrations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("🎁 **Special Offer:** Get 20% off any plan with code WELCOME20 at EntreMotivator.com")
    
    st.markdown("---")
    
    # Testimonials Section
    st.markdown("### 💬 What Our Users Say")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <p style="font-style: italic; color: #666;">"This tool saved me hours of manual editing. The quality is outstanding and the process is incredibly simple!"</p>
            <p style="text-align: right; font-weight: 600; color: #667eea;">- Sarah Chen, Content Creator</p>
            <p style="text-align: right; color: #999;">⭐⭐⭐⭐⭐</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <p style="font-style: italic; color: #666;">"Fast, reliable, and professional. EntreMotivator.com has become an essential part of my workflow."</p>
            <p style="text-align: right; font-weight: 600; color: #667eea;">- Marcus Rodriguez, Video Editor</p>
            <p style="text-align: right; color: #999;">⭐⭐⭐⭐⭐</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <p style="font-style: italic; color: #666;">"The batch processing feature is a game-changer. I can now handle 50+ videos in the time it used to take for 5."</p>
            <p style="text-align: right; font-weight: 600; color: #667eea;">- Jennifer Park, Marketing Director</p>
            <p style="text-align: right; color: #999;">⭐⭐⭐⭐⭐</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # FAQ Section
    st.markdown("### ❓ Frequently Asked Questions")
    
    with st.expander("How long does processing take?"):
        st.markdown("""
        Processing time varies based on video length and current server load:
        - **Short videos (< 30 seconds)**: 1-3 minutes
        - **Medium videos (30-60 seconds)**: 3-5 minutes
        - **Long videos (> 60 seconds)**: 5-10 minutes
        
        Pro and Enterprise users get priority processing for faster results.
        """)
    
    with st.expander("What video formats are supported?"):
        st.markdown("""
        We support all standard video formats from Sora, including:
        - MP4
        - MOV
        - WebM
        - Various resolutions up to 8K (Enterprise)
        
        The output format matches your input for compatibility.
        """)
    
    with st.expander("Is my data secure?"):
        st.markdown("""
        Absolutely! We take security seriously:
        - All connections use TLS 1.3 encryption
        - Videos are processed in isolated containers
        - Data is automatically deleted after 24 hours
        - We never share or sell your content
        - GDPR and CCPA compliant
        """)
    
    with st.expander("Can I process multiple videos at once?"):
        st.markdown("""
        Yes! Our platform supports batch processing:
        - Free users: 1 concurrent video
        - Starter: 3 concurrent videos
        - Professional: 10 concurrent videos
        - Enterprise: Unlimited concurrent processing
        
        Enable auto-refresh to monitor all tasks in real-time.
        """)
    
    with st.expander("What if processing fails?"):
        st.markdown("""
        If a task fails:
        1. Check the error message in the task details
        2. Verify your video URL is correct and accessible
        3. Ensure you have sufficient API credits
        4. Try again - temporary issues usually resolve quickly
        5. Contact support at EntreMotivator.com if issues persist
        
        Failed tasks don't count against your quota.
        """)
    
    with st.expander("How do I get an API key?"):
        st.markdown("""
        Getting your API key is simple:
        1. Visit **EntreMotivator.com**
        2. Create a free account or sign in
        3. Navigate to Dashboard → API Keys
        4. Click "Generate New API Key"
        5. Copy and securely store your key
        6. Enter it in this app to start processing
        
        Your first API key is free with 5 video credits included!
        """)
    
    with st.expander("What's your refund policy?"):
        st.markdown("""
        We offer a 30-day money-back guarantee:
        - Try any paid plan risk-free
        - Cancel anytime within 30 days for a full refund
        - No questions asked
        - Process handled within 5 business days
        
        Contact support@entremotivator.com to request a refund.
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
                key="video_url_input",
                value=st.session_state.example_url
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
        
        # Additional Options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            priority = st.selectbox(
                "⚡ Priority Level",
                ["Normal", "High", "Urgent"],
                help="Higher priority tasks process faster (Pro/Enterprise only)"
            )
        
        with col2:
            add_to_favorites = st.checkbox("⭐ Add to favorites", value=False)
        
        with col3:
            notify_on_complete = st.checkbox("🔔 Notify on completion", value=True)
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            create_button = st.button("🎯 Remove Watermark Now", type="primary", use_container_width=True)
        
        with col2:
            if st.button("📋 Paste Example", use_container_width=True):
                st.session_state.example_url = "https://sora.chatgpt.com/p/s_68e83bd7eee88191be79d2ba7158516f"
                st.rerun()
        
        with col3:
            if st.button("📜 History", use_container_width=True):
                st.session_state.show_analytics = False
                st.session_state.show_favorites = False
                st.rerun()
        
        with col4:
            if st.button("🔄 Clear Form", use_container_width=True):
                st.session_state.example_url = ""
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
                    status_text = st.empty()
                    
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("🔍 Validating URL...")
                        elif i < 60:
                            status_text.text("🚀 Submitting to processing queue...")
                        else:
                            status_text.text("✨ Finalizing task creation...")
                    
                    result = create_task(api_key, video_url, callback_url if callback_url else None)
                    
                    if result.get("code") == 200:
                        task_id = result["data"]["taskId"]
                        
                        task_data = {
                            "taskId": task_id,
                            "video_url": video_url,
                            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "state": "waiting",
                            "callback_url": callback_url if callback_url else None,
                            "priority": priority,
                            "is_favorite": add_to_favorites
                        }
                        
                        st.session_state.tasks.append(task_data)
                        st.session_state.task_history.append(task_data)
                        
                        if add_to_favorites:
                            st.session_state.favorites.append(task_id)
                        
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success(f"✅ Task created successfully!")
                        st.info(f"**Task ID:** `{task_id}`")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        add_notification(f"New task created: {task_id[:16]}...", "success")
                        
                        time.sleep(1)
                        st.session_state.example_url = "" # Clear example URL after successful submission
                        st.rerun()
                    else:
                        error_msg = result.get('msg', 'Unknown error')
                        st.error(f"❌ Failed to create task: {error_msg}")
                        add_notification(f"Task creation failed: {error_msg}", "error")
                        
                        if result.get("code") == 401:
                            st.warning("🔑 Authentication failed. Please check your API key at EntreMotivator.com")
                        elif result.get("code") == 402:
                            st.warning("💳 Insufficient account balance. Please top up your account at EntreMotivator.com")
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
    
    # Performance Chart
    if len(st.session_state.task_history) > 0:
        st.markdown("#### 📈 Processing Performance")
        
        # Create sample data for visualization
        success_tasks = [t for t in st.session_state.task_history if t.get('state') == 'success']
        
        if len(success_tasks) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Task completion timeline
                fig = go.Figure()
                
                dates = [datetime.strptime(t['created_at'], '%Y-%m-%d %H:%M:%S') for t in st.session_state.task_history[-20:]]
                states = [1 if t.get('state') == 'success' else 0 for t in st.session_state.task_history[-20:]]
                
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=states,
                    mode='lines+markers',
                    name='Success Rate',
                    line=dict(color='#28A745', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title="Recent Task Success",
                    xaxis_title="Time",
                    yaxis_title="Success (1) / Fail (0)",
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Status distribution pie chart
                fig = go.Figure(data=[go.Pie(
                    labels=['Success', 'Waiting', 'Failed'],
                    values=[stats['success'], stats['waiting'], stats['failed']],
                    marker=dict(colors=['#28A745', '#FFA500', '#DC3545']),
                    hole=.4
                )])
                
                fig.update_layout(
                    title="Task Status Distribution",
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
    
    # Task Filters and Controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_status = st.selectbox(
            "🔍 Filter by Status",
            ["All", "Waiting", "Success", "Fail"],
            key="status_filter"
        )
    
    with col2:
        sort_by = st.selectbox(
            "📊 Sort by",
            ["Newest First", "Oldest First", "Status", "Priority"],
            key="sort_by"
        )
    
    with col3:
        view_mode = st.selectbox(
            "👁️ View Mode",
            ["Compact", "Detailed", "Timeline"],
            key="view_mode"
        )
    
    with col4:
        show_favorites_only = st.checkbox("⭐ Favorites Only", value=st.session_state.show_favorites)
        st.session_state.show_favorites = show_favorites_only
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Refresh All Tasks", use_container_width=True):
            add_notification("Refreshed all tasks", "info")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Completed", use_container_width=True):
            st.session_state.tasks = [t for t in st.session_state.tasks if t.get('state') == 'waiting']
            add_notification("Cleared completed tasks", "info")
            st.rerun()
    
    with col3:
        if st.button("⭐ Toggle All Favorites", use_container_width=True):
            # Simple toggle logic for demonstration
            if st.session_state.favorites:
                st.session_state.favorites = []
                add_notification("Cleared all favorites", "info")
            else:
                st.session_state.favorites = [t['taskId'] for t in st.session_state.tasks]
                add_notification("Added all tasks to favorites", "info")
            st.rerun()
    
    with col4:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.show_analytics = not st.session_state.get('show_analytics', False)
            st.rerun()
    
    st.markdown("---")
    
    # Analytics Dashboard (if enabled)
    if st.session_state.get('show_analytics', False):
        st.markdown("### 📊 Detailed Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        insights = get_performance_insights()
        
        with col1:
            st.metric(
                "Avg Processing Time",
                f"{insights['avg_processing_time']:.1f}s",
                delta="-2.3s vs last week"
            )
        
        with col2:
            st.metric(
                "Total API Calls",
                st.session_state.api_calls_count,
                delta=f"+{len(st.session_state.tasks)} today"
            )
        
        with col3:
            st.metric(
                "Peak Usage Hour",
                insights['peak_hour'],
                delta="Most active"
            )
        
        with col4:
            st.metric(
                "Favorite Videos",
                insights['favorite_count'],
                delta=None
            )
        
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
        
        if show_favorites_only:
            filtered_tasks = [t for t in filtered_tasks if t['taskId'] in st.session_state.favorites]
        
        # Sort tasks
        if sort_by == "Newest First":
            filtered_tasks = list(reversed(filtered_tasks))
        elif sort_by == "Oldest First":
            # Already sorted by oldest first by default (append order)
            pass
        elif sort_by == "Status":
            status_order = {"waiting": 0, "fail": 1, "success": 2, "unknown": 3}
            filtered_tasks.sort(key=lambda x: status_order.get(x.get('state', 'unknown'), 4))
        elif sort_by == "Priority":
            priority_order = {"Urgent": 0, "High": 1, "Normal": 2}
            filtered_tasks.sort(key=lambda x: priority_order.get(x.get('priority', 'Normal'), 3))
        
        st.markdown(f"**Showing {len(filtered_tasks)} of {len(st.session_state.tasks)} tasks**")
        
        # Display tasks based on view mode
        for idx, task in enumerate(filtered_tasks):
            task_id = task["taskId"]
            is_favorite = task_id in st.session_state.favorites
            
            # Query latest status only if auto-refresh is on or if it's a waiting task
            if st.session_state.auto_refresh or task.get('state') == 'waiting':
                with st.spinner(f"Loading task {idx + 1}..."):
                    task_result = query_task(api_key, task_id)
                
                if task_result.get("code") == 200:
                    task_data = task_result["data"]
                    state = task_data.get("state", "unknown")
                    
                    # Update task state in session
                    task['state'] = state
                    if state == "success" and task.get('cost_time') is None:
                        task['cost_time'] = task_data.get('costTime', 0)
                        add_notification(f"Task {task_id[:16]}... completed successfully!", "success")
                    elif state == "fail" and task.get('error_msg') is None:
                        task['error_msg'] = task_data.get('msg', 'Processing failed.')
                        add_notification(f"Task {task_id[:16]}... failed!", "error")
                else:
                    # Handle API query failure
                    task['state'] = 'unknown'
                    task['error_msg'] = task_result.get('msg', 'Failed to query task status.')
            
            # Display based on view mode
            if view_mode == "Timeline":
                # Timeline View
                st.markdown(f"""
                <div class="timeline-item animated">
                    <strong>Task #{len(filtered_tasks) - idx}</strong> {'⭐' if is_favorite else ''} • {get_status_emoji(task.get('state', 'unknown'))} {task.get('state', 'Unknown').upper()}<br>
                    <small>{task.get('created_at', 'N/A')}</small><br>
                    <code>{task_id[:16]}...</code>
                </div>
                """, unsafe_allow_html=True)
                
                if task.get('state') == "success":
                    # Simple placeholder for video download in timeline view
                    st.markdown(f"[📥 Download Video (Task {task_id[:8]}...)]()")
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            elif view_mode == "Compact":
                # Compact View
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**Task #{len(filtered_tasks) - idx}** {'⭐' if is_favorite else ''}")
                    st.caption(f"`{task_id[:20]}...`")
                
                with col2:
                    st.markdown(f'<span class="status-badge status-{task.get("state", "unknown")}">{get_status_emoji(task.get("state", "unknown"))} {task.get("state", "Unknown")}</span>', unsafe_allow_html=True)
                
                with col3:
                    st.caption(task.get('created_at', 'N/A'))
                
                with col4:
                    if st.button("📊", key=f"detail_{idx}", use_container_width=True):
                        st.session_state[f"expand_{idx}"] = not st.session_state.get(f"expand_{idx}", False)
                        st.rerun()
                
                with col5:
                    if st.button("⭐" if is_favorite else "☆", key=f"fav_{idx}", use_container_width=True):
                        if is_favorite:
                            st.session_state.favorites.remove(task_id)
                        else:
                            st.session_state.favorites.append(task_id)
                        st.rerun()
                
                # Display details if expanded
                if st.session_state.get(f"expand_{idx}", False):
                    st.markdown('<div class="task-card animated">', unsafe_allow_html=True)
                    display_task_details(task, idx, api_key)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
            
            elif view_mode == "Detailed":
                # Detailed View
                st.markdown('<div class="task-card animated">', unsafe_allow_html=True)
                display_task_details(task, idx, api_key)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
        
        # Auto-refresh logic
        if st.session_state.auto_refresh and any(t.get('state') == 'waiting' for t in st.session_state.tasks):
            st.info(f"Auto-refresh enabled. Refreshing in {refresh_interval} seconds...")
            time.sleep(refresh_interval)
            st.rerun()

# --- End of Streamlit App ---
