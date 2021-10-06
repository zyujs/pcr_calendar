import re
import ast
from html.parser import HTMLParser


keyword_list = [
  'year',
  'month',
  'day',
  'qdhd', #庆典活动
  'tdz',  #团队战
  'tbhd', #特别活动
  'jqhd', #剧情活动
  'jssr', #角色生日
]

event_keyword_list = [
    'qdhd',
    'tbhd',
    'jqhd',
    'tdz',
]


class ContentParse(HTMLParser):
    def __init__(self):
          HTMLParser.__init__(self)
          self.data = []
          self.is_title = False 
    def handle_starttag(self, tag, attrs):
        if 'cl-t' in attrs[0]:
          self.is_title = True
        else:
          self.is_title = False 

    def handle_data(self, data):
        if self.is_title:
          self.data.append(data)



def parse_content(day_content):
    content_html = ''
    for keyword in event_keyword_list:
        content_html += day_content[keyword]
    parser = ContentParse()
    parser.feed(content_html)
    return parser.data

    
def extract_calendar_data(js_text):
    #提取js的data部分转换为python对象
    data_str = re.search(r'\[.*?\]', js_text, re.S).group(0)
    for keyword in keyword_list:
        data_str = data_str.replace(keyword, f'"{keyword}"')
    data = ast.literal_eval(data_str)
    #解析活动内容html
    for i in range(len(data)):
        for day in data[i]['day']:
            content = parse_content( data[i]['day'][day])
            data[i]['day'][day] = content
    return data

def transform_calendar_data(data):
    event_cache = {}
    event_list = []
    for i in range(len(data)):
        for day in data[i]['day']:
            #print(data[i]['year'], data[i]['month'], day, data[i]['day'][day])
            #遍历本日活动
            year = int(data[i]['year'])
            month = int(data[i]['month'])
            for event_name in data[i]['day'][day]:   
                if event_name not in event_cache.keys():
                    event_cache[event_name] = {'year': year, 'month': month, 'day': int(day)}
            for event_name in list(event_cache.keys()):
                if event_name not in data[i]['day'][day]:
                    event_list.append({
                        'title':event_name,
                        'start': f'{event_cache[event_name]["year"]}/{event_cache[event_name]["month"]}/{event_cache[event_name]["day"]} 05:00', 
                        'end': f'{year}/{month}/{int(day)} 23:59'})
                    event_cache.pop(event_name)
    return event_list

def transform_bilibili_calendar(data):
    data = extract_calendar_data(data)
    data = transform_calendar_data(data)
    return data

'''
fp = open('calendar.js', encoding='utf-8')
data = fp.read()
data = transform_bilibili_calendar(data)
print(data)
'''