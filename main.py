from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import http.client, urllib
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_word():
    conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
    params = urllib.parse.urlencode({'key':'2422cd2d2601a5d09f151e73100e47d2'})
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    conn.request('POST','/zaoan/index',params,headers)
    res = conn.getresponse()
    data = res.read()
    datas = data.decode('utf-8')
    #print(datas[52:-4])
    return datas[52:-4]

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_word(), "color":get_random_color()}}
#res = wm.send_template(user_id, template_id, data)
#res1 = wm.send_template("o95975ly8eeIp66tejL2okZUGWyQ", template_id, data)##小号
#res2 = wm.send_template("o95975jYcxQYKRraSx2384t5jYb0", template_id, data)##曹大梅
#res3 = wm.send_template("o95975qF8cDX6F6w_kb_KV-0Ya_Q", template_id, data)##龙
#res4 = wm.send_template("o95975uN4IRmGnUpXXQEzBUPPBNw", template_id, data)##罗
#res5 = wm.send_template("o95975rAnHKEejMJj-hMUlN-paI8", template_id, data)##胡
print(res)
print(res1)
