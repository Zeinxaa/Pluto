import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(page_title="Pluto - Minha IA", page_icon="🤖")

st.title("🤖 Pluto")
st.write("Seu assistente pessoal inteligente.")

# Puxa a chave de forma oculta direto do Streamlit Cloud
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("A chave da API do Gemini não foi configurada nos segredos do Streamlit Cloud.")
else:
    # Inicializa o cliente do Gemini
    client = genai.Client(api_key=api_key)

    # Inicializa o histórico de chat no Streamlit
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe as mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada do usuário
    if prompt := st.chat_input("O que você gostaria de conversar?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Resposta da IA
        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
