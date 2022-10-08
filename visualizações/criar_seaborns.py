import sys

sys.path.insert(0, "../")

from respondendo_perguntas import respostas_grupo_1 as g1
from respondendo_perguntas import respostas_grupo_2 as g2
from respondendo_perguntas import respostas_grupo_3 as g3
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

def graf_dur_vis(nome_arquivo: str):
    df = pd.read_excel(nome_arquivo, "informacoes_musicas")

    nome_grafico = "graf_dur_vis.png"
    caminho_graf = "../arquivos_relatorio/" + nome_grafico

    df.reset_index(inplace = True)

    ax = sb.scatterplot(x = df["Duração"],
                         y = df["Exibições"],
                         color = "black", markers = False) 

    ax.set(xlabel = "Duração", ylabel = "Exibições")
    fig = ax.get_figure()
    fig.savefig(caminho_graf)

    return nome_grafico

print(graf_dur_vis("../informacoes_pink_floyd.xlsx"))

def graf_var_letra_mus(nome_arquivo: str):
    """Gera um gráfico da relação entre o número de palavras
        e número de palavras diferentes nas músicas

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Nome do arquivo da imagem gerada
    :rtype: str
    """    
    df = g3.var_letra_mus(nome_arquivo)
    nome_grafico = "graf_var_letra_mus.png"
    caminho_graf = "../arquivos_relatorio/" + nome_grafico

    df.reset_index(inplace = True)

    ax = plt.subplots()
    ax = sb.scatterplot(x = df["N°Palavras"],
                         y = df["N°Palavras Diferentes"],
                         color = "black")

    df.sort_values(by = "N°Palavras Diferentes",
                     ascending = False, inplace = True)
    df_musica_max = df.copy().head(1)

    maximo = max(df["N°Palavras Diferentes"])
    lista_menores_max = list(df["N°Palavras Diferentes"])
    lista_menores_max.remove(maximo)

    df = df.replace(lista_menores_max, None)

    ax = sb.scatterplot(x = df["N°Palavras"],
                         y = df["N°Palavras Diferentes"],
                         color = "blue")
    ax.invert_yaxis()

    musica_max = str(df_musica_max["index"].values)
    musica_max_x = int(df_musica_max["N°Palavras"].values)
    musica_max_y = int(df_musica_max["N°Palavras Diferentes"].values)
    ax.annotate(musica_max, (musica_max_x - 50, musica_max_y - 30))  

    ax.set(xlabel="N° Palavras", ylabel="N° Palavras Diferentes")
    fig = ax.get_figure()
    fig.savefig(caminho_graf)

    return nome_grafico

#print(graf_var_letra_mus("../informacoes_pink_floyd.xlsx"))  

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
                      