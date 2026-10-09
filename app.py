import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(page_title="Pluto dos Ovao Inteligente", page_icon="🤖🐕")

st.title("🐕 Pluto")
st.write("Seu cachorro Ovudo Inteligente.")

# Campo para a chave da API do Gemini na barra lateral
st.sidebar.header("Configurações")
api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")

if not api_key:
    st.warning("Por favor, insira sua chave da API do Gemini na barra lateral para continuar.")
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
                # Usando o modelo padrão recomendado
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
