import enum
import tools
import database
import menu
import os

class roles(enum.Enum):
    admin_role = 1
    user_role  = 2
    guest_role = 3
    wrong_role = -1

# --- Класс "Пользователь"
class tUser(object):
    # --- Конструктор
    def __init__(self):
        self.name = ""
        self.password = ""
        self.role = roles.wrong_role
        self.roleName = ""
        self.menuItems = []

    # --- Деструктор
    def __del__(self):
        self.name     = None
        self.role     = None
        self.roleName = None

    # --- Метод авторизации пользователя
    def authorization(self):
        tools.printColoredText(3,10,"Логин  : ")
        tools.printColoredText(3,11,"Пароль : ")
        tools.show_cursor()

        tmpLogin = tools.readLine(13,10,20)
        tmpPass  = tools.readLine(13,11,20,"","*")

        tmpDB = database.tDatabase()
        self.role     = tmpDB.chkPass(tmpLogin, tmpPass)
        self.name     = tmpLogin
        self.password = tmpPass
        del tmpDB

        if self.role != roles.wrong_role:
            tools.printColoredText(3,13,"Данные верны. Доступ разрешен.")
        else:
            tools.printColoredText(3,13,"Неверные данные. Доступ запрещен.")
        tools.printColoredText(3,14,"Нажмите любую клавишу...")
        tools.getch()

        tools.printColoredText(3,10," "*35)
        tools.printColoredText(3,11," "*35)
        tools.printColoredText(3,13," "*35)
        tools.printColoredText(3,14," "*35)

    # --- Метод регистрации пользователя
    def newUser(self):
        tools.printColoredText(3,10,"Логин  : ")
        tools.printColoredText(3,11,"Пароль : ")
        tools.show_cursor()

        tmpLogin = tools.readLine(13,10,20).strip()
        tmpPass  = tools.readLine(13,11,20).strip()

        if len(tmpLogin)==0 or len(tmpPass)==0:
            tools.printColoredText(3,13,"ОШИБКА! Логин и/или пароль не заданы.")
        else:
            tmpDB = database.tDatabase()
            if tmpDB.chkUserExists(tmpLogin) == False:
                tmpDB.addUser(tmpLogin,tmpPass)
                tools.printColoredText(3,13,"Пользователь зарегистрирован.")
            else:
                tools.printColoredText(3,13,"ОШИБКА! Такой пользователь уже существует.")
            del tmpDB

        tools.printColoredText(3,14,"Нажмите любую клавишу...")
        tools.getch()
        tools.printColoredText(3,10," "*50)
        tools.printColoredText(3,11," "*50)
        tools.printColoredText(3,13," "*50)
        tools.printColoredText(3,14," "*50)

    # --- Метод удаления аккаунта зарегистрированного пользователя
    def killUser(self, userName):
        tmpDB = database.tDatabase()
        query = """DELETE FROM USERS WHERE NICKNAME =?"""
        tmpDB.cursor.execute(query, (userName, ))
        tmpDB.conn.commit()
        del tmpDB

    # --- Метод показа списка шоу
    def viewListShows(self):
        tmpDB = database.tDatabase()
        query = """SELECT S.DATE_TIME, O.NAME, O.LOCATION FROM SHOW S, ORGANIZATION O WHERE O.ORG_ID=S.ORG_ID"""
        lines = tmpDB.cursor.execute(query).fetchall()
        items = []
        for l in lines:
            items.append(l[0] + "  " + (l[1] + "").ljust(30," ") + l[2])
        del tmpDB

        os.system("cls")
        tools.printColoredText(3,1,"Список шоу  (Выход - Esc)\n"+
                               "-------------------------------------------\n"+
                               "  Дата".ljust(14," ")+"Дельфинарий".ljust(30," ")+"Адрес")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break


    # --- Метод показа списка дельфинариев
    def viewListOrganizations(self):
        tmpDB = database.tDatabase()
        query = """SELECT * FROM ORGANIZATION"""
        lines = tmpDB.cursor.execute(query).fetchall()
        items = []
        for l in lines:
            items.append(l[1].ljust(30," ") +
                         l[2].ljust(40," ") +
                         l[3].ljust(25," ") +
                         l[4])
        del tmpDB

        os.system("cls")
        tools.printColoredText(3,1,"Список дельфинариев  (Выход - Esc)\n"+
                               "-------------------------------------------\n"+
                               "  Название".ljust(32," ")+"Адрес".ljust(40," ")+"Сайт".ljust(25," ")+"Телефон")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- Метод выбора действий с пользователем
    def runActions(self):
        tmpDB = database.tDatabase()
        self.roleName = tmpDB.getRoleName(self.role)
        del tmpDB

        os.system("cls")
        title = "Возможные действия для "+self.name+" ("+self.roleName+")"
        tools.printColoredText(3,1,title+"\n"+"-"*(len(title)+2))
        self.curAction = self.menu.runMenu()

    def persCabinet(self):
        tmpDB = database.tDatabase()
        query = ("SELECT U.NICKNAME, U.PASSWORD, U.PERSON_ID "+
                 "FROM USERS U "+
                 "WHERE U.NICKNAME=?")
        lines = tmpDB.cursor.execute(query, (self.name, )).fetchall()
        tmpPass = lines[0][1]

        if lines[0][2] != None:
            query = ("SELECT U.NICKNAME, U.PASSWORD, P.FIO, P.EMAIL, U.PERSON_ID, P.PERSON_ID "+
                     "FROM USERS U, PERSON P "+
                     "WHERE U.NICKNAME=? AND U.PERSON_ID=P.PERSON_ID")
            lines = tmpDB.cursor.execute(query, (self.name, )).fetchall()            

            tmpFIO    = lines[0][2]
            tmpEMail  = lines[0][3]
            tmpPersID = lines[0][4]
        else:
            tmpFIO    = ""
            tmpEMail  = ""
            tmpPersID = -1

        del tmpDB

        tools.printColoredText(3,15,"Данные личного кабинета  (Выход - Esc)\n"+
                               "-------------------------------------------")
        key = 0
        while True:
            cabItems = [
                        "Пароль (сейчас - "+tmpPass+") :",
                        "ФИО    (сейчас - "+tmpFIO+") :",
                        "E-Mail (сейчас - "+tmpEMail+") :"
                       ]
            cabMenu = menu.tMenu(cabItems,1,17,key)
            
            key = cabMenu.runMenu()

            if key == 0: # Пароль
                tools.show_cursor()
                tmpPass = tools.readLine(len(cabItems[0])+3,17,20,tmpPass,"")
                tools.hide_cursor()

            elif key == 1:   # ФИО
                tools.show_cursor()
                tmpFIO = tools.readLine(len(cabItems[1])+3,18,20,tmpFIO,"")
                tools.hide_cursor()

            elif key == 2:   # E-Mail
                tools.show_cursor()
                tmpEMail = tools.readLine(len(cabItems[2])+3,19,30,tmpEMail,"")
                tools.hide_cursor()

            elif key == -27: # Escape
                tmpDB = database.tDatabase()

                if tmpPersID != -1:
                    query = "UPDATE PERSON SET FIO=?, EMAIL=? WHERE PERSON_ID=? "
                    params = (tmpFIO, tmpEMail, tmpPersID)
                    tmpDB.cursor.execute(query, params)
                    tmpDB.conn.commit()
                else:
                    query = "INSERT INTO PERSON (FIO, EMAIL) VALUES (?, ?)"
                    params = (tmpFIO, tmpEMail)
                    tmpDB.cursor.execute(query, params)
                    tmpDB.conn.commit()
                    tmpPersID = tmpDB.getMaxPersonID()

                query = "UPDATE USERS SET PASSWORD=?, PERSON_ID=? WHERE NICKNAME=? "
                params = (tmpPass, tmpPersID, self.name)
                tmpDB.cursor.execute(query, params)
                tmpDB.conn.commit()
                break

