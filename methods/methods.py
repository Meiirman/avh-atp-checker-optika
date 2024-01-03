import atexit
import json
import os
import pathlib
import tkinter as tk
import traceback
from tkinter import filedialog, messagebox

from models.model import AutoClosingWindow

from . import atp, parser_pdf, parser_docx



def get_value(parameter):
    """Читает settings/config.json и возвращает значение по ключу parameter"""

    try:
        with open("settings/config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # print(data)
            # print(data[parameter])
            return data[parameter]
    except:
        traceback.print_exc()
        return False


def send_message(message, message_type, out_of_queue=False):
    """Показывает сообщение в окне GUI\n
    message - текст сообщения\n
    message_type - тип сообщения (если в settings/config.json есть ключи show_notification, show_errors...)\n
    out_of_queue - если True, то сообщение показывается в окне GUI в любом случае, а если False, то показывает только если в settings/config.json message_type имеет значение True
    """

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
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data["folder_path"] = folder_path

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    send_message(
        'Новое местоположение рабочей папки: "' + folder_path + '"', "show_info"
    )


def change_excel_path(entry_var: tk.StringVar) -> None:
    excel_file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx;*.xls")]
    )

    # Получить относительный путь
    relative_path = (
        pathlib.Path(excel_file_path).relative_to(pathlib.Path.cwd()).as_posix()
    )
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

    send_message(
        'Новое местоположение Excel файла: "' + excel_path + '"',
        "show_info",
        message_type="show_info",
    )


def run_check_process():
    # 1. Получить все нужные ссылки
    # Получить ссылку на PDF
    # Получить ссылку на DOCX

    pdf_file = None
    docx_file = None

    folder_path = get_value("folder_path")

    if folder_path in [None, False]:
        send_message("Не задана рабочая папка", "show_errors")
        return 1

    files = os.listdir(folder_path)
    
    # Поиск в папке pdf-файлов
    pdf_files = [file for file in files if file.lower().endswith(".pdf")]
    if pdf_files:
        for file in pdf_files:
            if "атп" in file.lower():
                pdf_file = folder_path + "/" + file
        if not pdf_file:
            send_message(
                "Программа не нашел pdf файл у которого в названии есть слово 'АТП'",
                "show_warnings",
            )
            return 0
    else:
        send_message("В директории нет файлов PDF", "show_warnings")
        return 0
    

    # Поиск в папке docx-файлов
    docx_files = [file for file in files if file.lower().endswith(".docx")]
    if docx_files:
        for file in docx_files:
            if "заказ" in file.lower():
                docx_file = folder_path + "/" + file
        if not docx_files:
            send_message(
                "Программа не нашел docx файл у которого в названии есть слово 'Заказ'",
                "show_warnings",
            )
            return 0
    else:
        send_message("В директории нет файлов DOCX", "show_warnings")
        return 0
        

    # 2. Спарсить PDF и сохранить в dict
    # Временно закомментил, пока делаю docx
    pdf_data = parser_pdf.parse_pdf(pdf_file)
    send_message(pdf_data["message"], "show_notification")

    if not pdf_data["data"]:
        return 0


    # 3. Спарсить docx и сохранить в dict
    docx_data = parser_docx.parse_docx(docx_file)
    send_message(docx_data["message"], "show_notification")

    if not docx_data["data"]:
        return 0


    pdf_data = dict(pdf_data["data"])
    docx_data = dict(docx_data["data"])
    
    # 4. Сверить и сохранить в list[dict]
    results = []
    for key in pdf_data:
        current_sresult = {
            "Номер ТЦП": key,
            "Кол-во в заказе": None,
            "Кол-во в АТП": pdf_data[key][1],
            "Сумма": None,
            "Комменты": "Нет в Заказе",
        }
        if docx_data.get(key, None) != None:
            current_sresult["Кол-во в заказе"] = docx_data[key][1]
            current_sresult["Сумма"] = docx_data[key][2]
            current_sresult["Комменты"] = ""
        
        if current_sresult["Комменты"] == "":
            if current_sresult["Кол-во в заказе"] != current_sresult["Кол-во в АТП"]:
                current_sresult["Комменты"] = f"""Расхождение в количестве: 
                в АТП: {current_sresult['Кол-во в АТП']}. В заказе: {current_sresult['Кол-во в заказе']}"""
        results.append(current_sresult)
    
    for key in docx_data:
        if pdf_data.get(key, None) == None:
            current_sresult = {
                "Номер ТЦП": key,
                "Кол-во в заказе": docx_data[key][1],
                "Кол-во в АТП": None,
                "Сумма": docx_data[key][2],
                "Комменты": "Нет в АТП",
            }
            results.append(current_sresult)

    # 5. Сгенерировать отчет в как АТП .docx формате

    return 0
