# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 21:41:10 2022

@author: ScottStation
"""


import qesdk2

qesdk2.login('zys','scott221')
stratlist=(qesdk2.sm_get_clone_strat_list())
print(stratlist)
print(qesdk2.sm_get_clone_strat_position(stratlist))
qesdk2.auth('quantease','$1$$k7yjPQKv8AJuZERDA.eQX.')
df = qesdk2.get_realtime_minute_prices(['AU2212.SFE'])
print(df)
#print(qesdk2.get_price('AG2212.SFE','2022-09-01','2022-09-22'))