import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Твой токен бота
TOKEN = "9209314583:AAF2aEMK1lQrDkJJi-EXMGlx6ZPtHewKvU4"  # или оставь свою строку с токеном

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Хендлер на команду /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Создаем инлайн-кнопку "Скачать чит"
    builder = types.InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="📥 Скачать чит",
        callback_data="download_cheat"
    ))

    await message.answer(
        f"Привет, зимка! 👋\n\n"
        f"Ты попал в официального бота VanishCrack!\n"
        f"Здесь ты можешь скачать актуальную версию чита для RageMP и Majestic RP.",
        reply_markup=builder.as_markup()
    )


# Обработка нажатия на кнопку
@dp.callback_query(F.data == "download_cheat")
async def send_cheat_file(callback: types.CallbackQuery):
    await callback.answer()  # Закрываем часики на кнопке

    # Путь к архиву (должен лежать рядом с main.py в папке проекта)
    file_path = "Cheat.zip"

    if os.path.exists(file_path):
        document = FSInputFile(file_path)

        instruction_text = (
            "✅ Файл успешно загружен!\n\n"
            "📌 Инструкция по установке и запуску:\n"
            "1. Распакуйте архив Cheat.zip в новую папку на Рабочем столе.\n"
            "2. Перенесите все файлы из архива в эту папку.\n"
            "3. Запустите файл Vanish.exe (желательно от имени администратора).\n"
            "4. В окне авторизации введите данные:\n"
            "   • Логин: test\n"
            "   • Пароль: test\n"
            "5. Выберите RageMP или Majestic и нажмите кнопку Inject.\n"
            "6. Перейдите в игру — меню чита появится автоматически!"
        )

        await callback.message.answer_document(document=document, caption=instruction_text)
    else:
        await callback.message.answer("❌ Ошибка: файл архива Cheat.zip не найден на сервере!")


# Мини-веб-сервер для Render, чтобы он не закрывал порт (Free Web Service)
async def handle(request):
    return web.Response(text="VanishCrack Bot is running 24/7!")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()

    # Render передает порт через переменные окружения, по умолчанию берем 8080
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")


# Главная функция запуска
async def main():
    # Запускаем и веб-сервер для Render, и самого телеграм-бота одновременно
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )


if __name__ == "__main__":
    try:
        print("Бот VanishCrack запускается...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")