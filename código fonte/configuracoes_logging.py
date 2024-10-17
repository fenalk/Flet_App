from logging import INFO, basicConfig, info
from logging import FileHandler


#função responsável por salvar o log

"""
Nível de Logging INFO:

    Uso principal:
        Enviar/registrar informações sobre o fluxo normal do programa;

    Aqui registrar-se cada tentativa de login no sistema, ou se o login ou senha deram errado. 
    Registra data (DD/MM/AAA) e hora (HH:MM:SS).

    basicConfig()
    Informa o nível do logging, onde sua informação será registrada no arquivo de nome e tipo (logs.log), qual o tipo de 
    abertura do arquivo ('a', adiciona os logs conforme a interação do usuário com o sistema) e formato de data e hora.

    
"""

file_handler = FileHandler('logs.log','a')
file_handler.setLevel(INFO)


basicConfig(
    
    level=INFO,
    # filename='logs.log',
    # filemode='a',
    format='%(levelname)s: %(asctime)s: %(message)s', 
    datefmt='%d/%m/%y %H:%M:%S',
    handlers=[file_handler]    

)
