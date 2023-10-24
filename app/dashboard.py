import pandas as pd
import numpy as np
import panel as pn
import holoviews as hv
from bokeh.sampledata.autompg import autompg

pn.extension()

# Função para criar um gráfico de barra
def create_bar_chart():
    data = pd.DataFrame(autompg)
    bar = hv.Bars(data, ['cyl', 'count()'], 'mpg')
    return bar.opts(width=600, height=400, xrotation=45)

# Função para criar um gráfico de pizza
def create_pie_chart():
    data = pd.DataFrame(autompg)
    pie = hv.Pie(data, 'cyl', 'count()')
    return pie.opts(width=400, height=400)

# Crie um painel com os gráficos
dashboard = pn.Column(
    '# Dashboard com Gráficos',
    pn.Row(create_bar_chart, create_pie_chart)
)

dashboard.servable()
