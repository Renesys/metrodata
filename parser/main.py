import os
import csv
import json
import datetime

string_hour_map = {
    "eighteen_alight_num": ["18", "OFF"],
    "nineteen_alight_num": ["19", "OFF"],
    "five_alight_num": ["05", "OFF"],
    "fifteen_ride_num": ["15", "ON"],
    "twenty_three_alight_num": ["23", "OFF"],
    "eight_alight_num": ["08", "OFF"],
    "sixteen_ride_num": ["16", "ON"],
    "seventeen_alight_num": ["17", "OFF"],
    "twenty_two_alight_num": ["22", "OFF"],
    "twenty_two_ride_num": ["22", "ON"],
    "eleven_alight_num": ["11", "OFF"],
    "six_ride_num": ["06", "ON"],
    "thirteen_ride_num": ["13", "ON"],
    "four_alight_num": ["04", "OFF"],
    "seventeen_ride_num": ["17", "ON"],
    "fourteen_ride_num": ["14", "ON"],
    "seven_alight_num": ["07", "OFF"],
    "nine_alight_num": ["09", "OFF"],
    "eighteen_ride_num": ["18", "ON"],
    "three_alight_num": ["03", "OFF"],
    "twelve_alight_num": ["12", "OFF"],
    "two_alight_num": ["02", "OFF"],
    "twenty_alight_num": ["20", "OFF"],
    "ten_alight_num": ["10", "OFF"],
    "thirteen_alight_num": ["13", "OFF"],
    "one_ride_num": ["01", "ON"],
    "four_ride_num": ["04", "ON"],
    "sixteen_alight_num": ["16", "OFF"],
    "five_ride_num": ["05", "ON"],
    "fourteen_alight_num": ["14", "OFF"],
    "six_alight_num": ["06", "OFF"],
    "nineteen_ride_num": ["19", "ON"],
    "ten_ride_num": ["10", "ON"],
    "two_ride_num": ["02", "ON"],
    "twenty_three_ride_num": ["23", "ON"],
    "one_alight_num": ["01", "OFF"],
    "fifteen_alight_num": ["15", "OFF"],
    "midnight_alight_num": ["00", "OFF"],
    "seven_ride_num": ["07", "ON"],
    "nine_ride_num": ["09", "ON"],
    "eight_ride_num": ["08", "ON"],
    "twenty_one_ride_num": ["21", "ON"],
    "twenty_ride_num": ["20", "ON"],
    "twelve_ride_num": ["12", "ON"],
    "twenty_one_alight_num": ["21", "OFF"],
    "three_ride_num": ["03", "ON"],
    "midnight_ride_num": ["00", "ON"],
    "eleven_ride_num": ["11", "ON"]
}

station_num_map = {
    "1호선": ["1", "P1"],
    "2호선": ["2"],
    "3호선": ["3"],
    "4호선": ["4"],
    "5호선": ["5", "P5"],
    "6호선": ["6"],
    "7호선": ["7"],
    "8호선": ["8"],
    "9호선": ["9"],
    "경의중앙선": ["K1"],
    "수인분당선": ["K2"],
    "경춘선": ["K3"],
    "경강선": ["K4"],
    "서해선": ["S"],
    "공항철도": ["A"],
    "우이신설선": ["S1"],
    "인천1호선": ["I1"],
    "인천2호선": ["I2"],
    "용인에버라인": ["Y"],
    "의정부경전철": ["U1"],
    "김포골드라인": ["G1"]
}

def get_json():
    with open('metro.json', encoding='UTF8') as f:
        f_data = json.load(f)
        json_array = f_data["DATA"]
    return json_array


def get_line(line, sta):
    if line == "9호선2~3단계" or line == "9호선2단계":
        line = "9호선"
    elif line == "일산선":
        line = "3호선"
    elif line == "과천선" or line == "안산선":
        line = "4호선"
    elif line == "경의선" or line == "중앙선":
        line = "경의중앙선"
    elif line == "수인선" or line == "분당선":
        line = "수인분당선"
    elif line == "공항철도 1호선":
        line = "공항철도"
    elif line == "경원선":
        if sta == "청량리" or sta == "왕십리" or sta == "응봉" or sta == "옥수" or \
                sta == "한남" or sta == "서빙고" or sta == "이촌":
            line = "경의중앙선"
        else:
            line = "1호선"
    elif line == "경부선" or line == "경인선" or line == "장항선":
        line = "1호선"

    return line

def mod_station_name(raw_name, line):
    idx = raw_name.find('(');
    if idx == -1:
        sta = raw_name
    else:
        sta = raw_name[0:idx]
    if sta == "양평" and line == "5호선":
        sta = "양평동"
    if sta == "총신대입구":
        sta = "이수"
    if sta == "신천":
        sta = "잠실새내"
    if sta == "신촌" and line == "경의선":
        sta == "신촌역"
    if sta == "인천국제공항":
        sta = "인천공항1터미널"
    if sta == "쌍용동":
        sta = "쌍용"
    if sta == "동두천 중앙":
        sta = "동두천중앙"
    return sta

station_pos = {}
with open('station_info.csv', 'r', newline='', encoding='utf-8') as posfile:
    pos = csv.reader(posfile, delimiter=',')
    for p in pos:
        station_pos[p[0]] = [p[1], p[2]]


def get_pos(sta, type):
    res = 0
    if sta in station_pos:
       res = station_pos[sta][type]
    else:
        print(sta)
    return res

def write_csv_all(raw):
    with open('../graph/defined_metro.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writter = csv.writer(csvfile, delimiter=',')
        csv_writter.writerow(
            ["Line", "Station", "Time", "Year", "Month", "Hour", "Type", "Data", "Latitude", "Longitude"])
        for e in raw:
            month = str(e['use_mon'])
            sta = mod_station_name(e['sub_sta_nm'], e['line_num'])
            line = get_line(e['line_num'], sta)
            lati = get_pos(sta, 0)
            long = get_pos(sta, 1)
            for d in string_hour_map.keys():
                data = e[d]
                time_str = "{}-{}-01T{}:00:00Z".format(month[0:4], month[4:6], string_hour_map[d][0])
                ridetype = string_hour_map[d][1]
                # q = '["{}","{}","{}","{}","{}","0","0"]'.format(line, sta, time_str, ridetype, data)
                csv_writter.writerow(
                    [line, sta, time_str, month[0:4], month[4:6], string_hour_map[d][0], ridetype, data, lati, long])


def write_csv(raw):
    with open('defined_metro_partial.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writter = csv.writer(csvfile, delimiter=',')
        csv_writter.writerow(
            ["Line", "Station", "Time", "Year", "Month", "Hour", "Type", "Data", "Latitude", "Longitude"])
        for e in raw:
            month = str(e['use_mon'])
            sta = e['sub_sta_nm']
            line = get_line(e['line_num'], sta)
            # take latest data only
            if month == "202006":
                for d in string_hour_map.keys():
                    data = e[d]
                    time_str = "{}-{}-01T{}:00:00Z".format(month[0:4], month[4:6], string_hour_map[d][0])
                    ridetype = string_hour_map[d][1]
                    # q = '["{}","{}","{}","{}","{}","0","0"]'.format(line, sta, time_str, ridetype, data)
                    csv_writter.writerow(
                        [line, sta, time_str, month[0:4], month[4:6], string_hour_map[d][0], ridetype, data, "0", "0"])


def test():
    for d in string_hour_map.keys():
        print(string_hour_map[d][0])


if __name__ == "__main__":
    raw_array = get_json()
    write_csv_all(raw_array)
#	write_csv(raw_array)
# test()