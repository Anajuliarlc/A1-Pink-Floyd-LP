from ast import Return
from asyncio import streams
import pandas as pd
import re

def lista_palavras_excluidas():
    """Para fim de análise mais profundas a lista abaixo contêm as preposições
    e artigos mais comuns na língua inglesa que devem ser excluídas.
    Foram adicionadas também palavras que descrevem versões do álbum 
    (ex: PT. :(parte))

    :return: Retorna umas lista com as palavras que devem ser excluidas
    :rtype: list
    """
    lista_palavras_excluidas = ["A", "THE", "OF", "IN",
                                 "AT", "ON", "AN", "AND",
                                 "TO", "PT."]
    return lista_palavras_excluidas

def palavras_titulos(nome_arquivo: str, nome_folha: str, nome_coluna: str):
    """Faz a contagem das palavras nos títulos

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param nome_folha: Nome da folha do excel onde está a lista de títulos
    :type nome_folha: str
    :param nome_coluna: Nome da coluna na folha onde está a lista de títulos
    :type nome_coluna: str
    :return: Dicionário com a contagem das palavras
    :rtype: dict
    """
    try:
        nomes_albuns = pd.read_excel(nome_arquivo, nome_folha)
        cont_palavras = dict()
    except FileNotFoundError:
        return "Base de dados não encontrada"
    except ValueError:
        return "Tabela não encontrada"
    for titulo in nomes_albuns[nome_coluna]:
        lista_palavras_titulo = re.split(" ", titulo)
        for palavra in lista_palavras_titulo:
            palavra_uppercase = palavra.upper()
            if palavra_uppercase not in cont_palavras:
                cont_palavras[palavra_uppercase] = 1
            else:
                cont_palavras[palavra_uppercase] += 1
    lista_excluidas = lista_palavras_excluidas()
    for palavra in lista_excluidas:
        if palavra in cont_palavras:
            del cont_palavras[palavra]
    return cont_palavras

def palavras_mais_comuns(dicionario_palavras_contadas: dict):
    """A função recebe um dicionário de palavras e contagens
    e retorna um dataframe com as 3 palavras mais comuns

    :param dicionario_palavras_contadas: Dicionário com a contagem das palavras
    :type dicionario_palavras_contadas: dict
    :raises TypeError: Retorna uma mensagem se o argumento passado está errado
    :return: Dataframe com as 3 palavras mais comuns e sua contagem
    :rtype: pandas.core.frame.DataFrame
    """    
    if type(dicionario_palavras_contadas) != dict:
        raise TypeError("Não foi passado um dicionário")
    colunas = ["palavras", "contagem"]
    dados = list()
    for palavra, contagem in dicionario_palavras_contadas.items():
        palavra_contagem = [palavra, contagem]
        dados.append(palavra_contagem)
    df_palavras = pd.DataFrame(dados, columns = colunas)
    df_ordenado = df_palavras.sort_values(ascending = False,
                                            by = "contagem").copy()
    top_3 = df_ordenado.head(3)
    top_3.reset_index(inplace = True, drop = True)
    return top_3

def top_3_pal_titulos_albuns(nome_arquivo: str):
    """Retorna as 3 palavras mais comuns nos títulos dos albuns das musicas

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Dataframe com as 3 palavras mais comuns nos titulos e sua contagem
    :rtype: pandas.core.frame.DataFrame
    """    
    dicionario = palavras_titulos(nome_arquivo, "albuns", "albuns")
    top_3 = palavras_mais_comuns(dicionario)
    return top_3

def top_3_pal_titulos_musicas(nome_arquivo: str):
    """Retorna as 3 palavras mais comuns nos títulos dos albuns das musicas

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Dataframe com as 3 palavras mais comuns nos titulos e sua contagem
    :rtype: pandas.core.frame.DataFrame
    """    
    dicionario = palavras_titulos(nome_arquivo, "musicas", "musicas")
    top_3 = palavras_mais_comuns(dicionario)
    return top_3

print(top_3_pal_titulos_albuns("../informacoes_pink_floyd.xlsx"))
print(top_3_pal_titulos_musicas("../informacoes_pink_floyd.xlsx"))