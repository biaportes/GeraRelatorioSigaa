#
# manipulaarquivos.py : Responsável por abrir os arquivos do Sigaa, bem como gerar as saídas CSV e TXT
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação

import pandas as pd
import os

path = ""

def atualizaPath(p):
    global path
    path = p

def abreArquivoHTML():
    arquivos = [_ for _ in os.listdir(path) if _.endswith(".html")]
    if (len(arquivos) > 1) or (len(arquivos) == 0) :
        try:
            raise KeyboardInterrupt
        finally:
            print("#"*50)
            print('''
            ATENÇÃO!!!

            Deixe apenas UM arquivo .HTML referente ao conselho na pasta ''', path, "\n\n")

            print("#"*50)

    caminho = path + arquivos[0]
    table = pd.read_html(caminho)
    df = table[0]
    df = pd.DataFrame(df)
    df = df.rename(columns={"Unnamed: 1_level_0": 'NOME'})
    geraArquivoCSV(df, caminho[:-4] + "csv" )

def geraArquivoCSV(df, caminho):
    #apaga arquivos .csv que estejam na pasta
    arquivos = [_ for _ in os.listdir(path) if _.endswith(".csv")]
    for csv in arquivos:
        os.remove(path + csv)

    #cria o arquivo csv
    df.to_csv(caminho)

def abreArquivoCSV():
    arquivos = [_ for _ in os.listdir(path) if _.endswith(".csv")]

    if (len(arquivos) > 1) or (len(arquivos) == 0) :
        try:
            raise KeyboardInterrupt
        finally:
            print("#"*50)
            print('''
            Não conseguiu localizar o arquivo .CSV correto em ''', path, "\n\n")

            print("#"*50)

    caminho = path + arquivos[0]
    table = pd.read_csv(caminho)
    df = pd.DataFrame(table)

    return df


def geraArquivoComNomeDisciplinas(ultimoTrimestre):
    nomes = ultimoTrimestre.iloc[0].index
    aux = sorted(set(nomes[4:]))
    for i in range(1, len(aux)):
        if (i%4 == 0):
            continue
        aux[i] = aux[i][:-2]

    nomes = sorted(set(aux))
    with open(path+"/nomes_disciplinas.txt", 'w') as file:
        for n in nomes:
            file.write(n + "\n")
        file.close()

def todasDisciplinas():
    caminho = path + "nomes_disciplinas.txt"
    with open(caminho) as file:
        discs = file.readlines()
    return discs

def geraSaida(df, texto):
    caminho = path + texto
    df.to_csv(caminho)
    
'''
def abreArquivoInicialHTML(num):
    caminho = path + str(num) + 't.html'
    table = pd.read_html(caminho)
    df = table[0]
    df = pd.DataFrame(df)
    df = df.rename(columns={"Unnamed: 1_level_0": 'NOME'})
    geraSaidaAuxiliarCSV(df, num)

def abreArquivoNum(num):
    caminho = path + str(num) + 't.csv'
    table = pd.read_csv(caminho)
    df = pd.DataFrame(table)

    return df



def geraSaidaAuxiliarCSV(df, num):
    caminho = path + str(num)+'t.csv'
    df.to_csv(caminho)


'''
