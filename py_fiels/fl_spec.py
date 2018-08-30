# -*- coding: utf-8 -*-
import shared_script
import os

pref_save = u'FL_spec'
dir_save_files = u'brak_fl_spec/'
pref = dir_save_files

number_swap_col_full_adress = 0




def main(file_name):


    file_list = shared_script.open_csv_read(file_name)
    main_list = []  # состоит из head_llist и content_list
    content_list = []
    head_list = []
    shared_script.create_head(file_list, head_list, content_list)
    # '''
    rezult_content = shared_script.delete_nachislenovznosov(content_list, head_list, pref)
    rezult_content = shared_script.delete_null_rs(rezult_content, head_list, pref)
    rezult_content = shared_script.create_tarif_dop_vznos(rezult_content)
    rezult_content = shared_script.create_list_spec_shet(u'spec_shet.txt', rezult_content,dir_save_files)
    rezult_content = delete_3_4_spec_shet(rezult_content,pref)  # '''
    rezult_content_rs = create_list_rs_in_content(rezult_content)
    dont_rs(rezult_content_rs)
    main_list = shared_script.create_new_col_null(head_list, rezult_content)
    shared_script.csv_write(main_list, pref_save)





def write_spec_shet_txt(file_list, file_name):
    txt = open(file_name, u'w')
    for row in file_list:
        txt.writelines(row + '\n')
    txt.close()


def create_list_spec_shet(file_name, content_list):
    count_for_col_rs = 16
    new_content = []
    tmp = []
    date_file_spec_shet = shared_script.open_spec_shet_txt(u'spec_shet.txt')
    for row in content_list:
        if str(row[count_for_col_rs]) in date_file_spec_shet:
            new_content.append(row)  # есть в нашем списке
        else:
            tmp.append(row)  # нет в нашем списке
    if tmp:
        try:
            os.makedirs(dir_save_files)
        except OSError:
            pass

        shared_script.csv_write(tmp, dir_save_files+u'not_rs')
    return new_content


def delete_3_4_spec_shet(content_list,pref):
    new_content = []
    tmp = []
    find_and_not_delete_truda_29 = u"Омск, Труда, 29"
    count_for_col_ls = 21
    for row in content_list:
        if str(row[count_for_col_ls][0]) == u'5':
            if float(row[count_for_col_ls]) < 5008009:
                tmp.append(row)
            else:
                new_content.append(row)
        elif row[4] + u", " + row[6] + u", " + row[7] == find_and_not_delete_truda_29 and not row[8]:
            new_content.append(row)
        else:
            tmp.append(row)
    if tmp:
        shared_script.csv_write(tmp, pref+u'3_4')
    return new_content


def create_list_rs_in_content(
        content_list):  # формирует лист уникальных значений в оригинальном файле квитанций из гросса
    count_for_col_rs = 16
    tmp = []
    for row in content_list:
        if row[count_for_col_rs] not in tmp:
            tmp.append(str(row[count_for_col_rs]))
    return tmp


def dont_rs(content_list_rs):
    date_file_spec_shet = shared_script.open_spec_shet_txt(u'spec_shet.txt')
    tmp = []
    for row in date_file_spec_shet:
        if str(row) not in content_list_rs:
            tmp.append(str(row))
    if tmp:
        write_spec_shet_txt(tmp, dir_save_files+u'Не найденные РС_FL_spec.txt')
