import pandas as pd
path = "ano1/"

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
        
    geraSaida(todasNotas)
'''
def todasDisciplinas():
    caminho = path + "nomes_disciplinas.txt"
    with open(caminho) as file:
        discs = file.readlines()
    return discs

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


    
if __name__ == '__main__':
    passo = 1
    #
    path = "ano1/"
    
    #ETAPAS
    #1) Gero os relatórios no Sigaa em HTML com os nomes 1t.html, 2t.html e 3t.html (salvo nas respectivas pastas referentes ao ano do técnico: ano1, ano2 e ano3)
    #   Dá pra usar o Selenium/Python pra fazer isso, mas não fiz.
    #2) Altero a variável 'path' para dizer qual a pasta eu quero que a análise seja feita 
    #3) Altero a variável 'passo' para ZERO. Assim, entrará nesse if e gerará o CSV destes arquivos
    if passo == 0:
        abreArquivoInicialHTML(1)
        abreArquivoInicialHTML(2)
        abreArquivoInicialHTML(3)
    
    #4) Após essa etapa, eu altero nos arquivos de saída CSV a célula C1 para 'NOME'
    #   Dá pra fazer isso no código, mas não fiz.

    #5) Altero a variável 'passo' para UM. Assim, inicia-se a etapa de junção e análise dos CSVs
    #   Dá pra automatizar tudo isso, mas não fiz pois tive q testar vários módulos separados, então assim ficou melhor nessa etapa
    else:
        df1 = abreArquivo(1)
        df2 = abreArquivo(2)
        df3 = abreArquivo(3)
        
        #Aqui estão os dados referentes a cada trimestre do ano escolhido
        dfs=[df1, df2, df3]
        
        #6) Deve existir um arquivo na pasta com os nomes das disciplinas daquele ano
        disciplinas = todasDisciplinas()
        disc = disciplinas[9]
        
        #Retirei o '\n'
        disc = disc[:-1]

        #Fiz a análise de tudo, mas pode ser melhorado só para pegar a coluna nome.
        discdf = maiorNota(dfs, disc)
        nome = discdf['NOME']    
        
        #Inicio a junção dos arquivos CSVs para cada disciplina
        for disc in disciplinas:
            disc = disc[:-1]
            discdf = maiorNota(dfs, disc)
            colunatotalapenas = colunaTotal(discdf, disc)
            nome = pd.concat([nome,colunatotalapenas],axis=1 )

        geraSaida(nome, "arquivototalanodisc.csv")

    #7)Formato a tabela gerada (arquivototalanodisc.csv) 
    #   - Abro o CSV no Calc
    #   - Menu Editar/Localizar-substituir '.' por ','. Isso irá fazer com que a planinha reconheça os números de ponto flutuante, já que ela usa ','. Essa transformação pode ser feita via código
    #   - Altero a precisão para 2 casas decimais. Isso pode ser feito por código
    #   - Faço a formatação lógica para colorir de:
    #       - vermelho: notas abaixo de 9 (reprovado)
    #       - azul:     notas abaixo de 17,85 (final)
    #       - verde:    notas entre 17,85 e 17,99 (inconsistências do Sigaa)

    


