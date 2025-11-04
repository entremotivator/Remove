import streamlit as st
import requests
import time
import json
from io import BytesIO

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
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-message {
        padding: 1rem;
        background-color: #d1ecf1;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border-radius: 0.5rem;
        margin: 1rem 0;
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
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

# API Configuration - Updated to use correct endpoint structure
API_BASE_URL = "https://api.kie.ai"  # Using api subdomain
API_ENDPOINT = "/v1/watermark-remover"  # Common API pattern

def upload_video(video_file, api_key):
    """Upload video to the API with proper formatting"""
    try:
        # Read file content
        video_bytes = video_file.read()
        video_file.seek(0)  # Reset file pointer
        
        # Prepare multipart form data
        files = {
            'file': (video_file.name, video_bytes, 'video/mp4')
        }
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        }
        
        # Try the primary endpoint
        url = f"{API_BASE_URL}{API_ENDPOINT}"
        
        st.info(f"🔄 Attempting upload to: {url}")
        
        response = requests.post(
            url,
            files=files,
            headers=headers,
            timeout=60
        )
        
        st.info(f"📡 Response Status: {response.status_code}")
        
        # If primary fails, try alternative endpoints
        if response.status_code >= 400:
            alternative_urls = [
                "https://kie.ai/api/sora-2-watermark-remover",
                "https://api.kie.ai/sora-2-watermark-remover",
                "https://kie.ai/api/v1/watermark-remover"
            ]
            
            for alt_url in alternative_urls:
                st.info(f"🔄 Trying alternative: {alt_url}")
                try:
                    response = requests.post(
                        alt_url,
                        files=files,
                        headers=headers,
                        timeout=60
                    )
                    if response.status_code < 400:
                        break
                except:
                    continue
        
        if response.status_code == 200 or response.status_code == 201:
            try:
                return response.json()
            except:
                return {'task_id': 'manual_check', 'message': 'Upload successful'}
        else:
            error_detail = response.text[:500] if len(response.text) < 500 else response.text[:500] + "..."
            st.session_state.error_message = f"Status {response.status_code}: {error_detail}"
            return None
            
    except requests.exceptions.Timeout:
        st.session_state.error_message = "Request timeout. The server took too long to respond."
        return None
    except requests.exceptions.ConnectionError:
        st.session_state.error_message = "Connection error. Please check your internet connection."
        return None
    except Exception as e:
        st.session_state.error_message = f"Unexpected error: {str(e)}"
        return None

def check_task_status(task_id, api_key):
    """Check the status of the processing task"""
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        }
        
        # Try multiple endpoint patterns
        urls = [
            f"{API_BASE_URL}{API_ENDPOINT}/{task_id}",
            f"{API_BASE_URL}/v1/tasks/{task_id}",
            f"https://kie.ai/api/tasks/{task_id}"
        ]
        
        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    return response.json()
            except:
                continue
        
        return None
    except Exception as e:
        return None

def download_video(url):
    """Download the processed video"""
    try:
        response = requests.get(url, stream=True, timeout=120)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        return None

# Header
st.title("🎬 Sora Watermark Remover")
st.markdown("### Remove watermarks from your Sora-generated videos")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.markdown("**API Endpoint Options:**")
    endpoint_option = st.selectbox(
        "Select API endpoint",
        [
            "https://api.kie.ai/v1/watermark-remover",
            "https://kie.ai/api/sora-2-watermark-remover",
            "https://kie.ai/sora-2-watermark-remover",
            "Custom URL"
        ]
    )
    
    if endpoint_option == "Custom URL":
        custom_url = st.text_input("Enter custom API URL")
        if custom_url:
            API_BASE_URL = custom_url.rsplit('/', 1)[0]
            API_ENDPOINT = '/' + custom_url.rsplit('/', 1)[1]
    else:
        API_BASE_URL = endpoint_option.rsplit('/', 1)[0]
        API_ENDPOINT = '/' + endpoint_option.rsplit('/', 1)[1]
    
    api_key = st.text_input("API Key", type="password", help="Enter your KIE.AI API key")
    
    st.markdown("---")
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. Select the correct API endpoint
    2. Enter your API key
    3. Upload a Sora video
    4. Click 'Remove Watermark'
    5. Wait for processing
    6. Download result
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ Supported Formats")
    st.markdown("""
    - **Video:** MP4, MOV, AVI, WebM
    - **Max size:** 500MB
    - **Typical processing:** 2-5 minutes
    """)
    
    st.markdown("---")
    if st.button("🔄 Reset All"):
        st.session_state.processing = False
        st.session_state.result_url = None
        st.session_state.task_id = None
        st.session_state.error_message = None
        st.rerun()

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Video")
    
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=['mp4', 'mov', 'avi', 'webm'],
        help="Upload a Sora video with watermark"
    )
    
    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024*1024)
        st.success(f"✅ File: {uploaded_file.name}")
        st.info(f"📦 Size: {file_size_mb:.2f} MB")
        
        # Display video preview
        try:
            st.video(uploaded_file)
        except:
            st.warning("⚠️ Preview not available for this format")
        
        # Show current API endpoint
        st.info(f"🌐 Using endpoint: {API_BASE_URL}{API_ENDPOINT}")
        
        if st.button("🚀 Remove Watermark", disabled=not api_key or st.session_state.processing):
            if not api_key:
                st.error("⚠️ Please enter your API key")
            elif file_size_mb > 500:
                st.error("⚠️ File too large. Maximum size is 500MB")
            else:
                st.session_state.processing = True
                st.session_state.error_message = None
                
                with st.spinner("📤 Uploading video..."):
                    result = upload_video(uploaded_file, api_key)
                
                if result:
                    # Try to extract task ID from various response formats
                    task_id = result.get('task_id') or result.get('id') or result.get('job_id') or result.get('request_id')
                    
                    if task_id:
                        st.session_state.task_id = task_id
                        st.success(f"✅ Upload successful! Task ID: {task_id}")
                        
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        max_attempts = 120  # 10 minutes
                        attempt = 0
                        
                        while attempt < max_attempts:
                            status = check_task_status(task_id, api_key)
                            
                            if status:
                                state = status.get('status') or status.get('state') or status.get('progress')
                                
                                if state in ['completed', 'success', 'done']:
                                    progress_bar.progress(100)
                                    status_text.success("✅ Processing complete!")
                                    
                                    # Try to get result URL
                                    result_url = (status.get('output_url') or 
                                                status.get('result_url') or 
                                                status.get('download_url') or
                                                status.get('video_url'))
                                    
                                    if result_url:
                                        st.session_state.result_url = result_url
                                    
                                    st.session_state.processing = False
                                    st.rerun()
                                    break
                                    
                                elif state in ['failed', 'error']:
                                    error_msg = status.get('error') or status.get('message') or 'Unknown error'
                                    status_text.error(f"❌ Processing failed: {error_msg}")
                                    st.session_state.processing = False
                                    break
                                    
                                else:
                                    progress = min(int((attempt / max_attempts) * 95), 95)
                                    progress_bar.progress(progress)
                                    status_text.info(f"⏳ Status: {state}... (Attempt {attempt + 1}/{max_attempts})")
                            
                            time.sleep(5)
                            attempt += 1
                        
                        if attempt >= max_attempts:
                            status_text.warning("⏱️ Processing timeout. Check your task ID later.")
                            st.session_state.processing = False
                    else:
                        st.warning("⚠️ Upload accepted but no task ID returned. Check API documentation.")
                        st.json(result)
                        st.session_state.processing = False
                else:
                    if st.session_state.error_message:
                        st.error(f"❌ Upload failed: {st.session_state.error_message}")
                        
                        # Show troubleshooting tips
                        with st.expander("🔧 Troubleshooting Tips"):
                            st.markdown("""
                            **Common issues:**
                            1. **Invalid API Key**: Verify your API key at kie.ai
                            2. **Wrong Endpoint**: Try selecting a different endpoint option
                            3. **Server Error (520)**: The API server may be down, try again later
                            4. **File Format**: Ensure your video is in MP4, MOV, AVI, or WebM format
                            5. **File Size**: Keep files under 500MB
                            
                            **Next steps:**
                            - Check [KIE.AI documentation](https://kie.ai)
                            - Contact support if issue persists
                            - Try a different video file
                            """)
                    st.session_state.processing = False

with col2:
    st.subheader("📥 Download Result")
    
    if st.session_state.result_url:
        st.markdown("### ✨ Your video is ready!")
        
        video_data = download_video(st.session_state.result_url)
        
        if video_data:
            st.download_button(
                label="⬇️ Download Processed Video",
                data=video_data,
                file_name=f"watermark_removed_{int(time.time())}.mp4",
                mime="video/mp4"
            )
            
            # Try to display processed video
            try:
                st.video(st.session_state.result_url)
            except:
                st.info(f"🔗 [Direct Download Link]({st.session_state.result_url})")
        else:
            st.error("Failed to download. Use direct link:")
            st.markdown(f"🔗 [Download Here]({st.session_state.result_url})")
    else:
        st.info("👈 Upload a video to get started")
        
        st.markdown("### ✨ Features")
        st.markdown("""
        - 🚀 Fast processing (2-5 min)
        - 🎯 High quality output
        - 🔒 Secure processing
        - 📱 Multiple format support
        - 💾 Easy download
        """)
        
        if st.session_state.task_id and not st.session_state.result_url:
            st.warning(f"⏳ Task ID: {st.session_state.task_id} - Still processing...")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p><strong>Sora Watermark Remover</strong> | Powered by KIE.AI</p>
    <p>⚠️ Ensure you have rights to modify the videos you process</p>
    <p>📧 Issues? Check the API documentation or contact support</p>
</div>
""", unsafe_allow_html=True)
