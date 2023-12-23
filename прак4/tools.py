import sys
import msvcrt
import winsound
import ctypes

# --- Вспомогательные функции 
# --- Функция установки курсора в заданную позицию
def gotoxy(x,y):
    print ("%c[%d;%df" % (0x1B, y, x), end='')
    

# --- Функция вывода сообщения в заданных координатах и заданным цветом
def printColoredText(lx, ty, text="", fCol="white", bCol="black", stil="regular"):
    gotoxy(lx,ty)

    myColors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    outStr  = "\033[0m"
    outStr += "\033["+("1;" if stil=="light" else "") + str(myColors.index(fCol)+30)+"m";
    outStr += "\033["+str(myColors.index(bCol)+40)+"m";
    print(outStr+text, end="")


# --- Функция ожидания нажатия любой клавиши
def getch():
    sys.stdout.flush()
    chCode = int.from_bytes(msvcrt.getch(), "big")
    if chCode in range(127,176):   #А..Я,а..п
        chCode += 912
    elif chCode in range(224,242): #р..я
        chCode += 864
    res = chr(chCode)
    return res


# --- Функция ввода строки
def readLine(x,y,inpLen=10,oldStr="",passChar=""):
    gotoxy(x,y)
    print(oldStr)
    gotoxy(x+len(oldStr),y)
    res  = oldStr
    while True:
        ch = getch()

        if ord(ch)==27:   # ESC
            res = oldStr
            break

        elif ord(ch)==13: # Enter
            break

        elif (ch.isalnum() or (ch in (" ","-","_",".","@"))) and (len(res)<inpLen):
            res += ch
            gotoxy(x,y)
            if passChar=="":
                print(res, end="")
            else:
                print(passChar*len(res), end="")

        elif (ch == "\x08") and (len(res)>0): # Backspace
            res = res[:-1]
            gotoxy(x,y)
            print(" "*inpLen, end="")
            gotoxy(x,y)
            if passChar=="":
                print(res, end="")
            else:
                print(passChar*len(res), end="")
    return res


# --- Функция воспроизведения звука
def sound(freq, dur):
    winsound.Beep(freq, dur)


# --- Функция вывода сообщения в заданных координатах и заданным цветом
def printColoredText(lx, ty, text="", fCol="white", bCol="black", stil="regular"):
    gotoxy(lx,ty)

    myColors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    outStr  = "\033[0m"
    outStr += "\033["+("1;" if stil=="light" else "") + str(myColors.index(fCol)+30)+"m";
    outStr += "\033["+str(myColors.index(bCol)+40)+"m";
    print(outStr+text, end="")


# --- Класс описания структуры курсора
class _CursorInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),
                ("visible", ctypes.c_byte)]


# --- Функция выключения курсора в консоли
def hide_cursor():
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = False
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))


# --- Функция включения курсора в консоли
def show_cursor():
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = True
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))