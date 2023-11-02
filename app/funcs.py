import os
import pandas as pd
import unicodedata
import string
import math

def is_any_csv(path: str):
    count_csv_files = 0
    for file in os.listdir(path):
        if file.split('.')[-1] == 'csv':
            count_csv_files += 1

    if count_csv_files == 0:
        return ValueError('Não há arquivos .csv para gerar o(s) dashboard(s)')
    
def preprocess_text(text):
    text = ''.join([c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)])
    
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    
    text = text.lower()
    
    return text

def transform_note(note: str, kind=None) -> int:
    if kind == 'to_int':
        match note:
            case 'otimo':
                return 5
            case 'bom':
                return 4
            case 'regular':
                return 3
            case 'ruim':
                return 2
            case 'pessimo':
                return 1
    else:
        match note:
            case 5:
                return 'Ótimo'
            case 4:
                return 'Bom'
            case 3:
                return 'Regular'
            case 2:
                return 'Ruim'
            case 1:
                return 'Péssimo'
            
def get_aval_data(path: str):
    
    avals = []
    
    for aval in os.listdir(path):
        df = pd.read_csv(f'{path}/{aval}')
        avals.append({
        'professor': preprocess_text(df['professor'].to_string(index=False)),
        'escola': preprocess_text(df['escola'].to_string(index=False)),
        'data': df['data'].to_string(index=False),
        'turno': preprocess_text(df['turno'].to_string(index=False)),
        'ano': preprocess_text(df['ano'].to_string(index=False)),
        'autoavaliação': preprocess_text(df['autoavaliação'].to_string(index=False)),
        'avaliação_curso': preprocess_text(df['avaliação do curso'].to_string(index=False)),
        'nome_formador': preprocess_text(df['nome do formador'].to_string(index=False)),
        'dominio_conteudo': preprocess_text(df['domínio do conteúdo'].to_string(index=False)),
        'capacidade_lideranca': preprocess_text(df['capacidade de liderança'].to_string(index=False)),
        'clareza': preprocess_text(df['clareza'].to_string(index=False)),
        'relacionamento': preprocess_text(df['relacionamento'].to_string(index=False)),
        'metodologia': preprocess_text(df['metodologia trabalhada'].to_string(index=False)),
        'pontos_positivos': preprocess_text(df['pontos positivos'].to_string(index=False)),
        'pontos_negativos': preprocess_text(df['pontos negativos'].to_string(index=False)),
        'sugestoes': preprocess_text(df['sugestões'].to_string(index=False)),
        'experiencia': preprocess_text(df['experiência'].to_string(index=False))
        })
        
    return avals

def get_course_aval(all_avals: list):

    dom_cont = 0
    cap_lider = 0
    clareza = 0
    relac = 0
    metodo = 0
    count_avals = 0

    for aval in all_avals:
        dom_cont += transform_note(aval['dominio_conteudo'], 'to_int')
        cap_lider += transform_note(aval['capacidade_lideranca'], 'to_int')
        clareza += transform_note(aval['clareza'], 'to_int')
        relac += transform_note(aval['relacionamento'], 'to_int')
        metodo += transform_note(aval['metodologia'], 'to_int')
        count_avals += 1

    return dom_cont, cap_lider, clareza, relac, metodo, count_avals, count_avals

def get_professor_aval(all_avals: list, professor_name: str):
    
    professor_avals = [d for d in all_avals if d.get('professor') == professor_name]
    
    dom_cont = 0
    cap_lider = 0
    clareza = 0
    relac = 0
    metodo = 0
    count_avals = 0

    for aval in professor_avals:
        dom_cont += transform_note(aval['dominio_conteudo'], 'to_int')
        cap_lider += transform_note(aval['capacidade_lideranca'], 'to_int')
        clareza += transform_note(aval['clareza'], 'to_int')
        relac += transform_note(aval['relacionamento'], 'to_int')
        metodo += transform_note(aval['metodologia'], 'to_int')
        count_avals += 1

    return dom_cont, cap_lider, clareza, relac, metodo, count_avals, count_avals

def get_all_professors(all_avals: list) -> list:
    
    all_professors = set()
    
    for aval in all_avals:
        all_professors.add(aval['professor'])
    
    return list(all_professors)

def aval_note(all_avals, area, transform):
    final_note = 0
    for course_aval in all_avals:
        final_note += int(course_aval[f'{area}'])

    if transform == True:
        return transform_note(math.ceil(final_note/(2*len(all_avals))))
    if transform == False:
        return math.ceil(final_note/(2*len(all_avals)))
    
def get_note_distr(all_avals, area):
    quality = ['Ótimo', 'Bom', 'Regular', 'Ruim', 'Pessímo']
    all_notes = []
    data = []
    for aval in all_avals:
        all_notes.append(aval[f'{area}'])
    
    for note in quality:
        data.append((note, all_notes.count(f'{preprocess_text(note)}')))
    
    return data

def get_all_sugests(all_avals):
    sugestions = []
    for aval in all_avals:
        sugestions.append(aval['experiencia'])
    return sugestions