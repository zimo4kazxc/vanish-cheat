import asyncio
import logging
import os
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен твоего бота
TOKEN = "9209314583:AAF2aEMK1lQrDkJJi-EXMGlx6ZPtHewKvU4"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
  # Создаем клавиатуру с помощью InlineKeyboardBuilder (импортирован правильно)
  builder = InlineKeyboardBuilder()
  builder.add(
      types.InlineKeyboardButton(
          text="📥 Получить чит", callback_data="get_cheat"
      )
  )

  await message.answer(
      "Привет! Это официальный бот проекта **VanishCRACK**.\n\nНажми кнопку"
      " ниже, чтобы получить доступ к файлу:",
      reply_markup=builder.as_markup(),
      parse_mode="Markdown",
  )


@dp.callback_query(lambda c: c.data == "get_cheat")
async def process_callback_cheat(callback: types.CallbackQuery):
  await callback.message.answer(
      "Вот твой файл с читом! Не забудь отключить антивирус перед"
      " распаковкой. 🛡"
  )
  await callback.answer()


# --- Веб-сервер для Render (чтобы бот не засыпал и не было ошибок порта) ---
async def handle(request):
  return web.Response(text="VanishCRACK Bot is alive and running 24/7!")


async def start_web_server():
  app = web.Application()
  app.router.add_get("/", handle)
  runner = web.AppRunner(app)
  await runner.setup()

  # Render передает порт через переменную окружения PORT (по умолчанию 10000)
  port = int(os.getenv("PORT", 10000))
  site = web.TCPSite(runner, "0.0.0.0", port)
  await site.start()
  print(f"Web server started on port {port}")


async def main():
  # Запускаем веб-сервер параллельно с ботом
  await start_web_server()
  # Запуск поллинга сообщений
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())