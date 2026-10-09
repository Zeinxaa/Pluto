import streamlit as st
import random
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
        border-right: 1px solid #30363d;
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

# Lista de ganchos / incentivos para puxar assunto (Dev & Games)
incentivos_do_dia = [
    "🚀 **Missão de Hoje:** E se a gente criasse um script em Python para automatizar alguma tarefa chata do seu dia?",
    "🎮 **Papo de Gamer:** Qual jogo marcou mais a sua vida ou qual você está jogando e achou a programação/história fascinante?",
    "💡 **Desafio de Lógica:** Bora tentar entender como funcionam loops e condicionais criando um minijogo de adivinhação no terminal?",
    "👾 **Curiosidade Dev:** Você já parou para pensar em como os desenvolvedores otimizam gráficos pesados em jogos de mundo aberto?",
    "⚡ **Foco no Código:** Me conta o que você está tentando aprender ou construir hoje para a gente destrinchar passo a passo!"
]

# Seleciona um incentivo aleatório para aparecer na sessão
if "incentivo_atual" not in st.session_state:
    st.session_state.incentivo_atual = random.choice(incentivos_do_dia)

# Barra Lateral (Sidebar) com estilo Dev & Gamer
with st.sidebar:
    st.markdown("### 💻 Pluto.sys")
    st.caption("v2.2 // AI Assistant Core")
    st.markdown("---")
    
    st.markdown("**Status do Sistema:** 🟢 Online")
    st.markdown("**Criador:** Cauã Luppe (Zeinxa)")
    st.markdown("**Stack:** Python & Gemini")
    
    st.markdown("---")
    
    # Caixa de Incentivo / Conversa do Dia
    st.markdown("#### 🎯 Incentivo do Dia")
    st.info(st.session_state.incentivo_atual)
    
    st.markdown("---")
    
    # Botão para limpar a conversa
    if st.button("⚡ Resetar Sessão"):
        st.session_state.messages = []
        st.session_state.incentivo_atual = random.choice(incentivos_do_dia)
        st.rerun()

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

    # Inicializa o histórico de mensagens da tela
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Instrução de sistema fixa do Pluto
    system_instruction = (
        "Você se chama Pluto. Sua história de origem é que você foi forjado nas linhas de código e na dedicação "
        "de um jovem programador focado em evoluir, o seu criador oficial: Cauã Luppe (Zeinxa). "
        "Você tem uma vibe dev, minimalista, inteligente, amigável, curte games e programação, e está sempre pronto para ajudar o Cauã a construir ideias do zero. "
        "Nunca se apresente como Gemini ou Google — você é o Pluto, criado por Cauã Luppe - Zeinxa."
    )

    # Exibe o histórico de conversas na interface
    for message in st.session_state.messages:
        avatar = "💻" if message["role"] == "assistant" else "⚡"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Entrada de texto do usuário
    if prompt := st.chat_input("Digite um comando ou dúvida para o Pluto..."):
        # Adiciona mensagem do usuário no histórico visual
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="⚡"):
            st.markdown(prompt)

        # Resposta da IA recriando a sessão com o histórico atual para evitar erros de conexão fechada
        with st.chat_message("assistant", avatar="💻"):
            with st.spinner("Processando dados..."):
                try:
                    # Converte o histórico do Streamlit para o formato aceito pelo chats.create
                    chat_history = [
                        {"role": m["role"], "parts": [m["content"]]} 
                        for m in st.session_state.messages[:-1] # Pega tudo menos a última mensagem que vai ser enviada agora
                    ]

                    # Cria a sessão de chat injetando o histórico anterior
                    chat = client.chats.create(
                        model="gemini-3.8-flash",
                        history=chat_history if chat_history else None,
                        config={
                            'system_instruction': system_instruction
                        }
                    )

                    # Envia a nova mensagem do usuário
                    response = chat.send_message(prompt)
                    ai_response = response.text
                    st.markdown(ai_response)
                    
                    # Adiciona a resposta da IA no histórico visual
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.error(f"Erro na execução: {e}")
