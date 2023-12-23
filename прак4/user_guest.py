import menu
import users

# --- ����� "�����"
class tGuestUser(users.tUser):
    # --- �����������
    def __init__(self):
        super().__init__()
        self.name = "�����"
        self.role = users.roles.guest_role
        self.curAction = 0
        self.menuItems = [
                          "�������� ������ ���",
                          "�������� ������ ������������",
                          "�����"
                         ]
        self.menu = menu.tMenu(self.menuItems,1,3,self.curAction)
    
    # --- ����� ���������� �������� ������������
    def runActions(self):
        while True:
            users.tUser.runActions(self)
            if self.curAction == 0: # �������� ������ ���
                self.viewListShows()
            elif self.curAction == 1: # �������� ������ ������������
                self.viewListOrganizations()
            elif self.curAction == len(self.menuItems)-1: # ����� � ������� ����
                break