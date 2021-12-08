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
    #1) Gero os relatórios no Sigaa em HTML com os nomes 1t.html, 2t.html e 3t.html (salvo nas respectivas pastas referentes ao ano do técnico: ano1, ano2 e ano3)
    #   Dá pra usar o Selenium/Python pra fazer isso, mas não fiz.

    print('''Olá! Antes de tudo, lembre-se de salvar os arquivos de conselho de classe nas respectivas pastas!
    - 1º ano: pasta ano1
    - 2º ano: pasta ano2
    - 3º ano: pasta ano3

    ATENÇÃO! Os arquivos de conselho de classe gerados pelo Sigaa devem ser salvos com o seguinte padrão:
                   <número do trimestre> + 't.html'
    \tExemplo, se estivermos no 2º trimestre, você deve salvar os arquivos de conselho de classe da seguinte forma:
    \t\t dentro da pasta ano1: 1t.html e 2t.html
    \t\t dentro da pasta ano2: 1t.html e 2t.html
    \t\t dentro da pasta ano3: 1t.html e 2t.html''')
    input("SE ESTIVER TUDO PRONTO, APERTE ENTER!")

    trimestre = int(input("Em qual trimestre estamos? (1, 2 ou 3)"))

    for ano in range(1, 4):
        #2) Altero a variável 'path' para dizer qual a pasta eu quero que a análise seja feita
        pasta = "ano" + str(ano) + "/"
        man_arq.atualizaPath(pasta)

        #3) Gerará o CSV destes arquivos HTML (seja por trimestre (3 arquivos) ou para o trimestre em específico (1 arquivo apenas))
        for i in range(1, trimestre + 1):
            man_arq.abreArquivoInicialHTML(i)

        #4) Inicia-se a etapa de junção e análise dos CSVs (seja por trimestre (3 arquivos) ou para o trimestre em específico (1 arquivo apenas))
        listaDeDadosDeCadaTrimestre = [] #Lita de dados referentes a cada trimestre do ano escolhido
        for i in range(1, trimestre + 1):
            df = man_arq.abreArquivo(i)
            listaDeDadosDeCadaTrimestre.append(df)

        listaFreqTodosAlunos = calcFreq.somaFaltas(listaDeDadosDeCadaTrimestre[trimestre-1])

        #Gera arquivo na pasta com os nomes das disciplinas daquele ano
        man_arq.geraArquivoComNomeDisciplinas(listaDeDadosDeCadaTrimestre[trimestre-1])

        #5) Lê os nomes das disciplinas daquele ano
        disciplinas = man_arq.todasDisciplinas()
        disc = disciplinas[9]

        #Retirei o '\n' de uma disciplina qqr. No caso, a disciplina 9 da lista do arquivo .txt
        disc = disc[:-1]



        #Fiz a análise de tudo, mas pode ser melhorado só para pegar a coluna nome.
        discdf = calcNota.maiorNota(listaDeDadosDeCadaTrimestre, disc)
        arqSaida = discdf['NOME']

        #Inicio a junção dos arquivos CSVs para cada disciplina
        for disc in disciplinas:
            disc = disc[:-1]
            discdf = calcNota.maiorNota(listaDeDadosDeCadaTrimestre, disc)
            colunatotalapenas = calcNota.colunaTotal(discdf, disc)
            arqSaida = pd.concat([arqSaida,colunatotalapenas],axis=1 )

        arqSaida.insert(1, "FALTAS", listaFreqTodosAlunos, True)
        man_arq.geraSaida(arqSaida, "arquivototalanodisc.csv")


    print("Arquivos gerados! Confira nas pastas.")

#6)Formato a tabela gerada (arquivototalanodisc.csv)
#   - Abro o CSV no Calc (Libre Office)
#   - Menu Editar/Localizar-substituir '.' por ','. Isso irá fazer com que a planinha reconheça os números de ponto flutuante, já que ela usa ','. Essa transformação pode ser feita via código
#   - Altero a precisão para 2 casas decimais. Isso pode ser feito por código
#   - Faço a formatação lógica para colorir de:
#       - vermelho: notas abaixo de 9 (reprovado)
#       - azul:     notas abaixo de 17,85 (final)
#       - verde:    notas entre 17,85 e 17,99 (inconsistências do Sigaa)
