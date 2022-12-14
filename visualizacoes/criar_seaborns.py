#As funções deverão ser rodadas somente na pasta principal
import sys

sys.path.insert(0, "../")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from respondendo_perguntas import respostas_grupo_3 as g3
from respondendo_perguntas import respostas_grupo_1 as g1

def graf_top_3_vis_mus(nome_arquivo: str, caminho_graficos: str):
    """Gera dois gráficos com as músicas mais vistas e menos vistas

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param caminho_graficos: Nome do caminho para arquivar os gráficos
    :type caminho_graficos: str
    """    
    dic_df = g1.top_3_vis_mus(nome_arquivo)

    nome_grafico_maiores = "graf_vis_mus_maiores.png"
    caminho_graf_maiores = caminho_graficos + nome_grafico_maiores

    df_mais_vistas = dic_df["Mais Vistas"]

    df_mais_vistas.reset_index(inplace=True)

    ax1 = sb.barplot(x = df_mais_vistas["index"],
                        y = df_mais_vistas["Exibições"] / 100000,
                        color = "blue",
                        )
    ax1.set_xticklabels(ax1.get_xticklabels(), size = 6)

    ax1.set(xlabel = "Músicas",
            ylabel = "Exibições (Milhões de Visualizações)",
            title = "Mais Visualizadas")

    fig = ax1.get_figure()

    fig.savefig(caminho_graf_maiores)

    #Reinicia a geração de gráficos
    plt.figure()

    nome_grafico_menores = "graf_vis_mus_menores.png"
    caminho_graf_menores = caminho_graficos + nome_grafico_menores

    df_menos_vistas = dic_df["Menos Vistas"]

    df_menos_vistas.reset_index(inplace=True)

    ax2 = sb.barplot(x = df_menos_vistas["index"],
                        y = df_menos_vistas["Exibições"],
                        color = "red")
    
    ax2.set_xticklabels(ax2.get_xticklabels(), size = 6)
    
    ax2.set(xlabel = "Músicas",
            ylabel = "Exibições (Visualizações)",
            title = "Menos Visualizadas")
    fig = ax2.get_figure()

    fig.savefig(caminho_graf_menores)

    #Reinicia a geração de gráficos
    plt.figure()

def graf_top_3_dur_mus(nome_arquivo: str, caminho_graficos: str):
    """Gera dois gráficos com as músicas mais duradouras e menos duradouras

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param caminho_graficos: Nome do caminho para arquivar os gráficos
    :type caminho_graficos: str
    """    
    df_inf_mus = pd.read_excel(nome_arquivo, "informacoes_musicas")
    nome_col_dur = "Duração"
    nome_col_mus = "musicas"
    df_inf_mus_ord = df_inf_mus.sort_values(ascending = False,
                                             by = nome_col_dur).copy()
    head_3 = df_inf_mus_ord.copy().head(3)
    tail_3 = df_inf_mus_ord.copy().tail(3)

    nome_grafico_maiores = "graf_dur_mus_maiores.png"
    caminho_graf_maiores = caminho_graficos + nome_grafico_maiores

    ax1 = sb.barplot(x = head_3[nome_col_mus],
                        y = head_3[nome_col_dur],
                        color = "blue",
                        )
    ax1.set_xticklabels(ax1.get_xticklabels(), size = 6)

    ax1.set(xlabel = "Músicas",
            ylabel = "Minutos",
            title = "Mais Duradouras")

    fig = ax1.get_figure()

    fig.savefig(caminho_graf_maiores)

    #Reinicia a geração de gráficos
    plt.figure()

    nome_grafico_menores = "graf_dur_mus_menores.png"
    caminho_graf_menores = caminho_graficos + nome_grafico_menores

    ax2 = sb.barplot(x = tail_3[nome_col_mus],
                        y = tail_3[nome_col_dur],
                        color = "red")

    ax2.set_xticklabels(ax2.get_xticklabels(), size = 6)
    
    ax2.set(xlabel = "Músicas",
            ylabel = "Segundos",
            title = "Menos Duradouras")
    fig = ax2.get_figure()

    fig.savefig(caminho_graf_menores)

    #Reinicia a geração de gráficos
    plt.figure()

def graf_dur_vis(nome_arquivo: str, caminho_graficos: str):
    """Gera um gráfico com a relação entre a duração da música
        e o número de visualizações

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param caminho_graficos: Nome do caminho para arquivar os gráficos
    :type caminho_graficos: str
    """    
    df = pd.read_excel(nome_arquivo, "informacoes_musicas")

    nome_grafico = "graf_dur_vis.png"
    caminho_graf = caminho_graficos + nome_grafico

    df.reset_index(inplace=True)

    ax = sb.scatterplot(x = df["Duração"]/100,
                        y = df["Exibições"]/ 1000000,
                        color = "black", markers=False)

    ax.set(xlabel = "Duração (minutos)",
            ylabel = "Exibições (Milhões de Visualizações)")
    fig = ax.get_figure()
    fig.savefig(caminho_graf)

    #Reinicia a geração de gráficos
    plt.figure()


def graf_var_letra_mus(nome_arquivo: str, caminho_graficos: str):
    """Gera um gráfico da relação entre o número de palavras
        e número de palavras diferentes nas músicas

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param caminho_graficos: Nome do caminho para arquivar os gráficos
    :type caminho_graficos: str
    """
    df = g3.var_letra_mus(nome_arquivo)
    nome_grafico = "graf_var_letra_mus.png"
    caminho_graf = caminho_graficos + nome_grafico

    df.reset_index(inplace=True)

    ax = plt.subplots()
    ax = sb.scatterplot(x = df["N°Palavras"],
                        y = df["N°Palavras Diferentes"],
                        color = "black")

    df.sort_values(by="N°Palavras Diferentes",
                   ascending=False, inplace=True)
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

    ax.set(xlabel = "N° Palavras", ylabel = "N° Palavras Diferentes")
    fig = ax.get_figure()
    fig.savefig(caminho_graf)

    #Reinicia a geração de gráficos
    plt.figure()

def graf_alb_decada(nome_arquivo: str, caminho_graficos: str):
    """Gera um gráfico da relação de álbuns lançados por década

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param caminho_graficos: Nome do caminho para arquivar os gráficos
    :type caminho_graficos: str
    """    
    df = g3.albuns_decada(nome_arquivo)
    df.reset_index(inplace = True)
    nome_grafico = "graf_alb_decada.png"
    caminho_graf = caminho_graficos + nome_grafico

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

    ax.set(xlabel = "Década", ylabel = "N° Álbuns Lançados")

    fig = ax.get_figure()
    fig.savefig(caminho_graf)

    #Reinicia a geração de gráficos
    plt.figure()

def gerar_todos_graficos(nome_arquivo: str, caminho_graficos: str):
    """Gera todos os gráficos necessários para o relatório na pasta indicada

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :param caminho_graficos: Nome do caminho para arquivar os gráficos
    :type caminho_graficos: str
    """    
    graf_top_3_vis_mus(nome_arquivo, caminho_graficos)
    graf_top_3_dur_mus(nome_arquivo, caminho_graficos)
    graf_dur_vis(nome_arquivo, caminho_graficos)
    graf_var_letra_mus(nome_arquivo, caminho_graficos)
    graf_alb_decada(nome_arquivo, caminho_graficos)
    graf_alb_decada(nome_arquivo, caminho_graficos)
