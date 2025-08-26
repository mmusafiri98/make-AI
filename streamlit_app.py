import streamlit as st
from gradio_client import Client
import tempfile
import base64
import os

st.set_page_config(layout="wide")
st.title("Generatore di Video AI - InstaVideo")

# Inizializza il client
client = Client("jbilcke-hf/InstaVideo")

# Sidebar per il prompt e le impostazioni
st.sidebar.header("Impostazioni Video")
prompt = st.sidebar.text_area("Prompt", "cinematic footage, dancing in the streets")
negative_prompt = st.sidebar.text_area("Negative Prompt", "low quality, blurry")
width = st.sidebar.number_input("Width", min_value=64, max_value=1280, value=640, step=64)
height = st.sidebar.number_input("Height", min_value=64, max_value=1280, value=384, step=64)
duration_seconds = st.sidebar.slider("Durata (secondi)", min_value=1, max_value=10, value=2)
steps = st.sidebar.slider("Steps", min_value=1, max_value=50, value=4)
guidance_scale = st.sidebar.slider("Guidance Scale", min_value=0.0, max_value=20.0, value=1.0)
seed = st.sidebar.number_input("Seed", min_value=0, max_value=999999, value=42)
randomize_seed = st.sidebar.checkbox("Randomize Seed", value=True)

if st.button("Genera Video"):
    if not prompt.strip():
        st.warning("Inserisci un prompt per generare il video.")
    else:
        with st.spinner("Generazione del video in corso..."):
            try:
                # Chiamata al modello
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

                # Stampa il risultato per capire la struttura (solo la prima volta)
                st.write("Struttura del risultato restituito dal modello:")
                st.write(result)

                # Prova a estrarre i bytes del video
                video_bytes = None
                if isinstance(result, dict):
                    # Controlla chiavi comuni
                    for key in ["video", "data", "output"]:
                        if key in result:
                            video_bytes = result[key]
                            break
                elif isinstance(result, (bytes, bytearray)):
                    video_bytes = result

                if not video_bytes:
                    st.error("Errore: non è stato possibile trovare i dati video nel risultato.")
                else:
                    # Salva temporaneamente il video
                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                    tmp_file.write(video_bytes)
                    tmp_file.close()

                    # Mostra il video
                    st.video(tmp_file.name)
                    
                    # Pulsante per scaricare
                    with open(tmp_file.name, "rb") as f:
                        video_data = f.read()
                        b64 = base64.b64encode(video_data).decode()
                        st.markdown(f"[Scarica Video](data:video/mp4;base64,{b64})", unsafe_allow_html=True)

                    # Rimuovi il file temporaneo
                    os.unlink(tmp_file.name)

            except Exception as e:
                st.error(f"Errore durante la generazione del video: {e}")
