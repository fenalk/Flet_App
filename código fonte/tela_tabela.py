import flet as ft
import controle as con
import configuracoes_logging as logging

componentes = {
    'tabela': ft.Ref[ft.DataTable](),
    'pesquisa': ft.Ref[ft.TextField]()
}

def view():     
    return ft.View(
        "tela3",
        [
            ft.TextField(ref=componentes['pesquisa'], label='Pesquisar', 
                         icon=ft.icons.SEARCH, on_change=pesquisar), 
            # DataTable
            ft.DataTable(
                width=float('inf'),
                ref=componentes['tabela'],
                columns=[
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("E-mail")),
                    ft.DataColumn(ft.Text("Telefone")),
                    ft.DataColumn(ft.Text("UF")),
                    ft.DataColumn(ft.Text("Sexo")),
                    ft.DataColumn(ft.Text("Usuário")),
                    ft.DataColumn(ft.Text("Ações"))
                ],
                rows=atualizar_tabela()  # Atualiza a tabela com as linhas do cadastro
            ),
            # Botão de Sair
            ft.Row([
                ft.ElevatedButton("Sair", icon=ft.icons.LOGOUT_OUTLINED, 
                                  on_click=lambda e: con.navegar_para('1'))  # Voltar para a tela de login
            ], alignment="center"),
        ]
    )

# Mapeamento dos dados para a tabela
def atualizar_tabela():
    # Retorna as linhas com os dados do banco de dados
    return [
        ft.DataRow(cells=preencher_linha_tabela(cadastro)) for cadastro in con.banco_de_dados
    ]

def preencher_linha_tabela(cadastro):
    # Preenche as células com os dados de um cadastro
    return [
        ft.DataCell(ft.Text(cadastro['nome'])),
        ft.DataCell(ft.Text(cadastro['email'])),
        ft.DataCell(ft.Text(cadastro['telefone'])),
        ft.DataCell(ft.Text(cadastro['uf'])),
        ft.DataCell(ft.Text(cadastro['sexo'])),
        ft.DataCell(ft.Text(cadastro['login'])),

        # Ações de Editar e Deletar
        ft.DataCell(ft.Row([
            ft.IconButton(
                icon=ft.icons.EDIT,
                icon_color="blue",
                icon_size=35,
                tooltip="Atualizar",
                key=cadastro,
                on_click=atualizar,
            ),
            ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color="red",
                icon_size=35,
                tooltip="Remover",
                key=cadastro,
                on_click=deletar
            ),
        ]))
    ]

# Função que será chamada após salvar o novo usuário ou ao carregar a página
def carregar_tabela():
    # Verifica se o DataTable foi adicionado à página antes de atualizar
    if componentes['tabela'].current is not None:
        # Atualiza as linhas da tabela
        componentes['tabela'].current.rows = atualizar_tabela()
        componentes['tabela'].current.update()  # Atualiza a tabela
    
    # Atualiza a página
    con.page.update()

# Filtra os dados com base na pesquisa
def filtrar_dados(query):
    query_upper = query.upper()
    return [
        ft.DataRow(cells=preencher_linha_tabela(cadastro))
        for cadastro in con.banco_de_dados
        if query_upper in cadastro['nome'].upper() 
        or query_upper in cadastro['email'].upper()
        or query_upper in cadastro['telefone'].upper() 
        or query_upper in cadastro['uf'].upper()
        or query_upper in cadastro['sexo'].upper() 
        or query_upper in cadastro['login'].upper()
    ]

def pesquisar(e):
    query = componentes['pesquisa'].current.value
    componentes['tabela'].current.rows = filtrar_dados(query)
    con.page.update()

# Função para deletar cadastro da tabela
def deletar(e):
    usuario = e.control.key
    confirmar_exclusao(e, usuario)  # Chama a função para confirmar a exclusão

def atualizar(e):
    usuario = e.control.key
    con.tela_atualizar_cadastro.init(usuario)
    con.page.go('4')

# Exclusão de dados com confirmação
def confirmar_exclusao(e, usuario):
    # Cria um AlertDialog para confirmar a exclusão
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmação"),
        content=ft.Text("Tem certeza que deseja excluir este cadastro?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: deletar_confirmado(usuario)),
            ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo(dialog))
        ],
        actions_alignment="end"
    )
    con.page.dialog = dialog
    dialog.open = True
    con.page.update()

def fechar_dialogo(dialog):
    dialog.open = False
    con.page.update()

# Função para deletar o cadastro após a confirmação
def deletar_confirmado(usuario):
    con.remover(usuario)
    logging.info(f"Usuário de Nome: {usuario['nome']}, login: ({usuario['login']}) foi excluído.")
    carregar_tabela()  # Atualiza a tabela após a exclusão
    con.page.dialog.open = False
    con.page.update()
