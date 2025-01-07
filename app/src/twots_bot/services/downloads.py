from uuid import uuid4

from aiogram.types import Message

from twots_bot.config import bot


class DownloadMedia:
    def __init__(self, message):
        self.__message: Message = message
        self.__bot = bot
        self.__text = None
        self.__file_path = None

    async def __set_text(self, file):
        if file and not self.__message.caption:
            await self.__message.answer(text="Нельзя сохранить файл без описания.")
            return

        if file:
            self.__text = self.__message.caption

    async def __download_photo(self):
        try:
            file = await self.__bot.get_file(self.__message.photo[-1].file_id)
            file_name = f"{str(uuid4())}.{file.file_path.split(".")[-1]}"
            self.__file_path = f"media/{file_name}"
            await self.__bot.download_file(file_path=file.file_path, destination=self.__file_path)
            await self.__set_text(file=file)
        except TypeError:
            await self.__set_text(file=None)
            pass

    async def download_media(self):
        self.__text = self.__message.text
        await self.__download_photo()
        return self.__text, self.__file_path
