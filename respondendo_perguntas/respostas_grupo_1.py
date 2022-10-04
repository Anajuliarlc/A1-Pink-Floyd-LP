import pandas as pd
import re

def dataframe_inf_alb_mus(nome_arquivo: str, nome_folha_mus_alb: str,
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

def top_3_vis_mus_alb(nome_arquivo: str):
    """Cria um dicionário que possui as músicas mais ouvidas
        e menos ouvidas por album e seu número de visualizações

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type df_inf_alb_mus: str
    :return: Dicionário com dataframes de músicas mais ouvidas
        e menos ouvidas por album
    :rtype: dict
    """
    df_inf_alb_mus = dataframe_inf_alb_mus(nome_arquivo,
                                             "albuns_musicas",
                                             "informacoes_musicas",
                                             "albuns",
                                             "musicas")
    nome_col_vis = "Exibições"
    albuns = list(df_inf_alb_mus.index.unique(0))
    df_alb_mus_ord = df_inf_alb_mus.sort_values(ascending = False,
                                                 by = nome_col_vis).copy()
    df_vis = df_alb_mus_ord[nome_col_vis]
    dic_album_vis = dict()
    for album in albuns:
        mascara_album = df_vis.index.get_level_values(0) == album
        vis_album = df_vis[mascara_album]
        head_3 = vis_album.head(3).copy()
        tail_3 = vis_album.tail(3).copy()
        musicas_head_3 = list(head_3.index.get_level_values(1))
        musicas_tail_3 = list(tail_3.index.get_level_values(1))
        vis_head_3 = list(head_3)
        vis_tail_3 = list(tail_3)
        df_mus_vis_head_3 = pd.DataFrame(vis_head_3, index = musicas_head_3,
                                         columns = [nome_col_vis])
        df_mus_vis_tail_3 = pd.DataFrame(vis_tail_3, index = musicas_tail_3,
                                         columns = [nome_col_vis])
        df_mus_vis = {"Mais Vistas": df_mus_vis_head_3,
                        "Menos Vistas": df_mus_vis_tail_3}
        dic_album_vis[album] = df_mus_vis
    return dic_album_vis

def top_3_dur_mus_alb(nome_arquivo: str):
    """Cria um dicionário que possui as músicas mais duradouras
        e menos duradouras por album e seu tempo de duração

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type df_inf_alb_mus: str
    :return: Dicionário com dataframes de músicas mais duradouras
        e menos duradouras por album
    :rtype: dict
    """
    df_inf_alb_mus = dataframe_inf_alb_mus(nome_arquivo,
                                            "albuns_musicas",
                                            "informacoes_musicas",
                                            "albuns",
                                            "musicas")    
    nome_col_dur = "Duração"
    albuns = list(df_inf_alb_mus.index.unique(0))
    df_alb_mus_ord = df_inf_alb_mus.sort_values(ascending = False,
                                                 by = nome_col_dur).copy()
    df_dur = df_alb_mus_ord[nome_col_dur]
    dic_album_dur = dict()
    for album in albuns:
        mascara_album = df_dur.index.get_level_values(0) == album
        dur_album = df_dur[mascara_album]
        head_3 = dur_album.head(3).copy()
        tail_3 = dur_album.tail(3).copy()
        musicas_head_3 = list(head_3.index.get_level_values(1))
        musicas_tail_3 = list(tail_3.index.get_level_values(1))
        dur_head_3 = list(head_3)
        tempo_head_3 = list()
        for duracao in dur_head_3:
            duracao = str(duracao)
            segundos = duracao[-2:]
            minutos = duracao[:-2]
            tempo = minutos + "min " + segundos + "s"
            tempo_head_3.append(tempo)
        dur_tail_3 = list(tail_3)
        tempo_tail_3 = list()
        for duracao in dur_tail_3:
            duracao = str(duracao)
            segundos = duracao[-2:]
            minutos = duracao[:-2]
            if minutos != "":
                tempo = minutos + "min " + segundos + "s"
            else:
                tempo = segundos + "s"
            tempo = minutos + "min " + segundos + "s"
            tempo_tail_3.append(tempo)
        df_mus_dur_head_3 = pd.DataFrame(tempo_head_3, index = musicas_head_3,
                                         columns = [nome_col_dur])
        df_mus_dur_tail_3 = pd.DataFrame(tempo_tail_3, index = musicas_tail_3,
                                         columns = [nome_col_dur])
        df_mus_dur = {"Mais Vistas": df_mus_dur_head_3,
                        "Menos Vistas": df_mus_dur_tail_3}
        dic_album_dur[album] = df_mus_dur
    return dic_album_dur

def top_3_vis_mus(nome_arquivo: str):
    """Cria um dicionário que possui as músicas mais ouvidas
        e menos ouvidas de todas e seu número de visualizações

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Retorna um dicionário com um dataframe das músicas mais vistas
        e outro com as menos ouvidas
    :rtype: dict
    """    
    df_inf_mus = pd.read_excel(nome_arquivo, "informacoes_musicas")
    nome_col_vis = "Exibições"
    nome_col_mus = "musicas"
    df_inf_mus_ord = df_inf_mus.sort_values(ascending = False,
                                             by = nome_col_vis).copy()
    head_3 = df_inf_mus_ord.head(3).copy()
    tail_3 = df_inf_mus_ord.tail(3).copy()
    vis_head_3 = list(head_3[nome_col_vis])
    vis_tail_3 = list(tail_3[nome_col_vis])
    musicas_head_3 = list(head_3[nome_col_mus])
    musicas_tail_3 = list(tail_3[nome_col_mus])
    df_vis_mus_head_3 = pd.DataFrame(vis_head_3, index = musicas_head_3,
                                         columns = [nome_col_vis])
    df_vis_mus_tail_3 = pd.DataFrame(vis_tail_3, index = musicas_tail_3,
                                         columns = [nome_col_vis])

    df_mus_vis = {"Mais Vistas": df_vis_mus_head_3,
                    "Menos Vistas": df_vis_mus_tail_3}
    return df_mus_vis

def top_3_dur_mus(nome_arquivo: str):
    """Cria um dicionário que possui as músicas mais ouvidas
        e menos ouvidas de todas e seu número de visualizações

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Retorna um dicionário com um dataframe das músicas mais vistas
        e outro com as menos ouvidas
    :rtype: dict
    """    
    df_inf_mus = pd.read_excel(nome_arquivo, "informacoes_musicas")
    nome_col_dur = "Duração"
    nome_col_mus = "musicas"
    df_inf_mus_ord = df_inf_mus.sort_values(ascending = False,
                                             by = nome_col_dur).copy()
    head_3 = df_inf_mus_ord.copy().head(3)
    tail_3 = df_inf_mus_ord.copy().tail(3)
    dur_head_3 = list(head_3[nome_col_dur])
    dur_tail_3 = list(tail_3[nome_col_dur])
    tempo_head_3 = list()
    for duracao in dur_head_3:
        duracao = str(duracao)
        segundos = duracao[-2:]
        minutos = duracao[:-2]
        tempo = minutos + "min " + segundos + "s"
        tempo_head_3.append(tempo)
    tempo_tail_3 = list()
    for duracao in dur_tail_3:
        duracao = str(duracao)
        segundos = duracao[-2:]
        minutos = duracao[:-2]
        if minutos != "":
            tempo = minutos + "min " + segundos + "s"
        else:
            tempo = segundos + "s"
        tempo_tail_3.append(tempo)
    musicas_head_3 = list(head_3[nome_col_mus])
    musicas_tail_3 = list(tail_3[nome_col_mus])
    df_dur_mus_head_3 = pd.DataFrame(tempo_head_3, index = musicas_head_3,
                                         columns = [nome_col_dur])
    df_dur_mus_tail_3 = pd.DataFrame(tempo_tail_3, index = musicas_tail_3,
                                         columns = [nome_col_dur])
    
    df_mus_dur = {"Mais Duradouras": df_dur_mus_head_3,
                    "Menos Duradouras": df_dur_mus_tail_3}
    return df_mus_dur

def top_3_alb_prem(nome_arquivo: str):
    """Cria um dataframe com os 3 álbuns mais premiados de todos os tempos

    :param nome_arquivo: Nome do arquivo onde os dados estão contidos
    :type nome_arquivo: str
    :return: Dataframe com os álbuns mais premiados e suas premiações
    :rtype: pandas.core.frame.Dataframe
    """    
    nome_col_prem = "premiacoes"
    df_alb_pre = pd.read_excel(nome_arquivo, nome_col_prem)
    cont_prem = list()
    for premiacoes in df_alb_pre[nome_col_prem]:
        #Cada prêmio é separado por vírgula
        #Se for diferente de vazio, representado por "['-']"
        if premiacoes != "['-']":
            contagem = premiacoes.count(",") + 1
            cont_prem.append(contagem)
        else:
            cont_prem.append(0)
    dic_cont_prem = {"contagem": cont_prem}
    df_cont_prem = pd.DataFrame(dic_cont_prem)
    df_final = df_alb_pre.join(df_cont_prem)
    df_ord_pre = df_final.sort_values(ascending = False, by = "contagem")
    df_top_3 = df_ord_pre.head(3)
    df_top_3_alb_prem = df_top_3[["album",nome_col_prem]]
    return df_top_3_alb_prem
