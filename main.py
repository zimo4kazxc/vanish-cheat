import asyncio
import logging
import os
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен твоего бота
TOKEN = "9209314583:AAF2aEMK1lQrDkJJi-EXMGlx6ZPtHewKvU4"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
  builder = InlineKeyboardBuilder()
  builder.add(
      types.InlineKeyboardButton(
          text="📥 Получить чит", callback_data="get_cheat"
      )
  )

  await message.answer(
      "Привет! Это официальный бот проекта **VanishCRACK**.\n\nНажми кнопку"
      " ниже, чтобы получить архив с читом:",
      reply_markup=builder.as_markup(),
      parse_mode="Markdown",
  )


@dp.callback_query(lambda c: c.data == "get_cheat")
async def process_callback_cheat(callback: types.CallbackQuery):
  file_path = "cheat.zip"

  # Текст инструкции, который будет отправляться вместе с файлом
  instruction_text = (
      "📥 **Вот твой архив с читом!**\n\n"
      "📋 **Как установить и запустить:**\n"
      "1. Скачай архив `cheat.zip`.\n"
      "2. Распакуй его содержимое в удобную папку на компьютере.\n"
      "3. Прочитай текстовый файл с инструкцией внутри архива.\n"
      "4. Запусти приложение и следуй подсказкам на экране. 🚀"
  )

  if os.path.exists(file_path):
    document = FSInputFile(file_path)
    await callback.message.answer_document(
        document, caption=instruction_text, parse_mode="Markdown"
    )
  else:
    await callback.message.answer(
        "⚠️ Ошибка: файл `cheat.zip` пока не загружен в репозиторий на GitHub!"
    )

  await callback.answer()


# --- Веб-сервер для Render (предотвращает засыпание бота) ---
async def handle(request):
  return web.Response(text="VanishCRACK Bot is alive and running 24/7!")


async def start_web_server():
  app = web.Application()
  app.router.add_get("/", handle)
  runner = web.AppRunner(app)
  await runner.setup()

  port = int(os.getenv("PORT", 10000))
  site = web.TCPSite(runner, "0.0.0.0", port)
  await site.start()
  print(f"Web server started on port {port}")


async def main():
  await start_web_server()
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())