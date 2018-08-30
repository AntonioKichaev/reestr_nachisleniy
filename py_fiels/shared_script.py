# -*- coding: utf-8 -*-
import os
import csv
import datetime
import fl_spec

create_null_column = [u'Сумма задолженности', u'Вид работ', u'Стоимость ремонт', u'Стоимость псд',u'Начислено по дому',u'Уплачено по дому']


def open_csv_read(file_name):  # чтение всех файлов
    return_array = []
    with open(unicode(file_name), u'rb') as csv_file:
        docreader = csv.reader(csv_file, delimiter=';', quotechar='"', dialect=csv.excel)
        for row in docreader:
            tmp = []
            for col in row:
                try:
                    tmp.append(col.encode('cp1251'))
                except:
                    tmp.append(col.decode('cp1251'))
            return_array.append(tmp)
    csv_file.close()
    return return_array


def csv_write(file_list, pref):
    file_name = pref + "_RFKR_MKD_" + datetime.datetime.today().strftime("%Y%m%d") + ".csv"
    with open(file_name, 'wb') as csv_file:
        file_write = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in file_list:
            new_write = []
            for col in row:
                new_write.append(col.encode("cp1251"))
            file_write.writerow(new_write)
    csv_file.close()


def swap_name_adress(content_list, row_number_swap, find_adress, swap_adress):  # смена адерса по столбцу

    for row in content_list:
        row[row_number_swap] = row[row_number_swap].replace(find_adress, swap_adress)
    return content_list


def create_head(file_list, head_list, content_list):  # разделяю заголовок и контент
    count_first = 0
    for row in file_list:
        if count_first != 0:
            content_list.append(row)
        else:
            head_list.append(row)
            count_first = 1


def delete_nachislenovznosov(content_list, head_list, pref):  # удаляю где начислено взносов 0
    prefix = pref + u'_начислено_взносов_0'
    count_for_col_nachisleno_vznosov = 31
    new_content = []
    new_brak = []
    for row in content_list:
        if float(row[count_for_col_nachisleno_vznosov]) == 0:
            new_brak.append(row)
        else:
            new_content.append(row)
    if new_brak:
        try:
            os.makedirs(pref)
        except OSError:
            pass
        csv_write(head_list + new_brak, prefix)
    return new_content


def delete_null_rs(content_list, head_list, pref):  # отбрасывает данные у которых пустые Расчетный счет
    prefix = pref + u'_РС_пустота'
    count_for_col_rs = 16
    new_content = []
    new_brak = []
    for row in content_list:
        if row[count_for_col_rs].strip():
            new_content.append(row)
        else:
            new_brak.append(row)
    if new_brak:
        try:
            os.makedirs(pref)
        except OSError:
            pass
        csv_write(head_list + new_brak, prefix)
    return new_content


def create_tarif_dop_vznos(content_list):  # смена пустоты на 0 в тарифе доп взноса
    count_for_col_tarif_dop_vznos = 27
    for row in content_list:
        if row[count_for_col_tarif_dop_vznos] == "":
            row[count_for_col_tarif_dop_vznos] = "0"
    return content_list


'''

def swap_severna_24(content_list):
    swap_24_sever = u'Северная 24-я'
    swap_24_sever_dom = u'200'
    swap_24_sever_new = u'200 (200/к.1)'

    number_col_name_street = 6  # улица
    number_col_dom = 7
    for row in content_list:
        if row[number_col_name_street] == swap_24_sever and row[number_col_dom] == swap_24_sever_dom:
            row[number_col_dom] = row[number_col_dom].replace(swap_24_sever_dom, swap_24_sever_new)
    return content_list
'''

def creat_new_col(headers_list, name_col):
    for row in headers_list:
        row.insert(headers_list[0].__len__() + 1, name_col)
    return headers_list


def delete_organization(content_list, delete_organization_list, pref):
    count_for_col_fio_sobstvennika = 23  # номер столбца где собственник 24-1=23
    new_content = []
    tmp = []
    for row in content_list:
        if row[count_for_col_fio_sobstvennika] not in delete_organization_list:
            new_content.append(row)
        else:
            tmp.append(row)
    if tmp:
        try:
            os.makedirs(pref)
        except OSError:
            pass
        csv_write(tmp, pref + u'Удаленные_организации')
    return new_content


def create_new_col_null(header_list, content_list):
    for null_col in create_null_column:
        for row in header_list:
            row.insert(header_list[0].__len__() + 1, null_col)
        for row in content_list:
            row.insert(content_list[0].__len__() + 1, u'')
    main_list=header_list+content_list
    return main_list

def delete_adres_next_month_spec(content_list,pref):
    new_content = []
    tmp = []
    prefix_nas_pt = 3
    nas_punkt = 4
    prefix_ul = 5
    ulica = 6
    nomer_dom = 7
    korpus = 8
    adres = u''
    counte = 0
    counters = 0
    data_delete = fl_spec.open_spec_shet_txt(u'spec_shet_next_month.txt')

    for row in content_list:
        if row[korpus]:
            adres = row[prefix_nas_pt].replace(u".", u"") + u'. ' + row[nas_punkt] + u', ' + row[prefix_ul].replace(u".", u"")  + u'. ' + row[
                ulica] + u', д. ' + \
                    row[nomer_dom] + u', корпус. ' + row[korpus]
        else:
            adres = row[prefix_nas_pt].replace(u".", u"")  + u'. ' + row[nas_punkt] + u', ' + row[prefix_ul].replace(u".", u"")  + u'. ' + row[
                ulica] + u', д. ' + \
                    row[nomer_dom]

        if adres in data_delete:
            tmp.append(row)
        else:
            new_content.append(row)
    csv_write(tmp, pref + u'Дома на удаления')
    return new_content

def open_spec_shet_txt(file_name):
    txt = open(file_name, u'rb')
    tmp = []
    for row in txt:
        if row:
            try:
                tmp.append(str(row.replace('\n', '').replace('\r', '')).decode(u'cp1251'))
            except:
                tmp.append(str(row.replace('\n', '').replace('\r', '')))
    txt.close()
    return tmp


def create_list_spec_shet(file_name, content_list,dir_save):
    count_for_col_rs = 16
    new_content = []
    tmp = []
    date_file_spec_shet = open_spec_shet_txt(u'spec_shet.txt')
    for row in content_list:
        if str(row[count_for_col_rs]) in date_file_spec_shet:
            new_content.append(row)  # есть в нашем списке
        else:
            tmp.append(row)  # нет в нашем списке
    if tmp:
        try:
            os.makedirs(dir_save)
        except OSError:
            pass

        csv_write(tmp, dir_save+u'not_rs')
    return new_content