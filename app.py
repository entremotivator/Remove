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
    * { font-family: 'Inter', sans-serif; }
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 0; }
    .block-container { padding: 3rem 2rem; max-width: 1400px; }
    .hero-section { background: white; border-radius: 20px; padding: 3rem; margin-bottom: 2rem; box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center; }
    .hero-title { font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; }
    .hero-subtitle { font-size: 1.2rem; color: #666; margin-bottom: 2rem; }
    .feature-card { background: white; border-radius: 15px; padding: 2rem; margin: 1rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2); transition: transform 0.3s ease; }
    .feature-card:hover { transform: translateY(-5px); }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: 600; padding: 1rem 2rem; border-radius: 50px; border: none; font-size: 1.1rem; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6); }
    .stButton>button:disabled { background: #ccc; cursor: not-allowed; }
    .success-banner { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0; text-align: center; box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3); }
    .info-badge { display: inline-block; background: #e3f2fd; color: #1976d2; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; margin: 0.5rem; }
    .stat-box { background: white; border-radius: 10px; padding: 1.5rem; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .stat-number { font-size: 2rem; font-weight: 700; color: #667eea; }
    .stat-label { color: #666; font-size: 0.9rem; margin-top: 0.5rem; }
    .progress-container { background: white; border-radius: 10px; padding: 2rem; margin: 2rem 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .faq-item { background: white; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .faq-question { font-weight: 600; color: #333; font-size: 1.1rem; margin-bottom: 0.5rem; }
    .faq-answer { color: #666; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
for key, default in {
    "processing": False,
    "result_url": None,
    "credits_used": 0,
    "videos_processed": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# API Configuration
API_ENDPOINT = "https://kie.ai/api/v1/sora-watermark-remover"
API_DOCS_URL = "https://kie.ai/sora-2-watermark-remover"

def check_sora_url(url: str) -> bool:
    return "sora.chatgpt.com" in url or "cdn.openai.com" in url

def remove_watermark(video_url: str, api_key: str):
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"videoUrl": video_url, "removeWatermark": True}
        response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=120)
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def upload_to_host(video_file):
    try:
        files = {'file': (video_file.name, video_file.getvalue(), 'video/mp4')}
        response = requests.post('https://tmpfiles.org/api/v1/upload', files=files, timeout=120)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return data['data']['url'].replace('tmpfiles.org/', 'tmpfiles.org/dl/')
        return None
    except Exception:
        return None

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🎬 Sora 2 Watermark Remover</div>
    <div class="hero-subtitle">Remove watermarks from Sora-generated videos in 1–3 seconds using AI</div>
    <div>
        <span class="info-badge">⚡ 1–3 Second Processing</span>
        <span class="info-badge">🎯 AI Motion Tracking</span>
        <span class="info-badge">🔒 Secure & Private</span>
        <span class="info-badge">💰 $0.05 per video</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_key = st.text_input("KIE.AI API Key", type="password", help="Get your API key from kie.ai", placeholder="sk-kie-...")
    if not api_key:
        st.warning("⚠️ Enter API key to continue")
        st.markdown(f"[Get API Key →]({API_DOCS_URL})")
    st.markdown("---")

    st.markdown("### 📊 Your Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{st.session_state.videos_processed}</div><div class="stat-label">Videos Processed</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{st.session_state.credits_used}</div><div class="stat-label">Credits Used</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✅ Requirements")
    st.markdown("""
    - Video URL from `sora.chatgpt.com`
    - Must be public
    - Max 15 seconds
    - MP4, MOV, or WebM
    """)
    st.markdown("---")
    st.markdown("### 💰 Pricing")
    st.markdown("""
    - 10 credits = $0.50  
    - 1 video = 10 credits ($0.05)  
    - Free 10 credits for new users
    """)
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown(f"- [API Docs]({API_DOCS_URL})\n- [Get API Key](https://kie.ai)\n- [Pricing](https://kie.ai/pricing)")
    st.markdown("---")

    if st.button("🔄 Reset Session", use_container_width=True):
        for k in ["processing", "result_url"]:
            st.session_state[k] = None
        st.session_state.videos_processed = 0
        st.session_state.credits_used = 0
        st.rerun()

# Tabs
tab1, tab2, tab3 = st.tabs(["🎯 Remove Watermark", "📚 How It Works", "❓ FAQ"])

# --- Tab 1: Main Watermark Removal ---
with tab1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 📝 Enter Sora Video URL")
    video_url = st.text_input("Sora Video URL", placeholder="https://sora.chatgpt.com/share/...", label_visibility="collapsed")

    if video_url:
        if check_sora_url(video_url):
            st.success("✅ Valid Sora URL detected")
            st.video(video_url)
        else:
            st.error("❌ Invalid URL. Must be from sora.chatgpt.com")

    if st.button("🚀 Remove Watermark", use_container_width=True):
        if not api_key:
            st.error("❌ Enter your API key first.")
        elif not video_url:
            st.error("❌ Please enter a Sora video URL.")
        elif not check_sora_url(video_url):
            st.error("❌ Invalid URL. Must be a valid Sora URL.")
        else:
            st.session_state.processing = True
            with st.spinner("Processing your video..."):
                progress = st.progress(0)
                progress.progress(25)
                result = remove_watermark(video_url, api_key)
                progress.progress(70)
                if result:
                    output_url = result.get('outputUrl') or result.get('resultUrl') or result.get('videoUrl')
                    if output_url:
                        progress.progress(100)
                        st.success("✅ Watermark removed successfully!")
                        st.session_state.result_url = output_url
                        st.session_state.videos_processed += 1
                        st.session_state.credits_used += 10
                        st.session_state.processing = False
                        st.rerun()
                    else:
                        st.warning("⚠️ No result URL returned.")
                else:
                    st.error("❌ Failed to process video.")
                    st.session_state.processing = False

    st.markdown('</div>', unsafe_allow_html=True)

    # Result Display
    if st.session_state.result_url:
        st.markdown("""
        <div class="success-banner">
            <h2>✨ Your Video is Ready!</h2>
            <p>Watermark removed successfully.</p>
        </div>
        """, unsafe_allow_html=True)
        st.video(st.session_state.result_url)
        st.markdown(f"[⬇️ Download Video]({st.session_state.result_url})", unsafe_allow_html=True)

# --- Tab 2: How It Works ---
with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("""
    ## 🔬 How It Works
    1️⃣ **Detection:** AI identifies watermark areas  
    2️⃣ **Tracking:** Frame-by-frame motion detection  
    3️⃣ **Inpainting:** AI fills pixels naturally  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 3: FAQ ---
with tab3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    faqs = {
        "What is Sora 2 Watermark Remover?": "An AI-powered tool that removes 'Made with Sora' watermarks using deep learning.",
        "How much does it cost?": "$0.05 per video, with 10 free credits on signup.",
        "Is my video data secure?": "Yes, processed securely and deleted after 24 hours."
    }
    for q, a in faqs.items():
        st.markdown(f"<div class='faq-item'><div class='faq-question'>{q}</div><div class='faq-answer'>{a}</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style='text-align:center;color:white;padding:2rem;'>
    <h3>🎬 Sora 2 Watermark Remover</h3>
    <p>Powered by <a href='https://kie.ai' style='color:white;'>KIE.AI</a></p>
    <p style='font-size:0.9em;'>⚠️ Only remove watermarks from videos you own | Deleted after 24h</p>
</div>
""", unsafe_allow_html=True)
