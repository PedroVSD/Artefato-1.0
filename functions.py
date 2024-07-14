from datetime import datetime, timedelta
import openpyxl
from openpyxl.utils import get_column_letter
import pandas as pd
import os
import shutil

class Sala:
    def __init__(self, dia: int, semana: str, curso: str, sala: int, hora: list[str], n_hora: list[str]):
        self.dia = dia
        self.semana = semana
        self.curso = curso
        self.sala = sala
        self.hora = hora
        self.n_hora =n_hora

    def to_dict(self):
        return {
            "dia": self.dia,
            "semana": self.semana,
            "curso": self.curso,
            "sala": self.sala,
            "hora": self.hora,
            "n_hora": self.n_hora
        }

feira = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
n_hora = ['8:00-10:00', '10:00-12:00', '14:00-16:00', '16:00-18:00', '18:00-20:00', '20:00-22:00']

def ler_planilha_excel(bloco, filtro, js):
    try:
        dia_atual = datetime.today().weekday()
        
        salas = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dados = pd.read_excel(os.path.join(current_dir, 'dado.xlsx'), sheet_name=bloco)
        dados_excel = dados.fillna('Livre')
        if(filtro == True):
            dados_filtrados = dados_excel[dados_excel['Dia'] == dia_atual]
        else:
            dados_filtrados = dados_excel
        dados_filtrados = dados_filtrados[dados_filtrados['CURSO'] != 'Livre']
        #dados_final = dados_filtrados.drop('Dia', axis=1)

        for index, row in dados_filtrados.iterrows():

            dia = row['Dia']
            semana = feira[dia]
            curso = row['CURSO']
            sala = row['SALA']
            hora = [
                row['08:00-10:00'],
                row['10:00-12:00'],
                row['14:00-16:00'],
                row['16:00-18:00'],
                row['18:00-20:00'],
                row['20:00-22:00']
            ]

            
            # Criar uma instância de Sala
            nova_sala = Sala(dia, semana, curso, sala, hora, n_hora)
            salas.append(nova_sala)

            for hora in nova_sala.hora:
                # Pegar a posição atual da hora
                posicao_atual = nova_sala.hora.index(hora)
        
        if(js == True):
            return [sala.to_dict() for sala in salas]
        
        return salas
    
    except Exception as e:
        return f"Ocorreu um erro ao ler a planilha: {e}"

def get_Bloco(bloco):
    try:
        dia_atual = datetime.today().weekday()
        
        salas = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dados = pd.read_excel(os.path.join(current_dir, 'dado.xlsx'), sheet_name=bloco)

        dados_excel = dados.fillna('Livre')

        dados_filtrados = dados_excel[dados_excel['Dia'] == dia_atual]
        dados_filtrados = dados_filtrados[dados_excel['CURSO'] != 'Livre']

        for index, row in dados_filtrados.iterrows():

            dia = row['Dia']
            semana = feira[dia]
            curso = row['CURSO']
            sala = row['SALA']
            hora = [
                row['08:00-10:00'],
                row['10:00-12:00'],
                row['14:00-16:00'],
                row['16:00-18:00'],
                row['18:00-20:00'],
                row['20:00-22:00']
            ]

            
            # Criar uma instância de Sala
            nova_sala = Sala(dia, semana, curso, sala, hora, n_hora)
            salas.append(nova_sala)
        
        return salas, dia_atual
    
    except Exception as e:
        return f"Ocorreu um erro ao ler a planilha: {e}"

def get_Bloco_dia(bloco, dia):
    try:
        dia_atual = dia
        
        salas = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dados = pd.read_excel(os.path.join(current_dir, 'dado.xlsx'), sheet_name=bloco)
        dados_excel = dados.fillna('Livre')

        dados_filtrados = dados_excel[dados_excel['Dia'] == dia_atual]
        dados_filtrados = dados_filtrados[dados_excel['CURSO'] != 'Livre']

        for index, row in dados_filtrados.iterrows():

            dia = row['Dia']
            semana = feira[dia]
            curso = row['CURSO']
            sala = row['SALA']
            hora = [
                row['08:00-10:00'],
                row['10:00-12:00'],
                row['14:00-16:00'],
                row['16:00-18:00'],
                row['18:00-20:00'],
                row['20:00-22:00']
            ]

            
            # Criar uma instância de Sala
            nova_sala = Sala(dia, semana, curso, sala, hora, n_hora)
            salas.append(nova_sala)
        
        return salas
    
    except Exception as e:
        return f"Ocorreu um erro ao ler a planilha: {e}"   

def reset_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(os.path.join(current_dir, 'dados.xlsx'), os.path.join(current_dir, 'dado.xlsx'))

def get_next_weekday(target_weekday):
    today = datetime.now()

    days_ahead = int(target_weekday) - int(today.weekday())
    if days_ahead <= 0:  # Se já passou o dia da semana nesta semana
        days_ahead += 7
    return (today + timedelta(days=days_ahead)).strftime('%d/%m/%Y') + ' (' + feira[int(target_weekday)] + ')'