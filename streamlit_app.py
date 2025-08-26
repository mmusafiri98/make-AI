import streamlit as st
from gradio_client import Client
import tempfile
import base64
import os
import shutil

# Config layout
st.set_page_config(page_title="StreamVideo-AI", layout="wide")

# --- HEADER ---
st.markdown(
    """
    <style>
    .title-center {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle-center {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }
    .big-textbox textarea {
        min-height: 200px !important;
        font-size: 16px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #a855f7, #ec4899);
        color: white;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 12px;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #9333ea, #db2777);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title-center">🎬 StreamVideo-AI Generate video!</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-center">✨ Add your topic and detailed instructions to get started.</div>', unsafe_allow_html=True)

# --- MAIN INPUT ---
prompt = st.text_area(" ", placeholder="Write your video idea here...", key="main_prompt", label_visibility="collapsed", help="Describe your video prompt", height=200)

# Advanced options in sidebar
st.sidebar.header("⚙️ Advanced Settings")
negative_prompt = st.sidebar.text_area("Negative Prompt", "low quality, blurry")
width = st.sidebar.number_input("Width", min_value=64, max_value=1280, value=640, step=64)
height = st.sidebar.number_input("Height", min_value=64, max_value=1280, value=384, step=64)
duration_seconds = st.sidebar.slider("Duration (seconds)", min_value=1, max_value=10, value=2)
steps = st.sidebar.slider("Steps", min_value=1, max_value=50, value=4)
guidance_scale = st.sidebar.slider("Guidance Scale", min_value=0.0, max_value=20.0, value=1.0)
seed = st.sidebar.number_input("Seed", min_value=0, max_value=999999, value=42)
randomize_seed = st.sidebar.checkbox("Randomize Seed", value=True)

client = Client("jbilcke-hf/InstaVideo")

# --- GENERATE BUTTON ---
if st.button("✨ Generate"):
    if not prompt.strip():
        st.warning("Please enter a prompt to generate the video.")
    else:
        with st.spinner("🎥 Generating your video..."):
            try:
                result = client.predict(
                    prompt=prompt,
                    height=height,
                    width=width,
                    negative_prompt=negative_prompt,
                    duration_seconds=duration_seconds,
                    guidance_scale=guidance_scale,
                    steps=steps,
                    seed=seed,
                    randomize_seed=randomize_seed,
                    api_name="/generate_video"
                )

                if isinstance(result, tuple) and "video" in result[0]:
                    video_path = result[0]["video"]

                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                    shutil.copy(video_path, tmp_file.name)
                    tmp_file.close()

                    st.video(tmp_file.name)

                    with open(tmp_file.name, "rb") as f:
                        video_data = f.read()
                        b64 = base64.b64encode(video_data).decode()
                        st.markdown(f"[⬇️ Download Video](data:video/mp4;base64,{b64})", unsafe_allow_html=True)

                    os.unlink(tmp_file.name)
                else:
                    st.error("Error: No video found in the result.")

            except Exception as e:
                st.error(f"Error while generating video: {e}")

