import streamlit as st

st.set_page_config(page_title="Streamix-AI Video", layout="centered")

st.title("🎬 Streamix-AI Video")
st.write("Génère des vidéos en temps réel avec **VEO3 RealTime** (Hugging Face).")

prompt = st.text_area("📝 Décris la vidéo que tu veux générer :",
                      placeholder="Exemple : Un coucher de soleil sur la plage avec des vagues...")

if st.button("🚀 Générer la vidéo") and prompt.strip():
    st.success("✅ Vidéo générée !")

    # On affiche directement l'iframe du Space Hugging Face
    iframe = """
    <iframe src="https://heartsync-veo3-realtime.hf.space" 
            style="width:100%;height:600px;border:none;border-radius:12px;"
            allow="camera; microphone; autoplay; encrypted-media;">
    </iframe>
    """
    st.components.v1.html(iframe, height=600)


