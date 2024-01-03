# import io
# import os
# import tempfile
# import camelot
# from camelot.core import TableList

# def get_tables_from_pdf(bytes_io: io.BytesIO, line_scale: int) -> TableList | None:
#     fd, path = tempfile.mkstemp(".pdf")
#     with os.fdopen(fd, "wb") as temporary_file:
#         temporary_file.write(bytes_io.read())
#     try:
#         table_list = camelot.read_pdf(
#             path,
#             pages="all",
#             split_text=True,
#             line_scale=line_scale,
#             strip_text="\n",
#         )
#     except IndexError:
#         return None
#     os.remove(path)
#     return table_list


# def get_tables_as_html_from_pdf(bytes_io: io.BytesIO, **kwargs) -> list[str] | None:
#     table_list = get_tables_from_pdf(bytes_io, **kwargs)
#     if table_list is None:
#         return None
#     tables = []
#     for table in table_list:
#         tables.append(
#             table.df.to_html(
#                 header=False, index=False, classes="table table-bordered", border=1
#             )
#         )
#     return tables


# def file_to_bytes_io(pdf_file_path):
#     with open(pdf_file_path, "rb") as file:
#         pdf_bytes_io = io.BytesIO(file.read())
#     return pdf_bytes_io


# def parse_pdf(pdf_file):
#     tables: list[str] | None = get_tables_as_html_from_pdf(
#         file_to_bytes_io(pdf_file), line_scale="54"
#     )
#     print(tables)

# pdf_file_path = r"C:\Users\22186\Desktop\РабПапка\АТП г.Алматы, ул.Тулебаева, дом 125. Сектор А-24.pdf"
# parsed_tables = parse_pdf(pdf_file_path)


import io
import os
import tempfile
from pathlib import Path

import camelot
import pdfplumber
from camelot.core import TableList


def get_tables_from_pdf_camelot(
    bytes_io: io.BytesIO, line_scale: int
) -> TableList | None:
    fd, path = tempfile.mkstemp(".pdf")
    with os.fdopen(fd, "wb") as temporary_file:
        temporary_file.write(bytes_io.read())
    try:
        table_list = camelot.read_pdf(
            path,
            pages="all",
            split_text=True,
            line_scale=line_scale,
            strip_text="\n",
            ghostscript_path=gs_path
        )
    except IndexError:
        return None
    os.remove(path)
    return table_list


def get_tables_from_pdf_pdfplumber(bytes_io: io.BytesIO) -> list | None:
    with pdfplumber.open(bytes_io) as pdf:
        tables = []
        for page in pdf.pages:
            table = page.extract_tables()[0]
            tables.append(table.df)
    return tables


def parse_pdf_camelot(pdf_file):
    tables: TableList | None = get_tables_from_pdf_camelot(
        file_to_bytes_io(pdf_file), line_scale=54
    )
    if tables is not None:
        for i, table in enumerate(tables):
            print(f"Table {i + 1}:")
            print(table.df)
            print()


def parse_pdf_pdfplumber(pdf_file):
    tables = get_tables_from_pdf_pdfplumber(file_to_bytes_io(pdf_file))
    for i, table in enumerate(tables):
        print(f"Table {i + 1}:")
        print(table)
        print()


def file_to_bytes_io(pdf_file_path):
    with open(pdf_file_path, "rb") as file:
        pdf_bytes_io = io.BytesIO(file.read())
    return pdf_bytes_io


def parse_pdf(pdf_file):
    pdf_file_path = pdf_file
    parse_pdf_camelot(pdf_file_path)
    parse_pdf_pdfplumber(pdf_file_path)


gs_path=r"C:\Users\22186\Desktop\WORK_FOLDER\1. DEV\avh-atp-checker-optika\static\gs10.02.1\bin\gswin32.exe"
os.environ["PATH"] += os.pathsep + gs_path
pdf_file_path = r"C:\Users\22186\Desktop\РабПапка\АТП г.Алматы, ул.Тулебаева, дом 125. Сектор А-24.pdf"
parsed_tables = parse_pdf(pdf_file_path)