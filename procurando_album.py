#Importar bibliotecas
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
print(discografias)
#discografia_album = discografias.find_all(attrs={"data-type":"album"})
#print(discografia_album)
'''#Criar lista com nome das músicas em ordem de populariedade
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






