import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command

import openai

# Подключение вашего API-ключа GPT
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Инициализация бота и диспетчера
bot = Bot(token = 'YOUR_TELEGRAM_BOT_TOKEN')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Создание состояний для обработки различных событий
class ChatState(StatesGroup):
	DEFAULT = State()  # Состояние по умолчанию


# Обработка команды /start
@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
	await message.reply("Привет! Я бот, готовый отвечать на ваши сообщения.")


# Обработка всех остальных сообщений
@dp.message_handler()
async def handle_message(message: types.Message, state: FSMContext):
	# Получение текста сообщения от пользователя
	input_text = message.text
	
	# Вызов GPT для генерации ответа
	response = openai.ChatCompletion.create(
		model = "gpt-3.5-turbo",
		messages = [
			{"role": "system", "content": "Вы - пользователь"},
			{"role": "user", "content": input_text},
		],
		max_tokens = 4000,
	)
	
	# Получение сгенерированного ответа от GPT
	output_text = response['choices'][0]['message']['content']
	
	# Отправка ответа пользователю
	await message.reply(output_text)


# Запуск бота
if __name__ == '__main__':
	aiogram.executor.start_polling(dp, skip_updates = True)