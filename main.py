import sys
sys.path.insert(0, "./")

from adquirindo_dados import criar_csv as cc
from respondendo_perguntas import relatorio_mod as rm
from visualizacoes import criar_seaborns as cs

fim = False
opcao = 0

while not fim:
    print("""
    [1] Realizar nova pesquisa
    (Já realizada, mas pode ser atualizada, exigindo trabalho manual)
    [2] Gerar gráficos novamente
    (Já gerados, mas podem ser atualizados)
    [3] Gerar relatório final
    (Já gerado, mas pode ser atualizado)
    [4] Finalizar programa
    """)
    opcao = int(input("Escolha sua opcao: "))

    if opcao == 1:
        print("""
        A realização da pesquisa pode demorar alguns minutos
        """)
        cc.criar_arquivos()
        print("""
        É necessário acessar o arquivo criar_csv.py na pasta adquirindo_dados
        e seguir os passos para a criação do banco de dados completo.
        """)
        fim = False

    elif opcao == 2:
        cs.gerar_todos_graficos("informacoes_pink_floyd.xlsx",
                                 "arquivos_relatorio/")
        fim = False

    elif opcao == 3:
        rm.relatorio_final()
        fim = False

    elif opcao == 4:
        fim = True
        
    elif opcao < 1 or opcao > 4:
        fim = False
        print('opção inválida')

print('Programa finalizado.')