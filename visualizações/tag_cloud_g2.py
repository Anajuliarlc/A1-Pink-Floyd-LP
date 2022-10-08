from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from os import path
import re


#Quais são as palavras mais comuns nos títulos dos Álbuns?

nome_arquivo = "informacoes_pink_floyd.xlsx"

def pergunta_1(nome_arquivo, nome_folha, nome_coluna):
    titulos = pd.read_excel(nome_arquivo, nome_folha)
    titulos_concat = str()
    for titulo in titulos[nome_coluna]:
        soma = " " + titulo
        titulos_concat += soma
    return titulos_concat


def tag_1(texto):
    wc = WordCloud(
        background_color="black",
        height= 600,
        width= 400
    )
    wc.generate(texto)
    wc.to_file("tag_1.png")
    
pergunta_1(nome_arquivo, "albuns", "albuns")
#tag_1(pergunta_1(nome_arquivo, "albuns", "albuns"))

from PIL import Image

def tag_1pf(texto):
    mask = np.array(Image.open("./arquivos_relatorio/pf_darksidemod.png"))
    mask_wc = WordCloud(background_color="black", max_words=2000, mask = mask, contour_width=3, contour_color='steelblue')
    mask_wc.generate(texto)
    mask_wc.to_file("./arquivos_relatorio/tag_1m.png")

tag_1pf(pergunta_1(nome_arquivo, "albuns", "albuns"))