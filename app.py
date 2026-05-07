import streamlit as st
from groq import Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
SYSTEME = """Tu es Brahim IA, un assistant étudiant intelligent et motivant.
Tu parles toujours en français.
Tu expliques les concepts de façon simple avec des exemples concrets.
Tu encourages toujours l'étudiant et tu es positif.
Tu utilises des emojis pour rendre les réponses agréables.
Quand tu expliques quelque chose de complexe, tu le décomposes en étapes simples.
Tu es spécialisé en informatique, mathématiques et intelligence artificielle."""
st.set_page_config(page_title="Brahim IA", page_icon="🎓")
st.title("🎓 Brahim IA")
st.caption("Ton assistant étudiant personnel")
if st.button("🗑️ Nouvelle conversation"):
    st.session_state.messages = []
    st.rerun()
if "messages" not in st.session_state:
    st.session_state.messages = []
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("Salut ! Je suis **Brahim IA**, ton assistant étudiant personnel ! Pose-moi n'importe quelle question !")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pose ta question ici..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Je réfléchis..."):
            reponse = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEME}] + st.session_state.messages
            )
            texte = reponse.choices[0].message.content
            st.markdown(texte)

    st.session_state.messages.append({"role": "assistant", "content": texte})
