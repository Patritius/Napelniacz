import pandas as pd
import datetime

def checkList(list):
    # funkcja sprawdzająca czy wszystkie elementy w podanej liście są takie same
    ele = list[0]
    chk = True
    for i in list:
        if ele != i:
            chk = False
            break;
    return chk

def table_converter(df):
    # funkcja modyfikująca tabelę

    # Usuwanie wierszy bez wartości
    for ind, row in enumerate(df.values):
        lst = [str(j) for j in row[4:]]
        if checkList(lst):
            df.drop(ind, inplace=True)

    # Usuwanie zbędnych kolumn
    df.drop(2, axis=1, inplace=True)
    df.drop(3, axis=1, inplace=True)

    # Wstawianie dodatkowych kolumn
    for ind, column in enumerate(df.columns[:-2]):
        df.insert(3 + 2 * ind, 'col' + str(column), "nan")

    # Reset nazw kolumn
    df.columns = range(df.columns.size)

    # Wstawienie wiersza ze znakami '+' i '-'
    dict_of_signs = {k: v for k, v in zip(df.columns, ["+" if i % 2 == 0 else "-" for i in range(len(df.columns))])}
    line = pd.DataFrame(dict_of_signs, index=[0])
    df = pd.concat([df.iloc[:1], line, df.iloc[1:]]).reset_index(drop=True)

    # Przeniesienie godzin odjazdu do 2 wiersza
    dict_of_signs = {k: v for k, v in zip(df.columns, ["nan" for i in range(len(df.columns))])}
    line = pd.DataFrame(dict_of_signs, index=[1])
    df = pd.concat([df.iloc[:1], line, df.iloc[1:]]).reset_index(drop=True)
    for column in df.columns[2:]:
        for value in df[column]:
            if isinstance(value, datetime.time):
                df[column].values[1] = value
                break

    # Dodanie czasu odjazdu do nowoutworzonej kolumny
    for col in range(len(df.columns)):
        if col % 2 == 0:
            for val in range(len(df[df.columns[col]])):
                if isinstance(df[df.columns[col]].values[val], datetime.time):
                    df[df.columns[col + 1]].values[val] = df[df.columns[col]].values[val]

    # Zamiana pustych komórek na zakreślone 'XX'
    for column in df.columns[2:]:
        for value in range(len(df[column]))[3:]:
            if isinstance(df[column].values[value], str) or isinstance(df[column].values[value], float):
                df[column].values[value] = 'XX'

    # Zamiana komórek z datami na puste komórki
    for column in df.columns[2:]:
        for value in range(len(df[column]))[3:]:
            if isinstance(df[column].values[value], datetime.time):
                df[column].values[value] = ' '

    # Utworzenie wiersza z podsumowaniem
    sum_values = ['' for col in df.columns[2:]]
    summary = ['', 'Podsumowanie'] + sum_values
    df.loc[df.index.stop, :] = summary

    return df