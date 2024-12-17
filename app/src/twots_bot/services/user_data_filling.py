class UserDataFilling:
    def __init__(self, message, user, user_repo):
        self.__message = message
        self.__user = user
        self.__user_repo = user_repo

    async def __process(self):
        if not self.__user.city:
            self.__user.city = self.__message.text
            await self.__user_repo.persist()
            await self.__message.answer("Введите ваши ФИО")
        if not self.__user.full_name:
            self.__user.full_name = self.__message.text
            await self.__user_repo.persist()
            await self.__message.answer("Введите ваш контактный номер телефона")
        if not self.__user.contact_phone:
            self.__user.contact_phone = self.__message.text
            await self.__user_repo.persist()
            await self.__message.answer("Вы успешно завершили регистрацию. Теперь вы будете получать информацию о предстоящих событиях.")

    async def fill_data(self):
        await self.__process()
