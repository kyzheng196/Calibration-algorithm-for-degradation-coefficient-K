import pandas as pd

def RMSE_calcu(list1, list2):
    sum = 0

    for i in range(len(list1)):
        sum += (list1[i] - list2[i]) ** 2

    sum /= len(list1)
    sum = sum ** 0.5

    return round(sum, 3)


def MSE_calcu(list1, list2):
    sum = 0

    for i in range(len(list1)):
        sum += (list1[i] - list2[i]) ** 2

    sum /= len(list1)

    return round(sum, 3)


def MAE_calcu(list1, list2):
    sum = 0

    for i in range(len(list1)):
        sum += abs(list1[i] - list2[i])

    sum /= len(list1)

    return round(sum, 3)


fpath1 = r'C:\Users\ASUS\Desktop\科研\项目\前海深隧项目_专业实践\输出数据\误差分析表\模拟-实测值 对比表.xlsx'
sheet = ['COD', 'NH4', 'TN', 'TP']

for i in sheet:
    df = pd.read_excel(fpath1, sheet_name = i, header = 0)
    column_list = list(df.columns)

    RMSE = []
    MSE = []
    MAE = []

    for j in range(1, len(column_list)):
        RMSE.append(RMSE_calcu(df[column_list[0]], df[column_list[j]]))
        MSE.append(MSE_calcu(df[column_list[0]], df[column_list[j]]))
        MAE.append(MAE_calcu(df[column_list[0]], df[column_list[j]]))

    print(i + ' RMSE为： ' + str(RMSE))
    print(i + ' MSE为： ' + str(MSE))
    print(i + ' MAE为： ' + str(MAE))
    print('\n')

    name = [i + str(' model' + str(k)) for k in range(1, len(RMSE) + 1)]
    df = pd.DataFrame(columns=name, data=[RMSE, MSE, MAE])
    df.to_csv(r'C:\Users\ASUS\Desktop\误差分析输出结果.csv')
