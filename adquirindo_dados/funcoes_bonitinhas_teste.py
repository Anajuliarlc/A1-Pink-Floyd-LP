#Funções Bonitinhas
#Importar bibliotecas
import requests
from bs4 import BeautifulSoup
import pandas as pd
# "https://www.letras.com/pink-floyd/"
def coletar_nomes_musicas(url_letras_ponto_com):
    url = url_letras_ponto_com
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    songs_list = soup.find(class_="artista-todas")
    songs_url_name_list = songs_list.find_all(class_="song-name")
    songs = []
    for song in songs_url_name_list:  
        song_name = song.find("span").contents[0]
        songs.append(song_name)
    return songs

# "https://www.letras.com/pink-floyd/"
def coletar_url_musicas(url_letras_ponto_com, tipo):
    musicas = coletar_nomes_musicas("https://www.letras.com/pink-floyd/")
    url = url_letras_ponto_com
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    songs_list = soup.find(class_="artista-todas")
    songs_url_name_list = songs_list.find_all(class_="song-name")
    urls = []
    for song in songs_url_name_list:  
        url = song.get("href")
        urls.append("https://www.letras.com"+url)
    dic = {}
    for musica, url_ in zip(musicas, urls):
        dic[musica] = url_
    serie = pd.Series(dic)
    if tipo == "lista":
        return urls
    if tipo == "Serie":
        return serie

def coletar_exibicao_musicas():
    songs = coletar_nomes_musicas("https://www.letras.com/pink-floyd/")
    urls = coletar_url_musicas("https://www.letras.com/pink-floyd/", "Serie")
    song_url_dic = {}
    for song, url in zip(songs, urls):
        song_url_dic[song] = url
    exibicao_letras_ponto_com = {}
    for (key,value) in song_url_dic.items():
        data_song = requests.get(value)
        soup_song = BeautifulSoup(data_song.text, "html.parser")
        exibicao = soup_song.find(class_="cnt-info_exib").find("b").contents[0]
        exibicao_letras_ponto_com[key]=exibicao
    serie = pd.Series(exibicao_letras_ponto_com)
    return serie

def coletar_letra():
    songs = coletar_nomes_musicas("https://www.letras.com/pink-floyd/")
    urls = coletar_url_musicas("https://www.letras.com/pink-floyd/", "Serie")
    song_url_dic = {}
    for song, url in zip(songs, urls):
        song_url_dic[song] = url
    letras = []
    musicas = []
    for (key,value) in song_url_dic.items():
        data_song = requests.get(value)
        soup_song = BeautifulSoup(data_song.text, "html.parser")
        estrofes = soup_song.find(class_="cnt-letra p402_premium")
        p_inestrofes = estrofes.find_all("p")
        letra = []
        delimiter = "###"
        for p in p_inestrofes:
            estrofe = p.get_text(" ").split(delimiter)
            for parte in estrofe:
                letra.append(parte)
        musicas.append(key)
        letras.append(letra)
    dic = {}
    for musica, letra in zip(musicas, letras):
        dic[musica] = letra
    serie = pd.Series(dic)
    return serie

#"https://www.letras.com/pink-floyd/mais_acessadas.html"
def mais_ouvidas(url):
    data_mais_tocada = requests.get(url)
    soup_mais_tocada = BeautifulSoup(data_mais_tocada.text, "html.parser")
    mais_tocadas = soup_mais_tocada.find(class_="cnt-list-songs -counter -top-songs js-song-list")
    musicas_div_song_name = mais_tocadas.find_all(class_="song-name")
    musicas = []
    for song in musicas_div_song_name:  
        song_name = song.find("span").contents[0]
        musicas.append(song_name)
    lista_ranking = []
    num_musicas = len(musicas)
    for i in range(1,num_musicas+1):
        lista_ranking.append(i)
    serie_ranking = pd.Series(data=lista_ranking, index=musicas)
    return serie_ranking

# URL para discografia "https://www.letras.mus.br/pink-floyd/discografia/"
def discografia(url, tipo):
    data_discografia = requests.get(url)
    soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
    discografias = soup_discografia.find(class_="discography-container")
    discografia_toda = discografias.find_all(class_="album-item g-sp")
    album_lista = []
    dic_album_musica = {}
    dic_album_data = {}
    lista_tupla_musica_album = []
    
    for album in discografia_toda:
        lancamento = album.find(class_="header-info").contents[0]
        nome_album_biggest = album.find(class_="header-name -biggest")
        nome_album_big = album.find(class_="header-name -big")
        nome_album_medium = album.find(class_="header-name -medium")
        if nome_album_biggest != None:
            nome = nome_album_biggest.find("a").contents[0]
            album_lista.append(nome)
        if nome_album_big != None:
            nome = nome_album_big.find("a").contents[0]
            album_lista.append(nome)
        if nome_album_medium != None:
            nome = nome_album_medium.find("a").contents[0]
            album_lista.append(nome)
        dic_album_data[nome] = lancamento
        discos = album.find_all(class_="cnt-list-songs -counter js-song-list")
        for disco in discos:
            song = disco.find_all(class_="cnt-list-row -song is-visible")
            musicas_album = []
            for musica in song:
                buscar_nome = musica.find(class_="song-name").find("span").contents[0]
                musicas_album.append(buscar_nome)
                dic_album_musica[nome]=musicas_album
                tupla = (nome, buscar_nome)
                lista_tupla_musica_album.append(tupla)    
    serie_musica = pd.Series(dic_album_musica)
    serie_data = pd.Series(dic_album_data)
    if tipo == "data":
        return dic_album_data
    if tipo == "tupla":
        return lista_tupla_musica_album
    if tipo == "dicionario":
        return dic_album_musica
    if tipo == "lista":
        return album_lista
    if tipo == "Serie musica":
        return serie_musica
    if tipo == "Serie data":
        return serie_data

def tempo_musica():
    A = [4.01,8.37,0.39,5.12,39.25,1.05,5.52,13.01,5.58,2.50,41.39,5.05,3.11,3.18,1.14,3.26,3.03,2.53,4.13,23.41,2.35]
    B = [4.11,5.18,3.23,3.46,7.33,2.49,5.18,2.50,3.30]
    C = [6.36,3.38,2.45,6.47,3.42,3.30,5.18,5.56,6.22,6.19,4.12,4.42,4.16,3.33,6.04 ]
    D = [6.41,17.05,4.15,2.18]
    E = [1.55,23.34,5.54,10.46,3.15,2.36]
    F = [5.22,6.08,2.46,4.16]
    G = [1.16,2.43,2.00,2.47,1.17,3.46,3.22]
    H = [5.07,4.39,3.54,7.48]
    I = [3.19,4.30,4.15,3.20,9.40,2.40,3.47,6.17]
    J = [2.58,2.38]
    K = [7.34]
    L = [3.12,4.30,5.38,1.52,5.13,4.43,3.07,2.57]
    M = [5.26,2.25,3.08,3.59,0.38,4.43,2.12,5.34,4.17]
    N = [6.36,3.45,3.27,3.22,4.26]
    O = [40.32,3.47,1.42,3.45,9.16,6.03,3.36,1.13,5.55,6.08,6.27,1.46]
    P = [3.43,3.41,1.08,11.26,1.25,1.28,3.19,7.03,4.23]
    Q = [7.13]
    R = [12.35,4.32,1.13,4.24]
    S = [3.43,2.04,4.30,4.05,2.14,2.48,4.36,9.57,4.58,10.18,13.32,12.29,4.23,7.03,10.37,6.57,4.01,4.07,0.30,4.50,5.28,2.46,3.13,1.09,3.30,1.49,6.59]
    T = [6.15,3.06,3.29,6.17,66.26,6.03,4.51,4.10,2.13,3.07,0.59,7.06,0.38,4.44,5.08,1.50,2.42,4.03,3.25,1.33,1.42,3.28,2.53,5.57,3.26,3.00,21.17,1.36,2.26,5.18,12.20,6.53,2.35,5.18]
    U = [1.07,2.12,7.49]
    V = [2.31,1.33]
    W = [3.57,6.50,7.29,4.23,4.25,3.15,2.31,5.34,4.25,5.11]
    Y = [7.06,18.31,3.29,4.26]
    lista_tempo = A+B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+Y
    musicas = coletar_nomes_musicas("https://www.letras.com/pink-floyd/")
    dic = {}
    for musica, tempo in zip(musicas, lista_tempo):
        dic[musica] = tempo
    serie = pd.Series(dic)
    return serie

def premiacoes():
    discografia_lista = discografia("https://www.letras.mus.br/pink-floyd/discografia/", "lista")
    premio = ["Silver", "Gold", "Platinum", "Diamond", "-"]
    album_premiacao = [[f"{premio[4]}"], [f"{premio[0]}"], [f"{premio[4]}"], [f"{premio[4]}"], [f"{premio[0]}", f"{premio[2]}"], [f"{premio[2]}8x", f"{premio[2]}5x",f"{premio[2]}2x",f"{premio[2]}10x", f"{premio[3]}", f"{premio[3]}", f"{premio[2]}7x"], [f"{premio[2]}3x", f"{premio[2]}2x", f"{premio[2]}2x",f"{premio[2]}", f"{premio[2]}4x", f"{premio[2]}", f"{premio[2]}"], [f"{premio[2]}3x",f"{premio[1]}",f"{premio[1]}2x",f"{premio[1]}",f"{premio[2]}2x",f"{premio[1]}"], [f"{premio[2]}4x",f"{premio[1]}",f"{premio[2]}", f"{premio[1]}", f"{premio[2]}3x", f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[2]}2x", f"{premio[0]}", f"{premio[1]}",f"{premio[1]}",f"{premio[1]}"], [f"{premio[2]}2x", f"{premio[1]}"], [f"{premio[2]}23x", f"{premio[2]}", f"{premio[3]}", f"{premio[2]}4x", f"{premio[3]}2x"], [f"{premio[2]}4x", f"{premio[0]}", f"{premio[2]}",f"{premio[2]}", f"{premio[2]}2x", f"{premio[1]}"],[ f"{premio[2]}6x", f"{premio[1]}", f"{premio[3]}", f"{premio[2]}", f"{premio[2]}3x", f"{premio[2]}2x" ], [f"{premio[1]}"], [f"{premio[2]}15x", f"{premio[2]}9x", f"{premio[2]}", f"{premio[2]}2x", f"{premio[3]}2x", f"{premio[1]}"], [f"{premio[1]}", f"{premio[1]}2x",f"{premio[0]}"], [f"{premio[4]}"], [f"{premio[2]}3x", f"{premio[1]}2x", f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[1]}",f"{premio[1]}",f"{premio[1]}",f"{premio[1]}"], [f"{premio[1]}", f"{premio[2]}"], [f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[4]}"] ]
    dic = {}
    for album,premios in zip(discografia_lista,album_premiacao):
        dic[album] = premios
    serie = pd.Series(dic)
    return serie

# "https://bestsellingalbums.org/artist/10433"
def sales(url):
    url = requests.get(url)
    soup = BeautifulSoup(url.text, "html.parser")
    album_card = soup.find_all(class_="album_card")
    dic = {}
    for album in album_card:
        #coletar nome
        album_find_name = album.find(class_="album")
        album_name = album_find_name.find("a").contents[0]
        #coletar vendas
        album_find_sales = album.find(class_="sales").contents[0]
        dic[album_name] = album_find_sales
    serie = pd.Series(dic)
    return serie

def criar_df(tipo):
  
    ser_musica_urls = coletar_url_musicas("https://www.letras.com/pink-floyd/", "Serie")
    ser_musica_exibicao = coletar_exibicao_musicas()
    ser_musica_letra = coletar_letra()
    ser_musica_mais_ouvidas = mais_ouvidas("https://www.letras.com/pink-floyd/mais_acessadas.html")
    
    ser_album_data = discografia("https://www.letras.mus.br/pink-floyd/discografia/", "Serie data")

    
    ser_musica_tempo = tempo_musica()

    ser_album_premiacoes = premiacoes()
    ser_album_a_mais_sales = sales("https://bestsellingalbums.org/artist/10433")
    #DF INDEX MUSICAS
    dic_index_musicas = {"Mais Ouvida": ser_musica_mais_ouvidas,"Exibições": ser_musica_exibicao, "Duração": ser_musica_tempo, "Letra": ser_musica_letra, "URL": ser_musica_urls } 
    df_index_musicas = pd.DataFrame(dic_index_musicas)
    #DF INDEX ALBUM 
    dic_index_album = {"Lançamento": ser_album_data, "Premiações": ser_album_premiacoes}
    df_index_album = pd.DataFrame(dic_index_album)
    if tipo == "album":
        return df_index_album
    if tipo == "musicas":
        return df_index_musicas
    if tipo == "sales":
        return ser_album_a_mais_sales




