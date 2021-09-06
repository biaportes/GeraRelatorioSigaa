#
# calculanotas.py : Responsável por efetuar os cálculos com as notas dos alunos
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Professora Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação

import pandas as pd

def maiorNota(dfs, disc):
    todasNotasDisc=dfs[0].loc[1:,'NOME']

    cont = 1
    for df in dfs:
        nota = df.loc[1:, disc ]
        recupera = df.loc[1: , disc+'.1']
        #nota[0] = 'N'+str(cont)

        for i in range(1,nota.shape[0]+1):
            if nota[i] == '-':
                nota[i] = 0

            if recupera[i] == '-':
                recupera[i] = 0

            if float(nota[i]) < float(recupera[i]):
                if float(recupera[i]) > 6 :
                    nota[i] = 6
                else:
                    nota[i] = float(recupera[i])
            else:
                nota[i] = float(nota[i])

        try:
            nota = pd.to_numeric(nota, downcast='float')
        except:
            print(nota)
            print(i)
        todasNotasDisc = pd.concat([todasNotasDisc,nota], axis=1)
        cont+=1

    todasNotasDisc['TOTAL'] = todasNotasDisc.sum(axis =1)

    return todasNotasDisc

def abaixoMedia(df):
    df = df[df['TOTAL'] < 18]
    return df

def colunaTotal(df, disc):
    total = df[['NOME','TOTAL']]

    total = total.rename(columns={ "TOTAL": disc})

    return total[disc]
