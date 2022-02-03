from PIL import Image, ImageDraw, ImageFont
from .event import *
import os

he = 45
width = 0

font_path = os.path.join(os.path.dirname(__file__), 'wqy-microhei.ttc')
font = ImageFont.truetype(font_path, int(he * 0.67))

color = [
    {
        'front': 'black',
        'back': 'white'
    },  # 活动(中间)、掉率庆典(上方)、团队战(下方)
    {
        'front': 'white',
        'back': '#0fbec0'
    },
    {
        'front': 'white',
        'back': '#a1b75d'
    },
    {
        'front': 'white',
        'back': '#D0B777'
    },
]


def create_image(item_number, wid):
    global width
    width = int(he * wid * 0.7)
    height = item_number * he
    im = Image.new('RGBA', (int(width * 1.01), height), "white")
    return im


def draw_rec(im, color, x, y, w, h, r):
    draw = ImageDraw.Draw(im)
    draw.rectangle((x + r, y, x + w - r, y + h), fill=color)
    draw.rectangle((x, y + r, x + w, y + h - r), fill=color)
    r = r * 2
    draw.ellipse((x, y, x + r, y + r), fill=color)
    draw.ellipse((x + w - r, y, x + w, y + r), fill=color)
    draw.ellipse((x, y + h - r, x + r, y + h), fill=color)
    draw.ellipse((x + w - r, y + h - r, x + w, y + h), fill=color)


def draw_text(im, x, y, w, h, text, align, color):
    draw = ImageDraw.Draw(im)
    tw, th = draw.textsize(text, font=font)
    y = y + (h - th) / 2
    if align == 0:  #居中
        x = x + (w - tw) / 2
    elif align == 1:  #左对齐
        x = x + 5
    elif align == 2:  #右对齐
        x = x + w - tw - 5
    draw.text((x, y), text, fill=color, font=font)


def draw_item(im, n, t, text, days):
    if t >= len(color):
        t = 1
    x = 0
    y = n * he
    height = int(he * 0.93)

    draw_rec(im, color[t]['back'], x, y, width, height, 6)
    draw_text(im, x, y, width, height, text, 1, color[t]['front'])
    if days > 0:
        text1 = f'{days}天后结束'
    elif days < 0:
        text1 = f'{-days}天后开始'
    else:
        text1 = '即将结束'
    draw_text(im, x, y, width, height, text1, 2, color[t]['front'])


def draw_title(im, n, left=None, middle=None, right=None):
    x = 0
    y = n * he
    height = int(he * 0.93)

    draw_rec(im, color[0]['back'], x, y, width, height, 6)
    if middle:
        draw_text(im, x, y, width, height, middle, 0, color[0]['front'])
    if left:
        draw_text(im, x, y, width, height, left, 1, color[0]['front'])
    if right:
        draw_text(im, x, y, width, height, right, 2, color[0]['front'])


def draw_title1(im, n, day_list):
    x = 0
    y = n * he
    height = int(he * 0.93)
    color = 'black'

    n = len(day_list)
    for i in range(n):
        x = width / n * i
        draw_text(im, x, y, width, height, day_list[i], 1, color)
