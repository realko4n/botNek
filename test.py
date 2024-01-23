import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Журналим
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# установите более высокий уровень регистрации для httpx,
# чтобы не регистрировать все GET- и POST-запросы
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
NAME, YOURFRIEND, WASAP, PASSION, KNOWLEDGE = range(5)
user_info = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Список кнопок для ответа
    user = update.message.from_user
    user_info.append(
        {
            "name":"",
            "friend":"",
            "wasap":"",
            "passion":"",
            "knowledge":""
        }
    )

    await update.message.reply_text(
        # Начинаем разговор с вопроса
        'Привет, как тебя зовут?'
    )
    # переходим к этапу `GENDER`, это значит, что ответ
    # отправленного сообщения в виде кнопок будет список
    # обработчиков, определенных в виде значения ключа `GENDER`
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал биографию или рассказ пользователя
    logger.info("name of %s: %s", user.first_name, update.message.text)
    print(update.message.text)
    user_info[-1]['name'] = update.message.text
    # Отвечаем на то что пользователь рассказал.
    await update.message.reply_text(f"Приятно познакомиться, {update.message.text}!\n"
                                    "Напиши пару добрых слов о друге, который тебя пригласил.")


    # Заканчиваем разговор.
    return YOURFRIEND

async def yourFriend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал биографию или рассказ пользователя
    logger.info("Friend of %s: %s", user.first_name, update.message.text)
    print(update.message.text)
    user_info[-1]['friend'] = update.message.text
    # Отвечаем на то что пользователь рассказал.
    await update.message.reply_text("Думаю ему будет приятно!\n"
                                    "Расскажи, чем ты занимаешься?")

    # Заканчиваем разговор.
    return WASAP

async def wasap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал биографию или рассказ пользователя
    logger.info("занятие of %s: %s", user.first_name, update.message.text)
    print(update.message.text)
    user_info[-1]['wasap'] = update.message.text
    # Отвечаем на то что пользователь рассказал.
    await update.message.reply_text("Очень интересно!\n"
                                    "Что в жизни тебя радует и вдохновляет?")

    # Заканчиваем разговор.
    return PASSION

async def passion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал биографию или рассказ пользователя
    logger.info("Passion of %s: %s", user.first_name, update.message.text)
    print(update.message.text)
    user_info[-1]['passion'] = update.message.text
    # Отвечаем на то что пользователь рассказал.
    await update.message.reply_text("Интересно!\n"
                                    "Чем готов делиться с сообществом, в чем можешь быть ему полезен?")

    # Заканчиваем разговор.
    return KNOWLEDGE

async def knowledge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал биографию или рассказ пользователя
    logger.info("skills of %s: %s", user.first_name, update.message.text)
    print(update.message.text)
    user_info[-1]['knowledge'] = update.message.text
    # Отвечаем на то что пользователь рассказал.
    await update.message.reply_text("Спасибо, мы тебе перезвоним")

    # Заканчиваем разговор.
    print(user_info)
    return ConversationHandler.END


# Обрабатываем команду /cancel если пользователь отменил разговор
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("User %s canceled the conversation.", user.first_name)
    # Отвечаем на отказ поговорить
    await update.message.reply_text(
        "Пока, надеюсь увидимся снова.", reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6744306081:AAGWHwDyU9ZOxC-HCecCQ54YYnLv1I28Sxg").build()

    # Определяем обработчик разговоров `ConversationHandler`
    # с состояниями GENDER, PHOTO, LOCATION и BIO
    conv_handler = ConversationHandler(
        # точка входа в разговор
        entry_points=[
            CommandHandler("start", start)
        ],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, name)
            ],

            YOURFRIEND: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, yourFriend)
            ],

            WASAP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, wasap)
            ],

            PASSION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, passion)
            ],

            KNOWLEDGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, knowledge)
            ],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
