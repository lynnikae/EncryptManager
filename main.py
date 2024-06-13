import tkinter
import tkinter.messagebox as mb
from tkinter import ttk
import sqlite3, qrcode, cv2

from welcome import *


# Создаем универсальные переменные для шрифтов
headlabelfont = ("Arial", 16)
labelfont = ('Arial', 10)
labelbold = ('Arial', 10, 'bold')
entryfont = ('Arial', 12)

# Подключаемся к БД, где будет храниться вся информация
connector = sqlite3.connect('PasswordEncrMngr.db')
cursor = connector.cursor()

connector.execute(
"CREATE TABLE IF NOT EXISTS PASSWORD_MANAGER (PASSW_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, LOGIN TEXT, PASSWORD TEXT, DESKRYPT TEXT, TAG TEXT)"
)

# Создаем функции
def reset_fields(): #сброс значений текстовых полей
    global name_strvar, login_strvar, password_strvar, deskrypt_strvar, tag_strvar

    for i in ['name_strvar', 'login_strvar', 'password_strvar', 'deskrypt_strvar', 'tag_strvar']:
        exec(f"{i}.set('')")


def display_records(): #отображение значений в таблице
    tree.delete(*tree.get_children())

    curr = connector.execute('SELECT * FROM PASSWORD_MANAGER')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)


def add_record(): #создание новой записи
    global name_strvar, login_strvar, password_strvar, deskrypt_strvar, tag_strvar

    name = name_strvar.get()
    login = login_strvar.get()
    password = fer.encrypt(password_strvar.get().encode()).decode()
    deskrypt = deskrypt_strvar.get()
    tag = tag_strvar.get()

    if not login or not password:
        mb.showerror('Ошибка!', "Введите данные в обязательные поля: Логин, пароль")
    else:
        try:
            connector.execute(
            'INSERT INTO PASSWORD_MANAGER (NAME, LOGIN, PASSWORD, DESKRYPT, TAG) VALUES (?,?,?,?,?)', (name, login, password, deskrypt, tag)
            )
            connector.commit()
            mb.showinfo('Учетные данные сохранены', f"Учетные данные {name} успешно добавлены")
            reset_fields()
            display_records()
        except:
            mb.showerror('Ошибка: неверный ввод', 'Проверьте корректность обязательных полей')


def remove_record(): #удаление записи
    if not tree.selection():
        mb.showerror('Ошибка!', 'Выберите учетные данные из таблицы')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        tree.delete(current_item)

        connector.execute('DELETE FROM PASSWORD_MANAGER WHERE PASSW_ID=%d' % selection[0])
        connector.commit()

        mb.showinfo('Выполнено', 'Выбранные учетные данные удалены')

        display_records()


def view_record(): #отображение активной записи в текстовых полях
    global name_strvar, login_strvar, password_strvar, deskrypt_strvar, tag_strvar

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]
    selection[3] = fer.decrypt(selection[3].encode()).decode()

    name_strvar.set(selection[1]); login_strvar.set(selection[2])
    password_strvar.set(selection[3]); deskrypt_strvar.set(selection[4])
    tag_strvar.set(selection[5])


def QR_record(): # экспорт данных в qr код
    qrc = tkinter.Toplevel(main)
    qrc.title("Экспорт пароля в qr-код")
    qrc.geometry("500x460+100+200")
    qrc.config(bg="#fff")
    qrc.resizable(False, False)

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]
    try:
        selection[3] = fer.decrypt(selection[3].encode()).decode() #[1, 'Telegram', 'lynnikae', '05062006', 'мой', 'Мессенджер']
    except:
        qrc.destroy()
        messagebox.showinfo("Невозможно создать QR код", "Выберите учетные данные для экспрота на устройство")

    qr = qrcode.QRCode(3, 1, border=3)
    qr.add_data("Учетные данные для " + selection[1] + '\n' + "Логин: " + selection[2] + '\n' + "Пароль: " + selection[3])
    qr.make(fit=True)
    imgg = qr.make_image(fill_color="black", back_color="white")
    imgg.save('qr.png')

    imga = cv2.imread("qr.png", cv2.IMREAD_UNCHANGED)
    dim = (350, 350)
    resized = cv2.resize(imga, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("qr.png", resized)
    img = PhotoImage(file="qr.png")
    Label(qrc, image=img, bg='white').place(x=80, y=30)


    heading = Label(qrc, text='Отсканируйте код камерой своего устройства \n '
                                    'чтобы использвать учетные данные', fg='black', bg='white',
                    font=('Times New Roman', 11, 'bold'))
    heading.place(x=90, y=10)

    Button(qrc, width=15, pady=3, text='ОК',
           bg='#57a1f8', fg='white', border=0, command=qrc.destroy).place(x=205, y=390)

    qrc.mainloop()
    os.remove("qr.png")

def show_password(): #чекбокс "отобразить пароль"
    if entry.cget('show') == "•":
        entry.config(show='')
    else:
        entry.config(show="•")





# Инициализация графического окна основного интерфейса
if __name__ == "__main__":
    main = Tk()
    main.title('Менеджер паролей')
    main.wm_attributes('-alpha', 0.89)
    main.geometry('900x500')




#Создание переменных цвета фона и переднего плана
lf_bg = 'White' # цвет фона для левого кадра
cf_bg = 'White' # цвет фона для center_frame

# Создание переменных StringVar или IntVar
name_strvar = StringVar()
login_strvar = StringVar()
password_strvar = StringVar()
deskrypt_strvar = StringVar()
tag_strvar = StringVar()
psswrd = ''

# Размещение компонентов в главном окне
Label(main, text="Менеджер паролей", font=('Microsoft YaHei UI Light', 14, 'bold'), bg='white', fg="#57a1f8").pack(side=TOP, fill=X)


left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.3)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.3, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="White")
right_frame.place(relx=0.5, y=30, relheight=0.97, relwidth=0.6)

# Размещение компонентов в левой рамке
Label(left_frame, text="Ресурс (название) учетных данных", font=labelfont, bg=lf_bg).place(relx=0.059, rely=0.05)
Label(left_frame, text="Логин", font=labelfont, bg=lf_bg).place(relx=0.059, rely=0.18)
Label(left_frame, text="Пароль", font=labelfont, bg=lf_bg).place(relx=0.059, rely=0.31)
Label(left_frame, text="Примечание", font=labelfont, bg=lf_bg).place(relx=0.059, rely=0.51)
Label(left_frame, text="Добавить тег", font=labelfont, bg=lf_bg).place(relx=0.059, rely=0.62)


Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont, fg="black", border=0, bg="white").place(x=20, rely=0.1)
Frame(left_frame, width=200, height=2, bg='black').place(x=17, rely=0.148)
Entry(left_frame, width=19, textvariable=login_strvar, font=entryfont, fg='black', border=0, bg='white').place(x=20, rely=0.23)
Frame(left_frame, width=200, height=2, bg='black').place(x=17, rely=0.278)
entry = Entry(left_frame, width=19, show="•", textvariable=password_strvar, font=entryfont, fg='black', border=0, bg='white')
entry.place(x=20, rely=0.36)
Frame(left_frame, width=200, height=2, bg='black').place(x=17, rely=0.408)
Checkbutton(left_frame, text="Показать пароль", font=labelfont, bg="White", command=show_password).place(x=20, rely=0.42)
Entry(left_frame, width=19, textvariable=deskrypt_strvar, font=entryfont, fg='black', border=0, bg='white').place(x=20, rely=0.56)
Frame(left_frame, width=200, height=2, bg='black').place(x=17, rely=0.608)
OptionMenu(left_frame, tag_strvar, 'Личный', "Рабочий", "Корпоративный", "Социальная сеть", "Мессенджер", "Сайт").place(x=20, rely=0.67, relwidth=0.6)


Button(left_frame, text='Сохранить', overrelief="ridge", font=labelbold, border=0, background='#57a1f8', command=add_record, width=14).place(relx=0.079, rely=0.80)


# Размещение компонентов в центральной рамке
Button(center_frame, text='Удалить данные', overrelief="ridge", font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='Показать данные', overrelief="ridge", font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Очистить поля', overrelief="ridge", font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='На смартфон', overrelief="ridge", font=labelbold, command=QR_record, width=15).place(relx=0.1, rely=0.65)


# Размещение компонентов в правой рамке
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=("ID пароля", "Ресурс", "Логин", "Пароль", "Примечание", "Тег"))


X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)


tree.heading('ID пароля', text='ID', anchor=CENTER)
tree.heading('Ресурс', text='Ресурс', anchor=CENTER)
tree.heading('Логин', text='Логин', anchor=CENTER)
tree.heading('Пароль', text='Пароль', anchor=CENTER)
tree.heading('Примечание', text='Примечание', anchor=CENTER)
tree.heading('Тег', text='Тег', anchor=CENTER)


tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=30, stretch=NO)
tree.column('#2', width=100, stretch=NO)
tree.column('#3', width=100, stretch=NO)
tree.column('#4', width=0, stretch=NO)
tree.column('#5', width=100, stretch=NO)
tree.column('#6', width=100, stretch=NO)


tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Завершение работы с окном графического интерфейса
if Flag == True:
    main.update()
    main.mainloop()