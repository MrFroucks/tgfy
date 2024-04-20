import sqlite3

class Database(object):
	def __init__(self, db_file):
		# объявление переменных, для работы с базой данных
		self.connection = sqlite3.connect(db_file)
		self.cursor = self.connection.cursor()

		# проверка на наличие пользователя в базе данных
	def user_exists(self,user_id):
		with self.connection:
			result = self.cursor.execute('select * from users where user_id = ?',(user_id,)).fetchall()
			return bool(len(result))

		# добавление пользователя в базу данных
	def add_user(self,user_id,lang):
		with self.connection:
			return self.cursor.execute('insert into users (user_id, lang) values (?,?)',(user_id,lang,))
		# обновление языка пользователя
	def update_user(self,user_id,lang):
		with self.connection:
			return self.cursor.execute('update users set lang == ? where user_id = ?',(lang,user_id,))

		# считывание языка пользователя
	def get_lang(self,user_id):
		with self.connection:
			return self.cursor.execute('select lang from users where user_id = ?',(user_id,)).fetchone()[0]
