import pandas as pd
import datetime
import xlsxwriter
import openpyxl

from functions import table_converter

# wczytanie pliku, modyfikacja i zapis do pliku
schedule = pd.read_excel('Tab.xlsx', header=None, engine='openpyxl')
schedule = table_converter(schedule)
schedule.to_excel('Tabela_do_napelnien.xlsx', sheet_name = 'Arkusz1', engine = 'openpyxl')

# utworzenie listy kolumn z excela oraz ich przedziałów np A1:B1
letters = [chr(let+65) for let in range(26)]
exc_cols = [chr(i+65) if ord(chr(i+65)) < 91 else f'{letters[(i-26)//26]}{letters[(i-26)%26]}' for i in range(len(schedule.columns))]
exc_col_slices1 = [f'{exc_cols[i]}1:{exc_cols[i+1]}1' for i in range(len(exc_cols)-1)]
exc_col_slices2 = [f'{exc_cols[i]}2:{exc_cols[i+1]}2' for i in range(len(exc_cols)-1)]

# wgranie tabeli do xlsxwriter
writer = pd.ExcelWriter('Tabela_do_napelnien.xlsx', engine='xlsxwriter')
workbook = writer.book

# ustawienie formatowania
merge_format = workbook.add_format({
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'text_wrap': True})

date_format = workbook.add_format({
    'num_format': 'HH:MM',
    'border': 1,
    'align': 'center',
    'valign': 'vcenter'})

cell_format = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter'})

cell_bgcolor = workbook.add_format({
    'bg_color': '#A6A6A6'})

border_format = workbook.add_format({
    'border': 1})

# zapis tabeli w podanym arkuszu i zainicjowanie z niego zmiennej z tabelą
schedule.to_excel(writer, sheet_name='Arkusz1', startcol=-1, header=False)
worksheet = writer.sheets['Arkusz1']

# scalanie komórek
worksheet.merge_range('A1:B3', "LINIA NR", merge_format)

# scalanie komórek
for c in range(len(schedule.columns))[2::2]:
    worksheet.merge_range(exc_col_slices1[c], schedule.iloc[0, c], merge_format)
    worksheet.merge_range(exc_col_slices2[c], schedule.iloc[1, c], merge_format)
    worksheet.write_datetime(exc_col_slices2[c], schedule.iloc[1, c], date_format)

# dodanie podsumowania
for s in range(len(schedule.columns))[2:]:
    worksheet.write_formula(f'{exc_cols[s]}{(len(schedule.index))}',
                            f'=sum({exc_cols[s]}4:{exc_cols[s]}{(len(schedule.index)) - 1})')

# ustawienie szerokości kolumn
worksheet.set_column(0, 0, 4.5, cell_format)
worksheet.set_column(1, 1, 40)
worksheet.set_column(f'C:{exc_cols[(len(schedule.columns)) - 1]}', 2.5, cell_format)

# ustawienie koloru tła komórek z 'XX'
for column in range(len(schedule.columns))[2:]:
    for value in range(len(schedule[schedule.columns[column]]))[3:]:
        if schedule[column].values[value] == 'XX':
            worksheet.write(value, column, 'XX', cell_bgcolor)

# ustawienie obramowania tabeli
worksheet.conditional_format(f'A1:{exc_cols[s]}{(len(schedule.index))}', {'type': 'no_errors', 'format': border_format})

writer.save()
