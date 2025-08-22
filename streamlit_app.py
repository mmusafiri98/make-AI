import streamlit as st
from gradio_client import Client

# Connexion au Space Hugging Face
client = Client("Heartsync/VEO3-RealTime")

st.set_page_config(page_title="Streamix-AI Video", layout="centered")

st.title("🎬 Streamix-AI Video")
st.write("Génère et lit des vidéos en temps réel depuis le modèle **VEO3 RealTime**.")

# Prompt utilisateur
prompt = st.text_area("📝 Décris la vidéo que tu veux générer :", 
                      placeholder="Exemple : Un coucher de soleil sur la plage avec des vagues...")

# Paramètres
fps = st.slider("🎥 FPS (images/seconde)", 5, 30, 20)
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

            # Récupération du chemin ou URL
            if isinstance(result, tuple):
                video_url = result[0]
            elif isinstance(result, str):
                video_url = result
            else:
                video_url = None

            if video_url and video_url.endswith(".m3u8"):
                st.success("✅ Vidéo générée, lecture en cours...")

                # Utilisation de hls.js pour lire le flux
                hls_player = f"""
                <video id="video" controls autoplay style="width:100%;border-radius:12px;">
                    <source src="{video_url}" type="application/x-mpegURL">
                </video>
                <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
                <script>
                if(Hls.isSupported()) {{
                    var video = document.getElementById('video');
                    var hls = new Hls();
                    hls.loadSource("{video_url}");
                    hls.attachMedia(video);
                }}
                </script>
                """
                st.components.v1.html(hls_player, height=480)

            else:
                st.error("❌ Impossible de lire la vidéo générée.")
                st.write(result)

        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")

