import menu
import users
import database
import os
import tools

# --- Класс "Администратор"
class tAdminUser(users.tUser):
    # --- Конструктор
    def __init__(self, userName, userPass):
        super().__init__()
        self.name      = userName
        self.password  = userPass
        self.curAction = 0
        self.role = users.roles.admin_role
        self.menuItems = [
                          "Список шоу",
                          "Список дельфинариев",
                          "Список сотрудников дельфинариев",
                          "Список должностей",
                          "Список видов животных",
                          "Список животных",
                          "Список зарегистриованных пользователей",
                          "Личный кабинет",
                          "Выход"
                         ]
        self.menu = menu.tMenu(self.menuItems,1,3,self.curAction)

    # --- Метод выполнения действий пользователя
    def runActions(self):
        while True:
            users.tUser.runActions(self)
            if self.curAction == 0: # Список шоу
                self.viewListShows()
            elif self.curAction == 1: # Список дельфинариев
                self.viewListOrganizations()
            elif self.curAction == 2: # Список сотрудников дельфинариев
                self.viewListEmployee()
            elif self.curAction == 3: # Список должностей
                self.viewListPost()
            elif self.curAction == 4: # Список видов животных
                self.viewListAnimalTypes()
            elif self.curAction == 5: # Список животных
                self.viewListAnimals()
            elif self.curAction == 6: # Список зарегистриованных пользователей
                self.viewListUsers()
            elif self.curAction == 7: # Личный кабинет
                self.persCabinet()
            elif self.curAction == len(self.menuItems)-1: # Выход в главное меню
                break

    # --- Метод показа списка сотрудников дельфинариев
    def viewListEmployee(self):
        tmpDB = database.tDatabase()
        query = ("SELECT P.FIO, P.EMAIL, O.NAME, D.NAME, P.PERSON_ID, E.POST_ID, E.PERSON_ID, E.ORG_ID, D.POST_ID, O.ORG_ID "+ 
                 "FROM POST D, EMPLOYEE E, PERSON P, ORGANIZATION O "+
                 "WHERE P.PERSON_ID=E.PERSON_ID AND E.ORG_ID=O.ORG_ID AND E.POST_ID=D.POST_ID")
        lines = tmpDB.cursor.execute(query).fetchall()
        items = []
        for l in lines:
            items.append(l[0].ljust(20," ") +
                         l[1].ljust(30," ") +
                         l[2].ljust(30," ") +
                         l[3])
        del tmpDB

        os.system("cls")
        tools.printColoredText(3,1,"Список сотрудников дельфинариев  (Выход - Esc)\n"+
                               "----------------------------------------------------\n"+
                               "  ФИО".ljust(22," ")+"E-Mail".ljust(30," ")+"Дельфинарий".ljust(30," ")+"Должность")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- Метод показа списка должностей
    def viewListPost(self):
        tmpDB = database.tDatabase()
        query = "SELECT P.NAME, P.SALARY FROM POST P"
        lines = tmpDB.cursor.execute(query).fetchall()
        items = []
               
        for l in lines:
            items.append(l[0].ljust(20," ") +
                         str(l[1]).ljust(10," "))
        del tmpDB

        os.system("cls")
        tools.printColoredText(3,1,"Список должностей сотрудников  (Выход - Esc)\n"+
                               "------------------------------------------------\n"+
                               "  Должность".ljust(22," ")+"Оклад")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- Метод показа списка видов животных
    def viewListAnimalTypes(self):
        tmpDB = database.tDatabase()
        query = "SELECT A.NAME, A.AREAL FROM ANIMALTYPE A"
        lines = tmpDB.cursor.execute(query).fetchall()
        items = []
               
        for l in lines:
            items.append(l[0].ljust(20," ") +
                         l[1].ljust(20," "))
        del tmpDB

        os.system("cls")
        tools.printColoredText(3,1,"Список видов животных  (Выход - Esc)\n"+
                               "------------------------------------------------\n"+
                               "  Название".ljust(22," ")+"Ареал обитания")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- Метод показа списка животных
    def viewListAnimals(self):
        tmpDB = database.tDatabase()
        query = ("SELECT A.NAME, T.NAME, A.AGE, A.WEIGHT, A.GENDER, O.NAME, A.ORG_ID, A.TYPE_ID, O.ORG_ID, T.TYPE_ID "+
                 "FROM ANIMALS A, ORGANIZATION O, ANIMALTYPE T "+
                 "WHERE A.ORG_ID = O.ORG_ID AND A.TYPE_ID = T.TYPE_ID")
        lines = tmpDB.cursor.execute(query).fetchall()
        items = []
        for l in lines:
            items.append(l[0].ljust(20," ") +
                         l[1].ljust(20," ") +
                         str(l[2]).ljust(8," ") +
                         str(l[3]).ljust(8," ") +
                         l[4].ljust(6," ") +
                         l[5])
        del tmpDB

        os.system("cls")
        tools.printColoredText(3,1,"Список животных  (Выход - Esc)\n"+
                               "----------------------------------------------------\n"+
                               "  Кличка".ljust(22," ")+"Вид".ljust(20," ")+"Возраст".ljust(8," ")+
                               "Вес".ljust(8," ")+"Пол".ljust(6," ") + "Дельфинарий")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- Метод показа списка зарегистриованных пользователей
    def viewListUsers(self):
        tmpDB = database.tDatabase()
        query = ("SELECT U.NICKNAME, U.PASSWORD, P.FIO, P.EMAIL, U.PERSON_ID, P.PERSON_ID "+
                 "FROM USERS U, PERSON P "+
                 "WHERE U.PERSON_ID = P.PERSON_ID")
        lines = tmpDB.cursor.execute(query).fetchall()
        items = []
        for l in lines:
            items.append(l[0].ljust(20," ") +
                         l[1].ljust(20," ") +
                         l[2].ljust(20," ") +
                         l[3]) 
        del tmpDB

        os.system("cls")
        tools.printColoredText(3,1,"Список зарегистриованных пользователей  (Выход - Esc)\n"+
                               "---------------------------------------------------------\n"+
                               "  Логин".ljust(22," ")+"Пароль".ljust(20," ")+"ФИО".ljust(20," ")+"E-Mail".ljust(20," "))
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break
