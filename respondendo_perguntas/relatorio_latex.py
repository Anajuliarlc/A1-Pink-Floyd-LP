import pandas as pd
import warnings
from PyPDF2 import PdfFileMerger, PdfFileReader
from fpdf import FPDF
import respostas_grupo_1 as rg1
import respostas_grupo_2 as rg2
import respostas_grupo_3 as rg3
import sys

sys.path.insert(0, "./")


def add_texto(texto: str, obj_pdf: FPDF):
    """Função que pega o texto que é dado e imprime no pdf.

    :param texto: texto da pergunta
    :type texto: str
    :return: retorna a pergunta no pdf
    :rtype: texto no PDF
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    texto_pdf = obj_pdf.cell(0, 10, texto, ln=1)
    return texto_pdf


def acessar_exibicao(dataframe: pd.core.frame.DataFrame, obj_pdf: FPDF):
    """Função que recebe um dataframe e para cada música, ele pega a exibição. A 
    função também faz uma mensagem no pdf com o título da música e com o número de 
    exibições, adicionando-as ao PDF. O tratamento de erro ocorre quando a música 
    tem um  caractere diferente ao padrão do UTF-8, imprimindo no lugar da música 
    a mensagem de que não obedece ao padrão.

    :param dataframe: Dataframe com as informações das músicas
    :type dataframe: pd.core.frame.DataFrame
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
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
        add_texto("Essa música não obedece o padrão UTF-8.", obj_pdf)


def acessar_titulo_exibicao(dicionario: dict, obj_pdf: FPDF):
    """Função recebe um dicionário e acessa o nome do álbum, imprimindo-o no PDF. 
    Logo após, ele acessa o título do segundo dicionário e também o imprime. 
    Por último, a função puxa "acessar_exibicao()" para acessar a chave do segundo
    dicionário e imprimir no PDF corretamente por álbum.

    :param dicionario: dicionário com o álbum como chave e um dicionário como valor.
                       No segundo dicionário há o titulo do dataframe como chave 
                       e um dataframe como valor.
    :type dicionario: dict
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    for album, dic_exibi in dicionario.items():
        add_texto(album, obj_pdf)
        for titulo, dataframe in dic_exibi.items():
            titulo = str(titulo)
            add_texto("\n", obj_pdf)
            add_texto(titulo, obj_pdf)
            add_texto("\n", obj_pdf)
            acessar_exibicao(dataframe, obj_pdf)


def acessar_duracao(dataframe: pd.core.frame.DataFrame, obj_pdf: FPDF):
    """Função que recebe um dataframe e para cada música, ele pega a duração. A 
    função também faz uma mensagem no pdf com o título da música e com o tempo dela,
    adicionando-as ao PDF. O tratamento de erro ocorre quando a música tem um 
    caractere diferente ao padrão do UTF-8, imprimindo no lugar da música a 
    mensagem de que não obedece ao padrão.

    :param dataframe: Dataframe com informações da música
    :type dataframe: : pd.core.frame.DataFrame
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
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
        add_texto("Essa música não obedece o padrão UTF-8.", obj_pdf)


def acessar_titulo_duracao(dicionario: dict, obj_pdf: FPDF):
    """Função recebe um dicionário e acessa o nome do álbum, imprimindo-o no PDF. 
    Logo após, ele acessa o título do segundo dicionário e também o imprime. 
    Por último, a função puxa "acessar_duração()" para acessar a chave do segundo
    dicionário e imprimir no PDF corretamente por álbum.

    :param dicionario: dicionário com o álbum como chave e um dicionário como valor.
                       No segundo dicionário há o titulo do dataframe como chave 
                       e um dataframe como valor.
    :type dicionario: dict
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    for album, dic_dura in dicionario.items():
        add_texto(album, obj_pdf)
        for titulo, dataframe in dic_dura.items():
            titulo = str(titulo)
            add_texto("\n", obj_pdf)
            add_texto(titulo, obj_pdf)
            add_texto("\n", obj_pdf)
            acessar_duracao(dataframe, obj_pdf)


def vis_mus_historia(dicionario: dict, obj_pdf: FPDF):
    """Função que acessa o título da música e o seu dataframe, imprimindo o título
    e puxando a função "acessar_exibição()" para ver o número de visualização das 
    músicas e imprimir no PDF.

    :param dicionario: dicionário com um dataframe das músicas mais vistas
                       e outro com as menos ouvidas.
    :type dicionario: dict
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    for titulo, dataframe in dicionario.items():
        titulo = str(titulo)
        add_texto("\n", obj_pdf)
        add_texto(titulo, obj_pdf)
        add_texto("\n", obj_pdf)
        acessar_exibicao(dataframe, obj_pdf)


def dur_mus_historia(dicionario: dict, obj_pdf: FPDF):
    """Função que acessa o título da música e o seu dataframe, imprimindo o título
    e puxando a função "acessar_duração()" para ver o tempo das músicas e 
    imprimir no PDF.

    :param dicionario: dicionário com um dataframe das músicas mais duradouras
                       e outro com as menos duradouras.
    :type dicionario: dict
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    for titulo, dataframe in dicionario.items():
        titulo = str(titulo)
        add_texto("\n", obj_pdf)
        add_texto(titulo, obj_pdf)
        add_texto("\n", obj_pdf)
        acessar_duracao(dataframe, obj_pdf)


def acessar_premio(dataframe: pd.core.frame.DataFrame, obj_pdf: FPDF):
    """Função que recebe um dataframe e para cada album, ele pega a premição. A 
    função também faz uma mensagem no pdf com o título do álbum e prêmios que ganhou,
    adicionando-as ao PDF. O tratamento de erro ocorre quando o álbum tem um 
    caractere diferente ao padrão do UTF-8, imprimindo no lugar do álbum a 
    mensagem de que não obedece ao padrão.

    :param dataframe: Dataframe com os álbuns mais premiados e suas premiações
    :type dataframe: : pd.core.frame.DataFrame
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    premios = list(dataframe["premiacoes"])
    albuns = list(dataframe["album"])
    n_album = len(premios)
    contador = 0
    try:
        while contador < n_album:
            album = albuns[contador]
            premio = premios[contador]
            album = str(album)
            premio = str(premio)
            mensagem = "Álbum: " + album
            mensagem2 = "Premiações: " + premio
            add_texto(mensagem, obj_pdf)
            add_texto(mensagem2, obj_pdf)
            contador += 1
    except:
        add_texto("Esse álbum não obedece o padrão UTF-8.", obj_pdf)


def add_cont_palavras(dataframe: pd.core.frame.DataFrame, obj_pdf: FPDF):
    """Recebe um dataframe e para cada indice dele, ele pega a linha. Para ser 
    mais preciso e não retornar com "name", a função desempacota e transforma a
    contagem e a palavra em str para não dar erro. Após isso, ela imprime a 
    mensagem que vai ser a palavra mais a aparição dela de acordo com a pergunta
    no pdf.

    :param dataframe: dataframe da pergunta
    :type dataframe: pd.core.frame.DataFrame
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
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
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    for titulo, dataframe in dicionario.items():
        try:
            titulo = str(titulo)
            add_texto("\n", obj_pdf)
            add_texto(titulo, obj_pdf)
            add_cont_palavras(dataframe, obj_pdf)
        except:
            add_texto("Essa música não obedece o padrão UTF-8.", obj_pdf)

def acessar_vendas(dataframe: pd.core.frame.DataFrame, obj_pdf: FPDF):
    """Função que recebe um dataframe e para cada álbum, ele pega a venda. A 
    função também faz uma mensagem no pdf com o título do álbum e com o tempo dela,
    adicionando-as ao PDF. O tratamento de erro ocorre quando o álbum tem um 
    caractere diferente ao padrão do UTF-8, imprimindo no lugar da música a 
    mensagem de que não obedece ao padrão.

    :param dataframe: Dataframe com informações da música
    :type dataframe: : pd.core.frame.DataFrame
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    vendas = list(dataframe["vendas"])
    album = len(vendas)
    contador = 0
    try:
        while contador < album:
            musica = list(dataframe.index)
            venda = vendas[contador]
            albuns = str(musica[contador])
            venda = str(venda)
            mensagem = "   Álbum: " + albuns + "     vendas: " + venda
            add_texto(mensagem, obj_pdf)
            contador += 1
    except:
        add_texto("Essa música não obedece o padrão UTF-8.", obj_pdf)


def acessar_vendas_album(dicionario: dict, obj_pdf: FPDF):
    """Função recebe um dicionário e acessa a chave, imprimindo-o no PDF. 
    Logo após, ele acessa o valor que é um dataframe, puxando a função 
    "acessar_vendas" para imprimir o dataframe no pdf.

    :param dicionario: dicionário com a chave de mais e menos vendidos e um dataframe
                        como valor.
    :type dicionario: dict
    :param obj_pdf: PDF
    :type obj_pdf: FPDF
    """
    for mais_menos, dataframe in dicionario.items():
        mais_menos = str(mais_menos)
        add_texto("\n", obj_pdf)
        add_texto(mais_menos, obj_pdf)
        add_texto("\n", obj_pdf)
        acessar_vendas(dataframe, obj_pdf)

def criar_relatorio_g1():
    """Cria um PDF com a biblioteca FPDF para responder as perguntas do grupo 1, 
    puxando as funções acima para imprimir no PDF corretamente e utilizando as 
    funções do documento "respostas_grupo_1.py."(rg1) para puxar as informações.
    """

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("helvetica", size=12)

    nome_arquivo = "informacoes_pink_floyd.xlsx"

    add_texto("Grupo 1", pdf)
    # Resposta da pergunta 1 grupo 1
    add_texto("Músicas mais ouvidas e músicas menos ouvidas por Álbum", pdf)
    grupo1_pergunta_1 = rg1.top_3_vis_mus_alb(nome_arquivo)
    acessar_titulo_exibicao(grupo1_pergunta_1, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 2 grupo 1
    add_texto("Músicas mais longas e músicas mais curtas por Álbum", pdf)
    grupo1_pergunta_2 = rg1.top_3_dur_mus_alb(nome_arquivo)
    acessar_titulo_duracao(grupo1_pergunta_2, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 3 grupo 1
    add_texto(
        "Músicas mais ouvidas e músicas menos ouvidas [em toda a história da banda]", pdf)
    grupo1_pergunta_3 = rg1.top_3_vis_mus(nome_arquivo)
    vis_mus_historia(grupo1_pergunta_3, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 4 grupo 1
    add_texto(
        "Músicas mais longas e músicas mais curtas [em toda a história da banda]", pdf)
    grupo1_pergunta_4 = rg1.top_3_dur_mus(nome_arquivo)
    dur_mus_historia(grupo1_pergunta_4, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 5 grupo 1
    add_texto("Álbuns mais premiados", pdf)
    grupo1_pergunta_5 = rg1.top_3_alb_prem(nome_arquivo)
    acessar_premio(grupo1_pergunta_5, pdf)

    pdf.output("arquivos_relatorio/relatorio_g1.pdf")
    return pdf.page_no()


def criar_relatorio_g2():
    """Cria um PDF com a biblioteca FPDF para responder as perguntas do grupo 1, 
    puxando as funções acima para imprimir no PDF corretamente e utilizando as 
    funções do documento "respostas_grupo_2.py."(rg2) para puxar as informações.
    """

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("helvetica", size=12)

    nome_arquivo = "informacoes_pink_floyd.xlsx"

    add_texto("Grupo 2", pdf)
    # Resposta da pergunta 1 grupo 2
    add_texto("Quais são as palavras mais comuns nos títulos dos Álbuns?", pdf)
    pdf.image("arquivos_relatorio/tag_1.png", x=22, w=120)
    add_texto("Capa: The dark side of the moon", pdf)
    grupo2_pergunta_1 = rg2.top_3_pal_titulos_albuns(nome_arquivo)
    add_cont_palavras(grupo2_pergunta_1, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 2 grupo 2
    add_texto("Quais são as palavras mais comuns nos títulos das músicas?", pdf)
    pdf.image("arquivos_relatorio/tag_2.png", x=22, w=120)
    add_texto("Capa: The division bell", pdf)
    grupo2_pergunta_2 = rg2.top_3_pal_titulos_musicas(nome_arquivo)
    add_cont_palavras(grupo2_pergunta_2, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 3 grupo 2
    add_texto("Quais são as palavras mais comuns nas letras das músicas, por Álbum?", pdf)
    grupo2_pergunta_3 = rg2.top_3_pal_albuns(nome_arquivo)
    add_cont_palavras_alb(grupo2_pergunta_3, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 4 grupo 2
    add_texto("Quais são as palavras mais comuns nas letras das músicas, em toda a discografia?", pdf)
    pdf.image("arquivos_relatorio/tag_3.png", x=22, w=120)
    add_texto("Capa: Pulse", pdf)
    grupo2_pergunta_4 = rg2.top_3_pal_todas_musicas(nome_arquivo)
    add_cont_palavras(grupo2_pergunta_4, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 5 grupo 2
    add_texto("O título de um álbum é tema recorrente nas letras?", pdf)
    grupo2_pergunta_5 = rg2.tit_alb_recorrente_letras(nome_arquivo)
    add_cont_palavras_alb(grupo2_pergunta_5, pdf)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 6 grupo 2
    add_texto("O título de uma música é tema recorrente nas letras?", pdf)
    grupo2_pergunta_6 = rg2.tit_mus_recorrente_letras(nome_arquivo)
    add_cont_palavras_alb(grupo2_pergunta_6, pdf)

    pdf.output("arquivos_relatorio/relatorio_g2.pdf")
    return pdf.page_no()


def criar_relatorio_g3():
    """Cria um PDF com a biblioteca FPDF para responder as perguntas do grupo 1, 
    puxando as funções acima para imprimir no PDF corretamente e utilizando as 
    funções do documento "respostas_grupo_3.py."(rg3) para puxar as informações.
    """

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("helvetica", size=12)

    nome_arquivo = "informacoes_pink_floyd.xlsx"
    
    add_texto("Grupo 3", pdf)
    # Resposta da pergunta 1 grupo 3
    grupo3_pergunta2 = "Qual é a maior produção de álbum por década?"
    add_texto(grupo3_pergunta2, pdf)
    pdf.image("arquivos_relatorio/graf_alb_decada.png", x=22, w=120)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 2 grupo 3
    grupo3_pergunta1 = "Qual é o número de palavras por música e quantas palavras diferentes têm?"
    add_texto(grupo3_pergunta1, pdf)
    pdf.image("arquivos_relatorio/graf_var_letra_mus.png", x=22, w=120)
    add_texto("\n\n", pdf)

    # Resposta da pergunta 3 grupo 3
    grupo3_pergunta3 = rg3.top_5_vendas_album(nome_arquivo)
    add_texto("Quais são os álbuns mais vendidos?", pdf)
    acessar_vendas_album(grupo3_pergunta3, pdf)
    add_texto("\n\n", pdf)

    pdf.output("arquivos_relatorio/relatorio_g3.pdf")
    return pdf.page_no()


def sumario(n_pag1: int, n_pag2: int):
    """Cria a página de sumário para identificar as páginas que começam cada 
    pergunta, recebendo as páginas pelas funções de relatório por grupo.

    :param n_pag1: número de páginas do grupo 1
    :type n_pag1: int
    :param n_pag2: número de páginas do grupo 2
    :type n_pag2: int
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("helvetica", size=12)

    add_texto("Sumário", pdf)
    add_texto("\n\n", pdf)
    add_texto("Grupo de perguntas 1: página 3", pdf)
    add_texto(f"Grupo de perguntas 2: página {n_pag1}", pdf)
    add_texto(f"Grupo de perguntas 3: página {n_pag2}", pdf)

    pdf.output("arquivos_relatorio/sumario.pdf")


def relatorio_final():
    """Função que puxa as funções de criar relatório e sumário para criar um 
    relatório final, que terá todos os pdfs em um usando a biblioteca FPDF.
    """
    merger = PdfFileMerger()
    leitor = PdfFileReader
    n_pag1 = criar_relatorio_g1()
    n_pag1 = str(n_pag1 + 3)
    n_pag2 = criar_relatorio_g2()
    n_pag2 = str(n_pag2 + 37)
    sumario(n_pag1, n_pag2)
    merger.append(leitor(open("arquivos_relatorio/capa_a1_LP.pdf", 'rb')))
    merger.append(leitor(open("arquivos_relatorio/sumario.pdf", 'rb')))
    merger.append(leitor(open("arquivos_relatorio/relatorio_g1.pdf", "rb")))
    merger.append(leitor(open("arquivos_relatorio/relatorio_g2.pdf", 'rb')))
    merger.append(leitor(open("arquivos_relatorio/relatorio_g3.pdf", 'rb')))
    merger.write("arquivos_relatorio/relatoriofinal.pdf")


relatorio_final()