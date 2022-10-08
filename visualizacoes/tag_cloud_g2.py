import wordcloud as wd
import numpy as np
import pandas as pd
from os import path
from PIL import Image
import matplotlib.pyplot as plt

nome_arquivo = "informacoes_pink_floyd.xlsx"

def acessar_info(nome_arquivo: str, nome_folha: str, nome_coluna: str):
    """A função acessa o arquivo excel, a folha da informação pedida e a coluna
    para depois transformar em str e ir concatenando, colocando um espaço entre 
    as palavras e por fim retornando o texto final.

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param nome_folha:  Nome da folha do excel
    :type nome_folha: str
    :param nome_coluna:  Nome da coluna do excel
    :type nome_coluna: str
    :return: texto das informações pedidas
    :rtype: str
    """      
    informacao = pd.read_excel(nome_arquivo, nome_folha)
    informacao_concat = str()
    for informacao in informacao[nome_coluna]:
        soma = " " + informacao
        informacao_concat += soma
    return informacao_concat

def tag_cloud_1():
    """Função que faz a tag cloud da pergunta "Quais são as palavras mais comuns
    nos títulos dos Álbuns?". Usa a função "acessar_info" para entrar no excel e 
    retornar um texto. A função mascara a imagem para depois pegar o texto, 
    aplicar as tag clouds e gerar a imagem.
    """    
    texto = acessar_info(nome_arquivo, "albuns", "albuns")
    mask = np.array(Image.open("arquivos_relatorio/dark_side_of_the_moon.jpg"))
    word_cloud2 = wd.WordCloud(
        width=3000,
        height=2000,
        random_state=123,
        background_color="black",
        colormap="prism",
        collocations=False,
        stopwords=wd.STOPWORDS,
        mask=mask).generate(texto)

    word_cloud2.to_file("./arquivos_relatorio/tag_1.png")

def tag_cloud_2():
    """Função que faz a tag cloud da pergunta "Quais são as palavras mais comuns 
    nos títulos das músicas?". Usa a função "acessar_info" para entrar no excel 
    e retornar um texto. A função mascara a imagem para depois pegar o texto, 
    aplicar as tag clouds e gerar a imagem.
    """ 
    texto = acessar_info(nome_arquivo, "musicas", "musicas")
    mask = np.array(Image.open("arquivos_relatorio/pulse.jpg"))
    word_cloud2 = wd.WordCloud(
        width=3000,
        height=2000,
        random_state=123,
        background_color="black",
        colormap="cividis",
        collocations=False,
        stopwords=wd.STOPWORDS,
        mask=mask).generate(texto)

    word_cloud2.to_file("./arquivos_relatorio/tag_2.png")

def tag_cloud_3():
    """Função que faz a tag cloud da pergunta "Quais são as palavras mais comuns 
    nas letras das músicas, em toda a discografia?". Usa a função "acessar_info" 
    para entrar no excel e retornar um texto. A função mascara a imagem para 
    depois pegar o texto, aplicar as tag clouds e gerar a imagem.
    """  
    texto = acessar_info(nome_arquivo, "informacoes_musicas", "Letra")
    mask = np.array(Image.open("arquivos_relatorio/the_division_bell.jpg"))
    word_cloud2 = wd.WordCloud(
        width=3000,
        height=2000,
        random_state=123,
        background_color="black",
        colormap="ocean_r",
        collocations=False,
        stopwords=wd.STOPWORDS,
        mask=mask).generate(texto)

    word_cloud2.to_file("./arquivos_relatorio/tag_3.png")


"""Obs: As 3 funções acima são práticamente iguais, a diferença delas está nos 
arquivos e nas configurações de cada wordcloud.
"""
tag_cloud_1()
tag_cloud_2()
tag_cloud_3()