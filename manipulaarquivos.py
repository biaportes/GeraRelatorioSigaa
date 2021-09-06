#
# manipulaarquivos.py : Responsável por abrir os arquivos do Sigaa, bem como gerar as saídas CSV e TXT
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Professora Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação

import pandas as pd

path = ""

def atualizaPath(p):
    global path
    path = p

def abreArquivoInicialHTML(num):
    caminho = path + str(num) + 't.html'
    table = pd.read_html(caminho)
    df = table[0]
    df = pd.DataFrame(df)
    df = df.rename(columns={"Unnamed: 1_level_0": 'NOME'})
    geraSaidaAuxiliarCSV(df, num)


def abreArquivo(num):
    caminho = path + str(num) + 't.csv'
    table = pd.read_csv(caminho)
    df = pd.DataFrame(table)

    return df

def todasDisciplinas():
    caminho = path + "nomes_disciplinas.txt"
    with open(caminho) as file:
        discs = file.readlines()
    return discs

def geraSaidaAuxiliarCSV(df, num):
    caminho = path + str(num)+'t.csv'
    df.to_csv(caminho)

def geraSaida(df, texto):
    caminho = path + texto
    df.to_csv(caminho)


'''
def disciplinasss(df):
    with open("disciplinas1oano") as file:
        disciplinas = file.readlines()
    todasNotas=pd.DataFrame(df.set_index(('Unnamed: 1_level_0', 'Unnamed: 1_level_1')), columns=[('Unnamed: 1_level_0', 'Unnamed: 1_level_1')])
    for disc in disciplinas:
        disc = disc[:-1]
        nota = pd.DataFrame(df.set_index(('Unnamed: 1_level_0', 'Unnamed: 1_level_1')), columns=[(disc, 'N1')])
        recupera = pd.DataFrame(df.set_index(('Unnamed: 1_level_0', 'Unnamed: 1_level_1')), columns=[(disc, 'R')])
        for i in range(nota.shape[0]):
            if nota[(disc, 'N1')][i] < recupera[(disc, 'R')][i]:
                nota[(disc, 'N1')][i] = recupera[(disc, 'R')][i]
        todasNotas = todasNotas.join(nota)

    man_arq.geraSaida(todasNotas)
'''
