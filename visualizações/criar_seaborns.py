import sys

sys.path.insert(0, "../")

from respondendo_perguntas import respostas_grupo_1 as g1
from respondendo_perguntas import respostas_grupo_2 as g2
from respondendo_perguntas import respostas_grupo_3 as g3
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

def graf_alb_decada(nome_arquivo: str):
    """Gera um gráfico da relação de álbuns lançados por década

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Nome do arquivo da imagem gerada
    :rtype: str
    """    
    df = g3.albuns_decada(nome_arquivo)
    df.reset_index(inplace = True)
    nome_grafico = "graf_alb_decada.png"
    caminho_graf = "../arquivos_relatorio/" + nome_grafico

    ax = plt.subplots()
    ax = sb.barplot(x = df["index"],
                    y = df["N° Álbuns"],
                    color = "black")
    
    maximo = max(df["N° Álbuns"])
    lista_menores_max = list(df["N° Álbuns"])
    lista_menores_max.remove(maximo)

    df = df.replace(lista_menores_max, 0)
    ax = sb.barplot(x = df["index"],
                    y = df["N° Álbuns"],
                    color = "blue")

    ax.set(xlabel="Década", ylabel="N° Álbuns Lançados")

    fig = ax.get_figure()
    fig.savefig(caminho_graf)
    
    return nome_grafico

print(graf_alb_decada("../informacoes_pink_floyd.xlsx"))                       