from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot,Dispatcher,executor,types
from localisations import ll


# -------------------------------------------------------------------------------
# МЕНЮ ЯЗЫКОВ
# -------------------------------------------------------------------------------
langMenu = InlineKeyboardMarkup(row_width=3)
langEN = InlineKeyboardButton(text='English',callback_data='lang_en')
langES = InlineKeyboardButton(text='Español',callback_data='lang_es')
langRU = InlineKeyboardButton(text='Русский',callback_data='lang_ru')
langMenu.add(langEN,langES,langRU)


# -------------------------------------------------------------------------------
# МЕНЮ БЛОКОВ С ПЕРЕВОДОМ
# -------------------------------------------------------------------------------
def blocksMenu(lang):
	blocksMenu = InlineKeyboardMarkup(row_width=4)
	block1 = InlineKeyboardButton(text=ll('🍾Культура и тенденции',lang),callback_data='cultura')
	block2 = InlineKeyboardButton(text=ll('👾Навигация',lang),callback_data='nav')
	block3 = InlineKeyboardButton(text=ll('🦻Словарь',lang),callback_data='dic')
	block4 = InlineKeyboardButton(text=ll('👀Общество',lang),callback_data='obs')
	block5 = InlineKeyboardButton(text=ll('⭐️Повседневная жизнь',lang),callback_data='dlf')
	block6 = InlineKeyboardButton(text=ll('ПОМЕНЯТЬ ЯЗЫК',lang),callback_data='LNG')
	block7 = InlineKeyboardButton(text=ll('ПЛАТНАЯ ПОДПИСКА',lang),callback_data='VIP')
	blocksMenu.add(block2,block3,block5,block4,block6)
	return blocksMenu



# -------------------------------------------------------------------------------
# МЕНЮ СЛОВАРЯ
# -------------------------------------------------------------------------------
def divMenu(lang):
	divMenu = InlineKeyboardMarkup(row_width=2)
	dm1 = InlineKeyboardButton(text=ll('Жаргонизмы',lang),callback_data='jar')
	dm3 = InlineKeyboardButton(text=ll('Крылатые выражения',lang),callback_data='krl')
	divMenu.add(dm1,dm3)
	return divMenu
def BdivMenu(lang):
	BdivMenu = InlineKeyboardMarkup()
	Bdm1 = InlineKeyboardButton(text=ll('🦻Словарь',lang),callback_data='dic')
	BdivMenu.add(Bdm1)
	return BdivMenu

def trnMenu(lang):
	trnMenu = InlineKeyboardMarkup(row_width=2)
	trn1 = InlineKeyboardButton(text=ll('Транспорт',lang),callback_data='trn')
	trn2 = InlineKeyboardButton(text=ll('ChatGPT (soon...)'),callback_data='gpt')
	trn3 = InlineKeyboardButton(text=ll('Общественный транспорт',lang),callback_data='otrn')
	trnMenu.add(trn1,trn3)
	return trnMenu
def BtrnMenu(lang):
	BtrnMenu = InlineKeyboardMarkup()
	Btrn1 = InlineKeyboardButton(text=ll('👾Навигация',lang),callback_data='nav')
	BtrnMenu.add(Btrn1)
	return BtrnMenu

# -------------------------------------------------------------------------------
# КЛАВИАТУРА ОБЩЕСТВО
# -------------------------------------------------------------------------------
def obsMenu(lang):
	obsMenu = ReplyKeyboardMarkup(resize_keyboard=True)
	obs1 = KeyboardButton(ll('Почему посторонний может спросить сигарету или зажигалку?',lang))
	obs2 = KeyboardButton(ll('Почему русские угрюмые?',lang))
	obs3 = KeyboardButton(ll('Кто такой гопник?',lang))
	obs4 = KeyboardButton(ll('Кто такие маргиналы и где их можно встретить?',lang))
	obs5 = KeyboardButton(ll('Почему люди собираются у подъезда?',lang))
	obs6 = KeyboardButton(ll('Кто такие алкаши, пьянь?',lang))
	obs7 = KeyboardButton(ll('На какие части делится Москва?',lang))
	obs8 = KeyboardButton(ll('Как принято говорить между собой у русских, присутствует ли у них жестикуляция, как они обращаются друг к другу?',lang))
	obs9 = KeyboardButton(ll('Как здороваются русские?',lang))
	obs10 = KeyboardButton(ll('Как в России относятся к женщинам?',lang))
	obs11 = KeyboardButton(ll('Как в России относятся к мужчинам?',lang))
	obs12 = KeyboardButton(ll('Как прощаются русские?',lang))
	obs13 = KeyboardButton(ll('Как в России относятся к ЛГБТ?',lang))
	obs14 = KeyboardButton('/blocks')
	obsMenu.add(obs1,obs2,obs3,obs4,obs5,obs6,obs7,obs8,obs9,obs10,obs11,obs12,obs13,obs14)
	return obsMenu

def BobsMenu(lang):
	BobsMenu = InlineKeyboardMarkup()
	Bobs1 = InlineKeyboardButton(text=ll('/blocks',lang),callback_data='blocksBACK')
	BobsMenu.add(Bobs1)
	return BobsMenu




# -------------------------------------------------------------------------------
# КЛАВИАТУРА ДЛЯ ВОЗВРАЩЕНИЯ НАЗАД
# -------------------------------------------------------------------------------
def backBlocks(lang):
	backBlocksMenu = ReplyKeyboardMarkup(resize_keyboard=True)
	backBlocksBtn = KeyboardButton('/blocks')
	backBlocksMenu.add(backBlocksBtn)
	return backBlocksMenu