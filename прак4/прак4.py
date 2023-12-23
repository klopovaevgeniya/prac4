import database
import tools
import os
import users
import enum
import menu
import shutil
import user_guest
import user_client
import user_admin

# --- ������� "��������� �����"
def intro():
    lines = ['����-�������������� �������',
             '"�����������"',
             '������ 0.01',
             '',
             '�50-2-22, ������� �.�.']

    os.system("cls")
    width = shutil.get_terminal_size().columns
    tools.gotoxy(0,10)

    for line in lines:
        print(line.center(width))

    tools.gotoxy(0,25)
    print("������� ����� �������...".center(width), end='')
    tools.getch()


# --- ������� ��������� -------------------------------------------
db = database.tDatabase()
db.create_db()
db.fillDefaults()

key = 0
mainMenu = menu.tMenu(["���� ��� ����������� (�����)",
                       "���� � �������� �������",
                       "�����������",
                       "�����"],1,3,key)
intro()

while True:
    os.system("cls")
    tools.printColoredText(3,1,"���� � �������\n"+
                               "------------------------------")
    key = mainMenu.runMenu()

    curUser = users.tUser()

    if key == 0:    # ���� ��� �����������
        curUser = user_guest.tGuestUser()
        curUser.runActions()

    elif key == 1:  # ���� � �������� �������
        curUser.authorization()
        if curUser.role == users.roles.admin_role:
            curUser = user_admin.tAdminUser(curUser.name, curUser.password)
            curUser.runActions()

        elif curUser.role == users.roles.user_role:
            curUser = user_client.tAuthorizedUser(curUser.name, curUser.password)
            curUser.runActions()

    elif key == 2:  # ����������� ������ ������������
        curUser.newUser()

    elif key == 3:  # ����� �� �������
        break
    else:
        tools.sound(300,100)

    del curUser


del mainMenu
del db
tools.printColoredText(0,20,"��������� ���������.\n")
