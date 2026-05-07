import streamlit as st
from groq import Groq
import fitz

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEME = """Tu es Brahim IA, un assistant étudiant intelligent et motivant.
Tu parles toujours dans la langue de l'utilisateur.
Tu expliques les concepts de façon simple avec des exemples concrets.
Tu encourages toujours l'étudiant et tu es positif.
Tu utilises des emojis pour rendre les réponses agréables.
Tu es spécialisé en informatique, mathématiques et intelligence artificielle.
Si un document PDF est fourni, tu réponds en te basant sur son contenu."""

st.set_page_config(page_title="Brahim IA", page_icon="🎓", layout="centered")
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
h1 { text-align: center; color: #a78bfa !important; font-size: 3em !important; }
.stCaption { text-align: center; color: #c4b5fd !important; font-size: 1.1em !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Brahim IA")
st.caption("✨ Ton assistant étudiant intelligent • PDF • Multilingue")

with st.sidebar:
    st.markdown("## ⚙️ Paramètres")
    prenom = st.text_input("👤 Ton prénom", placeholder="Entre ton prénom...")
    st.markdown("---")
    st.markdown("## 📄 Uploader un PDF")
    pdf_file = st.file_uploader("Choisis un fichier PDF", type="pdf")
    contenu_pdf = ""
    if pdf_file:
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        nb_pages = doc.page_count
        for page in doc:
            contenu_pdf += page.get_text()
        doc.close()
        st.success(f"✅ PDF chargé ! ({nb_pages} pages)")
    st.markdown("---")
    mode = st.selectbox("🛠️ Fonctionnalité", [
        "💬 Conversation libre",
        "📝 Résumer le PDF",
        "🌍 Traduire un texte",
        "💻 Générer du code Python",
        "📚 Expliquer un concept",
        "❓ Quiz sur le PDF"
    ])
    st.markdown("---")
    if st.button("🗑️ Nouvelle conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    nom = f" {prenom}" if prenom else ""
    with st.chat_message("assistant"):
        if pdf_file:
            st.markdown(f"👋 Salut{nom} ! J'ai bien lu ton PDF **{pdf_file.name}** ! Pose-moi des questions dessus 📄🚀")
        else:
            st.markdown(f"👋 Salut{nom} ! Je suis **Brahim IA** ! Upload un PDF ou pose-moi n'importe quelle question ! 🚀")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def preparer_prompt(question, mode, contenu_pdf):
    if contenu_pdf:
        if "Résumer" in mode:
            return f"Voici le contenu complet d'un document PDF. Résume-le de façon claire et structurée :\n\n{contenu_pdf[:4000]}"
        elif "Quiz" in mode:
            return f"Voici le contenu d'un document PDF. Crée un quiz de 5 questions dessus :\n\n{contenu_pdf[:4000]}"
        else:
            return f"Voici le contenu d'un document PDF :\n\n{contenu_pdf[:4000]}\n\nQuestion de l'étudiant : {question}"
    elif "Traduire" in mode:
        return f"Traduis ce texte en français et en anglais : {question}"
    elif "code Python" in mode:
        return f"Génère du code Python propre et commenté pour : {question}"
    elif "Expliquer" in mode:
        return f"Explique ce concept simplement avec des exemples : {question}"
    return question

prompt = st.chat_input("Pose ta question ici...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    prompt_final = preparer_prompt(prompt, mode, contenu_pdf)
    systeme_final = SYSTEME
    if prenom:
        systeme_final += f"\nLe prénom de l'étudiant est {prenom}."
    with st.chat_message("assistant"):
        with st.spinner("Je réfléchis... 🧠"):
            reponse = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": systeme_final}] +
                st.session_state.messages[:-1] +
                [{"role": "user", "content": prompt_final}]
            )
            texte = reponse.choices[0].message.content
            st.markdown(texte)
    st.session_state.messages.append({"role": "assistant", "content": texte})
