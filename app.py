import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(
    page_title="Pluto // Dev Assistant",
    page_icon="💻",
    layout="wide"
)

# Estilização CSS personalizada (Dark Mode Dev / Cyber-Minimalista)
st.markdown("""
    <style>
    /* Fundo geral e fontes no estilo Dark Mode de IDE */
    .stApp {
        background-color: #0b0f19;
        color: #e6edf3;
    }
    
    /* Ajuste da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px. solid #30363d;
    }

    /* Estilização das caixas de mensagem do chat */
    .stChatMessage {
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #30363d;
        background-color: #161b22;
    }

    /* Botões personalizados estilo terminal/dev */
    .stButton button {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #30363d;
        border-color: #8b949e;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Barra Lateral (Sidebar) com estilo Dev & Gamer
with st.sidebar:
    st.markdown("### 💻 Pluto.sys")
    st.caption("v2.0 // AI Assistant Core")
    st.markdown("---")
    
    st.markdown("**Status do Sistema:** 🟢 Online")
    st.markdown("**Ambiente:** Streamlit Cloud")
    st.markdown("**Stack:** Python & Gemini")
    
    st.markdown("---")
    
    # Botão para limpar a conversa
    if st.button("⚡ Resetar Sessão"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("🎮 *Dica: Seja programando sistemas ou discutindo lore de games, o Pluto está na escuta.*")

# Tela Principal
st.title("⚡ Pluto AI")
st.caption("Terminal de Assistência Pessoal & Desenvolvimento")

# Puxa a chave oculta do Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("⚠️ Erro crítico: `GEMINI_API_KEY` não encontrada nos segredos do Streamlit.")
else:
    # Inicializa o cliente do Gemini
    client = genai.Client(api_key=api_key)

    # Inicializa o histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe o histórico de conversas
    for message in st.session_state.messages:
        avatar = "💻" if message["role"] == "assistant" else "⚡"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Entrada de texto do usuário
    if prompt := st.chat_input("Digite um comando ou dúvida para o Pluto..."):
        # Adiciona mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="⚡"):
            st.markdown(prompt)

        # Resposta da IA com indicador de carregamento
        with st.chat_message("assistant", avatar="💻"):
            with st.spinner("Processando dados..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )
                    ai_response = response.text
                    st.markdown(ai_response)
                    # Adiciona resposta ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.error(f"Erro na execução: {e}")
