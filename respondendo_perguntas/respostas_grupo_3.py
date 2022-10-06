import pandas as pd
import re

def palavras_letra_musica(letra_musica: str):
    """Faz a contagem das palavras na letra de música

    :param letra_musica: Letra inteira da música
    :type letra_musica: str
    :return: Dicionário com a contagem das palavras
    :rtype: dict
    """ 
    #Retira os caracteres que não são considerados parte da palavra
    lista_especiais = ["[", "]", "\"", "'", ":", "!",
                         "?", ",", "(", ")", ".", "\\"]
    for especial in lista_especiais:
        letra_musica = letra_musica.replace(especial, "")
    #Divide a letra inteira em palavras
    lista_palavras = re.split("\s+", letra_musica)
    cont_palavras = dict()
    #Realiza a contagem das palavras
    for palavra in lista_palavras:
        palavra_uppercase = palavra.upper()
        if palavra_uppercase not in cont_palavras:
            cont_palavras[palavra_uppercase] = 1
        else:
            cont_palavras[palavra_uppercase] += 1
    return cont_palavras

#Variaedade de Palavras Nas Músicas
def var_letra_mus(nome_arquivo: str):
    """Cria um Dataframe com o número de palavras e a razao de
        número de palavras / número de palavras diferentes para
        ser utilizado na criação de um gráfico com essa relação

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Dataframe com o número de palavras e a razao de
        número de palavras / número de palavras diferentes
    :rtype: pandas.core.frame.DataFrame
    """    
    df = pd.read_excel(nome_arquivo, "informacoes_musicas")
    lista_letras = list(df["Letra"])
    lista_n_pal = list()
    lista_razoes = list()
    for letra in lista_letras:
        pal_letra = palavras_letra_musica(letra)
        n_pal = len(pal_letra.keys())
        n_pal_dif = sum(pal_letra.values())
        razao = n_pal / n_pal_dif
        razao = round(razao, 2)
        lista_n_pal.append(n_pal)
        lista_razoes.append(razao)
    col_n_pal = "N°Palavras"
    col_razao = "Razao N°Pal/N°Pal Diferentes"
    novas_colunas = {col_n_pal: lista_n_pal,
                     col_razao: lista_razoes}
    lista_musicas = list(df["musicas"])
    df_novas_colunas = pd.DataFrame(novas_colunas, index = lista_musicas)
    return df_novas_colunas

#print(var_letra_mus("informacoes_pink_floyd.xlsx"))