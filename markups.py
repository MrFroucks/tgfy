from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot,Dispatcher,executor,types
from localisations import ll


langMenu = InlineKeyboardMarkup(row_width=3)
langEN = InlineKeyboardButton(text='English',callback_data='lang_en')
langES = InlineKeyboardButton(text='Español',callback_data='lang_es')
langRU = InlineKeyboardButton(text='Русский',callback_data='lang_ru')
langMenu.add(langEN,langES,langRU)


def blocksMenu(lang):
	blocksMenu = InlineKeyboardMarkup(row_width=2)
	block1 = InlineKeyboardButton(text=ll('🍾Культура и тенденции',lang),callback_data='cultura')
	block2 = InlineKeyboardButton(text=ll('👾Навигация',lang),callback_data='nav')
	block3 = InlineKeyboardButton(text=ll('🦻Словарь',lang),callback_data='dic')
	block4 = InlineKeyboardButton(text=ll('👀Общество',lang),callback_data='obs')
	block5 = InlineKeyboardButton(text=ll('⭐️Повседневная жизнь',lang),callback_data='dlf')
	block6 = InlineKeyboardButton(text=ll('ПОМЕНЯТЬ ЯЗЫК',lang),callback_data='LNG')
	blocksMenu.add(block1,block2,block3,block4,block5,block6)
	return blocksMenu

def backBlocks(lang):
	backBlocksMenu = ReplyKeyboardMarkup(resize_keyboard=True)
	backBlocksBtn = KeyboardButton(ll('Блоки',lang))
	backBlocksMenu.add(backBlocksBtn)
	return backBlocksMenu