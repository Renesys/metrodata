import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def year_trend(df, year):
    sub = df[df['Year'] == year]
    sub = sub.sort_values(by='Month')
    #print(sub.head(10))
    sns.set_palette('Set3')
    res = sns.barplot(x=sub['Month'], y=sub['Data'], estimator=np.sum)
    for p in res.patches:
        res.annotate("%.0f" % p.get_height(), (p.get_x() + p.get_width()/2, p.get_height()-30),\
                     ha="center", va="center", fontsize=10, color="black", xytext=(0,10),\
                     textcoords="offset points")
    plt.show()

def total_trend(df):
    df['YearMonth'] = df['Year'] + df['Month']
    df = df.sort_values(by=['YearMonth'])
    #print(df.head(10))
    sns.set_palette('Set3')
    res = sns.barplot(x=df['YearMonth'], y = df['Data'], estimator=np.sum)
    for p in res.patches:
        val = str(round(int(p.get_height()),-6))[:-6]+"M"
        res.annotate(val, (p.get_x() + p.get_width()/2, p.get_height()-30),\
                     ha="center", va="center", fontsize=10, color="black", xytext=(0,10),\
                     rotation=45, textcoords="offset points")
    plt.xticks(rotation=45)
    plt.show()

def total_trend_by_month(df):
    df = df.sort_values(by=['Year', 'Month'])
    res = sns.barplot(x="Month", y="Data", data=df, hue="Year",
                      estimator=np.sum,
                      palette='pastel')
    for p in res.patches:
        if not pd.isna(p.get_height()):
            val = str(round(int(p.get_height()),-6))[:-6]+"M"
        else:
            val = 0
        res.annotate(val, (p.get_x() + p.get_width()/2, p.get_height()+30),\
                     ha="center", va="center", fontsize=10, color="black", xytext=(0,10),\
                     rotation=90, textcoords="offset points")
    plt.legend(bbox_to_anchor=(1.02,1), loc='center right', borderaxespad=0)
    plt.show()

if __name__ == '__main__':
    pd.set_option('display.width', None)
    df = pd.read_csv('defined_metro.csv', dtype=str)
    types = {"Data":int, "Latitude":float, "Longitude":float}
    for key, typename in types.items():
        df[key] = df[key].astype(typename)

    print("1. 전체 이용량")
    print("2. 월별 전체 이용량")
    print("3. 특정년도 월별 이용량")
    selection = int(input("검색 : "))
    if selection == 1:
        total_trend(df)
    elif selection == 2:
        total_trend_by_month(df)
    elif selection == 3:
        year = str(input("연도 입력 : "))
        year_trend(df, year)


