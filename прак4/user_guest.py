import menu
import users

# --- Класс "Гость"
class tGuestUser(users.tUser):
    # --- Конструктор
    def __init__(self):
        super().__init__()
        self.name = "Гость"
        self.role = users.roles.guest_role
        self.curAction = 0
        self.menuItems = [
                          "Просмотр списка шоу",
                          "Просмотр списка дельфинариев",
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
            elif self.curAction == len(self.menuItems)-1: # Выход в главное меню
                break