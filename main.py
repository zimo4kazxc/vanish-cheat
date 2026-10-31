import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Укажите ваш токен бота от BotFather
BOT_TOKEN = "9209314583:AAF2aEMK1lQrDkJJi-EXMGlx6ZPtHewKvU4"

# Имя файла архива (должен лежать в одной папке с скриптом)
ARCHIVE_NAME = "Cheat.zip"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_main_keyboard():
    """Создаёт кнопку для скачивания."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥 Скачать чит", callback_data="download_cheat"
                )
            ]
        ]
    )
    return keyboard


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработчик команды /start."""
    # Получаем имя или ник пользователя
    user_name = message.from_user.first_name or message.from_user.username or "пользователь"

    welcome_text = (
        f"Привет, {user_name}! 👋\n\n"
        f"Ты попал в официального бота **VanishCrack**!\n"
        f"Здесь ты можешь скачать актуальную версию чита для RageMP и Majestic RP."
    )

    await message.answer(
        text=welcome_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


@dp.callback_query(F.data == "download_cheat")
async def process_download(callback: types.CallbackQuery):
    """Обработчик нажатия на кнопку 'Скачать чит'."""
    # Проверяем, существует ли файл рядом со скриптом
    if not os.path.exists(ARCHIVE_NAME):
        await callback.answer(
            "⚠️ Файл архива не найден на сервере. Обратитесь к администратору.",
            show_alert=True,
        )
        return

    # Отправляем уведомление о начале загрузки
    await callback.answer("Готовим файл к отправке...")

    instruction_text = (
        "✅ **Файл успешно загружен!**\n\n"
        "📌 **Инструкция по установке и запуску:**\n"
        "1. Распакуйте архив `Cheat.zip` в **новую папку** на Рабочем столе.\n"
        "2. Перенесите все файлы из архива в эту папку.\n"
        "3. Запустите файл `Vanish.exe` *(желательно от имени администратора)*.\n"
        "4. В окне авторизации введите данные:\n"
        "   • **Логин:** `test`\n"
        "   • **Пароль:** `test`\n"
        "5. Выберите **RageMP** или **Majestic** и нажмите кнопку **Inject**.\n"
        "6. Перейдите в игру — меню чита появится автоматически!"
    )

    # Отправляем архив с подписью-инструкцией
    file_to_send = FSInputFile(ARCHIVE_NAME)
    await callback.message.answer_document(
        document=file_to_send,
        caption=instruction_text,
        parse_mode="Markdown",
    )


async def main():
    print("Бот VanishCrack запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())