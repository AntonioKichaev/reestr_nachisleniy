# -*- coding: utf-8 -*-
import csv
import os
import shared_script
import fl_spec

#find_adress = u'г. Омск, ул. Северная 24-я, д. 200,'
#swap_adress = u'г. Омск, ул. Северная 24-я, д. 200 (200/к.1),'

pref_save = u'FL'
dir_save_files = u'brak_fl/'
pref = dir_save_files


def main(file_name):
    file_list = shared_script.open_csv_read(file_name)
    number_swap_col_full_adress = 0
    main_list = []  # состоит из head_llist и content_list
    content_list = []
    head_list = []

    shared_script.create_head(file_list, head_list, content_list)

    rezult_content = shared_script.delete_nachislenovznosov(content_list, head_list, pref)

    rezult_content = shared_script.delete_null_rs(rezult_content, head_list, pref)

    rezult_content = shared_script.create_tarif_dop_vznos(rezult_content)

    #rezult_content = shared_script.swap_name_adress(rezult_content, number_swap_col_full_adress, find_adress,
                                                    #swap_adress) #не актуально изменили в гроссе
    rezult_content= shared_script.delete_adres_next_month_spec(rezult_content,pref)
    main_list = shared_script.create_new_col_null(head_list, rezult_content)
    
    shared_script.csv_write(main_list, pref_save)






