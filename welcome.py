from tkinter import *
from tkinter import messagebox
import os
from cryptography.fernet import Fernet

# Инициализация графического окна интерфейса авторизации
root = Tk()
root.title('Авторизация')
root.geometry('925x500+300+200')
root.config(bg="#fff")
root.resizable(False, False)
Flag = False


# ---------Функция входа в систему-----------


def signin():
    global Flag, code
    password = code.get()

    with open('stcn.txt', 'r') as f:
        data = f.readline().rstrip()
        f.close()
        anc = fer.decrypt(data.encode()).decode()
        if anc == password:
            Flag = True
            root.destroy()
        else:
            messagebox.showerror("Ошибка", "Введите верный пароль \n"
                                    "При первом входе в систему воспользуйтесь восстановлением пароля")


# ---------Изображение----------


img = PhotoImage(file='images/login.png')
Label(root, image=img, bg='white').place(x=50, y=50)

# ------------Фрейм-------------

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

heading = Label(frame, text='Авторизация', fg='#57a1f8', bg='white',
                font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

info = Label(frame, text="Введите текущий мастер-пароль", fg="Black", bg="white")
info.place(x=25, y=180)


# ------------Функции пароля------------
def on_enter(e):
    code.delete(0, 'end')


def on_leave(e):
    cname = code.get()
    if cname == '':
        code.insert(0, 'Пароль')


def delall():
    res = messagebox.askokcancel(title="Удалить все сохранённые пароли?",
                                 message="Если вы забыли мастер-пароль, или хотите создать новый, то приложение не сможет расшифровать сохранённые пароли. \n \n"
                                         "В этом случае можно только удалить все сохраненные в базе данных пароли и создать новый мастер-пароль. \n \n"
                                         "НАЖМИТЕ 'ОК', ЕСЛИ ХОТИТЕ УДАЛИТЬ ВСЕ ПАРОЛИ")
    if res:
        os.remove("PasswordEncrMngr.db")
        r = open("PasswordEncrMngr.db", "w+")
        r.close()
        messagebox.showinfo("Учетные данные удалены", "Все учетные данные удалены")
        pwdwnd = Tk()
        pwdwnd.title("Создание нового мастер-пароля")
        pwdwnd.config(bg='white', border=0)
        pwdwnd.geometry("400x150")
        pwdwnd.wm_attributes('-alpha')

        # def onpwdentry(evt):
        #     write_key()
        #     scnt = pwdbox.get()
        #     with open('stcn.txt', 'a') as f:
        #         f.write(fer.encrypt(scnt.encode()).decode() + "\n")
        #         f.close()
        #     pwdwnd.destroy()

        def onokclick():
            global key, fer
            write_key()
            key = load_key()
            fer = Fernet(key)
            scnt = pwdbox.get()
            with open('stcn.txt', 'w') as f:
                f.write(fer.encrypt(scnt.encode()).decode())
                f.close()
            pwdwnd.destroy()

        Label(pwdwnd, text='Введите новый мастер-пароль', font=('Microsoft YaHei UI Light', 16, 'bold'),
              bg='white').place(x=40, y=20)
        pwdbox = Entry(pwdwnd, show='*', fg="black", border=0, bg="white", width=30,
                       font=('Microsoft YaHei UI Light', 11))
        pwdbox.place(x=80, y=70)
        Frame(pwdwnd, width=250, height=2, bg='black').place(x=75, y=95)
        Button(pwdwnd, command=onokclick, text='Сохранить новый пароль', border=0, background='#57a1f8', width=22,
               height=1).place(x=130, y=110)
    else:
        pass


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("key.key", 'rb').read()


if not os.path.exists("key.key"):
    write_key()

# ------------Окончание работы с интерфейсом-----------------------

key = load_key()
fer = Fernet(key)


code = Entry(frame, width=30, fg='black', show="•", border=0,
             bg='white', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# ----------------------------------
Button(frame, width=39, pady=7, text='Продолжить',
       bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)

sign_up = Button(frame, width=39, text='Не помню пароль или создать новый', border=0,
                 bg='white', cursor='hand2', fg='#57a1f8', command=delall)
sign_up.place(x=40, y=250)

root.mainloop()
