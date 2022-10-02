import funcoes_bonitinhas_teste as fbt
import pandas as pd
import openpyxl as op

def criar_arquivo_albuns_musicas():
    """
    Cria um arquivo excel com a relação entre os álbuns e músicas
    """
    planilha = op.Workbook()
    folha = planilha.active
    tuplas_album_musica = fbt.discografia("https://www.letras.mus.br/pink-floyd/discografia/", "tupla")
    for tupla in tuplas_album_musica:
        lista_album_musica = list(tupla)
        folha.append(lista_album_musica)
    planilha.save("albuns_musicas.xlsx")

def criar_arquivo_premiacoes():
    """
    Cria o csv com as premiações por álbum
    """    
    dataframe_premios = fbt.criar_df("album")
    dataframe_premios.reset_index(inplace = True)
    dataframe_premios.rename(columns = {"index": "album"}, inplace = True)
    dataframe_premios.to_csv("premiacoes.csv", index = False)

def criar_arquivo_informacoes_musicas():
    """
    Cria o csv com as informações coletadas das músicas
    """
    dataframe_musicas = fbt.criar_df("musicas")
    dataframe_musicas.reset_index(inplace = True)
    dataframe_musicas.rename(columns = {"index": "musicas"}, inplace = True)
    dataframe_musicas.to_csv("informacoes_musicas.csv", index = False)

def criar_arquivo_vendas():
    """
    Cria o csv com as informações de vendas dos álbuns
    """
    dataframe_vendas = fbt.criar_df("sales")
    dataframe_vendas.rename(columns = {"index": "album"}, inplace = True)
    dataframe_vendas.to_csv("vendas.csv", index = False)

criar_arquivo_albuns_musicas()
criar_arquivo_premiacoes()
criar_arquivo_informacoes_musicas()
criar_arquivo_vendas()
