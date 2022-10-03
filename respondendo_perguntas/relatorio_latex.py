import respostas_grupo_2 as rg
from fpdf import FPDF
import warnings
import pandas as pd


warnings.filterwarnings("ignore", category=DeprecationWarning)

pdf = FPDF("P", "mm", "A4")
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin = 15)
pdf.set_font("helvetica", size=12)


def add_texto(texto: str):
    """Função que pega o texto que é dado e imprime no pdf.

    :param texto: texto da pergunta
    :type texto: str
    :return: retorna a pergunta no pdf
    :rtype: PDF
    """    
    pergunta = pdf.cell(0, 10, texto, ln=1)
    return pergunta

add_texto("Quais são as palavras mais comuns nos títulos dos Álbuns?")

nome_arquivo = "informacoes_pink_floyd.xlsx"

pergunta_1 = rg.top_3_pal_titulos_albuns(nome_arquivo)
#print(pergunta_1)

def add_cont_palavras(dataframe: pd.core.frame.DataFrame):
    """Recebe um dataframe e para cada indice dele, ele pega a linha. Para ser 
    mais preciso e não retornar com "name", a função desempacota e transforma a
    contagem em str para não dar erro. Após isso, ela imprime a mensagem que vai 
    ser a palavra mais a aparição dela de acordo com a pergunta no pdf.

    :param dataframe: dataframe da pergunta
    :type dataframe: pd.core.frame.DataFrame
    """    
    for indice in dataframe.index:
        linha = dataframe.iloc[indice]
        palavra, contagem = linha
        palavra = str(palavra)
        contagem = str(contagem)
        mensagem = "   Palavra: " + palavra + "      Aparições: " + contagem
        add_texto(mensagem)
        


def add_cont_palavras_alb(dicionario: dict):
    """_summary_

    :param dicionario: _description_
    :type dicionario: dict
    """ 
    for titulo, dataframe in dicionario.items():
        try:
            titulo = str(titulo)
            add_texto(titulo)
            add_cont_palavras(dataframe)
        except:
            add_texto("Esse álbum não obedece o padrão UTF-8.")

add_cont_palavras(pergunta_1)
add_texto("\n\n")
add_texto("Quais são as palavras mais comuns nos títulos das músicas?")

pergunta_2 = rg.top_3_pal_titulos_musicas(nome_arquivo)
#print(pergunta_2)

add_cont_palavras(pergunta_2)
add_texto("\n\n")
add_texto("Quais são as palavras mais comuns nas letras das músicas, por Álbum?")

pergunta_3 = rg.top_3_pal_albuns(nome_arquivo)
#print(pergunta_3)

add_cont_palavras_alb(pergunta_3)
add_texto("\n\n")
add_texto("Quais são as palavras mais comuns nas letras das músicas, em toda a discografia?")

pergunta_4 = rg.top_3_pal_todas_musicas(nome_arquivo)

add_cont_palavras(pergunta_4)
add_texto("\n\n")
add_texto("O título de um álbum é tema recorrente nas letras?")

pergunta_5 = rg.tit_alb_recorrente_letras(nome_arquivo)
print(pergunta_5)

#add_cont_palavras(pergunta_5) #modificar funcao
add_texto("\n\n")
add_texto("O título de uma música é tema recorrente nas letras?")

pergunta_6 = rg
#print(pergunta_6)

#add_cont_palavras(pergunta_5) #modificar funcao
add_texto("\n\n")

pdf.output("relatorio.pdf")

