import logging
import markups as mk
from localisations import ll # файл с переводами 
from aiogram import Bot,Dispatcher,executor,types # импорт нужных для работы функций из библиотеки 
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from db import Database # файл для работы с базой данных


# -------------------------------------------------------------------------------
# ОПРЕДЕЛЕНИЕ ПЕРЕМЕННЫХ
# -------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)  # Уровень логов
bot = Bot(token='7023063772:AAFFbn8O4wnmyTaCDQnoDimkSC5KDLMeuw4',parse_mode="HTML")   # подключение id бота и выбор парсинга, для стилизации текста
dp = Dispatcher(bot) # обращение к боту для работы
db = Database('database.db') # подключение файла базы данных


# -------------------------------------------------------------------------------
# ПОСЛЕ КОМАНД /start /help /blocks
# -------------------------------------------------------------------------------
@dp.message_handler(commands=['start','help','blocks']) # работа данного блока кода после введения указанных команд
async def start(message: types.Message):
	await bot.delete_message(message.from_user.id,message.message_id) # удаление предыдущего сообщения
	if not db.user_exists(message.from_user.id): # выполнение действия, если пользователя нету в базе данных
		await bot.send_photo(chat_id = message.from_user.id,photo = "https://i.postimg.cc/dtBtL0P1/welcome.png",caption = '<b>[EN]</b>\nHi! I am your assistant, designed to help you adapt to a new society.\nChoose your language:\n\n\n<b>[ES]</b>\n¡Hola! Soy tu asistente para adaptarme a la nueva sociedad.\nElige tu idioma:\n\n\n<b>[RU]</b>\nПривет! Я — твой помощник, призванный помочь адаптироваться в новом обществе.\nВыбери свой язык:',
			reply_markup=mk.langMenu)
	else:
		lang = db.get_lang(message.from_user.id) # получение языка пользователя из базы данных
		await bot.send_photo(chat_id = message.from_user.id,photo = ll('https://i.postimg.cc/WzTrk6jK/blocksRU.png',lang) ,caption = ll('<b>Отлично! Теперь вам доступно несколько блоков для изучения.</b> (Вы всегда сможете вернуться к этому сообщению, используя команду /blocks. Что бы поменять язык, используйте /lang):\n\n\n🍾<b>Культура и тенденции.</b>\nУзнайте, что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.\n\n👾<b>Навигация.</b>\nУзнайте про опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.\n\n👀<b>Общество.</b>\nНормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.\n\n🦻<b>Словарь.</b>\nЖаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.\n\n<b>⭐️Повседневная жизнь.</b>\nПопулярные сервисы и магазины.',
			lang),reply_markup=mk.blocksMenu(lang))


# -------------------------------------------------------------------------------
# ПОСЛЕ КОМАНДЫ /lang
# -------------------------------------------------------------------------------
@dp.message_handler(commands=['lang']) # работа данного блока кода, после введения команды /lang
async def lang(message: types.Message):
	await bot.delete_message(message.from_user.id,message.message_id)
	await bot.send_photo(chat_id = message.from_user.id,photo = ll('https://i.postimg.cc/WbDWbTWk/langRU.png',lang),caption = '<b>[EN]</b>\nHi! I am your assistant, designed to help you adapt to a new society.\nChoose your language:\n\n\n<b>[ES]</b>\n¡Hola! Soy tu asistente para adaptarme a la nueva sociedad.\nElige tu idioma:\n\n\n<b>[RU]</b>\nПривет! Я — твой помощник, призванный помочь адаптироваться в новом обществе.\nВыбери свой язык:',
		reply_markup=mk.langMenu)


# -------------------------------------------------------------------------------
# РЕАКЦИЯ БОТА НА СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЯ
# -------------------------------------------------------------------------------
@dp.message_handler() # сообщения бота
async def mess(message: types.Message):
	lang = db.get_lang(message.from_user.id)
	if message.text == ll('Блоки',lang): # проверка текста, отправленного пользователем
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/WzTrk6jK/blocksRU.png',lang) ,caption = ll('<b>Отлично! Теперь вам доступно несколько блоков для изучения.</b> (Вы всегда сможете вернуться к этому сообщению, используя команду /blocks. Что бы поменять язык, используйте /lang):\n\n\n🍾<b>Культура и тенденции.</b>\nУзнайте, что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.\n\n👾<b>Навигация.</b>\nУзнайте про опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.\n\n👀<b>Общество.</b>\nНормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.\n\n🦻<b>Словарь.</b>\nЖаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.\n\n<b>⭐️Повседневная жизнь.</b>\nПопулярные сервисы и магазины.',
			lang),reply_markup=mk.blocksMenu(lang))


# -------------------------------------------------------------------------------
# РЕАКЦИЯ БОТА НА ИНЛАЙН КНОПКИ
# -------------------------------------------------------------------------------
@dp.callback_query_handler() # блок кода, работающий при нажатии инлайн кнопки
async def set_lang(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id,callback.message.message_id)
	if callback.data.count('lang_') == 1: # проверка значения колбека, после нажатия на инлайн кнопку
		if not db.user_exists(callback.from_user.id): # выполнение действия, если пользователя нету в базе данных
			lang = callback.data[5:] # удаление первых пяти символов колбека. Остаётся только язык
			db.add_user(callback.from_user.id,lang) # добавление информации о пользователе в базу данных 
			await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/WzTrk6jK/blocksRU.png',lang) ,caption = ll('<b>Отлично! Теперь вам доступно несколько блоков для изучения.</b> (Вы всегда сможете вернуться к этому сообщению, используя команду /blocks. Что бы поменять язык, используйте /lang):\n\n\n🍾<b>Культура и тенденции.</b>\nУзнайте, что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.\n\n👾<b>Навигация.</b>\nУзнайте про опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.\n\n👀<b>Общество.</b>\nНормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.\n\n🦻<b>Словарь.</b>\nЖаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.\n\n<b>⭐️Повседневная жизнь.</b>\nПопулярные сервисы и магазины.',
				lang),reply_markup=mk.blocksMenu(lang))
		else:
			lang = callback.data[5:]
			db.update_user(callback.from_user.id,lang) # обновление языка пользователя 
			await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/WzTrk6jK/blocksRU.png',lang) ,caption = ll('<b>Отлично! Теперь вам доступно несколько блоков для изучения.</b> (Вы всегда сможете вернуться к этому сообщению, используя команду /blocks. Что бы поменять язык, используйте /lang):\n\n\n🍾<b>Культура и тенденции.</b>\nУзнайте, что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.\n\n👾<b>Навигация.</b>\nУзнайте про опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.\n\n👀<b>Общество.</b>\nНормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.\n\n🦻<b>Словарь.</b>\nЖаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.\n\n<b>⭐️Повседневная жизнь.</b>\nПопулярные сервисы и магазины.',
				lang),reply_markup=mk.blocksMenu(lang))



	if callback.data == 'cultura':
		lang = db.get_lang(callback.from_user.id) # получение языка пользователя
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/HxC0J12W/1.jpg',lang),caption = ll('Культура и тенденции: что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.',lang),
			reply_markup=mk.backBlocks(lang))
	if callback.data == 'nav':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/75TD9LmG/6.jpg',lang),caption = ll('Навигация: опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.',lang),
			reply_markup=mk.trnMenu(lang))
	if callback.data == 'dic':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/t7shbLQD/3.jpg',lang),caption = ll('Словарь: жаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.',lang),
			reply_markup=mk.divMenu(lang))
	if callback.data == 'obs':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/Y93wzgTZ/TOP.png',lang),caption = ll('Общество: нормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.',lang),
			reply_markup=mk.backBlocks(lang))
	if callback.data == 'dlf':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/18gxB9MT/5.jpg',lang),caption = ll('<b>Рекомендуется использовать следующие банки:</b>\n1. Сбербанк\n2. ВТБ\n3. Тинькофф\n4. Альфа-Банк\n5. Газпромбанк\n\n<b>Продуктовые магазины</b>\n1. Вкусвилл. Дорогая, но качественная, полезная еда. Товар сильно отличается от товаров в других магазинах.\n2. Пятёрочка. Самый популярный продуктовый магазин, где очень большой выбор продуктов по хорошей цене. \n3. Дикси. Низкие цены и редкие товары, но качество обслуживания может быть далеко не высоким.\n\n<b>Маркетплейсы</b>\n1. Avito. Платформа, где каждый может разместить объявление о продаже чего-либо, предоставлении различных услуг и свободных вакансиях на разные работы.\n2. Ozon/Wildberries. Онлайн магазины, где можно приобрести разные товары, начиная едой и заканчивая музыкальными инструментами. Доставка товаров производится в пункты выдачи, которые открыты почти в каждом районе.\n3. Aliexpress. Огромный выбор самых разных товаров, которых не найти больше нигде. Однако, существует проблема с долгими сроками доставки и ненадёжностью.',lang),
			reply_markup=mk.backBlocks(lang))
	if callback.data == 'LNG':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/WbDWbTWk/langRU.png',lang),caption = '<b>[EN]</b>\nHi! I am your assistant, designed to help you adapt to a new society.\nChoose your language:\n\n\n<b>[ES]</b>\n¡Hola! Soy tu asistente para adaptarme a la nueva sociedad.\nElige tu idioma:\n\n\n<b>[RU]</b>\nПривет! Я — твой помощник, призванный помочь адаптироваться в новом обществе.\nВыбери свой язык:',
			reply_markup=mk.langMenu)
	if callback.data == 'VIP':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/WbDWbTWk/langRU.png',lang),caption = 'Приобретите',
			reply_markup=mk.langMenu)


	if callback.data == 'jar':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_message(callback.from_user.id,ll('<b>Жаргонизмы</b>\n\n1. Мыло — электронная почта\nБаранка, бублик — руль\n2. Дирик — директор\n3. Фраер — напоказ модно одетый человек, наивный человек\n3. Кент — приятель, товарищ\n4. Мани, кеш, бабки — деньги\n5. Тачка — машина\n6. Пиар — способы продвижения и получения популярности в обществе\n7. Хайп — кратковременная популярность',lang),
			reply_markup=mk.BdivMenu(lang))
	if callback.data == 'krl':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_message(callback.from_user.id,ll('<b>Крылатые выражения</b>\n\n1. "Ни пуха, ни пера" - выражение, пожелание удачи.\n2. "Хоть кол на голове теши" - про очень упрямого человека.\n3. "Как с гуся вода" - о чем-то очень легком.\n4. "Умом Россию не понять" - о том, что Россия загадочная и сложная страна.\n5. "Пошел в ноль" - описывает событие, которое не оправдало ожиданий.\n6. "Не бояться волка, а бояться бабушку" - о неожиданном источнике проблем или опасности.\n7. "Бить баклуши" - означает надуться, делать вид, что чего-то не знаешь.\n8. "Дуракам закон не писан" - о том, что глупые люди могут делать что угодно.\n9. "Муха медовая" - о том, что что-то приятное и легкое.\n10. "Не пойми не примите" - выражение раздражения или удивления.\n11. "Ботинки на выброс" (значит, выгнать кого-то из партии или коллектива)\n12. "Стеклянные души" (люди, чувства которых очень хрупки)\n13. "Кустарник на печи" (непонятный, заумный разговор)\n14. "Рубаха на вырост" (как временное средство устранения недостатка)\n15. "Разбил животом" (проиграл, потерпел неудачу)\n16. "Дубиной мерить" (устрашать, давить силой)\n17. "Крокодил слёз не проливает" (о бесчувственности, равнодушии)\n18. "Солнце-сковорода" (очень жарко)\n19. "Маски шатки" (ложь, обман)\n20. "Поедет в коляске" (получит по заслугам)',lang),
			reply_markup=mk.BdivMenu(lang))


	if callback.data == 'trn':	
		lang = db.get_lang(callback.from_user.id)
		await bot.send_message(callback.from_user.id,ll('<b>🚗Исходя из общего рейтинга исследования, тремя лучшими приложениями каршеринга признаны:</b>\n1. BelkaCar\n2. "Карусель"\n3. Anytime\n\n<b>🚕Для вызова такси отлично подходят:</b>\n1. ЯндексGo\n2. СитиМобил\n3. Uber',lang),
			reply_markup=mk.BtrnMenu(lang))
	if callback.data == 'otrn':	
		lang = db.get_lang(callback.from_user.id)
		await bot.send_message(callback.from_user.id,ll('<b>Как узнать расписания автобусов?</b>\nРасписание автобусов и прочего общественного транспорта можно узнать в приложениях "Яндекс Карта", "Google Карта" и подобные.\n\nОплата в общественном транспорте производится с помощью бакновских или льготных карт. Существует ряд льгот, позволяющие бесплатно пользоваться транспортом. Транспорт предусмотрен для людей с ограниченными возможностями.\n\n\n<b>Как пополнять проездные карты?</b>\nПополнить проездные карты можно либо в специальных приложениях, либо на местах, где стоят специальные автоматы для пополнения.',lang),
			reply_markup=mk.BtrnMenu(lang))
		

if __name__ == '__main__':
	executor.start_polling(dp,skip_updates=True) 