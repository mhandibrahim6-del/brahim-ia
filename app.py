import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEME = """Tu es Brahim IA, un assistant étudiant intelligent et motivant.
Tu parles toujours dans la langue de l'utilisateur (français, anglais, arabe...).
Tu expliques les concepts de façon simple avec des exemples concrets.
Tu encourages toujours l'étudiant et tu es positif.
Tu utilises des emojis pour rendre les réponses agréables.
Tu es spécialisé en informatique, mathématiques et intelligence artificielle.
Si l'utilisateur te donne son prénom, tu l'utilises dans tes réponses.
Tu peux résumer des textes, traduire, et générer du code Python."""

# Design amélioré
st.set_page_config(page_title="Brahim IA", page_icon="🎓", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
    .stChatMessage { border-radius: 15px; margin: 5px 0; }
    .stTextInput input { border-radius: 25px; }
    h1 { text-align: center; color: #a78bfa !important; font-size: 3em !important; }
    .stCaption { text-align: center; color: #c4b5fd !important; font-size: 1.1em !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Brahim IA")
st.caption("✨ Ton assistant étudiant intelligent • Multilingue • Spécialisé IA")

# Barre latérale
with st.sidebar:
    st.markdown("## ⚙️ Paramètres")
    prenom = st.text_input("👤 Ton prénom", placeholder="Entre ton prénom...")
    st.markdown("---")
    st.markdown("## 🛠️ Fonctionnalités")
    mode = st.selectbox("Mode", [
        "💬 Conversation libre",
        "📝 Résumer un texte",
        "🌍 Traduire un texte",
        "💻 Générer du code Python",
        "📚 Expliquer un concept"
    ])
    st.markdown("---")
    if st.button("🗑️ Nouvelle conversation"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("### 💡 Exemples")
    if st.button("C'est quoi Python ?"):
        st.session_state.exemple = "C'est quoi Python ?"
    if st.button("Explique l'IA simplement"):
        st.session_state.exemple = "Explique l'IA simplement"
    if st.button("Génère un jeu en Python"):
        st.session_state.exemple = "Génère un jeu en Python"

# Initialiser
if "messages" not in st.session_state:
    st.session_state.messages = []

# Message de bienvenue
if len(st.session_state.messages) == 0:
    nom = f" {prenom}" if prenom else ""
    with st.chat_message("assistant"):
        st.markdown(f"👋 Salut{nom} ! Je suis **Brahim IA** ! Je peux t'aider à apprendre, résumer, traduire et générer du code. Pose-moi n'importe quelle question ! 🚀")

# Afficher historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Préparer le prompt selon le mode
def preparer_prompt(question, mode):
    if "Résumer" in mode:
        return f"Résume ce texte de façon claire et concise : {question}"
    elif "Traduire" in mode:
        return f"Traduis ce texte en français et en anglais : {question}"
    elif "code Python" in mode:
        return f"Génère du code Python propre et commenté pour : {question}"
    elif "Expliquer" in mode:
        return f"Explique ce concept de façon simple avec des exemples : {question}"
    return question

# Zone de saisie
if "exemple" in st.session_state:
    prompt = st.session_state.exemple
    del st.session_state.exemple
else:
    prompt = st.chat_input("Pose ta question ici...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt_final = preparer_prompt(prompt, mode)
    systeme_final = SYSTEME
    if prenom:
        systeme_final += f"\nLe prénom de l'étudiant est {prenom}, utilise-le dans tes réponses."

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
