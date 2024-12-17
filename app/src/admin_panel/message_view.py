from sqladmin import ModelView

from twots_bot.models.orm.message import Message


class MessageAdmin(ModelView, model=Message):
    column_list = [Message.id, Message.text]
