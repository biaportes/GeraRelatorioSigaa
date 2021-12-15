#
# main.py : Uma solução para o problema de geração de relatório de acompanhamento de notas dos alunos
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação
import pandas as pd
import manipulaarquivos as man_arq
import calculanotas as calcNota
import calculafrequencia as calcFreq
import os

if __name__ == '__main__':

    for i in range(1, 4):
        pasta = "ano" + str(i)
        if not os.path.exists(pasta):
            os.mkdir(pasta)

    #ETAPAS
    #1) Gero os relatórios no Sigaa em HTML e salvo nas respectivas pastas referentes ao ano do técnico: ano1, ano2 e ano3
    #   Dá pra usar o Selenium/Python pra fazer isso, mas não fiz.

    print('''Olá! Antes de tudo, lembre-se de salvar o último arquivo de conselho de classe nas respectivas pastas!
    - 1º ano: pasta ano1
    - 2º ano: pasta ano2
    - 3º ano: pasta ano3

    ATENÇÃO! Os arquivos de conselho de classe gerados pelo Sigaa devem ser salvos como HTML.
    ''')
    input("SE ESTIVER TUDO PRONTO, APERTE ENTER!")

    trimestre = int(input("\n\nEm qual trimestre estamos? (1, 2 ou 3)"))

    limiarReprovFreq = calcFreq.calculaLimiarPerigoReprovacaoFreq(trimestre)

    print(limiarReprovFreq)


    for ano in range(1, 4):
        #2) Altero a variável 'path' para dizer qual a pasta eu quero que a análise seja feita
        pasta = "ano" + str(ano) + "/"
        man_arq.atualizaPath(pasta)

        #3) Gerará o CSV destes arquivos HTML
        man_arq.abreArquivoHTML()

        df = man_arq.abreArquivoCSV()

        listaFreqTodosAlunos = calcFreq.somaFaltas(df, limiarReprovFreq[ano-1], trimestre)

        #Gera arquivo na pasta com os nomes das disciplinas daquele ano
        man_arq.geraArquivoComNomeDisciplinas(df)

        #5) Lê os nomes das disciplinas daquele ano
        disciplinas = man_arq.todasDisciplinas()
        disc = disciplinas[0]
        #Retirei o '\n' da 1ª disciplina
        disc = disc[:-1]


        arqSaida = df.loc[1:,'NOME'] #nomes alunos

        #Inicio a junção dos arquivos CSVs para cada disciplina
        for disc in disciplinas:
            disc = disc[:-1] #Retirei o '\n' da 1ª disciplina
            arqAux = calcNota.media(df, disc)
            arqSaida = pd.concat([arqSaida,arqAux],axis=1 )
            arqSaida = arqSaida.rename(columns={ disc +'.3': disc})

        arqSaida = pd.concat([arqSaida, listaFreqTodosAlunos], axis=1)

        man_arq.geraSaida(arqSaida, "somaDasFaltasEMedias.csv")


        print("Arquivos gerados! Confira nas pastas.")
