import pandas as pd
import numpy as np
import re
import xlwt as xw

#数据提取
maint_path = "F:\检修语料\检修匹配.xls"
dbbase_path = "F:\检修语料\参数库导出.xls"

# #检修数据
# originalDataForm = pd.read_excel(maint_path,parse_cols=[0,1])
# original_dict = dict()
# devList = list()
# for item in originalDataForm.items():
#     templist = list()
#     for i in range(1,len(item)):
#         for j in range(len(item[i])):
#             templist.append(item[i][j])
#     devList.append(templist)
#
# for i in range(len(devList[0])):
#     original_dict[devList[0][i]] = devList[1][i]


# #参数库数据
# dbDataForm = pd.read_excel(dbbase_path,parse_cols=[0,1])
# db_dict = dict()
# devList.clear()
# for item in dbDataForm.items():
#     templist = list()
#     for i in range(1,len(item)):
#         for j in range(len(item[i])):
#             templist.append(item[i][j])
#     devList.append(templist)
#
# for i in range(len(devList[0])):
#     db_dict[devList[0][i]] = devList[1][i]

#句子的拆分和合并
class Split_Merge_Sentence:
    def split_sentence(self, sentence):
        reg = re.compile(r'[ , / : ; 、﹑，.；：]{1}')
        split_word = reg.split(sentence)
        return split_word

    def merge_sentence(self,mergeDict):
        dictKeys =  mergeDict.keys()
        mergeList = list()
        for item in dictKeys:
            mergeList.append(mergeDict[item] + item)

        return mergeList

    def pickDataFromFile(self,path,parse_cols = None):
        originalDataForm = pd.read_excel(path, usecols=parse_cols)
        original_dict = dict()
        devList = list()
        for item in originalDataForm.items():
            templist = list()
            for i in range(1, len(item)):
                for j in range(len(item[i])):
                    templist.append(item[i][j])
            devList.append(templist)

        for i in range(len(devList[0])):
            original_dict[devList[0][i]] = devList[1][i]

        return original_dict


def data_to_excel(dictorlist,path):
    wb = xw.Workbook()
    ws = wb.add_sheet("devs",cell_overwrite_ok=True)
    if isinstance(dictorlist,dict):
        ws.write(0,0,"设备名称")
        ws.write(0,1,"厂站")
        index = 1
        for item in dictorlist.keys():
            ws.write(index,0,item)
            ws.write(index,1,dictorlist[item])
            index = index + 1
    elif isinstance(dictorlist,list):
        ws.write(0,0,"设备名称")
        for i in range(len(dictorlist)):
            ws.write(i,0,dictorlist[i])
    else:
        return False

    wb.save(path)
    return True

#检修获取数据的处理
dataSplit = Split_Merge_Sentence()

original_dict = dataSplit.pickDataFromFile(maint_path,parse_cols=[0,1])
db_dict = dataSplit.pickDataFromFile(dbbase_path,parse_cols=[0,1])

original_split_dict = dict()
for item in original_dict.keys():
    oridevs = dataSplit.split_sentence(item)
    for i in range(len(oridevs)):
        original_split_dict[oridevs[i]] = original_dict[item]

data_to_excel(dictorlist=original_split_dict,path="F:\检修语料\拆分.xls")

#合并检修数据
finalMaintList = list()
for item in original_split_dict.keys():
    if original_split_dict[item] == '线路' or original_split_dict[item] == item:
        finalMaintList.append(item)
    else:
        finalMaintList.append(original_split_dict[item] + item)

data_to_excel(dictorlist=finalMaintList,path="F:\检修语料\合并.xls")
# for item in finalMaintList:
#     print(item)
