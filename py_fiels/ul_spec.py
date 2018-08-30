# -*- coding: utf-8 -*-
import os
import shared_script, fl_spec

pref_save = u'UL_spec'
dir_save_files = u'brak_ul_spec/'
pref = dir_save_files
delet_organization_list = [u'КУ \"ЦУС\"']


def main(file_name):
    main_list = []  # состоит из head_llist и content_list
    content_list = []
    head_list = []
    file_list = shared_script.open_csv_read(file_name)
    shared_script.create_head(file_list, head_list, content_list)
    rezult_content = shared_script.delete_organization(content_list, delet_organization_list, pref)
    rezult_content = shared_script.delete_nachislenovznosov(rezult_content, head_list, pref)
    rezult_content = shared_script.create_tarif_dop_vznos(rezult_content)
    rezult_content = fl_spec.delete_3_4_spec_shet(rezult_content, pref)
    rezult_content = shared_script.create_list_spec_shet(u'spec_shet.txt', rezult_content, dir_save_files)
    main_list = shared_script.create_new_col_null(head_list, rezult_content)

    shared_script.csv_write(main_list, pref_save)
