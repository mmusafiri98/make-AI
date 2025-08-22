import streamlit as st
from gradio_client import Client

# Connexion au Space Hugging Face
client = Client("Heartsync/VEO3-RealTime")

st.set_page_config(page_title="Streamix-AI Video", layout="centered")

st.title("🎬 Streamix-AI Video")
st.write("Génère des vidéos à partir d'un prompt texte grâce au modèle **VEO3 RealTime** hébergé sur Hugging Face.")

# Prompt utilisateur
prompt = st.text_area("📝 Décris la vidéo que tu veux générer :", 
                      placeholder="Exemple : Un coucher de soleil sur la plage avec des vagues...")

# Paramètres
col1, col2 = st.columns(2)
with col1:
    fps = st.slider("🎥 FPS (images/seconde)", 5, 30, 20)
with col2:
    random_seed = st.checkbox("🎲 Random Seed", value=True)

seed = -1 if random_seed else st.number_input("Seed fixe :", value=42, step=1)

# Bouton pour générer la vidéo
if st.button("🚀 Générer la vidéo") and prompt.strip():
    with st.spinner("⏳ Génération de la vidéo en cours..."):
        try:
            result = client.predict(
                prompt=prompt,
                seed=seed,
                fps=fps,
                api_name="/video_generation_handler_streaming"
            )

            # Résultat : tuple ou chemin de fichier
            if isinstance(result, tuple) and len(result) > 0:
                video_path = result[0]
            elif isinstance(result, str):
                video_path = result
            else:
                video_path = None

            if video_path:
                st.video(video_path)

                # Bouton de téléchargement
                with open(video_path, "rb") as f:
                    st.download_button(
                        label="📥 Télécharger la vidéo",
                        data=f,
                        file_name="streamix_ai_video.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error("❌ Impossible de récupérer la vidéo générée.")
                st.write(result)

        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")
