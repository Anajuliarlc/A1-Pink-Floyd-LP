import pandas as pd
import re

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

def top_3_vis_mus_alb(df_inf_alb_mus: pd.core.frame.DataFrame, nome_col_vis: str):
    """Cria um dicionário com as informações de músicas por álbum

    :param df_inf_alb_mus: Dataframe com as informações das músicas e
        multi-index de álbuns e músicas
    :type df_inf_alb_mus: pd.core.frame.DataFrame
    :param nome_col_letras: Nome da coluna onde estão o número de exibições
        da música
    :type nome_col_letras: str
    :return: Dicionário com as letras das músicas de cada álbum
    :rtype: dict
    """
    albuns = list(df_inf_alb_mus.index.unique(0))
    df_alb_mus_ord = df_inf_alb_mus.sort_values(ascending = False,
                                                 by = nome_col_vis).copy()
    df_vis = df_alb_mus_ord[nome_col_vis]
    dic_album_vis = dict()
    for album in albuns:
        mascara_album = df_vis.index.get_level_values(0) == album
        vis_album = df_vis[mascara_album]
        top_3 = vis_album.head(3)
        musicas = list(top_3.index.get_level_values(1))
        visualizacoes = list(top_3)
        df_mus_vis = pd.DataFrame(visualizacoes, index = musicas,
                                    columns = [nome_col_vis])
        dic_album_vis[album] = df_mus_vis
    return dic_album_vis

#df = dataframe_inf_album_musica("../informacoes_pink_floyd.xlsx", "albuns_musicas","informacoes_musicas", "albuns", "musicas")
#print(top_3_vis_mus_alb(df, "Exibições"))