import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8731395357:AAFAJArmt3mcQdxeNmiSgXgR3tM9VQUgJEo"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Временная база данных для подписок (в памяти)
subscribed_users = set()

class SnosState(StatesGroup):
 target = State()

# --- КЛАВИАТУРЫ ---
# Кнопка покупки (Inline)
buy_kb = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text="💎 Купить подписку", callback_data="buy_sub")]
])

# Главное меню (Reply)
main_kb = ReplyKeyboardMarkup(keyboard=[
 [KeyboardButton(text="💥 Снос (визуал)")]
], resize_keyboard=True)


# --- ОБРАБОТЧИКИ ---
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
 await state.clear()
 if message.from_user.id in subscribed_users:7572936594
  await message.answer("<b>Добро пожаловать в панель управления!</b>", parse_mode="HTML", reply_markup=main_kb)
 else:
  await message.answer(
   "🛑 <b>Доступ закрыт.</b>\nДля использования функционала необходимо приобрести подписку.", 
   parse_mode="HTML", 
   reply_markup=buy_kb
  )

# Обработка фейковой покупки
@dp.callback_query(F.data == "buy_sub")
async def process_buy(call: CallbackQuery):
 subscribed_users.add(call.from_user.id)
 await call.message.edit_text("✅ <b>Оплата прошла успешно!</b>\nПодписка активирована навсегда.", parse_mode="HTML")
 await call.message.answer("Главное меню открыто. Выберите действие внизу экрана ⬇️", reply_markup=main_kb)
 await call.answer()

# Запрос цели для сноса
@dp.message(F.text == "💥 Снос (визуал)")
async def start_snos(message: Message, state: FSMContext):
 if message.from_user.id not in subscribed_users:
  await message.answer("У вас нет подписки!")
  return
  
 await message.answer("🎯 <b>Введите @username или номер телефона цели для сноса:</b>", parse_mode="HTML")
 await state.set_state(SnosState.target)

# Имитация процесса сноса
@dp.message(SnosState.target)
async def execute_snos(message: Message, state: FSMContext):
 target = message.text
 await state.clear()

 # Отправляем первое сообщение, которое потом будем изменять
 msg = await message.answer(f"⏳ Инициализация атаки на <code>{target}</code>...", parse_mode="HTML")
 await asyncio.sleep(1.5)
 
 await msg.edit_text("🔄 Подключение к серверам ботнета (Proxy: ON)...", parse_mode="HTML")
 await asyncio.sleep(1.5)
 
 await msg.edit_text("⚡️ Генерация вредоносного трафика...", parse_mode="HTML")
 await asyncio.sleep(1.5)
 
 await msg.edit_text("🚀 Отправка сессий авторизации на целевой аккаунт...", parse_mode="HTML")
 await asyncio.sleep(2)
 
 sessions_count = random.randint(1, 100)
 
 final_text = (
  f"✅ <b>АТАКА УСПЕШНО ЗАВЕРШЕНА</b>\n\n"
  f"🎯 Цель: <code>{target}</code>\n"
  f"💉 <b>{sessions_count}</b> сессий закинуто на аккаунт.\n"
  f"☠️ Скоро он будет снесен."
 )
 await msg.edit_text(final_text, parse_mode="HTML")

async def main():
 await bot.delete_webhook(drop_pending_updates=True)
 await dp.start_polling(bot)

if __name__ == "__main__":
 asyncio.run(main())
