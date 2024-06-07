import json
import os
from tkinter import *
from tkinter import filedialog, messagebox

from fjudge.main import main

global path


def upload_file():
    global path
    path = filedialog.askopenfilename()
    path_text['text'] = str(path)


def result():
    global path
    if path is None:
        messagebox.showwarning('Ошибка', 'Выберите файл для проверки')
    else:
        res = main(path, int(time.get()), int(size.get()) * (2 ** 20), selected.get())
        if not os.path.isfile('db.json'):
            with open('db.json', 'w') as file:
                data = {'attemps':
                    [{
                        'id': 1,
                        'result': res
                    }]
                }
                json.dump(data, file)
        else:
            with open('db.json', "r") as file:
                data = json.load(file)
                ind = max([x['id'] for x in data['attemps']]) + 1
                data['attemps'].append({
                    'id': ind,
                    'result': res
                })
            with open('db.json', "w") as file:
                json.dump(data, file)
        messagebox.showinfo('Результат', res)


window = Tk()
window.title('Тестирующая система')
window.geometry('900x700')

frame = Frame(window, bg='white')
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

title = Label(frame, text='Проверить решение', font=('Calibri', 30), bg='white')
title.grid(column=0, row=0)

text_time = Label(frame, text='Введите ограничение по времени в секундах', font=('Calibri', 14), bg='white')
text_time.grid(column=0, row=1)

time = Entry(frame, bg='white', font=14)
time.grid(column=1, row=1)

text_size = Label(frame, text='Введите ограничение по памяти в МегаБайтах', font=('Calibri', 14), bg='white')
text_size.grid(column=0, row=2)

size = Entry(frame, bg='white', font=14)
size.grid(column=1, row=2)

file_btn = Button(frame, text='Выберите файл', command=upload_file)
file_btn.grid(column=1, row=3)

path_text = Label(frame, text='Файл не выбран')
path_text.grid(column=0, row=3)

radio_text = Label(frame, text='Выберите как будет осуществляться проверка', font=('Calibri', 14), bg='white')
radio_text.grid(column=1, row=4)
selected = BooleanVar()
rad1 = Radiobutton(frame, text='Файл с ответами', value=False)
rad2 = Radiobutton(frame, text='Скрипт', value=True)
rad1.grid(column=0, row=5)
rad2.grid(column=1, row=5)

res_btn = Button(frame, text='Проверить', fg='blue', command=result)
res_btn.grid(column=1, row=6)

if os.path.isfile('db.json'):
    text_prev = Label(frame, text='Последние 10 попыток', font=('Calibri', 20), bg='white', fg='red')
    text_prev.grid(column=1, row=7)
    text_id = Label(frame, text='ID попытки', font=('Calibri', 18), bg='white')
    text_id.grid(column=0, row=8)
    text_res = Label(frame, text='Результат', font=('Calibri', 18), bg='white')
    text_res.grid(column=1, row=8)
    row = 9
    with open('db.json', 'r') as f:
        show_data = json.load(f)
        attemps = show_data['attemps']
        for i in range(len(attemps) - 1, -1, -1):
            show_id = Label(frame, text=str(attemps[i]['id']))
            show_id.grid(column=0, row=row)
            show_res = Label(frame, text=str(attemps[i]['result']))
            show_res.grid(column=1, row=row)
            row += 1
            if row == 17:
                break

window.mainloop()
