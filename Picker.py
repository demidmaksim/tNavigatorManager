import os

import_file = """from scipy.optimize import minimize, LinearConstraint
from typing import BinaryIO, Dict
from struct import unpack, pack
import datetime as dt
import pandas as pd
import numpy as np
import os

"""

Main_link = os.getcwd() + '\\Eclipse_Binary_Parser'
f1 = Main_link + '\\BaseBinaryWorker\\Components\\Header.py'
f2 = Main_link + '\\BaseBinaryWorker\\Components\\Content.py'
f3 = Main_link + '\\BaseBinaryWorker\\BinaryReader.py'
f4 = Main_link + '\\BaseBinaryWorker\\BinarySavior.py'
f5 = Main_link + '\\Summary\\Components\\SMSPEC\\Components\\Storage.py'
f6 = Main_link + '\\Summary\\Components\\SMSPEC\\Components\\Time.py'
f7 = Main_link + '\\Summary\\Components\\SMSPEC\\SMSPECReader.py'
f8 = Main_link + '\\Summary\\Components\\SMSPEC\\SMSPECSavior.py'
f9 = Main_link + '\\Summary\\Components\\UNSMRY\\UNSMRYReader.py'
f10 = Main_link + '\\Summary\\Components\\UNSMRY\\UNSMRYSavior.py'
f11 = Main_link + '\\Summary\\SUMMARY.py'
f12 = Main_link + '\\Summary\\SUMMARYReader.py'
f13 = Main_link + '\\Summary\\SUMMARYSavior.py'

Main_link = os.getcwd()
f14 = Main_link + '\\BaseFunction\\Readers\\ReadHelperFunctions\\ASCII.py'
f15 = Main_link + '\\BaseFunction\\Readers\\ReadHelperFunctions\\KeyWordSet.py'
f16 = Main_link + '\\BaseFunction\\Readers\\Loader.py'
f17 = Main_link + '\\BaseFunction\\Readers\\MnimonicAPI.py'
f18 = Main_link + '\\BaseFunction\\Optim_model.py'
f19 = Main_link + '\\tNav\\For_Debugging.py'
f19 = Main_link + '\\tNav\\For_tNav.py'
f20 = Main_link + '\\ManagementObject\\AdditionalSchedule\\Bound.py'
f21 = Main_link + '\\ManagementObject\\AdditionalSchedule\\MyLinearConstraint.py'
f22 = Main_link + '\\ManagementObject\\AdditionalSchedule\\Schedule.py'
f23 = Main_link + '\\ManagementObject\\InflowZone.py'
f24 = Main_link + '\\ManagementObject\\Well.py'
f25 = Main_link + '\\ManagementObject\\Field.py'
f26 = Main_link + '\\OptimizationModel\\SimpleModel.py'
f27 = Main_link + '\\ALG.py'


F_list = [f19, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13,
          f14, f15, f16, f17, f18, f20, f21, f22, f23, f24, f25, f26, f27]

Text_list = []
for file in F_list:
    with open(file, 'r') as f:
        text = f.read()
        Text_list.append(text)

print(Text_list)
results = '\n'.join(Text_list)
while 'import' in results:
    ind1 = results.index('import')
    ind2 = results.index('\n', ind1)
    r = [results[:ind1], '\n', results[ind2:]]
    results = '\n'.join(r)
print(1)
while 'from ' in results:
    ind1 = results.index('from ')
    ind2 = results.index('\n', ind1)
    r = [results[:ind1], '\n', results[ind2:]]
    results = '\n'.join(r)
print(2)
while '\n\n\n\n' in results:
    ind1 = results.index('\n\n\n\n')
    r = [results[:ind1], results[ind1+3:]]
    results = '\n'.join(r)
print(3)
results = import_file + results

with open('Results.py', 'w') as file:
    file.write(results)

with open('Results.txt', 'w') as file:
    file.write(results)
