#Importar bibliotecas
import requests
from bs4 import BeautifulSoup
import pandas as pd

# função para coletar nome das músicas
def coletar_nomes_musicas():
    """Acha dentro da url "https://www.letras.com/pink-floyd/" o nome das músicas 
    e as coloca numa lista

    :return: lista com músicas coletadas
    :rtype: lista
    """    
    url = "https://www.letras.com/pink-floyd/"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    #achar todas músicas dentro em ordem alfabética
    songs_list = soup.find(class_="artista-todas")
    #achar o nome das músicas
    songs_url_name_list = songs_list.find_all(class_="song-name")
    #listagem das músicas 
    songs = []
    for song in songs_url_name_list:  
        #local no html onde está exatamente o nome de uma música
        song_name = song.find("span").contents[0]
        songs.append(song_name)
    return songs

#função para coletar urls das músicas e junta-las numa lista
def coletar_url_musicas_lista():
    """Acha dentro da url "https://www.letras.com/pink-floyd/" a url da página da música, 
    onde contém a letra, e as coloca numa lista

    :return: lista com urls das letras das músicas do site letras.com
    :rtype: lista
    """    
    url = "https://www.letras.com/pink-floyd/"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    #achar todas as músicas do artista em ordem alfabética
    songs_list = soup.find(class_="artista-todas")
    songs_url_name_list = songs_list.find_all(class_="song-name")
    #coletar a armazenar url's numa lista
    urls = []
    for song in songs_url_name_list:  
        url = song.get("href")
        urls.append("https://www.letras.com"+url)
    return urls

#função para criar serie índice música e coluna url
def serie_musica_url():
    """Usando as funções coletar_nomes_musicas() e coletar_url_musicas(), 
    criar uma série com índice música e coluna url 

    :return: série com índice música e coluna url
    :rtype: pd.Series
    """    
    musicas = coletar_nomes_musicas()
    url = coletar_url_musicas_lista()
    dic = {}
    for musica, url_ in zip(musicas, url):
        dic[musica] = url_
    serie = pd.Series(dic)
    return serie

#Coletar número de exibição no site letras.com e criar dicionário com índice música e coluna número de exibição 
def serie_musica_exibicao():
    """Coleta dentro da página da música o número de exibição de cada música e cria uma
    série com índice música e coluna exibição.

    :return: Série com índice música e coluna número de exibição 
    :rtype: pd.Series
    """    
    songs = coletar_nomes_musicas()
    urls = serie_musica_url()
    #criar um dicionário com chave música e item url
    song_url_dic = {}
    for song, url in zip(songs, urls):
        song_url_dic[song] = url
    #criar dicionário com chave música e item número de exibição 
    exibicao_letras_ponto_com = {}
    for (key,value) in song_url_dic.items():
        data_song = requests.get(value)
        soup_song = BeautifulSoup(data_song.text, "html.parser")
        exibicao = soup_song.find(class_="cnt-info_exib").find("b").contents[0]
        exibicao_letras_ponto_com[key]=exibicao
    #transformando o dicionário em série
    serie = pd.Series(exibicao_letras_ponto_com)
    return serie

# Coletar letra das músicas e criar uma série com índice músicas e coluna letras
def serie_musica_letra():
    """Coletar letra das músicas e criar uma série com índice músicas e coluna letras

    :return: Série com índice músicas e coluna letras
    :rtype: pd.Series
    """    
    song_url_dic = serie_musica_url()
    #coletando letra e música
    letras = []
    musicas = []
    for (key,value) in song_url_dic.items():
        data_song = requests.get(value)
        soup_song = BeautifulSoup(data_song.text, "html.parser")
        estrofes = soup_song.find(class_="cnt-letra p402_premium")
        p_inestrofes = estrofes.find_all("p")
        letra = []
        #se não usarmos o delimiter ele separa por palavra 
        delimiter = "###"
        for p in p_inestrofes:
            estrofe = p.get_text(" ").split(delimiter)
            for parte in estrofe:
                letra.append(parte)
        musicas.append(key)
        letras.append(letra)
    #criar dicionário chave música e item letra
    dic = {}
    for musica, letra in zip(musicas, letras):
        dic[musica] = letra
    serie = pd.Series(dic)
    return serie

# Coletar ranking de músicas mais ouvidas no site letras.com e criar série com índice músicas e coluna ranking
def serie_musica_ranking():
    """Coletar ranking de músicas mais ouvidas no site letras.com e 
    criar série com índice músicas e coluna ranking

    :return: Série com índice música e coluna ranking 
    :rtype: pd.Series 

    """    
    url_mais_tocada = requests.get("https://www.letras.com/pink-floyd/mais_acessadas.html")
    soup_mais_tocada = BeautifulSoup(url_mais_tocada.text, "html.parser")
    mais_tocadas = soup_mais_tocada.find(class_="cnt-list-songs -counter -top-songs js-song-list")
    musicas_div_song_name = mais_tocadas.find_all(class_="song-name")
    #Coletar música na ordem das músicas mais tocadas
    musicas = []
    for song in musicas_div_song_name:  
        song_name = song.find("span").contents[0]
        musicas.append(song_name)
    #Criar lista númerica de 1 até o número de música na lista de músicas
    lista_ranking = []
    num_musicas = len(musicas)
    for i in range(1,num_musicas+1):
        lista_ranking.append(i)
    #Criar série com índice música e coluna posição 
    serie_ranking = pd.Series(data=lista_ranking, index=musicas)
    return serie_ranking

#Dicionário chave albúm item data de lançamento
def dic_album_lancamento():
    """Achar data de lançamento do álbum e criar um dicionário
    com chave álbum e item lançamento

    :return: dicionário com chave album e item ano de lançamento
    :rtype: dicionário
    """    
    data_discografia = requests.get("https://www.letras.mus.br/pink-floyd/discografia/")
    soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
    discografias = soup_discografia.find(class_="discography-container")
    discografia_toda = discografias.find_all(class_="album-item g-sp")
    #criar dicionário
    dic_album_data = {}
    for album in discografia_toda:
        #achar data de lançamento
        lancamento = album.find(class_="header-info").contents[0]
        nome_album_biggest = album.find(class_="header-name -biggest")
        nome_album_big = album.find(class_="header-name -big")
        nome_album_medium = album.find(class_="header-name -medium")
        if nome_album_biggest != None:
            nome = nome_album_biggest.find("a").contents[0]
        if nome_album_big != None:
            nome = nome_album_big.find("a").contents[0]
        if nome_album_medium != None:
            nome = nome_album_medium.find("a").contents[0]
        dic_album_data[nome] = lancamento
    return dic_album_data

#lista de tuplas música álbum 
def lista_tupla_musica_album():
    """procura em cada álbum as músicas a quais pertence e cria
     uma lista com tuplas de música álbum 

    :return: lista de tuplas música álbum 
    :rtype: lista
    """    
    data_discografia = requests.get("https://www.letras.mus.br/pink-floyd/discografia/")
    soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
    discografias = soup_discografia.find(class_="discography-container")
    discografia_toda = discografias.find_all(class_="album-item g-sp")
    album_lista = []
    lista_tupla_musica_album = []
    #Procurar em cada álbum as músicas
    for album in discografia_toda:
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
        discos = album.find_all(class_="cnt-list-songs -counter js-song-list")
        for disco in discos:
            song = disco.find_all(class_="cnt-list-row -song is-visible")
            for musica in song:
                buscar_nome = musica.find(class_="song-name").find("span").contents[0]
                tupla = (nome, buscar_nome)
                lista_tupla_musica_album.append(tupla)    
    return lista_tupla_musica_album

#dicionário álbum música
def dic_album_musica():
    """Procura as músicas em cada álbum e retorna um dicionário 
    com chave álbum e item música

    :return: dicionário com chave álbum e item lista com as músicas de cada álbum 
    :rtype: dicionário
    """    
    data_discografia = requests.get("https://www.letras.mus.br/pink-floyd/discografia/")
    soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
    discografias = soup_discografia.find(class_="discography-container")
    discografia_toda = discografias.find_all(class_="album-item g-sp")
    album_lista = []
    dic_album_musica = {}
    #procurar músicas nos álbuns 
    for album in discografia_toda:
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
        discos = album.find_all(class_="cnt-list-songs -counter js-song-list")
        for disco in discos:
            song = disco.find_all(class_="cnt-list-row -song is-visible")
            musicas_album = []
            for musica in song:
                buscar_nome = musica.find(class_="song-name").find("span").contents[0]
                musicas_album.append(buscar_nome)
                dic_album_musica[nome]=musicas_album   
    return dic_album_musica

#lista com nome dos álbuns   
def lista_album():
    """Procura o nome dos álbuns e os lista em ordem alfabética

    :return: lista com nome dos álbuns
    :rtype: lista
    """    
    data_discografia = requests.get("https://www.letras.mus.br/pink-floyd/discografia/")
    soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
    discografias = soup_discografia.find(class_="discography-container")
    discografia_toda = discografias.find_all(class_="album-item g-sp")
    album_lista = []
    #achando o nome dos albúns 
    for album in discografia_toda:
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
    return album_lista

#função para obter uma série com índice álbum e coluna lista com músicas 
def serie_album_musica():
    """procurar músicas em cada álbum e criar um série com indice
    álbum e coluna lista com músicas

    :return: série com índice álbum e coluna lista de músicas 
    :rtype: pd.Series
    """    
    data_discografia = requests.get("https://www.letras.mus.br/pink-floyd/discografia/")
    soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
    discografias = soup_discografia.find(class_="discography-container")
    discografia_toda = discografias.find_all(class_="album-item g-sp")
    album_lista = []
    #criar dicionário com álbum e música
    dic_album_musica = {}
    for album in discografia_toda:
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
        discos = album.find_all(class_="cnt-list-songs -counter js-song-list")
        #em cada disco colocar as músicas
        for disco in discos:
            song = disco.find_all(class_="cnt-list-row -song is-visible")
            musicas_album = []
            for musica in song:
                buscar_nome = musica.find(class_="song-name").find("span").contents[0]
                musicas_album.append(buscar_nome)
                dic_album_musica[nome]=musicas_album    
    serie_musica = pd.Series(dic_album_musica)
    return serie_musica

#Serie com índice álbum e coluna data de lançamento 
def serie_album_lancamento():
    """#Serie com índice álbum e coluna data de lançamento 

    :return: série com índice álbum e coluna lançamento
    :rtype: pd.Series
    """    
    data_discografia = requests.get("https://www.letras.mus.br/pink-floyd/discografia/")
    soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
    discografias = soup_discografia.find(class_="discography-container")
    discografia_toda = discografias.find_all(class_="album-item g-sp")
    #listando albúns
    album_lista = []
    #gerando dicionário chave albúm e item data de laçamento
    dic_album_data = {}    
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
    #criando série apartir do dicionário     
    serie_data = pd.Series(dic_album_data)
    return serie_data

#criar lista de tempo manualmente e criar série com índice música e coluna tempo
def tempo_musica():
    """criar lista de tempo manualmente e criar série com índice música 
    e coluna tempo

    :return: Série com índice música e coluna tempo 
    :rtype: pd.Series
    """    
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
    musicas = coletar_nomes_musicas()
    #gerar dicionário com chave nome da música e item tempo
    #como a coleta de música foi em ordem alfabética
    #o tempo foi coleta em ordem alfabética também
    dic = {}
    for musica, tempo in zip(musicas, lista_tempo):
        dic[musica] = tempo
    #transformando dicionário em série 
    serie = pd.Series(dic)
    return serie

#Criar série com índice albúm e coluna tipo de premiação
def premiacoes():
    """Criar lista com tipo de premiação e depois dar para cada álbum
    a sua premiação e tanto de vezes

    :return: série com índice albúm e coluna tipo de premiação
    :rtype: pd.Series
    """    
    discografia_lista = lista_album()
    premio = ["Silver", "Gold", "Platinum", "Diamond", "-"]
    album_premiacao = [[f"{premio[4]}"], [f"{premio[0]}"], [f"{premio[4]}"], [f"{premio[4]}"], [f"{premio[0]}", f"{premio[2]}"], [f"{premio[2]}8x", f"{premio[2]}5x",f"{premio[2]}2x",f"{premio[2]}10x", f"{premio[3]}", f"{premio[3]}", f"{premio[2]}7x"], [f"{premio[2]}3x", f"{premio[2]}2x", f"{premio[2]}2x",f"{premio[2]}", f"{premio[2]}4x", f"{premio[2]}", f"{premio[2]}"], [f"{premio[2]}3x",f"{premio[1]}",f"{premio[1]}2x",f"{premio[1]}",f"{premio[2]}2x",f"{premio[1]}"], [f"{premio[2]}4x",f"{premio[1]}",f"{premio[2]}", f"{premio[1]}", f"{premio[2]}3x", f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[2]}2x", f"{premio[0]}", f"{premio[1]}",f"{premio[1]}",f"{premio[1]}"], [f"{premio[2]}2x", f"{premio[1]}"], [f"{premio[2]}23x", f"{premio[2]}", f"{premio[3]}", f"{premio[2]}4x", f"{premio[3]}2x"], [f"{premio[2]}4x", f"{premio[0]}", f"{premio[2]}",f"{premio[2]}", f"{premio[2]}2x", f"{premio[1]}"],[ f"{premio[2]}6x", f"{premio[1]}", f"{premio[3]}", f"{premio[2]}", f"{premio[2]}3x", f"{premio[2]}2x" ], [f"{premio[1]}"], [f"{premio[2]}15x", f"{premio[2]}9x", f"{premio[2]}", f"{premio[2]}2x", f"{premio[3]}2x", f"{premio[1]}"], [f"{premio[1]}", f"{premio[1]}2x",f"{premio[0]}"], [f"{premio[4]}"], [f"{premio[2]}3x", f"{premio[1]}2x", f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[1]}",f"{premio[1]}",f"{premio[1]}",f"{premio[1]}"], [f"{premio[1]}", f"{premio[2]}"], [f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[4]}"] ]
    dic = {}
    for album,premios in zip(discografia_lista,album_premiacao):
        dic[album] = premios
    serie = pd.Series(dic)
    return serie
    
#Série com índice álbum e coluna número de vendas
def sales():
    """coletar número de vendas de cada álbum 

    :return: Série com índice álbum e coluna número de vendas
    :rtype: pd.Series
    """    
    url = requests.get("https://bestsellingalbums.org/artist/10433")
    soup = BeautifulSoup(url.text, "html.parser")
    album_card = soup.find_all(class_="album_card")
    #criando dicionário chave álbum e item vendas
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

#Dicionário com chave nome do álbum e item número de vendas
def dic_sales():
    """acha albúm e o número de vendas de cada albúm 

    :return: Dicionário com chave nome do álbum e item número de vendas
    :rtype: dicionário
    """    
    url = requests.get("https://bestsellingalbums.org/artist/10433")
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
    return dic

#dataframe de vendas
def dataframe_sales():
    """Organiza as informações coletadas sobre o número de vendas dos álbuns, 
    data de lançamento e organiza em um Dataframe coim index numérico

    :return: Retorna um Dataframe com o álbum, ano de lançamento e n° de vendas
    :rtype: pandas.core.frame.DataFrame
    """ 
    #Chama o dicionário com o resultado da pesquisa no site
    album_ano_vendas = dic_sales().items()
    linhas_dataframe = list()
    for linha in album_ano_vendas:
        #Separa a chave composta por álbum e ano e
        #o número de vendas (em formato string) de cada linha
        album_ano, vendas_string = linha

        #Pega o nome do álbum na string inteira
        album = album_ano[:-7]
        #Pega o ano de lançamento entre () na string
        ano = int(album_ano[-5:-1])
        
        # Transforma número de vendas que está no padrão Sales: 100,000 em int
        vendas_sem_sales = vendas_string.replace("Sales: ", "")
        vendas_sem_virgula = vendas_sem_sales.replace(",", "")
        numero_vendas = int(vendas_sem_virgula)

        linha_dataframe = [album, ano, numero_vendas]
        linhas_dataframe.append(linha_dataframe)

    colunas = ["album", "ano_de_lancamento", "vendas"]
    dataframe_vendas = pd.DataFrame(data = linhas_dataframe, columns = colunas)
    return dataframe_vendas

#dataframe com informações sobre os álbuns
def df_index_album():
    """Usando as funções criadas anteriormente junta as informações sobre
    os álbuns e cria um dataframe com índice álbum com coluna lançamento e 
    coluna premiações, com o tipo de premiação 

    :return: DataFrame pandas com índice álbum com coluna lançamento e 
    coluna premiações 
    :rtype: ps.DataFrame
    """    
    ser_album_data = serie_album_lancamento()
    ser_album_premiacoes = premiacoes()
    #DF INDEX ALBUM 
    dic_index_album = {"lancamento": ser_album_data, "premiacoes": ser_album_premiacoes}
    df_index_album = pd.DataFrame(dic_index_album)
    
    return df_index_album

#dataframe com informações sobre as músicas 
def df_index_musica():
    """Junta série com índice música num DataFrame com índice música, coluna url, coluna exibição, coluna duração, coluna letra, coluna mais ouvidas.

    :return: DataFrame com índice música, coluna url, coluna exibição, coluna duração, coluna letra, coluna mais ouvidas.
    :rtype: pd.DataFrame
    """    
    ser_musica_urls = serie_musica_url()
    ser_musica_exibicao = serie_musica_exibicao()
    ser_musica_letra = serie_musica_letra()
    ser_musica_mais_ouvidas = serie_musica_ranking()
    
    ser_musica_tempo = tempo_musica()
    #DF INDEX MUSICAS
    dic_index_musicas = {"Mais Ouvida": ser_musica_mais_ouvidas,"Exibições": ser_musica_exibicao, "Duração": ser_musica_tempo, "Letra": ser_musica_letra, "URL": ser_musica_urls } 
    df_index_musicas = pd.DataFrame(dic_index_musicas)
    return df_index_musicas
