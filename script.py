import numpy as np
from jinja2 import Template
import plotly.express as px
from datetime import datetime
import requests as rqst

def daysToWeeks(x, weeks):
    xn = []
    for i in x:
        for j in weeks:
            daycurrent = int(i[8:])
            dayweek = int(j[8:])
            if i[5:7] == j[5:7] and abs(daycurrent - dayweek) < 7:
                xn.append(j)
    xn = set(xn)
    return xn

my_date = datetime.now()
token = "dIlUIIpKrjCcrmmM"
emails = ["damolchanov@miem.hse.ru", "damolchanov@edu.hse.ru"]
"""Всё, 
    что 
        связано 
            с   Git:"""
weeks = {"2022-01-03","2022-01-10","2022-01-17","2022-01-24","2022-01-31",
         "2022-02-07","2022-02-14","2022-02-21","2022-02-28",
         "2022-03-07","2022-03-14","2022-03-21","2022-03-28"}

respGit = rqst.post("http://94.79.54.21:3000/api/git/getData",
                        json = {
                            "studEmail": emails[1],
                            "beginDate": "2022-01-01",
                            "endDate": str(my_date)[:10],
                            "timeRange": 1,
                            "hideMerge": True,
                            "token": token }).json()

gitCount = 0
x_git = set()
y_git = np.zeros(1)

for i in respGit['projects']:
    if i['name'] == "ivt21-miniproject / Данил Молчанов":
        gitCount = i['commitCount']
        for j in i['commits']:
            x_git.add(j['committed_date'][:10])
            y_git.resize(len(x_git))
            y_git[len(x_git) - 1] += 1

y1_git = y_git.copy()
for i in range(0, len(y1_git)):
    for j in range(0,i):
        y1_git[i] = y1_git[i] + y_git[j]

x_git = list(daysToWeeks(x_git, weeks))
x_git.sort()
"""Всё, 
    что 
        связано 
            с   Zulip:"""

respZulip = rqst.post("http://94.79.54.21:3000/api/zulip/getData",
                        json = {
                            "studEmail": emails[0],
                            "beginDate": "2022-01-01",
                            "endDate": str(my_date)[:10],
                            "timeRange": 1,
                            "token": token }).json()
zulipMessages = len(respZulip['messages'])

zulipChannels = {}
x_zulip = set()
y_zulip = np.zeros(1)

zulipChannels = set(zulipChannels)

for channel in respZulip['messages']:
    zulipChannels.add(channel['name'])
    x_zulip.add(channel['timestamp'][:10])
    y_zulip.resize(len(x_zulip))
    y_zulip[len(x_zulip) - 1] += 1

y_zulip = np.array(y_zulip)
x_zulip = list(x_zulip)
x_zulip.sort()
y1_zulip = y_zulip.copy()

for i in range(0, len(y1_zulip)):
    for j in range(0,i):
        y1_zulip[i] = y1_zulip[i] + y_zulip[j]

"""Всё, 
    что 
        связано 
            с   Jitsi:"""
x_jitsi = set()
y_jitsi = np.zeros(1)
jitsiCount = 0

jitsiRooms = {}
jitsiRooms = set(jitsiRooms)

for i in emails:
    respJitsi = rqst.post("http://94.79.54.21:3000/api/jitsi/sessions",
                            json = {
                                "studEmail": i,
                                "endDate": str(my_date)[:10],
                                "token": token }).json()
    
    jitsiCount = jitsiCount + len(respJitsi)

    for i in respJitsi:
        jitsiRooms.add(i['room'])
        x_jitsi.add(i['date'][:10])
        y_jitsi.resize(len(x_jitsi))
        y_jitsi[len(x_jitsi) - 1] += 1
    
    y1_jitsi = y_jitsi.copy()
    for i in range(0, len(y1_jitsi)):
        for j in range(0, i):
            y1_jitsi[i] = y1_jitsi[i] + y_jitsi[j]

x_jitsi = list(x_jitsi)
x_jitsi.sort()
"""Всё, 
    что 
        связано 
            с   Taiga:"""

respTaiga = rqst.get("https://track.miem.hse.ru/api/v1/userstories",
                     headers = {"x-disable-pagination": "True"}).json()
taigaStoryCount = 0
taigaTasksCount = 0

for i in respTaiga:
    if type(i['assigned_to_extra_info']) != type(None):
        if i['assigned_to_extra_info']['full_name_display'] == "Данил Молчанов":
            taigaStoryCount += 1

respTaiga = rqst.get("https://track.miem.hse.ru/api/v1/tasks",
                     headers = {"x-disable-pagination": "True"}).json()

x_taiga = set()
y_taiga = np.zeros(1)

for i in respTaiga:
    if type(i['assigned_to_extra_info']) != type(None):
        if i['assigned_to_extra_info']['full_name_display'] == "Данил Молчанов":
            x_taiga.add(i['created_date'][:10])
            y_taiga.resize(len(x_taiga))
            y_taiga[len(x_taiga)-1] += 1

x_taiga = list(x_taiga)
x_taiga.sort()
y1_taiga = y_taiga.copy()
for i in range(0, len(y1_taiga)):
    for j in range(0, i):
        y1_taiga[i] = y1_taiga[i] + y_taiga[j]

x_taiga = list(daysToWeeks(x_taiga, weeks))
x_taiga.sort()
"""Генерация
            HTML-страницы
                    и графиков:"""

temp = open('/home/prsem/damolchanov/damolchanov/template.html').read()
template = Template(temp)

fig_zulip = px.bar(x = x_zulip, y = y_zulip, 
                   labels = dict(x = "Дата", y = "Сообщения"))
fig_zulip1 = px.line(x = x_zulip, y = y1_zulip, 
                    labels = dict(x = "Дата", y = "Общее кол-во сообщений"))
fig_jitsi = px.bar(x = x_jitsi, y = y_jitsi,
                   labels = dict(x = "Дата", y = "Посещённые занятия"))
fig_jitsi1 = px.line(x = x_jitsi, y = y1_jitsi,
                     labels = dict(x = "Дата", y = "Общее кол-во посещённых занятий"))
fig_git = px.bar(x = x_git, y = y_git,
                 labels = dict(x = "Дата", y = "Коммиты"))
fig_git1 = px.line(x = x_git, y = y1_git,
                   labels = dict(x = "Дата", y = "Общее кол-во коммитов"))
fig_tai = px.line(x = x_taiga, y =y1_taiga,
                  labels = dict(x = "Дата", y = "Общее кол-во задач"))
with open('index.html', 'w') as fh:
    fh.write(template.render(fullname = "Молчанов Данил Андреевич",
                             datetime = my_date.isoformat(), 
                             group = "БИВ 213", 
                             git = fig_git.to_html(),
                             git1 = fig_git1.to_html(),
                             tai = fig_tai.to_html(),
                             taigaStoryCount = taigaStoryCount,
                             taigaTasksCount = int(y1_taiga[len(y1_taiga) - 1]),
                             jit = fig_jitsi.to_html(), 
                             jit1 = fig_jitsi1.to_html(),
                             zul = fig_zulip.to_html(),
                             zul1 = fig_zulip1.to_html(),
                             zulipMessages = zulipMessages,
                             zulipChannels = zulipChannels,
                             jitsiCount = jitsiCount,
                             jitsiRooms = jitsiRooms,
                             gitCount = gitCount))
