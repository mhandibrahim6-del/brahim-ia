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

# Initialiser session_state EN PREMIER
if "messages" not in st.session_state:
    st.session_state.messages = []
if "contenu_pdf" not in st.session_state:
    st.session_state.contenu_pdf = ""
if "nom_pdf" not in st.session_state:
    st.session_state.nom_pdf = ""

with st.sidebar:
    st.markdown("## ⚙️ Paramètres")
    prenom = st.text_input("👤 Ton prénom", placeholder="Entre ton prénom...")
    st.markdown("---")
    st.markdown("## 📄 Uploader un PDF")
    pdf_file = st.file_uploader("Choisis un fichier PDF", type="pdf")

    if pdf_file is not None:
        if pdf_file.name != st.session_state.nom_pdf:
            pdf_bytes = pdf_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            texte = ""
            for page in doc:
                texte += page.get_text()
            nb_pages = doc.page_count
            doc.close()
            st.session_state.contenu_pdf = texte
            st.session_state.nom_pdf = pdf_file.name
            st.session_state.messages = []
            st.success(f"✅ PDF chargé ! ({nb_pages} pages)")
        else:
            st.success(f"✅ {st.session_state.nom_pdf} chargé")

    st.markdown("---")
    if st.button("🗑️ Nouvelle conversation"):
    st.session_state.messages = []
    st.rerun()

# Message de bienvenue
if len(st.session_state.messages) == 0:
    nom = f" {prenom}" if prenom else ""
    with st.chat_message("assistant"):
        if st.session_state.contenu_pdf:
            st.markdown(f"👋 Salut{nom} ! J'ai bien lu **{st.session_state.nom_pdf}** ! Pose-moi des questions dessus 📄🚀")
        else:
            st.markdown(f"👋 Salut{nom} ! Je suis **Brahim IA** ! Upload un PDF ou pose-moi n'importe quelle question ! 🚀")

# Afficher historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
prompt = st.chat_input("Pose ta question ici...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.contenu_pdf:
        contenu = f"Voici le contenu du PDF '{st.session_state.nom_pdf}':\n\n{st.session_state.contenu_pdf[:4000]}\n\nQuestion: {prompt}"
    else:
        contenu = prompt

    st.session_state.messages.append({"role": "user", "content": prompt})

    systeme_final = SYSTEME
    if prenom:
        systeme_final += f"\nLe prénom de l'étudiant est {prenom}."

    with st.chat_message("assistant"):
        with st.spinner("Je réfléchis... 🧠"):
            reponse = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": systeme_final},
                    {"role": "user", "content": contenu}
                ]
            )
            texte = reponse.choices[0].message.content
            st.markdown(texte)

    st.session_state.messages.append({"role": "assistant", "content": texte})
