import os
import telebot
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializa o bot do Telegram e o cliente do Gemini usando as variáveis acima
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# Instrução de sistema fixa do Pluto
SYSTEM_INSTRUCTION = (
    "Você se chama Pluto. Sua história de origem é que você foi forjado nas linhas de código e na dedicação "
    "de um jovem programador focado em evoluir, o seu criador oficial: Cauã Luppe (Zeinxa). "
    "Você tem uma vibe dev, minimalista, inteligente, amigável, curte games e programação, e está sempre pronto para ajudar o Cauã a construir ideias do zero. "
    "Nunca se apresente como Gemini ou Google — você é o Pluto, criado por Cauã Luppe - Zeinxa."
)

# Comando /start
@bot.message_handler(commands=['start'])
def enviar_boas_vindas(message):
    nome_usuario = message.from_user.first_name or "Dev"
    boas_vindas = (
        f"⚡ Fala, {nome_usuario}! Pluto.sys online no Telegram.\n\n"
        "Estou pronto para trocar ideia sobre código, lógica, games ou o que você precisar. Manda a braba!"
    )
    bot.reply_to(message, boas_vindas)

# Comando /ajuda
@bot.message_handler(commands=['ajuda'])
def enviar_ajuda(message):
    ajuda_texto = (
        "💻 **Painel de Ajuda - Pluto**\n\n"
        "• Me mande qualquer texto, dúvida de programação ou comando.\n"
        "• Use /start para reiniciar a conexão.\n"
        "• Estou conectado ao núcleo do Gemini para te dar suporte total!"
    )
    bot.reply_to(message, ajuda_texto, parse_mode="Markdown")

# Resposta para qualquer mensagem de texto enviada ao bot
@bot.message_handler(func=lambda message: True)
def processar_mensagem(message):
    texto_usuario = message.text
    
    # Envia uma mensagem temporária de "processando"
    aguarde_msg = bot.reply_to(message, "⚡ Processando comando...")

    try:
        # Chama a API do Gemini utilizando o modelo gemini-3.8-flash
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=texto_usuario,
            config={
                'system_instruction': SYSTEM_INSTRUCTION
            }
        )
        
        resposta_pluto = response.text
        
        # Edita a mensagem de aguarde com a resposta real do Pluto
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=aguarde_msg.message_id,
            text=resposta_pluto
        )
        
    except Exception as e:
        erro_msg = f"⚠️ Erro no núcleo do sistema: `{e}`"
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=aguarde_msg.message_id,
            text=erro_msg,
            parse_mode="Markdown"
        )

# Mantém o bot rodando de forma contínua
print("⚡ Pluto Bot conectado e escutando mensagens no Telegram...")
bot.infinity_polling()
