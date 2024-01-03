import datetime
import os
import tkinter as tk
import traceback
from itertools import cycle
from tkinter import filedialog

import requests
from tkcalendar import DateEntry

from methods.methods import (browse_folder, change_excel_path, get_value,
                             run_check_process,                             
                             send_closing_notification)


def run_project(*args, **kwargs):
    root = tk.Tk()
    root.title("АТП Генератор B2B (Optika)")
    row = 100


    # Показыать или скрывать кнопку
    if get_value("check_atp_order_button_visible"):
        button_generate_excel = tk.Button(
            root,
            text="Сверить АКТ(pdf) с заказом(docx)",
            command=run_check_process,
        )
        
        button_generate_excel.grid(column=0, padx=10, pady=10)


    # # Показыать или скрывать кнопку
    # if get_value("generator_b2b_html_button_visible"):
    #     button_generate_html = tk.Button(
    #         root,
    #         text="Генерировать B2B АТП (с использованием HTML)",
    #         command=generate_b2b_html,
    #     )
    #     button_generate_html.grid(column=0, padx=10, pady=10)


    # # Можно менять путь к папке или к файлу
    # if get_value("files_path_modification_access"):
    #     folder_change_excel_path_var = tk.StringVar(value=get_value("prices_list_path"))
    #     label_folder_change_excel_path = tk.Label(
    #         root,
    #         text="Изменить путь к файлу с ексель:                                                                         ",
    #     )
    #     entry_folder_change_excel_path = tk.Entry(
    #         root, textvariable=folder_change_excel_path_var, state="normal", width=70
    #     )
    #     button_change_excel_path = tk.Button(
    #         root,
    #         text="Выбрать",
    #         command=lambda: change_excel_path(folder_change_excel_path_var),
    #     )

    #     label_folder_change_excel_path.grid(column=0, padx=0, pady=(20, 0))
    #     entry_folder_change_excel_path.grid(row=98, column=0, padx=10, pady=10)
    #     button_change_excel_path.grid(row=98, column=1, padx=10, pady=10)

    # Создание элементов интерфейса в конце
    folder4_var = tk.StringVar(value=get_value("folder_path"))
    label_folder4 = tk.Label(
        root,
        text="Сменить рабочую папку:                                                                                  ",
    )
    entry_folder4 = tk.Entry(root, textvariable=folder4_var, state="normal", width=70)
    button_folder4 = tk.Button(
        root, text="Выбрать", command=lambda: browse_folder(folder4_var)
    )

    label_folder4.grid(column=0, padx=0, pady=(20, 0))
    entry_folder4.grid(row=100, column=0, padx=10, pady=10)
    button_folder4.grid(row=100, column=1, padx=10, pady=10)

    # Запуск цикла событий Tkinter
    root.mainloop()

    pass

    # Запуск цикла событий Tkinter
    root.mainloop()

    pass
