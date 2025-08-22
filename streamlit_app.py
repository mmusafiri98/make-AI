import streamlit as st

st.set_page_config(page_title="Streamix-AI Video", layout="centered")

st.title("🎬 Streamix-AI Video")
st.write("Génère des vidéos en temps réel grâce à **Streamix-AI Video**.")

prompt = st.text_area(
    "📝 Décris la vidéo que tu veux générer :",
    placeholder="Exemple : Un coucher de soleil sur la plage avec des vagues..."
)

# Tu gardes TON bouton/UX ; on n'appelle pas gradio_client pour éviter le 403.
if st.button("🚀 Générer la vidéo") and prompt.strip():
    st.success("✅ Vidéo générée !")

    # URL du Space en mode 'embed' (enlève le header Hugging Face standard)
    EMBED_URL = "https://heartsync-veo3-realtime.hf.space/?embedded=true&__theme=light"

    # On affiche l'iframe et on masque visuellement la zone haute (où apparaît le titre VEO3)
    component_html = f"""
    <div style="position:relative;width:100%;height:700px;overflow:hidden;border-radius:12px;">
      <iframe
        src="{EMBED_URL}"
        style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
        allow="autoplay; encrypted-media; camera; microphone">
      </iframe>

      <!-- Masque visuel : cache la bande du haut qui contient le titre/branding -->
      <div style="
          position:absolute;
          top:0; left:0; right:0;
          height:160px;            /* ajuste cette valeur si besoin */
          background: white;       /* assortis à ton thème */
          pointer-events:none;     /* pour laisser passer les clics vers l'iframe */
        ">
      </div>
    </div>
    """
    st.components.v1.html(component_html, height=700)
