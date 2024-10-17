"""
    Aqui foi criado o bando de dados para armazenar os dados cadastrados em um aarquivo txt.

    Inicialmente, caso não exista o arquivo txt, quando o programa tenta abrir o arquivo em modo de leitura, e ele não é encontrado,
    a exceção FileNotFoundError entra em execução e retorna uma lista vazia.


"""

#Função para carregar os dados do banco (banco_de_dados.txt)
def carregar_banco_de_dados():
    try:
        with open('banco_de_dados.txt', mode='r') as bd:        
            return [
                map_usuario(linha)
                for linha in bd.readlines() 
                if linha.strip()  # Ignora linhas vazias
            ]
    except FileNotFoundError:
        return []  #Retorna uma lista vazia se o arquivo não for encontrado

#Mapeamento para linhas do arquivo para um dicionário de usuário
def map_usuario(linha):
    values = linha.split(',')
    return {
        'nome': values[0].strip(),
        'email': values[1].strip(),
        'telefone': values[2].strip(),
        'uf': values[3].strip(),
        'sexo':values[4].strip(),
        'login': values[5].strip(),
        'senha': values[6].strip(),
    }

#Função para salvar novo usuário no banco de dados
def salvar(usuario):    
    with open('banco_de_dados.txt', mode='a') as bd:        
        bd.write(f"{usuario['nome']},{usuario['email']},{usuario['telefone']},"
                 f"{usuario['uf']},{usuario['sexo']},{usuario['login']},{usuario['senha']}\n")
    return carregar_banco_de_dados()


#Função para atualizar todo o banco de dados (reescrever o arquivo ('w'))
def atualizar_banco_de_dados(lista):
    with open('banco_de_dados.txt', mode='w') as bd:
        for usuario in lista:
            bd.write(f"{usuario['nome']},{usuario['email']},{usuario['telefone']},"
                     f"{usuario['uf']},{usuario['sexo']},{usuario['login']},{usuario['senha']}\n")
