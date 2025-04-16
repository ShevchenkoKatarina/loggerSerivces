import telebot

class TelegramBot:
    TOKEN = "8184856407:AAEaEZ8jM3Ko4B-3z6h-K4Gp2Jrt2LX4bqc"
    CHAT_ID = "CHAT_ID"
    bot = telebot.TeleBot(TOKEN)

    @staticmethod
    def send_error_telegram(msg):
        try:
            TelegramBot.bot.send_message(TelegramBot.CHAT_ID, msg)
            print("Сообщение успешно отправлено в Telegram.")
        except telebot.ExceptionHandler as ex:
            print(f"Ошибка отправки сообщения в чат: {ex}")