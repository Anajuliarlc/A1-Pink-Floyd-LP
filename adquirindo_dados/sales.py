
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    if tipo == "data":
        return dic_album_data
    if tipo == "tupla":
        return lista_tupla_musica_album
    if tipo == "dicionario":
        return dic_album_musica
    if tipo == "lista":
        return album_lista

discografia = discografia("https://www.letras.mus.br/pink-floyd/discografia/", "lista")
url  = "https://bestsellingalbums.org/artist/10433"
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
    