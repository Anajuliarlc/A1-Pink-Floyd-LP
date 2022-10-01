#Importar bibliotecas
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
print(discografia("https://www.letras.mus.br/pink-floyd/discografia/", "lista"))
#Vamos listar os prêmios
premio = ["Silver", "Gold", "Platinum", "Diamond", "-"]
album_premiacao = [[f"{premio[4]}"], [f"{premio[0]}"], [f"{premio[4]}"], [f"{premio[4]}"], [f"{premio[0]}", f"{premio[2]}"], [f"{premio[2]}8x", f"{premio[2]}5x",f"{premio[2]}2x",f"{premio[2]}10x", f"{premio[3]}", f"{premio[3]}", f"{premio[2]}7x"], [f"{premio[2]}3x", f"{premio[2]}2x", f"{premio[2]}2x",f"{premio[2]}", f"{premio[2]}4x", f"{premio[2]}", f"{premio[2]}"], [f"{premio[2]}3x",f"{premio[1]}",f"{premio[1]}2x",f"{premio[1]}",f"{premio[2]}2x",f"{premio[1]}"], [f"{premio[2]}4x",f"{premio[1]}",f"{premio[2]}", f"{premio[1]}", f"{premio[2]}3x", f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[2]}2x", f"{premio[0]}", f"{premio[1]}",f"{premio[1]}",f"{premio[1]}"], [f"{premio[2]}2x", f"{premio[1]}"], [f"{premio[2]}23x", f"{premio[2]}", f"{premio[3]}", f"{premio[2]}4x", f"{premio[3]}2x"], [f"{premio[2]}4x", f"{premio[0]}", f"{premio[2]}",f"{premio[2]}", f"{premio[2]}2x", f"{premio[1]}"],[ f"{premio[2]}6x", f"{premio[1]}", f"{premio[3]}", f"{premio[2]}", f"{premio[2]}3x", f"{premio[2]}2x" ], [f"{premio[1]}"], [f"{premio[2]}15x", f"{premio[2]}9x", f"{premio[2]}", f"{premio[2]}2x", f"{premio[3]}2x", f"{premio[1]}"], [f"{premio[1]}", f"{premio[1]}2x",f"{premio[0]}"], [f"{premio[4]}"], [f"{premio[2]}3x", f"{premio[1]}2x", f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[1]}",f"{premio[1]}",f"{premio[1]}",f"{premio[1]}"], [f"{premio[1]}", f"{premio[2]}"], [f"{premio[1]}"], [f"{premio[4]}"], [f"{premio[4]}"] ]
print(len(album_premiacao))
print(album_premiacao)
discografia = discografia("https://www.letras.mus.br/pink-floyd/discografia/", "lista") 
print(len(discografia))
#fazer lista de cds vendidos
# https://www.discogs.com/release/16239176-Pink-Floyd-
for album in discografia:
    completar_url = album.split()
    completar_url = "-".join(completar_url)
    data_discografia = requests.get(f"https://www.discogs.com/release/16239176-Pink-Floyd-{completar_url}")
    soup_discografia = BeautifulSoup(data_discografia.text, "html.parser")
   