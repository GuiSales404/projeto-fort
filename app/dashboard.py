import pandas as pd
import numpy as np
import math
import panel as pn
import holoviews as hv
from holoviews import opts
from fort_script import selected_path
from panel.template import FastListTemplate
from funcs import * 
from sentiment_analysis import analyze_sentiment
hv.extension('bokeh')
pn.extension(sizing_mode="stretch_width")

all_avals = get_aval_data(selected_path)

columns = ['Domínio do Conteúdo', 'Capacidade de Lideranca', 'Clareza', 'Relacionamento', 'Metodologia']

all_course_notes = get_course_aval(all_avals)[0:-1]
all_course_notes = [note/all_course_notes[-1] for note in all_course_notes]

def courseAval_barChart(notes):
    data_for_plot = []
    for value, column in zip(notes, columns):
        data_for_plot.append((column, value))
    bar = hv.Bars(data_for_plot, hv.Dimension('Áreas de Ensino'), 'Notas')
    return bar.opts(
                    opts.Bars(width=900, height=350, color=hv.Cycle('Category20'), xticks={'angle': 45}),
                    opts.Overlay(xrotation=45)
                    )

def courseAval_table(notes):
    table = {
        'Domínio do Conteúdo': transform_note(math.ceil(notes[0])), 
        'Capacidade de Lideranca': transform_note(math.ceil(notes[1])), 
        'Clareza': transform_note(math.ceil(notes[2])), 
        'Relacionamento': transform_note(math.ceil(notes[3])), 
        'Metodologia': transform_note(math.ceil(notes[4])),
        'Nota do Curso': aval_note(all_avals, 'avaliação_curso', True)
    }
    df = pd.DataFrame(table, index=[0])
    table = hv.Table(df)
    table.opts(height=60, width=800)
    return table

def area_aval_barChart(area):
    barAval = hv.Bars(get_note_distr(all_avals, area), hv.Dimension('Avaliações'), 'Notas')
    return barAval.opts(
                    opts.Bars(width=750, height=270, color=hv.Cycle('Category20'), xticks={'angle': 45}),
                    opts.Overlay(xrotation=45)
                    )

def sugestion_table(experiences):
    experiences_list = []

    for experience in experiences:
        experiences_list.append(analyze_sentiment(experience))

    table_exp = {
    'Experiência': experiences, 
    'Sentimento':  experiences_list
    }
    
    df = pd.DataFrame(table_exp)
    table_exp = hv.Table(df)
    return table_exp.opts(height=90, width=800)

words = pn.Column(sugestion_table(get_all_sugests(all_avals)))

graphs = pn.Column(
                    '# Dashboard com Gráficos',
                    pn.Row(pn.layout.HSpacer(), pn.Column(pn.Row(pn.layout.HSpacer(), courseAval_table(all_course_notes), pn.layout.HSpacer()), courseAval_barChart(all_course_notes)),pn.layout.HSpacer()), 
                    pn.Row(pn.Column('### Domínio do Conteúdo', area_aval_barChart('dominio_conteudo')), pn.Column('### Capacidade de Liderança', area_aval_barChart('capacidade_lideranca'))),
                    pn.Row(pn.Column('### Clareza', area_aval_barChart('clareza')), pn.Column('### Relacionamento', area_aval_barChart('relacionamento'))),
                    pn.Row(pn.layout.HSpacer(), pn.Column('### Metodologia', area_aval_barChart('metodologia')), pn.layout.HSpacer())
                )

wordcloud = pn.Row('Giuseppe Careta')

tabs = pn.Tabs(("Gráficos", graphs), ("Texto", words), ("Professores", 'professores'))

# Crie um painel com os gráficos
dashboard = FastListTemplate(
    site='Fort Dashboard',
    title="Lista de Itens",
    main=[tabs]
)

pn.serve(dashboard, port=8000, live=True)


""" 
Alterar plotagem dos gráficos de valores
para nota escrita, além disso, criar gráfico
por área de avaliação. Em casa área deve conter 
uma coluna de cada valor de avaliação. Na plotagem
referência o gráfico que fica do lado direito
gráfico pizza, sera substituido pela nuvem de 
palavras, na parte direita mantém a cidade/escola/infos.
"""

# Gráficos de avaliação, wordcloud, professor aval