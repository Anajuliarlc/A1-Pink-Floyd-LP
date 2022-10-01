#Importar bibliotecas
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Coletar URL da página conténdo todas as músicas da banda
url = "https://www.letras.com/pink-floyd/"
data = requests.get(url)
soup = BeautifulSoup(data.text, "html.parser")

#Procurar por música
'''
<div id="cnt-artist-songlist" class="artista-todas" data-spy="scroll"> 
<a class="song-name" href"/pink-floyd/98794/">
    <span> A Great Day For Freedom </span>
</a>
'''
#Pegar texto em div class="artista-todas"
songs_list = soup.find(class_="artista-todas")

#Pegar o texto dentro da tag <a class="song-name"> dentro da div class="artista-todas"
songs_url_name_list = songs_list.find_all(class_="song-name")

songs = []
urls = []

for song in songs_url_name_list:  
    #Coletando URL da música
    url = song.get("href")
    urls.append("https://www.letras.com"+url)
    #Coletar nome da música
    song_name = song.find("span").contents[0]
    songs.append(song_name)

#Criar Serie e Dic
song_url_serie = pd.Series(data = urls, index = songs)
song_url_dic = {}
for song, url in zip(songs, urls):
    song_url_dic[song] = url

#Coletar letra da música
'''  
<div class="cnt-letra p402_premium">
  
    <p>
    <br>
    <br>
    </p>
  
<div class="viewFractions">...</div>
</div>
'''
letras = []
for (key,value) in song_url_dic.items():
    #Acessar página da música
    #Lembrando que aqui o nome da música e a URL já estão com " "
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
    letras.append(letra)
    
#Até aqui temos uma lista, letra, onde cada item é uma estrofe da música
#E uma lista com as letras de todas as músicas
#Temos uma lista com nomes, url e letras, bora fazer um dataframe
lista_url_letra = []
for u,l in zip(urls,letras):
    url_letra = [u,l]
    lista_url_letra.append(url_letra)
indices = songs
colunas = ["URL","LYRICS"]
dados = lista_url_letra
df_url_lyrics = pd.DataFrame(dados,index=indices,columns=colunas)

'''
Saída do data frame: 
Nome da música URL  letras=(lista com estrofes da letra) 
'''
#Web Scraping mais tocadas letras.com 
#Coletar URL da página contendo as músicas mais tocadas
url_mais_tocada = "https://www.letras.com/pink-floyd/mais_acessadas.html"
data_mais_tocada = requests.get(url_mais_tocada)
soup_mais_tocada = BeautifulSoup(data_mais_tocada.text, "html.parser")
#Procurar pela lista de músicas
'''
<ul class="cnt-list-songs -counter -top-songs js-song-list">
'''
mais_tocadas = soup_mais_tocada.find(class_="cnt-list-songs -counter -top-songs js-song-list")
#Achar nome das músicas
'''
<a class="song-name" href"/pink-floyd/63065/">
    <span> Wish You Were Here </span>
</a>
'''
musicas_div_song_name = mais_tocadas.find_all(class_="song-name")
#Criar lista com nome das músicas em ordem de populariedade
musicas = []
for song in musicas_div_song_name:  
    #Coletar nome da música
    song_name = song.find("span").contents[0]
    musicas.append(song_name)

#O que faremos agora? A idea é criar uma série com indice nome da música e posição
#Depois juntar no DF com coluna posição mais tocada letras.com
lista_rank = []
for i in range(1,210):
    lista_rank.append(i)

serie_rank = pd.Series(data=lista_rank, index=musicas)
df_url_lyrics.insert(0, "Posição Letras.com", serie_rank)


#Agora faremos uma outra série com indices músicas e albúm 

#Web Scraping discografia letras.com 
#Coletar URL da página 
url_discografia = "https://www.letras.mus.br/pink-floyd/discografia/"
data_discografia = requests.get(url_discografia)
soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
#Procurar pela lista de músicas
'''
<div class="discography-container">
'''
discografias = soup_discografia.find(class_="discography-container")
#Achar albúns das músicas
'''
<div class="album-item g-sp" data-type="album">
'''
discografia_album = discografias.find_all(attrs={"data-type":"album"})
album_lista = []
#Vou por a data manualmente
lista_data = [2014, 1994, 1987, 1983, 1979, 1977, 1975, 1973, 1972, 1971, 1970, 1969, 1969, 1968, 1997]
for album in discografia_album:
    
    nome_album_biggest = album.find(class_="header-name -biggest")
    nome_album_big = album.find(class_="header-name -big")
    nome_album_medium = album.find(class_="header-name -medium")
    if nome_album_biggest != None:
        nome = nome_album_biggest.find("a").contents[0]
    if nome_album_big != None:
        nome = nome_album_big.find("a").contents[0]
        album_lista.append(nome)
    if nome_album_medium != None:
        nome = nome_album_medium.find("a").contents[0]
        album_lista.append(nome)

#Coletar músicas nos álbuns, a ideia é achar em discografia_album cujo nome esteja em album lista, 
#E assim coletar as músicas desses álbuns


#Vamos criar uma lista as músicas do albúm para facilitar as buscas
albuns_html = []
for album in discografia_album:
    nome_album_biggest = album.find(class_="header-name -biggest")
    nome_album_big = album.find(class_="header-name -big")
    nome_album_medium = album.find(class_="header-name -medium")
    if nome_album_biggest != None:
        nome = nome_album_biggest.find("a").contents[0]
        if nome in album_lista:
            songs_album = album.find(class_="cnt-list-songs -counter js-song-list")
            albuns_html.append(songs_album)
    if nome_album_big != None:
        nome = nome_album_big.find("a").contents[0]
        if nome in album_lista:
            songs_album = album.find(class_="cnt-list-songs -counter js-song-list")
            albuns_html.append(songs_album)
    if nome_album_medium != None:
        nome = nome_album_medium.find("a").contents[0]
        if nome in album_lista: 
            songs_album = album.find(class_="cnt-list-songs -counter js-song-list")
            albuns_html.append(songs_album)


#Agora vamos trabalhar com albuns_html
#Tenhamos em mente que queremos só uma série com indice música e nome do album 
#Logo temos que coletar a música de cada álbum 
todas=[]
for album in albuns_html:
    #vamos guardar aqui a música de cada álbum
    lista_musica_album = []
    buscar_musica = album.find_all(class_="cnt-list-row -song is-visible")
    print(buscar_musica)
    for musica in buscar_musica:
        buscar_nome = musica.find(class_="song-name").find("span").contents[0]
        lista_musica_album.append(buscar_nome)
        todas.append(buscar_nome)
print(len(todas))
print(len(songs))
    

'''
#Criar lista com nome das músicas em ordem de populariedade
musicas = []
for song in musicas_div_song_name:  
    #Coletar nome da música
    song_name = song.find("span").contents[0]
    musicas.append(song_name)

#O que faremos agora? A idea é criar uma série com indice nome da música e posição
#Depois juntar no DF com coluna posição mais tocada letras.com
lista_rank = []
for i in range(1,210):
    lista_rank.append(i)

serie_rank = pd.Series(data=lista_rank, index=musicas)
df_url_lyrics.insert(0, "Posição Letras.com", serie_rank)
print(df_url_lyrics) 
'''

