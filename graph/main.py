import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def total_trend(df):
    df = df.sort_values(by=['Year', 'Month'])
    sns.set_theme(style='whitegrid', palette='Paired')
    res = sns.barplot(x="Year", y="Data", data=df, hue="Month",
                      estimator=np.sum, ci=None)
    for p in res.patches:
        if not pd.isna(p.get_height()):
            val = str(round(int(p.get_height()),-6))[:-6]+"M"
        else:
            val = 0
        res.annotate(val, (p.get_x() + p.get_width()/2, p.get_height()),\
                     ha="center", va="center", fontsize=10, color="black", xytext=(2,16),\
                     rotation=90, textcoords="offset points")
    plt.legend(bbox_to_anchor=(1,1.05))
    plt.show()

def total_trend_by_month(df):
    df = df.sort_values(by=['Year', 'Month'])
    sns.set_theme(style='whitegrid', palette='deep')
    res = sns.barplot(x="Month", y="Data", data=df, hue="Year",
                      estimator=np.sum, ci=None)
    for p in res.patches:
        if not pd.isna(p.get_height()):
            val = str(round(int(p.get_height()),-6))[:-6]+"M"
        else:
            val = 0
        res.annotate(val, (p.get_x() + p.get_width()/2, p.get_height()),\
                     ha="center", va="center", fontsize=10, color="black", xytext=(2,16),\
                     rotation=90, textcoords="offset points")
    plt.legend(bbox_to_anchor=(1,1.05))
    plt.show()

def year_trend(df, year):
    sub = df[df['Year'] == year]
    sub = sub.sort_values(by='Month')
    sns.set_theme(style='whitegrid', palette='Paired')
    res = sns.barplot(x='Month', y='Data', data=sub, estimator=np.sum, ci=None)
    for p in res.patches:
        if not pd.isna(p.get_height()):
            val = str(round(int(p.get_height()),-6))[:-6]+"M"
        else:
            val = 0
        res.annotate(val, (p.get_x() + p.get_width()/2, p.get_height()),\
                     ha="center", va="center", fontsize=10, color="black", xytext=(0,10),\
                     textcoords="offset points")
    plt.show()

def daily_trend(df, sta):
    sub = df[df['Station'] == sta]
    sub = sub.sort_values(by=['Hour'])
    print(sub.head(10))
    fig, ax = plt.subplots(figsize=(15, 5))
    #plt.rcParams['font.family'] = 'Malgun Gothic'
    #plt.rcParams['axes.unicode_minus'] = False
    sns.set(font="Malgun Gothic", rc={"axes.unicode_minus":False}, style='whitegrid')
    pt = sns.lineplot(x="Hour", y="Data", data=sub, hue="Type", ax=ax)
    pt.set_title("{}역 시간대별 승하차량 평균".format(sta))
    plt.show()


if __name__ == '__main__':
    pd.set_option('display.width', None)
    df = pd.read_csv('defined_metro.csv', dtype=str)
    types = {"Data":int, "Latitude":float, "Longitude":float}
    for key, typename in types.items():
        df[key] = df[key].astype(typename)

    while True:
        print("1. 전체 이용량")
        print("2. 월별 전체 이용량")
        print("3. 특정년도 월별 이용량")
        print("4. 특정 역 시간대별 승하차량 추세")
        print("0. 종료")
        selection = int(input("검색 : "))
        if selection == 1:
            total_trend(df)
        elif selection == 2:
            total_trend_by_month(df)
        elif selection == 3:
            year = str(input("연도 입력 : "))
            year_trend(df, year)
        elif selection == 4:
            sta = input("역 이름 : ")
            daily_trend(df, sta)
        elif selection == 0:
            break


