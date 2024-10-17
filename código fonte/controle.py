"""

Controla a navegação entre telas e gerencia os dados do cadastro do usuário. 
As funções de salvar, remover e atualizar são para registros no banco de dados.

"""

import tela_login_senha, tela_cadastro, tela_tabela, tela_atualizar_cadastro
import flet as ft
import banco_de_dados as bd
import controle as con



def init(p):
    global page, telas, banco_de_dados
    page = p
    banco_de_dados = bd.carregar_banco_de_dados()

    # Define as telas
    telas = {
        '1': tela_login_senha.view(),
        '2': tela_cadastro.view(),
        '3': tela_tabela.view(),
        '4': tela_atualizar_cadastro.view()
    }

#Controla a mudança de rota e atualiza a página
def controle_de_rota(route_event):
    page.views.clear()
    page.views.append(telas[route_event.route])
    page.update()

#Função de navegação entre as páginas
def navegar_para(pagina):
    page.go(pagina)

#Função para salvar novos usuários no bando de dados e atualiza 
def salvar(usuario):
    con.banco_de_dados = bd.salvar(usuario)
    bd.atualizar_banco_de_dados(con.banco_de_dados)

#Função para remover usuários da lista de usuários na memória e atualiza
def remover(usuario):
    con.banco_de_dados.remove(usuario)
    bd.atualizar_banco_de_dados(con.banco_de_dados)

#Função Atualiza o bando de dados na memória e atualiza no arquivo
def atualizar(usuario, idx):
    con.banco_de_dados[idx] = usuario
    bd.atualizar_banco_de_dados(con.banco_de_dados)


