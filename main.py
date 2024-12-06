from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from info import token

# =============================================================

api = token  # получить токен бота
bot = Bot(api)  # объект класса Bot()
dp = Dispatcher(bot, storage=MemoryStorage())  # диспетчер управления ботом

kb_start = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
button_calc = KeyboardButton(text='Рассчитать')
button_info = KeyboardButton(text='Информация')
kb_start.row(button_calc, button_info)


@dp.message_handler(commands=['start'])  # декоратор для обработки команды /start
async def start(message):
    """Асинхронный метод выполнения команды 'start'.
    Выводим сообщение и показываем клавиатуру"""
    await message.reply(f'Привет {message["from"]["first_name"]}!', reply_markup=kb_start)


@dp.message_handler(text='Рассчитать')
async def calculate(message):
    """Обработка клика по кнопке Рассчитать. Выводит в Telegram-бот сообщение 'Введите свой возраст:'.
    и после этого ожидает ввода возраста в атрибут UserState.age при помощи метода set."""
    msg = f'{message["from"]["first_name"]}! Сейчас я помогу Вам рассчитать суточную норму потребления калорий.\nВведите свой возраст, лет:'
    await message.answer(msg)
    await UserState.age.set()  # вызываем функцию установки возраста


@dp.message_handler(text='Информация')
async def inform(message):
    """Обработка клика по кнопке Информация. Функция выводит информацию о словаре 'message'"""
    await message.answer(message)


class UserState(StatesGroup):
    """Дочерний класс, унаследованный от StatesGroup"""
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


@dp.message_handler(text='Calories')
async def set_age(message):
    """Эта функция выводит в Telegram-бот сообщение 'Введите свой возраст:'.
    и после этого ожидает ввода возраста в атрибут UserState.age при помощи метода set."""
    msg = f'Сейчас я помогу Вам рассчитать суточную норму потребления калорий.\nВведите свой возраст, лет:'
    await message.answer(msg)
    await UserState.age.set()  # вызываем функцию установки возраста


@dp.message_handler(state=UserState.age)  # декоратор, указывает, что функция будет реагировать на state=UserState.age
async def set_growth(message, state):  # в функцию передаются уже два параметра
    """Эта функция обновляет данные в состоянии age на message.text, используя метод update_data.
    Далее выводит в Telegram-бот сообщение 'Введите свой рост:'.
    После этого ожидает ввода роста в атрибут UserState.growth при помощи метода set."""
    age_text = message.text
    if not age_text.isdigit():  # проверка, что введенные данные являются строкой из числовых символов
        await message.answer('Ошибка! Неверно ввели возраст!')
        age_text = -1
    await state.update_data(age=age_text)  # обновим данные в состоянии age
    await message.answer('Введите свой рост, см.:')  # выведем сообщение для пользователя
    await UserState.growth.set()  # вызовем функцию установки веса


@dp.message_handler(
    state=UserState.growth)  # декоратор, указывает, что функция будет реагировать на state=UserState.growth
async def set_weight(message, state):
    """Эта функция обновляет данные в состоянии growth на message.text (написанное пользователем сообщение),
    используя для этого метод update_data. Далее выводит в Telegram-бот сообщение 'Введите свой вес:'.
    После этого ожидает ввод веса в атрибут UserState.weight при помощи метода set."""
    growth_text = message.text
    if not growth_text.isdigit():  # проверка, что введенные данные являются строкой из числовых символов
        await message.answer('Ошибка! Неверно ввели свой рост!')
        growth_text = -1
    await state.update_data(growth=growth_text)  # обновим данные в состоянии growth
    await message.answer('Введите свой вес, кг.:')  # выведем сообщение для пользователя
    await UserState.weight.set()  # вызовем функцию установки веса


@dp.message_handler(
    state=UserState.weight)  # декоратор, указывает, что функция будет реагировать на state=UserState.weight
async def send_calories(message, state):
    """Эта функция обновляет данные в состоянии weight на message.text (написанное пользователем сообщение),
     используя для метод update_data. Далее в функции получает в переменную data все ранее введённые состояния
     при помощи метода state.get_data() и рассчитывает суточную норму калорий для мужчит и для женщин,
     отправляет результаты расчета в Телеграм и финиширует машину состояний методом finish()."""
    weight_text = message.text
    if not weight_text.isdigit():  # проверка, что введенные данные являются строкой из числовых символов
        await message.answer('Ошибка! Неверно ввели свой вес!')
        weight_text = -1
    await  state.update_data(weight=weight_text)  # обновим данные в состоянии weight
    data = await state.get_data()  # получим наши данные из машины состояний

    # получим из машины состояний введенные ранее значения
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    if age < 0 or growth < 0 or weight < 0:  # если какое-либо значение неверное
        msg = f'Расчет калорий невозможен. Неверные данные ...'  # формируем сообщение
    else:
        # рассчитаем суточную норму калорий для мужчин и для женщин
        calories_men = 10 * weight + 6.25 * growth - 5 * age + 5
        calories_women = 10 * weight + 6.25 * growth - 5 * age - 161

        # сформируем сообщение для пользователя и выведем его в Телеграмм
        msg = f'Суточная норма калорий:\n    Для мужчин: {str(calories_men)},\n    Для женщин: {str(calories_women)}'
    await message.answer(msg)

    await state.finish()  # завершим работу с машиной состояний


# для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
# для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.


@dp.message_handler()  # декоратор для обработки любых текстовых сообщений
async def all_messages(message):
    """Асинхронный метод отправки эхо-сообщений"""
    msg = message.text[::-1]
    await message.answer(msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # запуск бота
