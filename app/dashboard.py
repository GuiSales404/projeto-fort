import pandas as pd
import numpy as np
import panel as pn
import holoviews as hv
from holoviews import opts
from fort_script import selected_path
from funcs import * 
hv.extension('bokeh')
pn.extension()

# Função para criar um gráfico de barra
all_avals = get_aval_data(selected_path)

columns = ['dominio_conteudo', 'capacidade_lideranca', 'clareza', 'relacionamento', 'metodologia', 'count_avals', 'count']

def create_bar_chart():
    data_for_plot = []
    for value, column in zip(get_course_aval(all_avals), columns):
        data_for_plot.append((column, value))
    bar = hv.Bars(data_for_plot, hv.Dimension('Avaliações'), 'nota')
    return bar.opts(
                    opts.Bars(width=600, height=300, tools=['hover'], color=hv.Cycle('Category20'), xticks={'angle': 45}),
                    #opts.Curve(xrotation=45, show_legend=False),
                    opts.Overlay(xrotation=45)
                    )

# Crie um painel com os gráficos
dashboard = pn.Column(
    '# Dashboard com Gráficos',
    pn.Row(create_bar_chart)
)

dashboard.servable()


""" Alterar plotagem dos gráficos de valores
para nota escrita, além disso, criar gráfico
por área de avaliação. Em casa área deve conter 
uma coluna de cada valor de avaliação. Na plotagem
referência o gráfico que fica do lado direito
gráfico pizza, sera substituido pela nuvem de 
palavras, na parte direita mantém a cidade/escola/infos.
 """