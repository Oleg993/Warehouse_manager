from docxtpl import DocxTemplate
import openpyxl
import openpyxl as op
from datetime import date, datetime
import subprocess, os, platform
import xlsxwriter
import pandas as pd
import csv
import os


list_sell = {'article_number': '1',
             'good_name': 'Труба',
             'warehouse_address': 'Улица Пушкина',
             'delivery_address': 'Улица Колотушкина',
             'date': '20.01.2023',
             'measure_unit': 'KG',
             'description': 'Описаниe',
             'amount': '2000',
             'price_sell': '257333'}


def files_sell(list_sell):
    # # создание doxc файла
    doc = DocxTemplate("Documents\\blanksell.docx")
    doc.render(list_sell)
    date = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
    doc_name = f"Documents\\Sale {date}.docx"
    doc.save(doc_name)

    # создание exel файла
    df = pd.DataFrame(data=list_sell, index=[0])
    df = (df.T)
    file_name = f"Documents\\Sale {date}.xlsx"
    df.to_excel(file_name)

    return [os.path.abspath(doc_name), os.path.abspath(file_name)]

# list_add = {'article_number': '1',
#             'good_name': 'Труба',
#             'address_purchase': 'Улица Интересная',
#             'address_add': 'Улица Красивая',
#             'date_buy': '20.01.2023',
#             'date_add': '20.01.2023',
#             'measure_unit': 'KG',
#             'description': 'Описаниe',
#             'amount': '2000',
#             'sum_good': '20',
#             'price': '257333'}


def add_good(list_add):
    # создание doxc файла
    doc = DocxTemplate("blankadd.docx")
    doc.render(list_add)
    doc_name = "добавление" + list_add['good_name'] + ".docx"
    doc.save(doc_name)

    # создание exel файла
    df = pd.DataFrame(data=list_add, index=[0])
    df = (df.T)
    df.to_excel('добавление.xlsx')

    # открытие файла docx
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', doc_name))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(doc_name)
    else:  # linux variants
        subprocess.call(('xdg-open', doc_name))


# add_good(list_add)

# list_travel = {'article_number': '1',
#                'good_name': 'Труба',
#                'address_dep': 'Улица Складская№1',
#                'address_arrival': 'Улица Складская№2',
#                'date_dep': '10.01.2023',
#                'date_arrival': '31.01.2023',
#                'measure_unit': 'KG',
#                'description': 'Описаниe',
#                'amount': '2000',
#                'sum_good': '20'}


def travel_good(list_travel):
    # создание doxc файла
    doc = DocxTemplate("blanktravel.docx")
    doc.render(list_travel)
    doc_name = "перемещение" + list_travel['good_name'] + ".docx"
    doc.save(doc_name)

    # создание exel файла
    df = pd.DataFrame(data=list_travel, index=[0])
    df = (df.T)
    df.to_excel('перемещение.xlsx')

    # открытие файла docx
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', doc_name))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(doc_name)
    else:  # linux variants
        subprocess.call(('xdg-open', doc_name))


# travel_good(list_travel)

# list_description = {'article_number': '1',
#                     'good_name': 'Труба',
#                     'address_description': 'Улица Складская',
#                     'date_description': '10.01.2023',
#                     'measure_unit': 'KG',
#                     'description': 'Описаниe',
#                     'amount': '2000',
#                     'price': '20'}


def description_good(list_description):
    # создание doxc файла
    doc = DocxTemplate("Documents\\blankdescription.docx")
    doc.render(list_description)
    doc_name = f"Documents\\Списание {list_description['good_name']} {date.today()}.docx"
    doc.save(doc_name)

    # создание exel файла
    df = pd.DataFrame(data=list_description, index=[0])
    df = (df.T)
    excel_name = f"Documents\\Списание {list_description['good_name']} {date.today()}.xlsx"
    df.to_excel(excel_name)

    # открытие файла docx
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', doc_name))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(os.getcwd() + "\\" + doc_name)
    else:  # linux variants
        subprocess.call(('xdg-open', doc_name))


# description_good(list_description)
