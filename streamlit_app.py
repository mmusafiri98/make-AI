import streamlit as st
from gradio_client import Client
import tempfile
import base64
import os
import shutil
import uuid
import json

# Config layout
st.set_page_config(page_title="StreamVideo-AI", layout="wide")

# --- PATH POUR VIDEOS ---
VIDEO_DIR = "generated_videos"
os.makedirs(VIDEO_DIR, exist_ok=True)
GALLERY_FILE = os.path.join(VIDEO_DIR, "gallery.json")

# --- INIT SESSION ---
if "gallery" not in st.session_state:
    # Charger la galerie depuis disque
    if os.path.exists(GALLERY_FILE):
        with open(GALLERY_FILE, "r", encoding="utf-8") as f:
            st.session_state["gallery"] = json.load(f)
    else:
        st.session_state["gallery"] = []

# --- HEADER ---
st.markdown("""
<style>
.title-center { text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 10px; }
.subtitle-center { text-align: center; font-size: 18px; color: #666; margin-bottom: 30px; }
.big-textbox textarea { min-height: 200px !important; font-size: 16px; }
.stButton>button { background: linear-gradient(90deg, #a855f7, #ec4899); color: white; font-weight: bold; padding: 12px 24px; border-radius: 12px; border: none; }
.stButton>button:hover { background: linear-gradient(90deg, #9333ea, #db2777); }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-center">🎬 StreamVideo-AI Generate video!</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-center">✨ Add your topic and detailed instructions to get started.</div>', unsafe_allow_html=True)

# --- MAIN INPUT ---
prompt = st.text_area(" ", placeholder="Write your video idea here...", key="main_prompt", label_visibility="collapsed", help="Describe your video prompt", height=200)

# --- ADVANCED OPTIONS ---
st.sidebar.header("⚙️ Advanced Settings")
negative_prompt = st.sidebar.text_area("Negative Prompt", "low quality, blurry")
width = st.sidebar.number_input("Width", min_value=64, max_value=1280, value=640, step=64)
height = st.sidebar.number_input("Height", min_value=64, max_value=1280, value=384, step=64)
duration_seconds = st.sidebar.slider("Duration (seconds)", min_value=1, max_value=10, value=2)
steps = st.sidebar.slider("Steps", min_value=1, max_value=50, value=4)
guidance_scale = st.sidebar.slider("Guidance Scale", min_value=0.0, max_value=20.0, value=1.0)
seed = st.sidebar.number_input("Seed", min_value=0, max_value=999999, value=42)
randomize_seed = st.sidebar.checkbox("Randomize Seed", value=True)

# --- CLIENT ---
client = Client("jbilcke-hf/InstaVideo")

# --- GALLERY SIDEBAR ---
st.sidebar.header("📂 Gallery")
if st.session_state["gallery"]:
    for idx, item in enumerate(st.session_state["gallery"]):
        with st.sidebar.expander(f"Video {idx+1}"):
            if os.path.exists(item["path"]):
                st.video(item["path"])
                st.markdown(f"[⬇️ Download Video {idx+1}]({item['download_link']})", unsafe_allow_html=True)
            else:
                st.warning("Video file missing.")
else:
    st.sidebar.info("No videos generated yet.")

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

                # Vérifier que la vidéo est dans le résultat
                if isinstance(result, tuple) and "video" in result[0]:
                    video_path = result[0]["video"]

                    # Sauvegarder la vidéo de façon unique
                    unique_name = f"video_{uuid.uuid4().hex}.mp4"
                    save_path = os.path.join(VIDEO_DIR, unique_name)
                    shutil.copy(video_path, save_path)

                    # Générer un lien de téléchargement base64
                    with open(save_path, "rb") as f:
                        video_data = f.read()
                        b64 = base64.b64encode(video_data).decode()
                        download_link = f"data:video/mp4;base64,{b64}"

                    # Afficher la vidéo dans le main
                    st.video(save_path)
                    st.markdown(f"[⬇️ Download Video]({download_link})", unsafe_allow_html=True)

                    # Ajouter à la galerie et sauvegarder
                    st.session_state["gallery"].append({
                        "path": save_path,
                        "download_link": download_link
                    })
                    with open(GALLERY_FILE, "w", encoding="utf-8") as f:
                        json.dump(st.session_state["gallery"], f, ensure_ascii=False, indent=2)

                else:
                    st.error("Error: No video found in the result.")

            except Exception as e:
                st.error(f"Error while generating video: {e}")

