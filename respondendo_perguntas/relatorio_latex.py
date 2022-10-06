import respostas_grupo_1 as rg1
import respostas_grupo_2 as rg2
from fpdf import FPDF
from PyPDF2 import PdfFileMerger, PdfFileReader
import warnings
import pandas as pd

def add_texto(texto: str, obj_pdf: FPDF):
    """Função que pega o texto que é dado e imprime no pdf.

    :param texto: texto da pergunta
    :type texto: str
    :return: retorna a pergunta no pdf
    :rtype: PDF
    """    
    texto_pdf = obj_pdf.cell(0, 10, texto, ln=1)
    return texto_pdf


def add_cont_palavras(dataframe: pd.core.frame.DataFrame, obj_pdf: FPDF):
    """Recebe um dataframe e para cada indice dele, ele pega a linha. Para ser 
    mais preciso e não retornar com "name", a função desempacota e transforma a
    contagem e a palavra em str para não dar erro. Após isso, ela imprime a 
    mensagem que vai ser a palavra mais a aparição dela de acordo com a pergunta
    no pdf.

    :param dataframe: dataframe da pergunta
    :type dataframe: pd.core.frame.DataFrame
    """    
    for indice in dataframe.index:
        linha = dataframe.iloc[indice]
        palavra, contagem = linha
        palavra = str(palavra)
        contagem = str(contagem)
        mensagem = "   Palavra: " + palavra + "      Aparições: " + contagem
        add_texto(mensagem, obj_pdf)
        

def add_cont_palavras_alb(dicionario: dict, obj_pdf: FPDF):
    """Recebe um dicionario e para cada título, ele lê o dataframe. A função 
    tranforma o título em srt para evitar erros. Ela adiciona ao pdf o título e
    usa a função add_cont_palavras para exibir a palavra e a contagem após o 
    título. A função também trata a exceção para palavras que tem caracteres que
    não fazem parte do UTF-8 e imprime a mensagem no pdf.

    :param dicionario: dicionario com titulo como chave e dataframe como valor.
    :type dicionario: dict
    """ 
    for titulo, dataframe in dicionario.items():
        try:
            titulo = str(titulo)
            add_texto("\n", obj_pdf)
            add_texto(titulo, obj_pdf)
            add_cont_palavras(dataframe, obj_pdf)
        except:
            add_texto("Esse álbum não obedece o padrão UTF-8.", obj_pdf)


def acessar_dataframe(dataframe, obj_pdf):
        try:
            exibicoes = list(dataframe["Exibições"])
            n_musicas = len(exibicoes)
            contador = 0  
            while contador < n_musicas:
                musica = list(dataframe.index)
                exibicao = exibicoes[contador]
                musica = str(musica[contador])
                exibicao = str(exibicao)
                mensagem = "   Musica: " + musica + "     Exibições: " + exibicao
                add_texto(mensagem, obj_pdf)
                contador += 1
        except:
            add_texto("Esse álbum não obedece o padrão UTF-8.", obj_pdf)

def acessar_titulo(dicionario, obj_pdf):
    for album, dic_exibi in dicionario.items():
        add_texto(album, obj_pdf)
        for titulo, dataframe in dic_exibi.items():
            titulo = str(titulo)
            add_texto("\n", obj_pdf)
            add_texto(titulo, obj_pdf)
            add_texto("\n", obj_pdf)
            acessar_dataframe(dataframe, obj_pdf)
            
def acessar_duracao(dataframe, obj_pdf):
        duracoes = list(dataframe["Duração"])
        n_musicas = len(duracoes)
        contador = 0 
        try:
            while contador < n_musicas:
                musica = list(dataframe.index)
                duracao = duracoes[contador]
                musica = str(musica[contador])
                duracao = str(duracao)
                mensagem = "   Musica: " + musica + "     Duração: " + duracao
                add_texto(mensagem, obj_pdf)
                contador += 1
        except:
            add_texto("Esse álbum não obedece o padrão UTF-8.", obj_pdf)


def acessar_titulo_duracao(dicionario, obj_pdf):
    for album, dic_dura in dicionario.items():
        add_texto(album, obj_pdf)
        for titulo, dataframe in dic_dura.items():
            titulo = str(titulo)
            add_texto("\n", obj_pdf)
            add_texto(titulo, obj_pdf)
            add_texto("\n", obj_pdf)
            acessar_duracao(dataframe, obj_pdf)
            

def criar_relatorio_g2():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin = 15)
    pdf.set_font("helvetica", size=12)
    
    nome_arquivo = "informacoes_pink_floyd.xlsx"

    add_texto("Quais são as palavras mais comuns nos títulos dos Álbuns?", pdf)
    grupo2_pergunta_1 = rg2.top_3_pal_titulos_albuns(nome_arquivo)
    add_cont_palavras(grupo2_pergunta_1, pdf)
    add_texto("\n\n", pdf)

    add_texto("Quais são as palavras mais comuns nos títulos das músicas?", pdf)
    grupo2_pergunta_2 = rg2.top_3_pal_titulos_musicas(nome_arquivo)
    add_cont_palavras(grupo2_pergunta_2, pdf)
    add_texto("\n\n", pdf)
    
    add_texto("Quais são as palavras mais comuns nas letras das músicas, por Álbum?", pdf)
    grupo2_pergunta_3 = rg2.top_3_pal_albuns(nome_arquivo)
    add_cont_palavras_alb(grupo2_pergunta_3, pdf)
    add_texto("\n\n", pdf)

    add_texto("Quais são as palavras mais comuns nas letras das músicas, em toda a discografia?", pdf)
    grupo2_pergunta_4 = rg2.top_3_pal_todas_musicas(nome_arquivo)
    add_cont_palavras(grupo2_pergunta_4, pdf)
    add_texto("\n\n", pdf)

    add_texto("O título de um álbum é tema recorrente nas letras?", pdf)
    grupo2_pergunta_5 = rg2.tit_alb_recorrente_letras(nome_arquivo)
    add_cont_palavras_alb(grupo2_pergunta_5, pdf)
    add_texto("\n\n", pdf)

    add_texto("O título de uma música é tema recorrente nas letras?", pdf)
    grupo2_pergunta_6 = rg2.tit_mus_recorrente_letras(nome_arquivo)
    add_cont_palavras_alb(grupo2_pergunta_6, pdf)
    add_texto("\n\n", pdf)

    pdf.output("arquivos_relatorio/relatorio_g2.pdf")


def relatorio_final():
    merger = PdfFileMerger()
    leitor = PdfFileReader
    criar_relatorio_g2()
    merger.append(leitor(open("arquivos_relatorio/capa_a1_LP.pdf", 'rb')))
    merger.append(leitor(open("arquivos_relatorio/relatorio_g1.pdf", "rb")))
    merger.append(leitor(open("arquivos_relatorio/relatorio_g2.pdf", 'rb')))
    merger.write("arquivos_relatorio/relatoriofinal.pdf")

#relatorio_final()

#def criar_relatorio_g1():
warnings.filterwarnings("ignore", category=DeprecationWarning)
pdf = FPDF("P", "mm", "A4")
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin = 15)
pdf.set_font("helvetica", size=12)

nome_arquivo = "informacoes_pink_floyd.xlsx"

add_texto("Músicas mais ouvidas e músicas menos ouvidas por Álbum", pdf)
grupo1_pergunta_1 = rg1.top_3_vis_mus_alb(nome_arquivo)
acessar_titulo(grupo1_pergunta_1, pdf)

add_texto("Músicas mais longas e músicas mais curtas por Álbum", pdf)
grupo1_pergunta_2 = rg1.top_3_dur_mus_alb(nome_arquivo)
acessar_titulo_duracao(grupo1_pergunta_2, pdf)

add_texto("Músicas mais ouvidas e músicas menos ouvidas [em toda a história da banda]", pdf)
grupo1_pergunta_3 = rg1.



pdf.output("arquivos_relatorio/relatorio_g1.pdf")
print(pdf.page_no())