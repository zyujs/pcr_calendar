import json
import datetime
import pytz
from hoshino import logger
from typing import Optional
from playwright.async_api import Browser, async_playwright
from functools import reduce

url = "https://gamewith.jp/pricone-re/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60"}
tz = pytz.timezone("Asia/Shanghai")


async def get_clendar():
    try:
        events = await get_gamewith()
        calendars = []
        for index, event in enumerate(events):
            js = json.loads(event)
            js_start = js["start_time"]
            js_end = js["end_time"]

            # 源数据是时间戳，格式化一下
            start = datetime.datetime.fromtimestamp(
                int(js_start), tz).strftime('%Y/%m/%d %H:%M:%S')
            start_time = datetime.datetime.strptime(start, r'%Y/%m/%d %H:%M:%S')
            end = datetime.datetime.fromtimestamp(
                int(js_end), tz).strftime('%Y/%m/%d %H:%M:%S')
            end_time = datetime.datetime.strptime(end, r'%Y/%m/%d %H:%M:%S')
            calendar = {"id": js["id"], "title": js["event_name"], "start": start_time, "end": end_time, "type": 1}

            if '倍' in calendar["title"]:
                calendar["type"] = 2
            elif 'クラバト' in calendar["title"]:
                event["type"] = 3

            calendars.append(calendar)
        # gamewith日历是两周的时间表，这里需要去重
        calendars_news = reduce(lambda x, y: x if y in x else x + [y], [[], ] + calendars)
        return calendars_news
    except Exception as e:
        logger.error(e)
        return []


_browser: Optional[Browser] = None


async def init(**kwargs) -> Browser:
    global _browser
    browser = await async_playwright().start()
    _browser = await browser.chromium.launch(**kwargs)
    return _browser


async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)


async def get_gamewith():
    browser = await get_browser()
    page = None
    try:
        page = await browser.new_page(device_scale_factor=2)
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        await page.set_viewport_size({"width": 2560, "height": 1080})
        await page.wait_for_selector(".js-calendar-item", state="attached")
        await page.click("text=イベントカレンダー")
        event = await page.query_selector_all(".js-calendar-item")
        assert event
        res = []
        for item in event:
            attr = await item.get_attribute("data-calendar")
            res.append(attr)
        await page.close()
        return res
    except Exception as e:
        logger.error(e)
        if page:
            await page.close()
        return []
