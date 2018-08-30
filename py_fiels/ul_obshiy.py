# -*- coding: utf-8 -*-
import shared_script, fl_spec
import os

delete_organization_list = [u"Департамент городского хозяйства Администрации города Омска",
                            u"Департамент имущественных отношений Администрации города Омска", u'КУ \"ЦУС\"']
pref_save = u'UL'
dir_save_files = u'brak_ul/'
pref = dir_save_files
index_dostavki = u'Индекс доставки'



def main(file_name):
    main_list = []  # состоит из head_llist и content_list
    content_list = []
    head_list = []
    file_list = shared_script.open_csv_read(file_name)
    shared_script.create_head(file_list, head_list, content_list)
    rezult_content = shared_script.delete_organization(content_list,delete_organization_list,pref)
    rezult_content = shared_script.delete_nachislenovznosov(rezult_content, head_list, pref)
    rezult_content = shared_script.create_tarif_dop_vznos(rezult_content)
    rezult_content = create_index_dostavko(rezult_content)
    head_list = shared_script.creat_new_col(head_list, index_dostavki)
    rezult_content = shared_script.delete_adres_next_month_spec(rezult_content,pref)
    #
    main_list = shared_script.create_new_col_null(head_list, rezult_content)
    shared_script.csv_write(main_list, pref_save)





def create_index_dostavko(content_list):
    new_content = []
    count_for_col_adres_dostavki = 46
    for row in content_list:
        index_dostavki = row[count_for_col_adres_dostavki][0:6:1]
        row.insert(count_for_col_adres_dostavki + 1, index_dostavki)
        new_content.append(row)
    return new_content



