import streamlit as st
from groq import Groq
import fitz

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEME = """Tu es Brahim IA, un assistant étudiant intelligent et motivant.
Tu parles toujours dans la langue de l'utilisateur.
Tu expliques les concepts de façon simple avec des exemples concrets.
Tu utilises des emojis pour rendre les réponses agréables."""

st.set_page_config(page_title="Brahim IA", page_icon="🎓", layout="centered")
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
h1 { text-align: center; color: #a78bfa !important; font-size: 3em !important; }
.stCaption { text-align: center; color: #c4b5fd !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Brahim IA")
st.caption("✨ Ton assistant étudiant intelligent • PDF • Multilingue")

# Initialiser
if "messages" not in st.session_state:
    st.session_state.messages = []
if "contenu_pdf" not in st.session_state:
    st.session_state.contenu_pdf = ""
if "nom_pdf" not in st.session_state:
    st.session_state.nom_
