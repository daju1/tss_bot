#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from telegram import Bot, Chat, ChatPermissions, ReactionTypeEmoji, User
from telegram.constants import ChatAction, ChatType, ReactionEmoji
from telegram.helpers import escape_markdown

from telegram._message import MaybeInaccessibleMessage, Message

from mydblib import common
import mysql.connector as mysql_connector

def insert_tss_msg(date, username, first_name, msg):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'tss'
    }
    connection = mysql_connector.connect(**config)
    cursor = connection.cursor()
    sql = "INSERT INTO tss_messages (date, username, first_name, msg) VALUES (%s, %s, %s, %s)"
    val = (date, username, first_name, msg)
    cursor.execute(sql, val)
    connection.commit()
    print(cursor.rowcount, "record inserted.")
    cursor.close()
    connection.close()

#@pytest.fixture(scope="module")
def chat(bot):
    chat = Chat(
        ChatTestBase.id_,
        title=ChatTestBase.title,
        type=ChatTestBase.type_,
        username=ChatTestBase.username,
        is_forum=True,
        first_name=ChatTestBase.first_name,
        last_name=ChatTestBase.last_name,
    )
    chat.set_bot(bot)
    chat._unfreeze()
    return chat

class ChatTestBase:
    id_ = -28767330
    type_ = "group"
    username = ""

class TestChatWithoutRequest(ChatTestBase):

    __slots__ = (
        #"business_connection_id",
        #"chat",
        #"message_ids",
    )

    def __init__(self, chat_username):

        super().__init__()

        self.username = chat_username

        json_dict = {
            "id": self.id_,
            #"title": self.title,
            "type": self.type_,
            "username": self.username,
            #"is_forum": self.is_forum,
        }
        self.chat: Chat = Chat.de_json(json_dict)#, offline_bot)

    def test_slot_behaviour(self, chat):
        for attr in chat.__slots__:
            assert getattr(chat, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(chat)) == len(set(mro_slots(chat))), "duplicate slot"

    def get_chat(self):
        return self.chat

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот для мониторинга чата. Введите /help для получения списка команд.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Список команд:\n/start - Запустить бота\n/help - Помощь")

async def stat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = common.get_tss_msg(rendered=False)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Здесь будет логика мониторинга

    text = f"Получено: {update}\n\n" \
         + f"сообщение: {update.message}\n\n" \
         + f"message_id: {update.message.message_id}\n" \
         + f"message_thread_id: {update.message.message_thread_id}\n" \
         + f"sender_chat: {update.message.sender_chat}\n" \
         + f"sender_boost_count: {update.message.sender_boost_count}\n" \
         + f"date: {update.message.date}\n" \
         + f"business_connection_id: {update.message.business_connection_id}\n" \
         + f"chat: {update.message.chat}\n" \
         + f"forward_origin: {update.message.forward_origin}\n" \
         + f"is_topic_message: {update.message.is_topic_message}\n" \
         + f"is_automatic_forward: {update.message.is_automatic_forward}\n" \
         + f"reply_to_message: {update.message.reply_to_message}\n" \
         + f"external_reply: {update.message.external_reply}\n" \
         + f"quote: {update.message.quote}\n" \
         + f"reply_to_story: {update.message.reply_to_story}\n" \
         + f"via_bot: {update.message.via_bot}\n" \
         + f"edit_date: {update.message.edit_date}\n" \
         + f"has_protected_content: {update.message.has_protected_content}\n" \
         + f"is_from_offline: {update.message.is_from_offline}\n" \
         + f"media_group_id: {update.message.media_group_id}\n" \
         + f"author_signature: {update.message.author_signature}\n" \
         + f"paid_star_count: {update.message.paid_star_count}\n" \
         + f"text: {update.message.text}\n" \
         + f"entities: {update.message.entities}\n" \
         + f"link_preview_options: {update.message.link_preview_options}\n" \
         + f"effect_id: {update.message.effect_id}\n" \
         + f"animation: {update.message.animation}\n" \
         + f"audio: {update.message.audio}\n" \
         + f"document: {update.message.document}\n" \
         + f"paid_media: {update.message.paid_media}\n" \
         + f"photo: {update.message.photo}\n" \
         + f"sticker: {update.message.sticker}\n" \
         + f"story: {update.message.story}\n" \
         + f"video: {update.message.video}\n" \
         + f"video_note: {update.message.video_note}\n" \
         + f"voice: {update.message.voice}\n" \
         + f"caption: {update.message.caption}\n" \
         + f"caption_entities: {update.message.caption_entities}\n" \
         + f"show_caption_above_media: {update.message.show_caption_above_media}\n" \
         + f"has_media_spoiler: {update.message.has_media_spoiler}\n" \
         + f"contact: {update.message.contact}\n" \
         + f"dice: {update.message.dice}\n" \
         + f"game: {update.message.game}\n" \
         + f"poll: {update.message.poll}\n" \
         + f"new_chat_members: {update.message.new_chat_members}\n" \
         + f"left_chat_member: {update.message.left_chat_member}\n" \
         + f"new_chat_title: {update.message.new_chat_title}\n" \
         + f"new_chat_photo: {update.message.new_chat_photo}\n" \
         + f"supergroup_chat_created: {update.message.supergroup_chat_created}\n"

    text = f"Получено: {update}\n\n" \
         + f"сообщение: {update.message}\n\n" \
         + f"message_id: {update.message.message_id}\n" \
         + f"from_user: {update.message.from_user}\n" \
         + f"from_user.first_name: {update.message.from_user.first_name}\n" \
         + f"from_user.last_name: {update.message.from_user.last_name}\n" \
         + f"from_user.username: {update.message.from_user.username}\n" \
         + f"from_user: {update.message.from_user}\n" \
         + f"from_user: {update.message.from_user}\n" \
         + f"from_user: {update.message.from_user}\n" \
         + f"date: {update.message.date}\n" \
         + f"chat: {update.message.chat}\n" \
         + f"reply_to_message: {update.message.reply_to_message}\n" \
         + f"external_reply: {update.message.external_reply}\n" \
         + f"via_bot: {update.message.via_bot}\n" \
         + f"edit_date: {update.message.edit_date}\n" \
         + f"text: {update.message.text}\n" \
         + f"audio: {update.message.audio}\n" \
         + f"document: {update.message.document}\n" \
         + f"photo: {update.message.photo}\n" \
         + f"supergroup_chat_created: {update.message.supergroup_chat_created}\n"

    message_text = update.message.text

    insert_tss_msg(
        update.message.date,
        update.message.from_user.username,
        update.message.from_user.first_name,
        message_text)

    # await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

if __name__ == '__main__':
    YOUR_TELEGRAM_BOT_TOKEN = None
    try:
        with open('/app/YOUR_TELEGRAM_BOT_TOKEN.txt', "r") as file:
            YOUR_TELEGRAM_BOT_TOKEN = file.read()
    except FileNotFoundError:
        print("Error: The file 'YOUR_TELEGRAM_BOT_TOKEN.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    chat_username = None
    try:
        with open('/app/chat.username', "r") as file:
            chat_username = file.read()
    except FileNotFoundError:
        print("Error: The file 'chat.username' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    if YOUR_TELEGRAM_BOT_TOKEN is None or chat_username is None:
        print("YOUR_TELEGRAM_BOT_TOKEN is None", flush=True)
        print("chat_username is None", flush=True)
    else:
        application = ApplicationBuilder().token(YOUR_TELEGRAM_BOT_TOKEN).build()

        test_my_chat = TestChatWithoutRequest(chat_username=chat_username)

        start_handler = CommandHandler('start', start)
        help_handler = CommandHandler('help', help_command)
        stat_handler = CommandHandler('stat', stat_command)

        message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

        application.add_handler(start_handler)
        application.add_handler(help_handler)
        application.add_handler(stat_handler)
        application.add_handler(message_handler)

        application.run_polling()
