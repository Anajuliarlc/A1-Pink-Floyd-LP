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

"""
Os arquivos foram unidos em somente um excel,
com padronização de dados manual(como nome de musicas ou albuns diferentes)
e utilização de funções do excel para facilitar esse processo

Informações faltantes foram pesquisadas a mão na internet
Informações adicionadas:

relação album-musica

album musica
Barrett	Baby Lemonade
Concept Album	Breakthrough
Showing Feelings	Call The Schoolmaster
Barrett	Golden Hair
Hey Hey Rise Up	Hey Hey Rise Up
The Wall	Late Night
Barrett	Let's Roll Another One
The Early Years	Lucy Leave
The Piper at the Gates of Dawn	Matilda Mother (2010 Mix)
London 666	Nick's Boogie
Barrett	No Good Trying
Barrett	Octupus
Barrett	One In a Million
Barrett	Opel
Point Me At The Sky	Point Me At The Sky
Wish You Were Here	Raving And Drooling
The Early Years	Scream Thy Last Scream
The Early Years	Seabirds
Barrett	Swan Lee (Silas Lang)
The Division Bell	The Division Bell
The Final Cut	The Hero's Return (Pt. 2)
The Return Of The Son Of Nothing	The Return Of The Son Of Nothing
Barrett	Two Of a Kind
Live at the Roundhouse	Vegetable Man
Barrett	Wolfpack
Wish You Were Here	You Gotta Be Crazy

Albuns Acrescentados:

A NICE PAIR	
IS THERE ANYBODY OUT THERE? THE WALL: LIVE 1980-1981
Shine On
Discovery
"""