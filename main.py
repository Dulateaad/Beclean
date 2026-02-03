# pip install pyTelegramBotAPI==4.12.0 flask

from flask import Flask, request, jsonify
import telebot
import threading

# =============================
# CONFIG
# =============================
BOT_TOKEN = "8447073218:AAFAt9e-aFbE96Vk8dhdJd2MAAMEWEd3hhI"
ADMIN_CHAT_IDS = [
    759300791,1542351599,
    1298555678,1722760600, 8518059493  # если это группа/канал
]

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
app = Flask(__name__)

# =============================
# TELEGRAM COMMANDS
# =============================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ Бот заявок запущен")


@bot.message_handler(commands=['myid'])
def myid(message):
    bot.send_message(message.chat.id, f"Ваш chat_id: {message.chat.id}")


# =============================
# API ENDPOINT — сюда сайт шлет заявки
# =============================
@app.route("/lead", methods=["POST"])
def receive_lead():
    data = request.json or {}

    name = data.get("name", "—")
    phone = data.get("phone", "—")
    info = data.get("info", "—")
    source = data.get("source", "website")

    text = (
        "📥 <b>Новая заявка</b>\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📝 Инфо: {info}\n"
        f"🌍 Источник: {source}"
    )

    bot.send_message(ADMIN_CHAT_ID, text)

    return jsonify({"status": "ok"})


# =============================
# HEALTH CHECK
# =============================
@app.route("/")
def home():
    return "Lead bot is running"


# =============================
# RUN BOTH BOT + API
# =============================
def run_bot():
    print("Telegram bot started...")
    bot.infinity_polling()


if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()

    print("Flask API started...")
    app.run(host="0.0.0.0", port=5000)
