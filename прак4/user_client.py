import menu
import users

# --- ����� "�������������� ������������"
class tAuthorizedUser(users.tUser):
    # --- �����������
    def __init__(self, userName, userPass):
        super().__init__()
        self.name      = userName
        self.password  = userPass
        self.curAction = 0
        self.role = users.roles.user_role
        self.menuItems = [
                          "�������� ������ ���",
                          "�������� ������ ������������",
                          "������ �������",
                          "������� ���� �������",
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
            elif self.curAction == 2: # ������ �������
                self.persCabinet()
            elif self.curAction == 3: # ������� ���� �������
                self.killUser(self.name)
                break
            elif self.curAction == len(self.menuItems)-1: # ����� � ������� ����
                break