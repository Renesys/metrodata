import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mat
import numpy as np


def total_trend(df):
    df['Data'] = df['GetOn'] + df['GetOff']
    df = df.sort_values(by=['Year', 'Month'])
    sns.set_theme(font="Malgun Gothic", rc={"axes.unicode_minus": False},\
                  style='whitegrid', palette='Paired')
    fig, ax = plt.subplots(figsize=(15, 5))
    res = sns.barplot(x="Year", y="Data", data=df, hue="Month",
                      estimator=np.sum, ci=None, ax=ax)
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
    df['Data'] = df['GetOn'] + df['GetOff']
    df = df.sort_values(by=['Year', 'Month'])
    sns.set_theme(font="Malgun Gothic", rc={"axes.unicode_minus": False},\
                  style='whitegrid', palette='deep')
    fig, ax = plt.subplots(figsize=(15, 5))
    res = sns.barplot(x="Month", y="Data", data=df, hue="Year",
                      estimator=np.sum, ci=None, ax=ax)
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
    df['Data'] = df['GetOn'] + df['GetOff']
    sub = df[df['Year'] == year]
    sub = sub.sort_values(by='Month')
    sns.set_theme(font="Malgun Gothic", rc={"axes.unicode_minus": False},\
                  style='whitegrid', palette='Paired')
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

def get_days(m):
    if m == '02':
        return 28
    elif m == '04' or m == '06' or m == '09' or m == '11':
        return 30
    else:
        return 31

def station_trend(df, sta):
    df['Data'] = df['GetOn'] + df['GetOff']
    df['YearMonth'] = df['Year'] + df['Month']
    df = df.sort_values(by=['YearMonth', 'Hour'])
    sub = df[df['Station'] == sta]
    sub['avg'] = df['Data'] / df['Month'].apply(get_days)
    if sub.empty:
        print("******** 잘못된 역 이름 ********")
        return
    print(sub.head(100))
    sns.set_theme(font="Malgun Gothic", rc={"axes.unicode_minus": False}, \
                  style='whitegrid')
    fig, ax = plt.subplots(figsize=(19, 9), nrows=2)
    fig.tight_layout(pad=2)
    ax[0].title.set_text("{}역 시간대별 월 평균 승하차량".format(sta))
    ax[1].title.set_text("{}역 월별 일 평균 승하차량".format(sta))
    sns.lineplot(x="Hour", y="Data", data=sub, hue="Type", ax=ax[0])
    sns.lineplot(x="YearMonth", y="avg", data=sub, estimator=np.sum, ax=ax[1])
    plt.xticks(rotation=90)
    plt.show()

if __name__ == '__main__':
    pd.set_option('display.width', None)
    df = pd.read_csv('defined_metro_temp.csv', dtype=str)
    types = {"GetOn":int, "GetOff":int, "Latitude":float, "Longitude":float}
    for key, typename in types.items():
        df[key] = df[key].astype(typename)
    while True:
        print("1. 전체 이용량")
        print("2. 월별 전체 이용량")
        print("3. 특정년도 월별 이용량")
        print("4. 특정 역 시간대 별 / 월별 승하차량")
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
            station_trend(df, sta)
        elif selection == 0:
            break


