"""
    Configura a tela de Login e Senha, faz a verificação de login e senha do usuárion na função validar_login_de_entrada(e). 
    Se o usuário não for cadastrado ou se for cadastrado e tentar entrar com senha incorreta,
    essas informações serão registradas no arquivo logs.log.

"""

import flet as ft
import controle as con
import configuracoes_logging as logging  # importa as config de logging

##Tela de login
def view():

    #Variáveis de referências que armazenam os valores de login e senha para comparação 
    tf_login = ft.Ref[ft.TextField]()
    tf_senha = ft.Ref[ft.TextField]()
    

    #Função de validação de login, verifica se não há login identico já cadastrado no bando de dados
    def validar_login_de_entrada(e):
        login = tf_login.current.value
        senha = tf_senha.current.value

        # Verifica se o login está no banco de dados
        usuario = next((u for u in con.banco_de_dados if u['login'] == login), None)

        if usuario:
            # Se o login existir, verifica se a senha está correta
            if usuario['senha'] == senha:
                # Login bem-sucedido
                logging.info(f"Login bem-sucedido: Login='{login}'")
                limpar_campos()
                con.navegar_para('3')
            else:
                # Senha incorreta
                logging.info(f"Login falhou. Senha incorreta: Login='{login}'")
                mostrar_alerta(e, "Senha incorreta. Por favor, tente novamente.")
        else:
            # Login não encontrado
            logging.info(f"Login falhou. Usuário não cadastrado!")
            mostrar_alerta(e, "Usuário não cadastrado. Por favor, realize o cadastro.")



    #Função para mostrar o AlertDialog caso não haja cadastro do usuário
    def mostrar_alerta(e, mensagem):
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Alerta"),
            content=ft.Text(mensagem),
            actions=[
                ft.TextButton("Cadastrar", on_click=lambda e: [limpar_campos(), con.navegar_para('2')]),
                ft.TextButton("Fechar", on_click=lambda e: fechar_alerta(dialog))
            ],
            actions_alignment="end"
        )
        con.page.dialog = dialog  
        dialog.open = True  
        con.page.update()  # Atualiza a página para exibir o diálogo

    #Função padrão para fechar o AlertDialog
    def fechar_alerta(dialog):
        dialog.open = False  
        con.page.update()  #Atualiza a página para refletir a mudança

    #Função para limpar os campos de login e senha
    def limpar_campos():
        tf_login.current.value = ""
        tf_senha.current.value = ""
        tf_login.current.update()
        tf_senha.current.update()

##Configurações visuais da tela login e senha
    return ft.View(
        "tela1", 
        [
            ft.Container(
                content=ft.Column(
                    [
                        ##Título
                        ft.Text("Sistema de Cadastro", size=20),
                        ft.Icon(name=ft.icons.PEOPLE, size=100),
                        
                        ##Campo de Login
                        ft.Container(
                            content=ft.TextField(label="Login", ref=tf_login, width=300, autofocus=True),
                            margin=ft.margin.only(top=30)
                        ), #ft.Container
                        
                        ##Campo de Senha
                        ft.Container(
                            content=ft.TextField(label="Senha", password=True, ref=tf_senha, width=300),
                            margin=ft.margin.only(top=20)
                        ),#ft.Container
                        
                        ##Botão "Entrar"
                        ft.Container(
                            content=ft.ElevatedButton("Entrar", width=300, icon=ft.icons.LOGIN, on_click=validar_login_de_entrada),
                            margin=ft.margin.only(top=30)
                        ),#ft.Container
                        
                        ##Botão de Cadastrar
                        ft.Container(
                            content=ft.ElevatedButton("Cadastrar", icon=ft.icons.SAVE, on_click=lambda e: [limpar_campos(), con.navegar_para('2')]),
                            margin=ft.margin.only(top=20)
                        )#ft.Container
                    ],
                    alignment="center",  # Centraliza os itens verticalmente
                    horizontal_alignment="center",  # Centraliza os itens horizontalmente

                ), #ft.Column

                padding=40,
                alignment=ft.alignment.center,
                width=400,
                height=550,
                bgcolor=ft.colors.WHITE,
                border_radius=ft.border_radius.all(20),
                shadow=ft.BoxShadow(blur_radius=20, spread_radius=5, color=ft.colors.GREY_400),
            )
        ], #ft.Container

        horizontal_alignment="center",
        vertical_alignment="center"

    ) #ft.View
