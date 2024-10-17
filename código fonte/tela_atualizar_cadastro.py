"""
Tela de Atualização do Cadastro, onde se encontra a validação de entrada. Permite que o usuário modifique suas informações, 
confirme a atualização e, caso os dados estejam corretos, os salve no banco de dados.

"""

import flet as ft
import controle as con
from tela_tabela import carregar_tabela


#alertas de componentes

componentes = {
    'nome': ft.Ref[ft.TextField](),
    'email': ft.Ref[ft.TextField](),
    'telefone': ft.Ref[ft.TextField](),
    'uf': ft.Ref[ft.Dropdown](),  # Usando Dropdown para UF
    'sexo': ft.Ref[ft.RadioGroup](),  # Usando RadioGroup para Sexo
    'login': ft.Ref[ft.TextField](),
    'senha': ft.Ref[ft.TextField](),  # Ref para senha
}

def view():
    return ft.View(
        "tela4", 
        [
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Editar Cadastro", size=20, weight="bold", text_align="center"),
                        ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, size=50),
                    ], alignment="center"),
                    
                    # Row para Nome
                    ft.Row([
                        ft.Container(content=ft.Text("Nome", size=20), width=150),
                        ft.TextField(label="Nome", ref=componentes['nome'],autofocus=True, on_change=validar_nome_atualizado)
                    ]),

                    # Row para E-mail
                    ft.Row([
                        ft.Container(content=ft.Text("E-mail", size=20), width=150),
                        ft.TextField(label="E-mail", ref=componentes['email'], on_change=validar_email_atualizado) #validar email
                    ]),

                    # Row para Telefone
                    ft.Row([
                        ft.Container(content=ft.Text("Telefone", size=20), width=150),
                        ft.TextField(label="Telefone", ref=componentes['telefone'], on_change=validar_telefone_atualizado)
                    ]),

                    # Row para UF (Dropdown)
                    ft.Row([
                        ft.Container(content=ft.Text("UF", size=20), width=150),
                        ft.Dropdown(
                            ref=componentes['uf'],
                            width=300,
                            label="UF",
                            options=[
                                ft.dropdown.Option("AC"),
                                ft.dropdown.Option("AL"),
                                ft.dropdown.Option("AP"),
                                ft.dropdown.Option("AM"),
                                ft.dropdown.Option("BA"),
                                ft.dropdown.Option("CE"),
                                ft.dropdown.Option("DF"),
                                ft.dropdown.Option("ES"),
                                ft.dropdown.Option("GO"),
                                ft.dropdown.Option("MA"),
                                ft.dropdown.Option("MT"),
                                ft.dropdown.Option("MS"),
                                ft.dropdown.Option("MG"),
                                ft.dropdown.Option("PA"),
                                ft.dropdown.Option("PB"),
                                ft.dropdown.Option("PR"),
                                ft.dropdown.Option("PE"),
                                ft.dropdown.Option("PI"),
                                ft.dropdown.Option("RJ"),
                                ft.dropdown.Option("RN"),
                                ft.dropdown.Option("RS"),
                                ft.dropdown.Option("RO"),
                                ft.dropdown.Option("RR"),
                                ft.dropdown.Option("SC"),
                                ft.dropdown.Option("SP"),
                                ft.dropdown.Option("SE"),
                                ft.dropdown.Option("TO"),
                            ]
                        )
                    ]),

                    # Row para Sexo (RadioGroup)
                    ft.Row([
                        ft.Container(content=ft.Text("Sexo", size=20), width=150), 
                        ft.RadioGroup(
                            ref=componentes["sexo"],
                            content=ft.Row([
                                ft.Radio(value="Masculino", label="M"),
                                ft.Radio(value="Feminino", label="F")
                            ])
                        )
                    ]),

                    # Row para Login
                    ft.Row([
                        ft.Container(content=ft.Text("Login", size=20), width=150),
                        ft.TextField(label="Login", ref=componentes['login'], on_change=validar_login_atualizado)
                    ]),

                    # Row para Senha
                    ft.Row([
                        ft.Container(content=ft.Text("Senha", size=20), width=150),
                        ft.TextField(label="Senha", password=True, can_reveal_password=True, ref=componentes['senha'], on_change=validar_senha_atualizada, on_submit=atualizar_tabela)
                    ]),
                    
                    # Botões
                    ft.Row([
                        ft.ElevatedButton("Voltar", icon=ft.icons.ARROW_BACK, on_click=lambda e: con.navegar_para('3')),  # Voltar para a tela tabela
                        ft.ElevatedButton("Atualizar Cadastro", icon="save", on_click=mostrar_alerta_atualizar)
                    ], alignment="center"),
                ], horizontal_alignment="center"),
                padding=40,
                alignment=ft.alignment.center,
                width=600,
                height=550,
                bgcolor=ft.colors.WHITE,
                border_radius=ft.border_radius.all(20),
                shadow=ft.BoxShadow(blur_radius=20, spread_radius=5, color=ft.colors.GREY_400),
            )
        ],
        horizontal_alignment="center",  # Centraliza o View horizontalmente
        vertical_alignment="center",  # Centraliza o View verticalmente
    )  # ft.View

# Função para inicializar os dados
def init(u):
    global usuario
    usuario = u
    componentes['nome'].current.value = usuario['nome']
    componentes['email'].current.value = usuario['email']
    componentes['telefone'].current.value = usuario['telefone']
    componentes['uf'].current.value = usuario['uf']
    componentes['sexo'].current.value = usuario['sexo']
    componentes['login'].current.value = usuario['login']
    componentes['senha'].current.value = usuario['senha']


# Função para mostrar o alerta de confirmação
def mostrar_alerta_atualizar(e):
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmação"),
        content=ft.Text("Tem certeza que deseja atualizar o cadastro?"),
        actions=[
            ft.TextButton("Sim", on_click=atualizar_tabela),
            ft.TextButton("Fechar", on_click=lambda e: fechar_dialogo(dialog))
        ],
        actions_alignment="end"
    )
    con.page.dialog = dialog
    dialog.open = True
    con.page.update()

# Função para fechar o alerta de diálogo
def fechar_dialogo(dialog):
    dialog.open = False
    con.page.update()

# Função de atualização do cadastro
def atualizar_tabela(e):
    nome = componentes["nome"].current.value
    email = componentes["email"].current.value
    telefone = componentes["telefone"].current.value
    uf = componentes["uf"].current.value
    sexo = componentes["sexo"].current.value
    login = componentes["login"].current.value
    senha = componentes["senha"].current.value        

    # Atualiza o usuário no banco de dados
    idx = con.banco_de_dados.index(usuario)
    usuario_atualizado = {
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'uf': uf,
        'sexo': sexo,
        'login': login,
        'senha': senha
    }

    # Chama a função de atualização no controle para atualizar o banco
    con.atualizar(usuario_atualizado, idx)

    # Limpar os campos da tela
    for campo in componentes:
        componentes[campo].current.value = ""
        componentes[campo].current.update()

    # Atualiza a tabela e redireciona para a página da tabela
    
    con.page.go('3')  # Volta para a tela da tabela
    carregar_tabela()  # Atualiza a tabela com os novos dados
    # Atualiza a página para refletir as alterações
    con.page.update()

#######################################################################################################

### VALIDE NOME ATUALIZADO###
def validar_nome_atualizado(e=None):
    nome = componentes['nome'].current.value.strip()  # Remove espaços em branco no início e no fim

    # Verifica se o nome tem entre 4 e 30 caracteres
    if len(nome) < 4 or len(nome) > 30:
        componentes['nome'].current.error_text = "O nome deve ter entre 4 e 30 caracteres."
        componentes['nome'].current.update()
        return False

    # Verifica se o nome contém apenas letras e espaços
    if not nome.replace(" ", "").isalpha():
        componentes['nome'].current.error_text = "O nome só pode conter letras e espaços."
        componentes['nome'].current.update()
        return False

    # Se tudo estiver correto, retorna True e limpa qualquer mensagem de erro
    componentes['nome'].current.error_text = None
    componentes['nome'].current.update()
    return True

### VALIDAR TELEFONE ATUALIZADO ###
def validar_telefone_atualizado(e=None):
    telefone = componentes['telefone'].current.value.strip()
    telefone = ''.join(filter(str.isdigit, telefone))  # Remove tudo que não é dígito
    
    # Aplica máscara de formatação
    if len(telefone) == 9:
        telefone_formatado = f"{telefone[:5]}-{telefone[5:]}"
    else:
        telefone_formatado = telefone
    
    componentes['telefone'].current.value = telefone_formatado
    componentes['telefone'].current.update()

    if not telefone.isdigit() or len(telefone) != 9:
        componentes['telefone'].current.error_text = "O telefone deve ter 9 dígitos numéricos."
        componentes['telefone'].current.update()
        return False

    componentes['telefone'].current.error_text = None
    componentes['telefone'].current.update()
    return True

### VALIDAR E-MAIL ###
def validar_email_atualizado(e=None):
    email = componentes['email'].current.value.strip()

    # Verifica se o e-mail contém "@"
    if "@" not in email:
        componentes['email'].current.error_text = "O e-mail precisa conter o @."
        componentes['email'].current.update()
        return False

    # Divide o e-mail em duas partes: antes e depois do "@"
    partes = email.split("@")
    if len(partes) != 2:
        componentes['email'].current.error_text = "O e-mail deve ter apenas um @."
        componentes['email'].current.update()
        return False

    local, dominio = partes

    # Verifica se há caracteres antes do "@"
    if not local:
        componentes['email'].current.error_text = "O e-mail deve ter caracteres antes do @."
        componentes['email'].current.update()
        return False

    # Verifica se o domínio contém um ponto "."
    if "." not in dominio:
        componentes['email'].current.error_text = "O domínio do e-mail deve ter um ponto (.)"
        componentes['email'].current.update()
        return False

    # Verifica se há pelo menos um caractere antes e depois do ponto no domínio
    dominio_partes = dominio.split(".")
    if len(dominio_partes) < 2 or not all(dominio_partes):
        componentes['email'].current.error_text = "O domínio deve ser algo como 'dominio.com'."
        componentes['email'].current.update()
        return False

    # Verifica se o e-mail já existe no banco de dados
    email_ja_existe = any(u['email'] == email for u in con.banco_de_dados)

    if email_ja_existe:
        # Define o texto de erro diretamente no campo de e-mail
        componentes['email'].current.error_text = f"O e-mail '{email}' já está cadastrado."
        componentes['email'].current.update()

        return False  # Indica que o e-mail não é válido

    # Se o e-mail for válido (não existir), remove qualquer erro e atualiza o campo
    componentes['email'].current.error_text = None
    componentes['email'].current.update()
    

    return True  # E-mail é válido e pode prosseguir


### VALIDAR LOGIN ###
def validar_login_atualizado(e=None):

    login = componentes['login'].current.value.strip()
    
    # Verifica se o login tem no mínimo 5 caracteres
    if len(login) < 5:
        componentes['login'].current.error_text = "O login deve ter no mínimo 5 caracteres."
        componentes['login'].current.update()
        return False
    
    # Verifica se o login já existe
    login_ja_existe = any(u['login'] == login for u in con.banco_de_dados)
    if login_ja_existe:
        componentes['login'].current.error_text = f"Login '{login}' já está em uso. Escolha outro."
        componentes['login'].current.update()
        return

    
    # Se ambos estiverem corretos, limpa qualquer mensagem de erro
    componentes['login'].current.error_text = None
    componentes['login'].current.update()
    
    
    return True

### VALIDAR SENHA ###
def validar_senha_atualizada(e=None):
    senha = componentes['senha'].current.value.strip()

    # Verifica se a senha tem no mínimo 5 caracteres
    if len(senha) < 5:
        componentes['senha'].current.error_text = "A senha deve ter no mínimo 5 caracteres."
        componentes['senha'].current.update()
        return False
    
    # Se ambos estiverem corretos, limpa qualquer mensagem de erro
    componentes['senha'].current.error_text = None
    componentes['senha'].current.update()
    
    return True

