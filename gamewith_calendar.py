import re
import ast
import time

translate_list = {
    'ベリーハード': 'VH',
    'ハード': '困难',
    'ノーマル': '普通',
    'ノマクエ': '普通',
    'ダンジョン': '地下城玛娜',
    'ルナの塔': '露娜塔',
    'クランバトル': '公会战',
    'プレイヤー': '玩家',
}


def transform_gamewith_calendar(html_text):
    data_list = re.findall(r"data-calendar='(.*?)'", html_text, re.S)
    event_list = {}
    for data in data_list:
        event = ast.literal_eval(data)
        start = time.localtime(event['start_time'])
        end = time.localtime(event['end_time'])
        # gamewith: 1 庆典活动 2 剧情活动 3 工会战 4 露娜塔 5 复刻活动
        type_id = int(event['color_id'])
        if type_id == 1:
            type_id = 2
        elif type_id == 3:
            type_id = 3
        else:
            type_id = 1
        name = event['event_name']
        for k, v in translate_list.items():
            name = name.replace(k, v)
        event_list[event['id']] = {
            'name': name,
            'start_time': time.strftime("%Y/%m/%d %H:%M:%S", start),
            'end_time': time.strftime("%Y/%m/%d %H:%M:%S", end),
            'type': type_id,
            }
    return list(event_list.values())


'''
fp = open('gamewith.html', encoding='utf-8')
data = fp.read()
data = transform_gamewith_calendar(data)
print(data)
'''
