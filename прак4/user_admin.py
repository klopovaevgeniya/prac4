import menu
import users
import database
import os
import tools

# --- ����� "�������������"
class tAdminUser(users.tUser):
    # --- �����������
    def __init__(self, userName, userPass):
        super().__init__()
        self.name      = userName
        self.password  = userPass
        self.curAction = 0
        self.role = users.roles.admin_role
        self.menuItems = [
                          "������ ���",
                          "������ ������������",
                          "������ ����������� ������������",
                          "������ ����������",
                          "������ ����� ��������",
                          "������ ��������",
                          "������ ����������������� �������������",
                          "������ �������",
                          "�����"
                         ]
        self.menu = menu.tMenu(self.menuItems,1,3,self.curAction)

    # --- ����� ���������� �������� ������������
    def runActions(self):
        while True:
            users.tUser.runActions(self)
            if self.curAction == 0: # ������ ���
                self.viewListShows()
            elif self.curAction == 1: # ������ ������������
                self.viewListOrganizations()
            elif self.curAction == 2: # ������ ����������� ������������
                self.viewListEmployee()
            elif self.curAction == 3: # ������ ����������
                self.viewListPost()
            elif self.curAction == 4: # ������ ����� ��������
                self.viewListAnimalTypes()
            elif self.curAction == 5: # ������ ��������
                self.viewListAnimals()
            elif self.curAction == 6: # ������ ����������������� �������������
                self.viewListUsers()
            elif self.curAction == 7: # ������ �������
                self.persCabinet()
            elif self.curAction == len(self.menuItems)-1: # ����� � ������� ����
                break

    # --- ����� ������ ������ ����������� ������������
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
        tools.printColoredText(3,1,"������ ����������� ������������  (����� - Esc)\n"+
                               "----------------------------------------------------\n"+
                               "  ���".ljust(22," ")+"E-Mail".ljust(30," ")+"�����������".ljust(30," ")+"���������")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- ����� ������ ������ ����������
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
        tools.printColoredText(3,1,"������ ���������� �����������  (����� - Esc)\n"+
                               "------------------------------------------------\n"+
                               "  ���������".ljust(22," ")+"�����")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- ����� ������ ������ ����� ��������
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
        tools.printColoredText(3,1,"������ ����� ��������  (����� - Esc)\n"+
                               "------------------------------------------------\n"+
                               "  ��������".ljust(22," ")+"����� ��������")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- ����� ������ ������ ��������
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
        tools.printColoredText(3,1,"������ ��������  (����� - Esc)\n"+
                               "----------------------------------------------------\n"+
                               "  ������".ljust(22," ")+"���".ljust(20," ")+"�������".ljust(8," ")+
                               "���".ljust(8," ")+"���".ljust(6," ") + "�����������")
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break

    # --- ����� ������ ������ ����������������� �������������
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
        tools.printColoredText(3,1,"������ ����������������� �������������  (����� - Esc)\n"+
                               "---------------------------------------------------------\n"+
                               "  �����".ljust(22," ")+"������".ljust(20," ")+"���".ljust(20," ")+"E-Mail".ljust(20," "))
        viewShowMenu = menu.tMenu(items,1,4,0)
        while True:
            key = viewShowMenu.runMenu()
            if key == -27: # Escape
                break
