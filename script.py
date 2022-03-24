import numpy as np
from jinja2 import Template
import plotly.graph_objects as go
from datetime import datetime

temp = open('template.html').read()
template = Template(temp)


my_date = datetime.now()

x = np.arange(0, 5, 0.1)
def f(x):
    return x**2

fig = go.Figure([go.Scatter(x=x, y=f(x))])

with open('index.html', 'w') as fh:
    fh.write(template.render(fullname = "Молчанов Данил Андреевич",datetime = my_date.isoformat(), group = "БИВ 213", git = fig.to_html(), tai = fig.to_html(), jit = fig.to_html(), zul = fig.to_html()))
