import menu
import users

# --- Класс "Авторизованный пользователь"
class tAuthorizedUser(users.tUser):
    # --- Конструктор
    def __init__(self, userName, userPass):
        super().__init__()
        self.name      = userName
        self.password  = userPass
        self.curAction = 0
        self.role = users.roles.user_role
        self.menuItems = [
                          "Просмотр списка шоу",
                          "Просмотр списка дельфинариев",
                          "Личный кабинет",
                          "Удалить свой аккаунт",
                          "Выход"
                         ]
        self.menu = menu.tMenu(self.menuItems,1,3,self.curAction)

    # --- Метод выполнения действий пользователя
    def runActions(self):
        while True:
            users.tUser.runActions(self)
            if self.curAction == 0: # Просмотр списка шоу
                self.viewListShows()
            elif self.curAction == 1: # Просмотр списка дельфинариев
                self.viewListOrganizations()
            elif self.curAction == 2: # Личный кабинет
                self.persCabinet()
            elif self.curAction == 3: # Удалить свой аккаунт
                self.killUser(self.name)
                break
            elif self.curAction == len(self.menuItems)-1: # Выход в главное меню
                break