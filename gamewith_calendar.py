import re
import ast
import time

def transform_gamewith_calendar(html_text):
    data_list = re.findall(r"data-calendar='(.*?)'", html_text, re.S)
    event_list = {}
    for data in data_list:
        event = ast.literal_eval(data)
        start = time.localtime(event['start_time'])
        end = time.localtime(event['end_time'])
        # gamewith: 1 庆典活动 2 剧情活动 3 露娜塔 4 工会战 5 免费十连
        type_id = int(event['color_id'])
        if type_id == 1:
            type_id = 2
        elif type_id == 4:
            type_id = 3
        else:
            type_id = 1;
        event_list[event['id']] = {
            'name': event['event_name'],
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