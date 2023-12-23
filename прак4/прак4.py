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

# --- Функция "Начальный экран"
def intro():
    lines = ['Мини-Информационная система',
             '"Дельфинарий"',
             'версия 0.01',
             '',
             'П50-2-22, Клопова Е.Д.']

    os.system("cls")
    width = shutil.get_terminal_size().columns
    tools.gotoxy(0,10)

    for line in lines:
        print(line.center(width))

    tools.gotoxy(0,25)
    print("Нажмите любую клавишу...".center(width), end='')
    tools.getch()


# --- Главная программа -------------------------------------------
db = database.tDatabase()
db.create_db()
db.fillDefaults()

key = 0
mainMenu = menu.tMenu(["Вход без регистрации (гость)",
                       "Вход с учетными данными",
                       "Регистрация",
                       "Выход"],1,3,key)
intro()

while True:
    os.system("cls")
    tools.printColoredText(3,1,"Вход в систему\n"+
                               "------------------------------")
    key = mainMenu.runMenu()

    curUser = users.tUser()

    if key == 0:    # Вход без авторизации
        curUser = user_guest.tGuestUser()
        curUser.runActions()

    elif key == 1:  # Вход с учетными данными
        curUser.authorization()
        if curUser.role == users.roles.admin_role:
            curUser = user_admin.tAdminUser(curUser.name, curUser.password)
            curUser.runActions()

        elif curUser.role == users.roles.user_role:
            curUser = user_client.tAuthorizedUser(curUser.name, curUser.password)
            curUser.runActions()

    elif key == 2:  # Регистрация нового пользователя
        curUser.newUser()

    elif key == 3:  # Выход из системы
        break
    else:
        tools.sound(300,100)

    del curUser


del mainMenu
del db
tools.printColoredText(0,20,"Программа завершена.\n")
