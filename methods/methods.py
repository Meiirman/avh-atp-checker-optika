import atexit
import json
import os
import pathlib
import tkinter as tk
import traceback
from tkinter import filedialog, messagebox

from models.model import AutoClosingWindow


def get_value(parameter):
    try:
        with open("settings/config.json", "r") as f:
            data = json.load(f)
            print(data)
            print(data[parameter])
            return data[parameter]
    except:
        traceback.print_exc()
        return False


def send_message(message, message_type, out_of_queue=False):
    print(message)
    if out_of_queue:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("АТП Генератор", message)
    elif get_value(message_type):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("АТП Генератор", message)
    else:
        pass


def send_closing_notification(message, message_type="show_info", out_of_queue=False):
    print(message)
    timeout_seconds = 2
    if out_of_queue:
        root = tk.Tk()
        app = AutoClosingWindow(root, timeout_seconds, message)
        root.mainloop()
    elif get_value(message_type):
        root = tk.Tk()
        app = AutoClosingWindow(root, timeout_seconds, message)
        root.mainloop()

    else:
        root = tk.Tk()
        timeout_seconds = 5
        app = AutoClosingWindow(root, timeout_seconds, message)
        root.mainloop()


def browse_folder(entry_var: tk.StringVar) -> None:
    folder_selected = filedialog.askdirectory()
    entry_var.set(folder_selected)
    set_work_folder(folder_selected)


def set_work_folder(folder_path: str):
    config_path = "settings/config.json"
    
    try:
        with open(config_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data["folder_path"] = folder_path

    with open(config_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    send_message(
        'Новое местоположение рабочей папки: "' + folder_path + '"', "show_info"
    )


def generate_b2b_excel():
    pass


def generate_b2b_html():
    pass


def change_excel_path(entry_var: tk.StringVar) -> None:
    excel_file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx;*.xls")]
    )
    
    # Получить относительный путь
    relative_path = pathlib.Path(excel_file_path).relative_to(pathlib.Path.cwd()).as_posix()
    # relative_path = os.path.relpath(excel_file_path, start=os.getcwd())

    entry_var.set(relative_path)
    excel_path = relative_path

    config_path = "settings/config.json"

    try:
        with open(config_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data["prices_list_path"] = excel_path

    with open(config_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    send_message('Новое местоположение Excel файла: "' + excel_path + '"', "show_info")
