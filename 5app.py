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

# --- 1. Code to Hide GitHub Settings (The user's specific request) ---
# This CSS snippet hides the Streamlit menu button (three dots) which contains
# the "Deploy this app" and "View source" options.
st.markdown("""
<style>
    /* Hide the Streamlit Menu button (three dots) */
    #MainMenu {visibility: hidden;}
    /* Hide the Streamlit Footer */
    footer {visibility: hidden;}
/* Optional: Hide the "Deploy this app" button in the top right corner */
	header {visibility: hidden;}
	/* Colorful Up Back Enhancement */
	.main {
	    background: linear-gradient(180deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.02) 100%);
	}
</style>
""", unsafe_allow_html=True)

# Enhanced Custom CSS (Original code)
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
if 'show_favorites' not in st.session_state:
    st.session_state.show_favorites = False
if 'example_url' not in st.session_state:
    st.session_state.example_url = ""
if 'page' not in st.session_state:
    st.session_state.page = 'home' # New state for multi-page structure

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
    
    with st.expander(f"🎬 Task Details: {task_id[:16]}... - {task.get('state', 'Unknown').upper()}", expanded=False):
        
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

# --- New: Multi-Page Navigation Functions ---

def render_home_page(api_key):
    st.markdown('<h1 class="main-header animated">Sora Watermark Remover Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle animated">Remove watermarks from your Sora videos with a single API call. Fast, reliable, and high-quality.</p>', unsafe_allow_html=True)

    # Main Input Card
    with st.container():
        st.markdown('<div class="card animated">', unsafe_allow_html=True)
        st.subheader("🚀 Submit New Video Task")
        
        video_url = st.text_input(
            "Video URL",
            placeholder="Paste your Sora video URL here (e.g., https://example.com/video.mp4)",
            key="video_url_input"
        )
        
        callback_url = st.text_input(
            "Optional: Callback URL",
            placeholder="Enter a URL to be notified when the task is complete",
            key="callback_url_input"
        )
        
        col_submit, col_example = st.columns([3, 1])
        
        with col_submit:
            if st.button("✨ Start Watermark Removal", use_container_width=True):
                if not api_key:
                    st.error("🔑 Please enter your API Key in the sidebar first.")
                elif not video_url:
                    st.error("🔗 Please enter a valid Video URL.")
                else:
                    # Call API to create task
                    with st.spinner("Submitting task to API..."):
                        response = create_task(api_key, video_url, callback_url)
                        
                        if response.get("code") == 200:
                            task_id = response["data"]["taskId"]
                            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            
                            new_task = {
                                "taskId": task_id,
                                "video_url": video_url,
                                "created_at": created_at,
                                "state": "waiting",
                                "cost_time": None,
                                "priority": "Normal",
                                "callback_url": callback_url
                            }
                            st.session_state.tasks.insert(0, new_task)
                            st.session_state.task_history.append(new_task)
                            add_notification(f"Task submitted successfully! ID: {task_id[:16]}...", "success")
                            st.success(f"Task submitted! ID: `{task_id}`. Check the 'Task List' tab.")
                            # Clear input fields
                            st.session_state.video_url_input = ""
                            st.session_state.callback_url_input = ""
                            st.rerun()
                        else:
                            error_msg = response.get("msg", "Unknown API Error")
                            st.error(f"Task submission failed: {error_msg}")
                            add_notification(f"Task submission failed: {error_msg}", "fail")
        
        with col_example:
            if st.button("Use Example URL", use_container_width=True):
                st.session_state.video_url_input = "https://example.com/sora_sample_video.mp4"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- New: Feature Showcase Section ---
    st.markdown("---")
    st.subheader("Key Features & Benefits")
    
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    # Feature 1
    st.markdown("""
    <div class="feature-card animated" style="animation-delay: 0.1s;">
        <div class="feature-icon">⚡</div>
        <h4>Ultra-Fast Processing</h4>
        <p>Leverage our optimized infrastructure for minimal wait times. Get your clean video back in minutes, not hours.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 2
    st.markdown("""
    <div class="feature-card animated" style="animation-delay: 0.2s;">
        <div class="feature-icon">💎</div>
        <h4>High-Fidelity Output</h4>
        <p>Advanced AI models ensure the watermark removal is seamless, preserving the original video quality and detail.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 3
    st.markdown("""
    <div class="feature-card animated" style="animation-delay: 0.3s;">
        <div class="feature-icon">🔒</div>
        <h4>Secure & Private</h4>
        <p>Your videos are processed securely and deleted after a short period. Your privacy is our top priority.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- New: Call to Action ---
    st.markdown("---")
    st.subheader("Ready to Get Started?")
    st.info("Sign up on EntreMotivator.com to get your API key and start processing videos today!")
    
def render_task_list_page(api_key):
    st.markdown('<h1 class="main-header" style="font-size: 2.5rem;">Task Management Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Monitor the status and retrieve the results of your video processing tasks.</p>', unsafe_allow_html=True)

    if not api_key:
        st.warning("🔑 Please configure your API Key in the sidebar to view and manage tasks.")
        return

    # --- Task List Filtering and Sorting ---
    col_filter, col_sort, col_fav, col_refresh = st.columns([2, 2, 1, 1])
    
    status_filter = col_filter.selectbox(
        "Filter by Status",
        options=["All", "Waiting", "Success", "Fail"],
        index=0
    )
    
    sort_by = col_sort.selectbox(
        "Sort by",
        options=["Newest First", "Oldest First", "Status"],
        index=0
    )
    
    if col_fav.button("⭐ Favorites", use_container_width=True):
        st.session_state.show_favorites = not st.session_state.show_favorites
        st.rerun()
        
    if col_refresh.button("🔄 Manual Refresh", use_container_width=True):
        st.rerun()

    # Apply filters and sorting
    tasks_to_display = st.session_state.tasks
    
    # 1. Filter by Favorites
    if st.session_state.show_favorites:
        tasks_to_display = [t for t in tasks_to_display if t["taskId"] in st.session_state.favorites]
        st.info(f"Showing {len(tasks_to_display)} favorite tasks.")
        
    # 2. Filter by Status
    if status_filter != "All":
        tasks_to_display = [t for t in tasks_to_display if t.get('state', 'Unknown').lower() == status_filter.lower()]
        
    # 3. Sort
    if sort_by == "Newest First":
        tasks_to_display.sort(key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    elif sort_by == "Oldest First":
        tasks_to_display.sort(key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S'))
    elif sort_by == "Status":
        tasks_to_display.sort(key=lambda x: x.get('state', 'Unknown'))

    st.markdown("---")

    if not tasks_to_display:
        st.info("No tasks to display based on current filters.")
    else:
        for idx, task in enumerate(tasks_to_display):
            # Task Card Summary
            task_id = task["taskId"]
            status = task.get('state', 'Unknown').upper()
            is_favorite = task_id in st.session_state.favorites
            
            # Use the custom CSS class for a nicer look
            st.markdown(f'<div class="task-card slide-in">', unsafe_allow_html=True)
            
            col_sum_1, col_sum_2, col_sum_3, col_sum_4 = st.columns([3, 2, 2, 1])
            
            with col_sum_1:
                st.markdown(f"**Task ID:** `{task_id[:16]}...`")
                st.caption(f"Created: {task.get('created_at', 'N/A')}")
            
            with col_sum_2:
                st.markdown(f"**Status:** <span class='status-badge status-{status.lower()}'>{get_status_emoji(status)} {status}</span>", unsafe_allow_html=True)
            
            with col_sum_3:
                st.markdown(f"**Time:** {task.get('cost_time', 'N/A')}s")
            
            with col_sum_4:
                if st.button("Details", key=f"show_details_{idx}", use_container_width=True):
                    # Toggle the expander state in session state if needed, but for now, rely on the expander below
                    pass 
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Detailed View (Expander)
            display_task_details(task, idx, api_key)
            
def render_analytics_page():
    st.markdown('<h1 class="main-header" style="font-size: 2.5rem;">Performance Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Deep dive into your video processing usage and performance metrics.</p>', unsafe_allow_html=True)

    stats = calculate_stats()
    insights = get_performance_insights()
    
    # --- Metrics Grid ---
    st.subheader("Overall Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Tasks</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["total"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card" style="background: linear-gradient(135deg, #28A745 0%, #20C997 100%);">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Success Rate</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["success_rate"]:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card" style="background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg. Time</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{insights["avg_processing_time"]:.1f}s</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-card" style="background: linear-gradient(135deg, #DC3545 0%, #C82333 100%);">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Failed Tasks</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{stats["failed"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # --- Task Status Distribution Chart (New Feature) ---
    st.subheader("Task Status Distribution")
    
    labels = ['Success', 'Waiting', 'Failed']
    values = [stats['success'], stats['waiting'], stats['failed']]
    colors = ['#20C997', '#FF8C00', '#C82333']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors, hole=.3)])
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # --- Timeline of Recent Tasks (New Feature) ---
    st.subheader("Recent Task Timeline")
    
    recent_tasks = st.session_state.tasks[:5] # Show last 5 tasks
    
    if recent_tasks:
        for task in recent_tasks:
            status = task.get('state', 'Unknown').upper()
            time_ago = datetime.strptime(task['created_at'], '%Y-%m-%d %H:%M:%S')
            
            st.markdown(f"""
            <div class="timeline-item">
                <p style="margin-bottom: 0.2rem;">
                    <strong>{status}</strong> for Task `{task['taskId'][:10]}...`
                    <span class='status-badge status-{status.lower()}' style="margin-left: 10px;">{get_status_emoji(status)} {status}</span>
                </p>
                <small style="color: #999;">{time_ago.strftime('%Y-%m-%d %H:%M:%S')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent tasks to show in the timeline.")

def render_pricing_page():
    st.markdown('<h1 class="main-header" style="font-size: 2.5rem;">Pricing & Plans</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Choose the plan that best fits your video processing needs.</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    # Plan 1: Basic
    with col1:
        st.markdown('<div class="pricing-card animated" style="animation-delay: 0.1s;">', unsafe_allow_html=True)
        st.subheader("Basic")
        st.markdown("## $9/mo")
        st.caption("Billed Annually")
        st.markdown("---")
        st.markdown("""
        - ✅ 50 Video Tasks/mo
        - ✅ Standard Processing Speed
        - ✅ Email Support
        - ❌ Priority Queue
        - ❌ Advanced Analytics
        """)
        st.button("Select Basic", key="basic_plan", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Plan 2: Pro (Popular)
    with col2:
        st.markdown('<div class="pricing-card pricing-popular animated" style="animation-delay: 0.2s;">', unsafe_allow_html=True)
        st.markdown('<div class="popular-tag">Most Popular</div>', unsafe_allow_html=True)
        st.subheader("Pro")
        st.markdown("## $29/mo")
        st.caption("Billed Annually")
        st.markdown("---")
        st.markdown("""
        - ✅ 250 Video Tasks/mo
        - ✅ **High-Speed Processing**
        - ✅ Priority Support
        - ✅ Priority Queue
        - ✅ Advanced Analytics
        """)
        st.button("Select Pro", key="pro_plan", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Plan 3: Enterprise
    with col3:
        st.markdown('<div class="pricing-card animated" style="animation-delay: 0.3s;">', unsafe_allow_html=True)
        st.subheader("Enterprise")
        st.markdown("## Custom")
        st.caption("Contact Sales")
        st.markdown("---")
        st.markdown("""
        - ✅ Unlimited Video Tasks
        - ✅ Dedicated Infrastructure
        - ✅ 24/7 Phone Support
        - ✅ Custom SLA
        - ✅ On-Premise Option
        """)
        st.button("Contact Sales", key="enterprise_plan", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.info("All plans come with a 7-day free trial. Cancel anytime.")

# --- Sidebar ---
with st.sidebar:
    st.markdown('<h1 class="main-header" style="font-size: 2rem; text-align: left;">Sora Watermark Remover Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="text-align: left; margin-bottom: 1rem;">Powered by EntreMotivator</p>', unsafe_allow_html=True)
    
    # --- New: Navigation Menu ---
    st.subheader("🧭 Navigation")
    
    # Use radio buttons for navigation
    page_selection = st.radio(
        "Go to",
        ('Home', 'Task List', 'Analytics', 'Pricing'),
        index=['Home', 'Task List', 'Analytics', 'Pricing'].index(st.session_state.page.capitalize()),
        key="page_selector"
    )
    st.session_state.page = page_selection.lower()
    
    st.markdown("---")
    
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
    st.subheader("📊 Quick Stats")
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
    
    # --- New: Notifications Panel ---
    st.markdown("---")
    st.subheader("🔔 Notifications")
    
    if st.session_state.notifications:
        for notif in st.session_state.notifications:
            if notif['type'] == 'success':
                st.success(f"[{notif['timestamp']}] {notif['message']}")
            elif notif['type'] == 'fail':
                st.error(f"[{notif['timestamp']}] {notif['message']}")
            else:
                st.info(f"[{notif['timestamp']}] {notif['message']}")
    else:
        st.caption("No recent notifications.")

# --- Main App Logic (Multi-Page Router) ---

if st.session_state.page == 'home':
    render_home_page(api_key)
elif st.session_state.page == 'task list':
    render_task_list_page(api_key)
elif st.session_state.page == 'analytics':
    render_analytics_page()
elif st.session_state.page == 'pricing':
    render_pricing_page()

# --- Auto-Refresh Logic ---
if st.session_state.auto_refresh:
    # Use a placeholder to display the countdown
    placeholder = st.empty()
    
    # Calculate time until next refresh
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
        
    time_elapsed = time.time() - st.session_state.last_refresh
    time_to_wait = refresh_interval - (time_elapsed % refresh_interval)
    
    # Display countdown
    placeholder.info(f"Auto-refresh enabled. Next refresh in {int(time_to_wait)} seconds...")
    
    # Wait for the remaining time
    time.sleep(time_to_wait)
    
    # Update last refresh time and rerun
    st.session_state.last_refresh = time.time()
    st.rerun()

