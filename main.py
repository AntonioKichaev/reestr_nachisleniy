# -*- coding: utf-8 -*-
__author__ = u"kichaev_antonio@mail.ru"

from py_fiels import shared_script, fl_spec, fl_obshiy, ul_obshiy, ul_spec

file_name_fl_obs = u'Общий_счет_FL.csv'
file_name_fl_spec = u'Спец_счет_FL.csv'
file_name_ul_obs = u'Общий_счет_UL.csv'
file_name_ul_spec = u'Спец_счет_UL.csv'

fl_obshiy.main(file_name_fl_obs)
fl_spec.main(file_name_fl_spec)

ul_obshiy.main(file_name_ul_obs)
ul_spec.main(file_name_ul_spec)
