import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def year_trend(df, year):
    sub = df[df['Year'] == year]
    sub = sub.sort_values(by='Month')
    #print(sub.head(10))
    res = sns.barplot(x=sub['Month'], y=sub['Data'])
    plt.show()

def total_trend(df):
    df['YearMonth'] = df['Year'] + df['Month']
    df = df.sort_values(by=['YearMonth'])
    #print(df.head(10))
    sns.barplot(x=df['YearMonth'], y = df['Data'], estimator=np.sum)
    plt.xticks(rotation=45)
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pd.set_option('display.width', None)
    df = pd.read_csv('defined_metro.csv', dtype=str)
    types = {"Data":int, "Latitude":float, "Longitude":float}
    for key, typename in types.items():
        df[key] = df[key].astype(typename)

    print("1. 전체 이용량")
    print("2. 특정년도 월별 이용량")
    selection = int(input("검색 : "))
    if selection == 1:
        total_trend(df)
    elif selection == 2:
        year = str(input("연도 입력 : "))
        year_trend(df, year)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
