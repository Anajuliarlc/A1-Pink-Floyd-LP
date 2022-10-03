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
                                 "IT", "TO", "PT."]
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
        titulos = pd.read_excel(nome_arquivo, nome_folha)
    except FileNotFoundError:
        return "Base de dados não encontrada"
    except ValueError:
        return "Tabela não encontrada"
    cont_palavras = dict()    
    #Divide a letra inteira em palavras
    for titulo in titulos[nome_coluna]:
        lista_palavras_titulo = re.split(" ", titulo)
        #Realiza a contagem das palavras
        for palavra in lista_palavras_titulo:
            palavra_uppercase = palavra.upper()
            if palavra_uppercase not in cont_palavras:
                cont_palavras[palavra_uppercase] = 1
            else:
                cont_palavras[palavra_uppercase] += 1
    #Retira palavras que não devem ser consideradas
    lista_excluidas = lista_palavras_excluidas()
    for palavra in lista_excluidas:
        if palavra in cont_palavras:
            del cont_palavras[palavra]
    return cont_palavras

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
    #Retira palavras que não devem ser consideradas
    lista_excluidas = lista_palavras_excluidas()
    for palavra in lista_excluidas:
        if palavra in cont_palavras:
            del cont_palavras[palavra]
    return cont_palavras

def letras_todas_musicas(nome_arquivo: str, nome_folha: str, nome_coluna: str):
    """Faz a contagem das palavras de todas as letras de música

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param nome_folha: Nome da folha do excel onde está a lista de letras
    :type nome_folha: str
    :param nome_coluna: Nome da coluna na folha onde está a lista de letras
    :type nome_coluna: str
    :return: Dicionário com a contagem das palavras
    :rtype: dict
    """
    try:
        informacoes_musicas = pd.read_excel(nome_arquivo, nome_folha)
    except FileNotFoundError:
        return "Base de dados não encontrada"
    except ValueError:
        return "Tabela não encontrada"
    lista_letras = list()
    for letra in informacoes_musicas[nome_coluna]:
        lista_letras.append(letra)
    return lista_letras

def pal_todas_musicas(nome_arquivo: str, nome_folha: str, nome_coluna: str):
    """Faz a contagem das palavras de todas as letras de música

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param nome_folha: Nome da folha do excel onde está a lista de letras
    :type nome_folha: str
    :param nome_coluna: Nome da coluna na folha onde está a lista de letras
    :type nome_coluna: str
    :return: Dicionário com a contagem das palavras
    :rtype: dict
    """    
    lista_letras = letras_todas_musicas(nome_arquivo, nome_folha, nome_coluna)
    cont_palavras = dict()
    for letra in lista_letras:
        palavras_letra = palavras_letra_musica(letra)
        for palavra in palavras_letra:
            if palavra not in cont_palavras:
                cont_palavras[palavra] = palavras_letra[palavra]
            else:
                cont_palavras[palavra] += palavras_letra[palavra]
    return cont_palavras

def dataframe_inf_album_musica(nome_arquivo: str, nome_folha_mus_alb: str,
                                nome_folha_inf_mus: str, nome_coluna_alb: str,
                                nome_coluna_mus: str):
    """Cria um dataframe com as informações das músicas indexadas por álbum

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param nome_folha_mus_alb: Nome da folha do excel onde está
        a relação músicas com álbuns
    :type nome_folha_mus_alb: str
    :param nome_folha_inf_mus:  Nome da folha do excel onde estão
        as informações das músicas
    :type nome_folha_inf_mus: str
    :param nome_coluna_alb: Nome da coluna na folha onde está a lista de álbuns
    :type nome_coluna_alb: str
    :param nome_coluna_mus: Nome da coluna na folha onde está
        a lista de músicas com letras
    :type nome_coluna_mus: str
    :return: Retorna um dataframe com as informações das músicas e
        multi-index de álbuns e músicas
    :rtype: pandas.core.frame.DataFrame
    """    
    df_mus_album = pd.read_excel(nome_arquivo, nome_folha_mus_alb)
    df_inf_mus = pd.read_excel(nome_arquivo, nome_folha_inf_mus)
    df_inf_alb_mus = pd.merge(df_mus_album, df_inf_mus, on = nome_coluna_mus)
    ind_albuns = df_inf_alb_mus[nome_coluna_alb]
    ind_musicas = df_inf_alb_mus[nome_coluna_mus]
    indices = pd.MultiIndex.from_arrays([ind_albuns, ind_musicas],
                                         names = (nome_coluna_alb,
                                                    nome_coluna_mus))
    df_inf_alb_mus.drop([nome_coluna_alb, nome_coluna_mus],
                         inplace=True,
                         axis=1)
    df_inf_alb_mus.set_index(indices, inplace = True)
    return df_inf_alb_mus

def letras_album(df_inf_alb_mus: pd.core.frame.DataFrame, nome_col_letras: str):
    """Cria um dicionário com as letras de músicas por álbum

    :param df_inf_alb_mus: Dataframe com as informações das músicas e
        multi-index de álbuns e músicas
    :type df_inf_alb_mus: pd.core.frame.DataFrame
    :param nome_col_letras: Nome da coluna onde estão as letras das músicas
    :type nome_col_letras: str
    :return: Dicionário com as letras das músicas de cada álbum
    :rtype: dict
    """
    albuns = list(df_inf_alb_mus.index.unique(0))
    df_letras = df_inf_alb_mus[nome_col_letras]
    dic_album_letras = dict()
    for album in albuns:
        mascara_album = df_letras.index.get_level_values(0) == album
        letras_album = list(df_letras[mascara_album])
        dic_album_letras[album] = letras_album
    return dic_album_letras

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

def top_3_pal_todas_musicas(nome_arquivo: str):
    """Retorna as 3 palavras mais comuns em todas letras de músicas

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Dataframe com as 3 palavras mais comuns nos titulos e sua contagem
    :rtype: pandas.core.frame.DataFrame
    """    
    dicionario = pal_todas_musicas(nome_arquivo, "informacoes_musicas", "Letra")
    top_3 = palavras_mais_comuns(dicionario)
    return top_3

def top_3_pal_albuns(nome_arquivo: str):
    """Retorna um dicionário com a chave sendo o nome dos álbuns
        e o valor um dataframe com as top 3 palavras das letras
        do álbum e sua contagem

    :param nome_arquivo:  Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Dicionário com dataframe de top 3 palavras por álbum
    :rtype: dict
    """    
    df_inf = dataframe_inf_album_musica(nome_arquivo, "albuns_musicas",
                                         "informacoes_musicas", "albuns",
                                         "musicas")
    dic_letras_alb = letras_album(df_inf, "Letra")
    dic_top_3_pal_album = dict()
    for album, letras in dic_letras_alb.items():
        #Une todas as letras em uma só string
        letra_total = str(letras)
        palavras = palavras_letra_musica(letra_total)
        top_3_pal = palavras_mais_comuns(palavras)
        dic_top_3_pal_album[album] = top_3_pal
    return dic_top_3_pal_album

def tit_alb_recorrente_letras(nome_arquivo: str):
    """Retorna um dicionário com a chave sendo o nome dos álbuns
        e o valor um dataframe com a contagem das palavras do título do
        álbum nas letras das músicas por álbum

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Dicionário com dataframe de contagem palavras do título do
        álbum nas letras das músicas por álbum
    :rtype: dict
    """    
    df_inf = dataframe_inf_album_musica(nome_arquivo, "albuns_musicas",
                                        "informacoes_musicas", "albuns",
                                        "musicas")
    dic_letras_alb = letras_album(df_inf, "Letra")
    dic_alb_cont_letras = dict()
    for titulo_alb, letras in dic_letras_alb.items():
        pal_titulo_alb = palavras_letra_musica(titulo_alb).keys()
        letra_alb_todo = str(letras)
        pal_let_alb_todo = palavras_letra_musica(letra_alb_todo)
        dic_pal_tit = {"palavra":[], "contagem":[]}
        for palavra in pal_titulo_alb:
            if palavra in pal_let_alb_todo:
                dic_pal_tit["palavra"].append(palavra)
                dic_pal_tit["contagem"].append(pal_let_alb_todo[palavra])
            else:
                dic_pal_tit["palavra"].append(palavra)
                dic_pal_tit["contagem"].append("0")
        df_pal_tit = pd.DataFrame(dic_pal_tit)
        dic_alb_cont_letras[titulo_alb] = df_pal_tit
    return dic_alb_cont_letras

def tit_mus_recorrente_letras(nome_arquivo: str):
    letras_mus = letras_todas_musicas(nome_arquivo, "informacoes_musicas",
                                        "Letra")
    dic_mus_cont_letras = dict()
    for musica, letra in letras_mus.items():
        pal_tit_mus = palavras_letra_musica(musica).keys()
        pal_letra = palavras_letra_musica(letra)
        dic_pal_tit = {"palavra":[], "contagem":[]}
        for palavra in pal_tit_mus:
            if palavra in pal_tit_mus:
                dic_pal_tit["palavra"].append(palavra)
                dic_pal_tit["contagem"].append(pal_letra[palavra])
            else:
                dic_pal_tit["palavra"].append(palavra)
                dic_pal_tit["contagem"].append("0")
        df_pal_tit_mus = pd.DataFrame(dic_pal_tit)
        dic_mus_cont_letras[musica] = df_pal_tit_mus
    return dic_mus_cont_letras    

print(tit_mus_recorrente_letras("../informacoes_pink_floyd.xlsx"))
#print(top_3_pal_albuns("../informacoes_pink_floyd.xlsx"))
#print(top_3_pal_todas_musicas("../informacoes_pink_floyd.xlsx"))
#print(top_3_pal_titulos_albuns("../informacoes_pink_floyd.xlsx"))
#print(top_3_pal_titulos_musicas("../informacoes_pink_floyd.xlsx"))
#print(dataframe_inf_album_musica("../informacoes_pink_floyd.xlsx", "albuns_musicas", "informacoes_musicas", "albuns", "musicas"))