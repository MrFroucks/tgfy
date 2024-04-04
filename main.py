import logging 
import markups as mk
from localisations import ll
from aiogram import Bot,Dispatcher,executor,types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from db import Database




logging.basicConfig(level=logging.INFO)
bot = Bot(token='7023063772:AAFFbn8O4wnmyTaCDQnoDimkSC5KDLMeuw4',parse_mode="HTML")      # parse_mode="HTML"
dp = Dispatcher(bot)
db = Database('database.db')



@dp.message_handler(commands=['start','help','blocks'])
async def start(message: types.Message):
	if not db.user_exists(message.from_user.id):
		await bot.send_photo(chat_id = message.from_user.id,photo = "https://i.postimg.cc/dtBtL0P1/welcome.png",caption = '<b>[EN]</b>\nHi! I am your assistant, designed to help you adapt to a new society.\nChoose your language:\n\n\n<b>[ES]</b>\n¡Hola! Soy tu asistente para adaptarme a la nueva sociedad.\nElige tu idioma:\n\n\n<b>[RU]</b>\nПривет! Я — твой помощник, призванный помочь адаптироваться в новом обществе.\nВыбери свой язык:',
			reply_markup=mk.langMenu)
	else:
		lang = db.get_lang(message.from_user.id)
		await bot.send_photo(chat_id = message.from_user.id,photo = ll('https://i.postimg.cc/WzTrk6jK/blocksRU.png',lang) ,caption = ll('<b>Отлично! Теперь вам доступно несколько блоков для изучения.</b> (Вы всегда сможете вернуться к этому сообщению, используя команду /blocks. Что бы поменять язык, используйте /lang):\n\n\n🍾<b>Культура и тенденции.</b>\nУзнайте, что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.\n\n👾<b>Навигация.</b>\nУзнайте про опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.\n\n👀<b>Общество.</b>\nНормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.\n\n🦻<b>Словарь.</b>\nЖаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.\n\n<b>⭐️Повседневная жизнь.</b>\nПопулярные сервисы и магазины.',
			lang),reply_markup=mk.blocksMenu(lang))




@dp.message_handler(commands=['lang'])
async def start(message: types.Message):
	await bot.delete_message(message.from_user.id,message.message_id)
	await bot.send_photo(chat_id = message.from_user.id,photo = ll('https://i.postimg.cc/WbDWbTWk/langRU.png',lang),caption = '<b>[EN]</b>\nHi! I am your assistant, designed to help you adapt to a new society.\nChoose your language:\n\n\n<b>[ES]</b>\n¡Hola! Soy tu asistente para adaptarme a la nueva sociedad.\nElige tu idioma:\n\n\n<b>[RU]</b>\nПривет! Я — твой помощник, призванный помочь адаптироваться в новом обществе.\nВыбери свой язык:',
		reply_markup=mk.langMenu)



@dp.message_handler()
async def mess(message: types.Message):
	lang = db.get_lang(message.from_user.id)
	if message.text == ll('Блоки',lang):
		await bot.send_photo(chat_id = message.from_user.id,photo = ll('https://i.postimg.cc/WzTrk6jK/blocksRU.png',lang) ,caption = ll('<b>Отлично! Теперь вам доступно несколько блоков для изучения.</b> (Вы всегда сможете вернуться к этому сообщению, используя команду /blocks. Что бы поменять язык, используйте /lang):\n\n\n🍾<b>Культура и тенденции.</b>\nУзнайте, что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.\n\n👾<b>Навигация.</b>\nУзнайте про опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.\n\n👀<b>Общество.</b>\nНормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.\n\n🦻<b>Словарь.</b>\nЖаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.\n\n<b>⭐️Повседневная жизнь.</b>\nПопулярные сервисы и магазины.',
			lang),reply_markup=mk.blocksMenu(lang))



@dp.callback_query_handler()
# @dp.callback_query_handler(text_contains = 'lang_') 
async def set_lang(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id,callback.message.message_id)
	if callback.data.count('lang_') == 1:
		if not db.user_exists(callback.from_user.id):
			lang = callback.data[5:]
			db.add_user(callback.from_user.id,lang)
			await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/WzTrk6jK/blocksRU.png',lang) ,caption = ll('<b>Отлично! Теперь вам доступно несколько блоков для изучения.</b> (Вы всегда сможете вернуться к этому сообщению, используя команду /blocks. Что бы поменять язык, используйте /lang):\n\n\n🍾<b>Культура и тенденции.</b>\nУзнайте, что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.\n\n👾<b>Навигация.</b>\nУзнайте про опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.\n\n👀<b>Общество.</b>\nНормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.\n\n🦻<b>Словарь.</b>\nЖаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.\n\n<b>⭐️Повседневная жизнь.</b>\nПопулярные сервисы и магазины.',
				lang),reply_markup=mk.blocksMenu(lang))
		else:
			lang = callback.data[5:]
			db.update_user(callback.from_user.id,lang)
			await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/WzTrk6jK/blocksRU.png',lang) ,caption = ll('<b>Отлично! Теперь вам доступно несколько блоков для изучения.</b> (Вы всегда сможете вернуться к этому сообщению, используя команду /blocks. Что бы поменять язык, используйте /lang):\n\n\n🍾<b>Культура и тенденции.</b>\nУзнайте, что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.\n\n👾<b>Навигация.</b>\nУзнайте про опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.\n\n👀<b>Общество.</b>\nНормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.\n\n🦻<b>Словарь.</b>\nЖаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.\n\n<b>⭐️Повседневная жизнь.</b>\nПопулярные сервисы и магазины.',
				lang),reply_markup=mk.blocksMenu(lang))

	if callback.data == 'cultura':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = 'https://i.postimg.cc/5tx7qv3h/cultura.png',caption = ll('Культура и тенденции: что популярно сейчас: музыка, кино, искусство, развлечения и другие активности: рекомендации мест по категориям.',lang),
			reply_markup=mk.backBlocks(lang))
	if callback.data == 'nav':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = 'https://i.postimg.cc/t49wDLRv/nav.png',caption = ll('Навигация: опасные районы, транспортные особенности (карта метро, система навигации), условия передвижения, приложения по геопозиции.',lang),
			reply_markup=mk.backBlocks(lang))
	if callback.data == 'dic':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = 'https://i.postimg.cc/hvSTNbJn/slovar.png',caption = ll('Словарь: жаргонизмы, профессионализмы, традиционные выражения, шутки, особенности произношения.',lang),
			reply_markup=mk.backBlocks(lang))
	if callback.data == 'obs':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = 'https://i.postimg.cc/Y93wzgTZ/TOP.png',caption = ll('Общество: нормы, этикет, социальные типы, рекомендации по общению с русскими, как правильно выйти из конфликта.',lang),
			reply_markup=mk.backBlocks(lang))
	if callback.data == 'dlf':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = 'https://i.postimg.cc/QNTzDc63/image.png',caption = ll('Повседневная жизнь: современные продуктовые тенденции, торговые центры/интернет-магазины, финансовая составляющая покупок.',lang),
			reply_markup=mk.backBlocks(lang))
	if callback.data == 'LNG':
		lang = db.get_lang(callback.from_user.id)
		await bot.send_photo(chat_id = callback.from_user.id,photo = ll('https://i.postimg.cc/WbDWbTWk/langRU.png',lang),caption = '<b>[EN]</b>\nHi! I am your assistant, designed to help you adapt to a new society.\nChoose your language:\n\n\n<b>[ES]</b>\n¡Hola! Soy tu asistente para adaptarme a la nueva sociedad.\nElige tu idioma:\n\n\n<b>[RU]</b>\nПривет! Я — твой помощник, призванный помочь адаптироваться в новом обществе.\nВыбери свой язык:',
			reply_markup=mk.langMenu)





if __name__ == '__main__':
	executor.start_polling(dp,skip_updates=True)
