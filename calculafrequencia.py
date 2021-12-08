#
# calculanotas.py : Responsável por efetuar os cálculos das frequências dos alunos
# Github    : https://github.com/biaportes/GeraRelatorioSigaa
# data      : 20/03/2021
# autora    : Bianca Portes de Castro,
#            IFSEMG/DACC/Ciência da Computação

def somaFaltas(dadosUltimoTrimestre):
    alunos = dadosUltimoTrimestre.shape[0]
    colunas = dadosUltimoTrimestre.shape[1]
    listaFreqTodosAlunos = []
    for i in range(1, alunos):
        linhaAluno = dadosUltimoTrimestre.iloc[i]
        freqAlunoTotal = 0
        for j in range(6, colunas, 4): #Primeira coluna da frequência é a 6, próxima é a 10, ...
            freqAlunoTotal+= int(linhaAluno[j])
        nome = linhaAluno[2]
        listaFreqTodosAlunos.append(freqAlunoTotal)

    return listaFreqTodosAlunos
