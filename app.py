import streamlit as st
import requests
import time
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Sora Watermark Remover",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        transform: translateY(-2px);
    }
    .upload-box {
        border: 2px dashed #FF4B4B;
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'result_url' not in st.session_state:
    st.session_state.result_url = None
if 'task_id' not in st.session_state:
    st.session_state.task_id = None

# API Configuration
API_BASE_URL = "https://kie.ai"
API_ENDPOINT = f"{API_BASE_URL}/sora-2-watermark-remover"

def upload_video(video_file, api_key):
    """Upload video to the API"""
    try:
        files = {'video': (video_file.name, video_file, 'video/mp4')}
        headers = {'Authorization': f'Bearer {api_key}'}
        
        response = requests.post(
            API_ENDPOINT,
            files=files,
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error uploading video: {str(e)}")
        return None

def check_task_status(task_id, api_key):
    """Check the status of the processing task"""
    try:
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(
            f"{API_ENDPOINT}/{task_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error checking status: {str(e)}")
        return None

def download_video(url, filename="processed_video.mp4"):
    """Download the processed video"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        return None

# Header
st.title("🎬 Sora Watermark Remover")
st.markdown("### Remove watermarks from your Sora-generated videos effortlessly")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("API Key", type="password", help="Enter your KIE.AI API key")
    
    st.markdown("---")
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. Enter your API key
    2. Upload a Sora video with watermark
    3. Click 'Remove Watermark'
    4. Wait for processing
    5. Download your clean video
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This tool uses the KIE.AI API to remove watermarks from Sora-generated videos.
    
    **Supported formats:**
    - MP4
    - MOV
    - AVI
    
    **Max file size:** 500MB
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("[API Documentation](https://kie.ai/sora-2-watermark-remover)")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Video")
    
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=['mp4', 'mov', 'avi'],
        help="Upload a Sora video with watermark"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.markdown(f"**File size:** {uploaded_file.size / (1024*1024):.2f} MB")
        
        # Display video preview
        st.video(uploaded_file)
        
        if st.button("🚀 Remove Watermark", disabled=not api_key or st.session_state.processing):
            if not api_key:
                st.error("⚠️ Please enter your API key in the sidebar")
            else:
                st.session_state.processing = True
                
                with st.spinner("Uploading video..."):
                    result = upload_video(uploaded_file, api_key)
                
                if result:
                    st.session_state.task_id = result.get('task_id') or result.get('id')
                    
                    if st.session_state.task_id:
                        st.info(f"📝 Task ID: {st.session_state.task_id}")
                        
                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Poll for completion
                        max_attempts = 120  # 10 minutes max
                        attempt = 0
                        
                        while attempt < max_attempts:
                            status = check_task_status(st.session_state.task_id, api_key)
                            
                            if status:
                                state = status.get('status') or status.get('state')
                                
                                if state == 'completed':
                                    progress_bar.progress(100)
                                    status_text.success("✅ Processing complete!")
                                    st.session_state.result_url = status.get('output_url') or status.get('result_url')
                                    st.session_state.processing = False
                                    st.rerun()
                                    break
                                elif state == 'failed':
                                    status_text.error("❌ Processing failed")
                                    st.session_state.processing = False
                                    break
                                elif state in ['processing', 'pending', 'queued']:
                                    progress = min(int((attempt / max_attempts) * 100), 95)
                                    progress_bar.progress(progress)
                                    status_text.info(f"⏳ Status: {state.capitalize()}...")
                            
                            time.sleep(5)
                            attempt += 1
                        
                        if attempt >= max_attempts:
                            status_text.warning("⏱️ Processing timeout. Please check back later.")
                            st.session_state.processing = False
                    else:
                        st.error("❌ Failed to get task ID from response")
                        st.session_state.processing = False
                else:
                    st.session_state.processing = False

with col2:
    st.subheader("📥 Download Result")
    
    if st.session_state.result_url:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### ✨ Your video is ready!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button
        video_data = download_video(st.session_state.result_url)
        
        if video_data:
            st.download_button(
                label="⬇️ Download Processed Video",
                data=video_data,
                file_name="watermark_removed.mp4",
                mime="video/mp4"
            )
            
            # Display processed video
            st.video(st.session_state.result_url)
            
            # Reset button
            if st.button("🔄 Process Another Video"):
                st.session_state.result_url = None
                st.session_state.task_id = None
                st.session_state.processing = False
                st.rerun()
        else:
            st.error("Failed to download video. Please try the direct link:")
            st.markdown(f"[Download Link]({st.session_state.result_url})")
    else:
        st.info("👈 Upload a video and click 'Remove Watermark' to get started")
        
        # Feature highlights
        st.markdown("### ✨ Features")
        st.markdown("""
        - **Fast Processing**: Typically 2-5 minutes
        - **High Quality**: Maintains original video quality
        - **Easy to Use**: Simple 3-step process
        - **Secure**: Your videos are processed securely
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Made with ❤️ using Streamlit | Powered by KIE.AI</p>
    <p>⚠️ Please ensure you have the rights to remove watermarks from the videos you process</p>
</div>
""", unsafe_allow_html=True)
