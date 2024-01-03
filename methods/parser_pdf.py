import tabula
import pandas as pd


def get_table_data(tables):
    print(tables[2])
    print("tables[2]")

    # Это кастыль который преобразует датаФрейм в строку и обратно делит его в двумерный массив. 
    # Мне так нужно было сделать потому что он не читал первые элементы фрейма и так легче разделить каждый row по пробелам
    table = [row.split() for row in "\n".join([f'-1 {table}' for table in tables]).split("\n")]

    # Фитрую таблицу так что бы остались олько те в котором есть данные которые мне нужны
    result = [
        (float(row[1]), row[2], float(row[-2])) # [<номер строки>, <номер ТЦП>, <количество>]
        for row in table
        if "NaN" != row[1] # нам не нужно NaN
        if len(row) >= 5  # Предотвращаем IndexError
        if row[1].replace(".", "").isdigit() and row[-2].replace(".", "").isdigit() # Предотвращаем ValueError
    ]

    # Разделяем таблицу на части и получаем первую таблицу 
    row_index = 1
    table_index = -1
    res = []
    for row in result:
        if row[0] == 1:
            res.append([])
            table_index += 1
            row_index = 1
        if row[0] == row_index:
            res[table_index].append(row)
            row_index += 1

    rrr = []
    for i in res[0]:
        rrr.append(( i[1], (i[0], i[2]) ))
    return rrr


def parse_pdf(pdf_file):
    
    pdf_path = pdf_file
    tabula_options = {
        'pandas_options': {'dtype': str}
    }
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, **tabula_options)



    for i, df in enumerate(tables):
        tables[i] = df.astype(str)

    table = get_table_data(tables)

    return {"message": "Успешно получил данные из PDF", "data": table}


