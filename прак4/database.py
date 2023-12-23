import sqlite3
import users

class tDatabase(object):
	# --- �����������
	def __init__ (self):
		self.db_name = "dolphins.db"
		self.conn = sqlite3.connect(self.db_name)
		self.cursor = self.conn.cursor()

	# --- ����������
	def __del__(self):
		if self.conn:
			self.conn.close()
	
	# --- ����� �������� ��
	def create_db(self):
		# �������� ������� "���������"
		query = (''' CREATE TABLE IF NOT EXISTS POST
					(
	                POST_ID		INTEGER		PRIMARY KEY AUTOINCREMENT,
					NAME		CHAR(20)	NOT NULL,
					SALARY		INTEGER		NOT NULL
					);
				 ''')
		self.cursor.execute(query)

		# �������� ������� "����"
		query = (''' CREATE TABLE IF NOT EXISTS ROLES
					(
	                ROLE_ID		INTEGER		PRIMARY KEY AUTOINCREMENT,
					NAME		CHAR(20)	NOT NULL
					);
				 ''')
		self.cursor.execute(query)

		# �������� ������� "���� ��������"
		query = (''' CREATE TABLE IF NOT EXISTS ANIMALTYPE
					(
					TYPE_ID		INTEGER		PRIMARY KEY AUTOINCREMENT,
					NAME		CHAR(30)	NOT NULL,
					AREAL		CHAR(30)	NOT NULL
					);
			 	 ''')
		self.cursor.execute(query)

		# �������� ������� "������������"
		query = (''' CREATE TABLE IF NOT EXISTS USERS
					(
					USER_ID		INTEGER		PRIMARY KEY AUTOINCREMENT,
					PERSON_ID	INTEGER		NULL,
					ROLE_ID		INTEGER		NOT NULL,
					NICKNAME	CHAR(30)	NOT NULL,
					PASSWORD	CHAR(30)	NOT NULL,
					FOREIGN KEY(PERSON_ID)	REFERENCES PERSON(PERSON_ID),
					FOREIGN KEY(ROLE_ID)	REFERENCES ROLES(ROLE_ID)
					);
		 		 ''')
		self.cursor.execute(query)

		# �������� ������� "�����������"
		query = (''' CREATE TABLE IF NOT EXISTS ORGANIZATION
					(
					ORG_ID		INTEGER		PRIMARY KEY AUTOINCREMENT,
					NAME		CHAR(30)	NOT NULL,
					LOCATION	CHAR(30)	NOT NULL,
					SITE		CHAR(40)	NULL,
					PHONE		CHAR(16)	NULL
					);
			 	 ''')
		self.cursor.execute(query)

		# �������� ������� "����������"
		query = (''' CREATE TABLE IF NOT EXISTS EMPLOYEE
					(
					EMPLOYEE_ID	INTEGER		PRIMARY KEY AUTOINCREMENT,
					POST_ID		INTEGER		NOT NULL,
					ORG_ID		INTEGER		NOT NULL,
					PERSON_ID	INTEGER		NULL,
					FOREIGN KEY(ORG_ID)		REFERENCES ORGANIZATION(ORG_ID),
					FOREIGN KEY(PERSON_ID)	REFERENCES PERSON(PERSON_ID),
					FOREIGN KEY(POST_ID)	REFERENCES POST(POST_ID)
					);
		 		 ''')
		self.cursor.execute(query)


		# �������� ������� "�������"
		query = (''' CREATE TABLE IF NOT EXISTS PERSON
					(
					PERSON_ID	INTEGER		PRIMARY KEY AUTOINCREMENT,
					FIO			CHAR(30)	NULL,
					EMAIL		CHAR(30)	NULL
					);
		 		 ''')
		self.cursor.execute(query)


		# �������� ������� "��������"
		query = (''' CREATE TABLE IF NOT EXISTS ANIMALS
					(
					ANIMAL_ID	INTEGER			PRIMARY KEY AUTOINCREMENT,
					NAME		CHAR(30)		NOT NULL,
					AGE			INTEGER			NOT NULL,
					WEIGHT		INTEGER			NOT NULL,
					GENDER		CHAR(1)			NOT NULL,
					ORG_ID		INTEGER			NOT NULL,
					TYPE_ID		INTEGER			NOT NULL,
					EMPLOYEE_ID	INTEGER			NOT NULL,
					FOREIGN KEY(ORG_ID)			REFERENCES ORGANIZATION(ORG_ID),
					FOREIGN KEY(TYPE_ID)		REFERENCES ANIMALTYPE(TYPE_ID),
					FOREIGN KEY(EMPLOYEE_ID)	REFERENCES EMPLOYEE(EMPLOYEE_ID)
					);
			 	 ''')
		self.cursor.execute(query)

		# �������� ������� "���"
		query = (''' CREATE TABLE IF NOT EXISTS SHOW
					(
					SHOW_ID		INTEGER		PRIMARY KEY AUTOINCREMENT,
					DATE_TIME	TEXT		NOT NULL,
					ORG_ID		INTEGER		NOT NULL,
					FOREIGN KEY(ORG_ID)		REFERENCES ORGANIZATION(ORG_ID)
					);
			 	 ''')
		self.cursor.execute(query)
	
		# �������� ������� "���-��������"
		query = (''' CREATE TABLE IF NOT EXISTS SHOW_ANIMALS
					(
					SA_ID		INTEGER		PRIMARY KEY AUTOINCREMENT,
					SHOW_ID		INTEGER		NOT NULL,
					ANIMAL_ID	INTEGER		NOT NULL,
					FOREIGN KEY(ANIMAL_ID)	REFERENCES ANIMALS(ANIMAL_ID),
					FOREIGN KEY(SHOW_ID)	REFERENCES SHOW(SHOW_ID)
					);
			 	 ''')
		self.cursor.execute(query)

	# --- ����� ����������� �������� ���� �� �� ID
	def getRoleName(self, roleID):
		query = """SELECT NAME FROM ROLES WHERE ROLE_ID=?"""
		_roleID = roleID.value
		lines = self.cursor.execute(query,(_roleID,)).fetchall()
		res = lines[0][0]
		return res

	# --- ����� ����������� ������������� ID � PERSON
	def getMaxPersonID(self):
		query = "SELECT MAX(PERSON_ID) FROM PERSON"
		lines = self.cursor.execute(query).fetchall()
		res = lines[0][0]
		return res

	# --- ����� �������� ������/������
	def chkPass(self, userName, userPassword):
		query = """SELECT NICKNAME,PASSWORD,ROLE_ID FROM USERS WHERE NICKNAME=?"""
		lines = self.cursor.execute(query,(userName,)).fetchall()
		if len(lines)==0:
			res = users.roles.wrong_role
		elif lines[0][1] == userPassword:
			res = users.roles(lines[0][2])
		else:
			res = users.roles.wrong_role
		return res

	# --- ����� �������� ������������� ������������
	def chkUserExists(self, userName):
		res = False
		query  = """SELECT * FROM USERS WHERE NICKNAME=?"""
		lines = self.cursor.execute(query,(userName,)).fetchall()
		if len(lines)!=0:
			res = True
		return res

	# --- ����� ���������� ������ ������������
	def addUser(self, userName, userPass):
		query  = """INSERT INTO USERS (NICKNAME, PASSWORD, ROLE_ID) VALUES (?, ?, ?)"""
		params = (userName, userPass, users.roles.user_role.value)
		self.cursor.execute(query, params)
		self.conn.commit()	

	# --- ����� ���������� �� ���������� "�� ���������"
	def fillDefaults(self):
		# ���������� ������� "���������" ���������� "�� ���������"
		lines = self.cursor.execute("""SELECT * FROM POST""").fetchall()
		if len(lines) == 0:
			query = ("""INSERT INTO POST (NAME, SALARY) VALUES ('��������', 100000)""")
			self.cursor.execute(query)
			query = ("""INSERT INTO POST (NAME, SALARY) VALUES ('������������', 50000)""")
			self.cursor.execute(query)
			query = ("""INSERT INTO POST (NAME, SALARY) VALUES ('������', 20000)""")
			self.cursor.execute(query)
			query = ("""INSERT INTO POST (NAME, SALARY) VALUES ('��������', 30000)""")
			self.cursor.execute(query)
			self.conn.commit()

		# ���������� ������� "����" ���������� "�� ���������"
		lines = self.cursor.execute("""SELECT * FROM ROLES""").fetchall()
		if len(lines) == 0:
			query = ("""INSERT INTO ROLES (NAME) VALUES ('�������������')""")
			self.cursor.execute(query)
			query = ("""INSERT INTO ROLES (NAME) VALUES ('������������������ ������������')""")
			self.cursor.execute(query)
			query = ("""INSERT INTO ROLES (NAME) VALUES ('�����')""")
			self.cursor.execute(query)
			self.conn.commit()

		# ���������� ������� "���� ��������" ���������� "�� ���������"
		lines = self.cursor.execute("""SELECT * FROM ANIMALTYPE""").fetchall()
		if len(lines) == 0:
			query = ("""INSERT INTO ANIMALTYPE (NAME, AREAL) VALUES ('�������', '����')""")
			self.cursor.execute(query)
			query = ("""INSERT INTO ANIMALTYPE (NAME, AREAL) VALUES ('�������', '�����')""")
			self.cursor.execute(query)
			query = ("""INSERT INTO ANIMALTYPE (NAME, AREAL) VALUES ('������', '����')""")
			self.cursor.execute(query)
			query = ("""INSERT INTO ANIMALTYPE (NAME, AREAL) VALUES ('������� �����', '����')""")
			self.cursor.execute(query)
			self.conn.commit()

		# �������� � ������� "������������" ������������ � ����� "�������������"
		query = """SELECT * FROM USERS WHERE ROLE_ID=1"""
		self.cursor.execute(query).fetchall()
		if len(lines)==0:
			query = ("""INSERT INTO USERS (ROLE_ID, NICKNAME, PASSWORD) VALUES (1, 'admin','admin')""")
			self.cursor.execute(query)
			self.conn.commit()

		# ��������!!! ***********************************************************************************
		# ���������� ���������� "�� ���������"
		lines = self.cursor.execute("""SELECT * FROM ORGANIZATION""").fetchall()
		if len(lines) == 0:
			query = ("""INSERT INTO ORGANIZATION (NAME, LOCATION, SITE, PHONE)
		                VALUES ('�������', '�. ����, ��. �������, �.1' ,'delfin-riviera.ru', '8(862)555-29-20')""")
			self.cursor.execute(query)
			query = ("""INSERT INTO ORGANIZATION (NAME, LOCATION, SITE, PHONE)
		                VALUES ('����', '�. �����, ���������� ��������, �.20�' ,'delfinanapa.ru', '8(86133)9-66-18')""")
			self.cursor.execute(query)
			query = ("""INSERT INTO ORGANIZATION (NAME, LOCATION, SITE, PHONE)
		                VALUES ('����������� �����������', '�. ������, ��. ������� ����������, �.1' ,
						        'yardelfin.ru', '8(4852)62-00-11')""")
			self.cursor.execute(query)
			query = ("""INSERT INTO ORGANIZATION (NAME, LOCATION, SITE, PHONE)
		                VALUES ('����������', '�. ������, �����. ����, 119, ���. 23' ,'moskvarium.ru', '8(499)677-77-77')""")
			self.cursor.execute(query)
			self.conn.commit()

