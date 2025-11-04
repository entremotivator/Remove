import streamlit as st
import requests
import time
import json
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Sora 2 Watermark Remover - KIE.AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 3rem 2rem;
        max-width: 1400px;
    }
    
    .hero-section {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 1rem 2rem;
        border-radius: 50px;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:disabled {
        background: #ccc;
        cursor: not-allowed;
    }
    
    .success-banner {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
    }
    
    .info-badge {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem;
    }
    
    .stat-box {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .progress-container {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .url-input {
        font-size: 1rem;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        width: 100%;
    }
    
    .sidebar-section {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .faq-item {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .faq-question {
        font-weight: 600;
        color: #333;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .faq-answer {
        color: #666;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'result_url' not in st.session_state:
    st.session_state.result_url = None
if 'credits_used' not in st.session_state:
    st.session_state.credits_used = 0
if 'videos_processed' not in st.session_state:
    st.session_state.videos_processed = 0

# API Configuration
API_ENDPOINT = "https://kie.ai/api/v1/sora-watermark-remover"
API_DOCS_URL = "https://kie.ai/sora-2-watermark-remover"

def check_sora_url(url):
    """Validate if URL is from Sora"""
    return 'sora.chatgpt.com' in url or 'cdn.openai.com' in url

def remove_watermark(video_url, api_key):
    """Remove watermark from Sora video URL"""
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'videoUrl': video_url,
            'removeWatermark': True
        }
        
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=120
        )
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def upload_to_host(video_file):
    """Upload video to temporary hosting"""
    try:
        files = {'file': (video_file.name, video_file.getvalue(), 'video/mp4')}
        
        # Try tmpfiles.org
        response = requests.post(
            'https://tmpfiles.org/api/v1/upload',
            files=files,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                url = data['data']['url']
                return url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
        
        return None
        
    except Exception as e:
        return None

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🎬 Sora 2 Watermark Remover</div>
    <div class="hero-subtitle">
        Remove watermarks from Sora-generated videos in 1-3 seconds using AI
    </div>
    <div>
        <span class="info-badge">⚡ 1-3 Second Processing</span>
        <span class="info-badge">🎯 AI Motion Tracking</span>
        <span class="info-badge">🔒 Secure & Private</span>
        <span class="info-badge">💰 $0.05 per video</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    api_key = st.text_input(
        "KIE.AI API Key",
        type="password",
        help="Get your API key from kie.ai",
        placeholder="sk-kie-..."
    )
    
    if not api_key:
        st.warning("⚠️ Enter API key to continue")
        st.markdown(f"[Get API Key →]({API_DOCS_URL})")
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Your Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{st.session_state.videos_processed}</div>
            <div class="stat-label">Videos Processed</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{st.session_state.credits_used}</div>
            <div class="stat-label">Credits Used</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Requirements
    st.markdown("### ✅ Requirements")
    st.markdown("""
    - Video URL from `sora.chatgpt.com`
    - URL must be publicly accessible
    - Max duration: 15 seconds
    - Supported: MP4, MOV, WebM
    """)
    
    st.markdown("---")
    
    # Pricing
    st.markdown("### 💰 Pricing")
    st.markdown("""
    **Pay-as-you-go:**
    - 10 credits = $0.50
    - 1 video = 10 credits ($0.05)
    - No subscription needed
    
    **Free trial:** 10 credits on signup
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔗 Links")
    st.markdown(f"""
    - [API Documentation]({API_DOCS_URL})
    - [Get API Key](https://kie.ai)
    - [Pricing Details](https://kie.ai/pricing)
    """)
    
    st.markdown("---")
    
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.processing = False
        st.session_state.result_url = None
        st.rerun()

# Main Content
tab1, tab2, tab3 = st.tabs(["🎯 Remove Watermark", "📚 How It Works", "❓ FAQ"])

with tab1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    st.markdown("## 📝 Enter Sora Video URL")
    st.markdown("Paste your Sora video URL below. It must start with `sora.chatgpt.com`")
    
    video_url = st.text_input(
        "Sora Video URL",
        placeholder="https://sora.chatgpt.com/share/...",
        help="Must be a publicly accessible Sora video URL",
        label_visibility="collapsed"
    )
    
    if video_url:
        if check_sora_url(video_url):
            st.success("✅ Valid Sora URL detected")
            try:
                st.video(video_url)
            except:
                st.info("🔗 URL accepted (preview may not be available)")
        else:
            st.error("❌ Invalid URL. Must be from sora.chatgpt.com")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        process_button = st.button(
            "🚀 Remove Watermark",
            disabled=not api_key or not video_url or st.session_state.processing,
            use_container_width=True,
            type="primary"
        )
    
    if process_button:
        if not check_sora_url(video_url):
            st.error("⚠️ Please enter a valid Sora URL")
        else:
            st.session_state.processing = True
            
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            
            with st.spinner("🔄 Processing your video..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.info("📤 Sending request to KIE.AI...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                result = remove_watermark(video_url, api_key)
                
                if result:
                    status_text.info("🤖 AI analyzing video...")
                    progress_bar.progress(50)
                    time.sleep(1)
                    
                    status_text.info("✨ Removing watermark...")
                    progress_bar.progress(80)
                    time.sleep(1)
                    
                    output_url = (result.get('outputUrl') or 
                                result.get('videoUrl') or 
                                result.get('resultUrl') or
                                result.get('downloadUrl'))
                    
                    if output_url:
                        progress_bar.progress(100)
                        status_text.success("✅ Processing complete!")
                        
                        st.session_state.result_url = output_url
                        st.session_state.videos_processed += 1
                        st.session_state.credits_used += 10
                        st.session_state.processing = False
                        
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("⚠️ Processing initiated. Response:")
                        st.json(result)
                        st.session_state.processing = False
                else:
                    st.error("❌ Processing failed. Please check:")
                    st.markdown("""
                    - Valid API key
                    - Publicly accessible URL
                    - URL from sora.chatgpt.com
                    - Sufficient credits
                    """)
                    st.session_state.processing = False
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Alternative: Upload file
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    st.markdown("## 📤 Alternative: Upload Video File")
    st.markdown("Don't have a Sora URL? Upload your video file and we'll process it")
    
    uploaded_file = st.file_uploader(
        "Upload Sora Video",
        type=['mp4', 'mov', 'webm'],
        help="Upload a Sora-generated video file"
    )
    
    if uploaded_file:
        file_size = uploaded_file.size / (1024 * 1024)
        st.info(f"📦 File: {uploaded_file.name} ({file_size:.2f} MB)")
        
        try:
            st.video(uploaded_file)
        except:
            pass
        
        if st.button("📤 Upload & Process", use_container_width=True):
            if file_size > 500:
                st.error("❌ File too large. Maximum 500MB")
            else:
                with st.spinner("📤 Uploading to temporary host..."):
                    hosted_url = upload_to_host(uploaded_file)
                
                if hosted_url:
                    st.success(f"✅ Uploaded: {hosted_url}")
                    
                    with st.spinner("🔄 Removing watermark..."):
                        result = remove_watermark(hosted_url, api_key)
                    
                    if result:
                        output_url = (result.get('outputUrl') or 
                                    result.get('videoUrl') or 
                                    result.get('resultUrl'))
                        
                        if output_url:
                            st.session_state.result_url = output_url
                            st.session_state.videos_processed += 1
                            st.session_state.credits_used += 10
                            st.rerun()
                else:
                    st.error("❌ Upload failed. Try using a Sora URL instead.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results
    if st.session_state.result_url:
        st.markdown("""
        <div class="success-banner">
            <h2>✨ Your Video is Ready!</h2>
            <p>Watermark removed successfully. Download your clean video below.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("### 🎬 Processed Video")
            try:
                st.video(st.session_state.result_url)
            except:
                st.markdown(f"[🔗 View Video]({st.session_state.result_url})")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("### 📥 Download")
            
            try:
                video_data = requests.get(st.session_state.result_url, timeout=60).content
                st.download_button(
                    "⬇️ Download Video",
                    data=video_data,
                    file_name=f"sora_no_watermark_{int(time.time())}.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
            except:
                st.markdown(f"[⬇️ Direct Link]({st.session_state.result_url})")
            
            st.markdown("---")
            
            st.markdown("**Video Info:**")
            st.markdown("- ✅ Watermark removed")
            st.markdown("- 🎨 Original quality")
            st.markdown("- ⚡ 1-3 sec processing")
            st.markdown("- 💰 10 credits used")
            
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    st.markdown("## 🔬 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ AI Detection
        Advanced computer vision detects the Sora watermark position and motion path
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ Motion Tracking
        AI tracks watermark movement frame-by-frame with sub-pixel accuracy
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ Inpainting
        Deep learning reconstructs occluded pixels naturally using surrounding context
        """)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Key Features")
    
    features = [
        ("⚡", "Lightning Fast", "1-3 second processing time"),
        ("🎨", "Quality Preservation", "Maintains original video quality"),
        ("🤖", "AI-Powered", "Advanced deep learning models"),
        ("🔒", "Secure", "Your videos are processed securely"),
        ("💰", "Affordable", "$0.05 per video removal"),
        ("📱", "API Access", "Integrate into your workflows")
    ]
    
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            **{icon} {title}**  
            {desc}
            """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    st.markdown("## 📋 Step-by-Step Guide")
    
    st.markdown("""
    ### Method 1: Using Sora URL
    
    1. **Get your video URL**
       - Go to sora.chatgpt.com
       - Generate or find your video
       - Copy the share URL
    
    2. **Enter API Key**
       - Sign up at kie.ai
       - Get your API key
       - Paste it in the sidebar
    
    3. **Process video**
       - Paste Sora URL
       - Click "Remove Watermark"
       - Wait 1-3 seconds
    
    4. **Download result**
       - Preview cleaned video
       - Download MP4 file
       - Use in your projects
    
    ### Method 2: Upload File
    
    1. Upload your Sora video file
    2. We host it temporarily
    3. Process automatically
    4. Download clean version
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    st.markdown("## ❓ Frequently Asked Questions")
    
    faqs = [
        ("What is Sora 2 Watermark Remover?", 
         "An AI-powered tool that removes the 'Made with Sora' watermark from Sora-generated videos in 1-3 seconds using advanced motion tracking and inpainting."),
        
        ("How much does it cost?", 
         "10 credits ($0.50) per video. New users get 10 free credits on signup. No subscription required."),
        
        ("What video formats are supported?", 
         "MP4, MOV, and WebM formats up to 15 seconds duration and 500MB file size."),
        
        ("Is it legal to remove Sora watermarks?", 
         "You should only remove watermarks from videos you own or have permission to edit. Check OpenAI's terms of service."),
        
        ("How fast is the processing?", 
         "Typically 1-3 seconds per video, depending on length and complexity."),
        
        ("Do I need a Sora URL?", 
         "Preferred, but you can also upload video files. URLs must be publicly accessible from sora.chatgpt.com."),
        
        ("Is my video data secure?", 
         "Yes. Videos are processed securely and deleted after 24 hours. We don't store your content."),
        
        ("Can I use the API in my app?", 
         "Yes! Check the API documentation for integration details."),
        
        ("What if processing fails?", 
         "Check: valid API key, public URL, sufficient credits, and correct format. Contact support if issues persist."),
        
        ("Do you offer refunds?", 
         "Credits are refunded automatically if processing fails. Contact support for other issues.")
    ]
    
    for question, answer in faqs:
        st.markdown(f"""
        <div class="faq-item">
            <div class="faq-question">{question}</div>
            <div class="faq-answer">{answer}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; padding: 2rem;'>
    <h3>🎬 Sora 2 Watermark Remover</h3>
    <p>Powered by <a href="https://kie.ai" style="color: white; text-decoration: underline;">KIE.AI</a> | 
    <a href="https://kie.ai/sora-2-watermark-remover" style="color: white;">API Docs</a> | 
    <a href="https://kie.ai/pricing" style="color: white;">Pricing</a></p>
    <p style="font-size: 0.9em; margin-top: 1rem;">
        ⚠️ Only remove watermarks from videos you own or have permission to edit<br>
        🔒 Your videos are processed securely and deleted after 24 hours<br>
        💡 Processing time: 1-3 seconds | Cost: $0.05 per video (10 credits)
    </p>
</div>
""", unsafe_allow_html=True)
