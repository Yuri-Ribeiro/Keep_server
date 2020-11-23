import socket
from os import system, name as osName
from datetime import datetime

host = ''
port = 7008
address = (host, port)

# otherHost = input("IP servidor de arquivos: ")
otherHost = '127.0.0.1'
otherPort = 7005
otherAddress = (otherHost, otherPort)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(otherAddress)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serverSocket.bind(address)
serverSocket.listen(10)

print('Aguardando conexao com servidor')
connection, cliente = serverSocket.accept()
print('Conectado ao servidor')

def captureServerResponse():
    print( "aguardando servidor..." )
    receive = connection.recv(1024)

    return  receive.decode("utf-8")

def logServerResponse(response):
    currentyTime = datetime.now().strftime('%H:%M:%S')
    print(currentyTime + " - Resposta recebedida: " + response)

def clearConsole(): 
    # for windows 
    if osName == 'nt':
        _ = system('cls') 

    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

while True:
    print('--------------SISTEMA DE ARQUIVOS DE TEXTO--------------')
    print("""ESCOLHA UMA OPÇÃO:
            [1] LISTAR ARQUIVOS 
            [2] CRIAR ARQUIVO
            [3] LER CONTEÚDO DE ARQUIVO
            [4] ESCREVER CONTEÚDO EM ARQUIVO
            [5] APAGAR CONTEÚDO DE ARQUIVO
            [6] APAGAR ARQUIVO
            [0] SAIR
            """
            )
    try:
        option = int(input("\n\nQUAL OPÇÃO?: "))
    except ValueError:
        option = 'OPÇÃO INVÁLIDA.'
    
    showInitialMenu = False

    while not showInitialMenu:
        if option == 1:
            command = 'listar'
            clientSocket.send(command.encode('utf-8'))
        elif option == 2:
            command = 'criar'
            fileName = str(input('Nome do arquivo [*.txt]:'))
            clientSocket.send((command + ' --' + fileName).encode('utf-8'))
        elif option == 3:
            command = 'ler'
            fileName = str(input('Nome do arquivo [*.txt]: '))
            clientSocket.send((command + ' --' + fileName).encode('utf-8'))
        elif option == 4:
            command = 'buscar'
            fileName = str(input('Nome do arquivo [*.txt]: '))
            clientSocket.send((command + ' --' + fileName).encode('utf-8'))

            print( "Buscando arquivo no servidor..." )
            response = connection.recv(1024).decode("utf-8")

            if response != f'{fileName} não encontrado.':
                print( "Arquivo encontrado." )
                print('(Digite \'#\' na última linha para ecerrar)Conteúdo a ser inserido:\n')

                texto = ''
                endOfFileIndicator = '\n#\n'
                command = 'escrever'
                
                while True:
                    texto += str(input('')) + '\n'
                    endOfFile = True if texto.find(endOfFileIndicator) != -1 else False

                    if endOfFile:
                        texto = texto.replace(endOfFileIndicator, '\n')

                        clientSocket.send((command + ' --' + fileName + ' --' + texto).encode('utf-8'))
                        break

        elif option == 5:
            command = 'apagarConteudo'
            fileName = str(input('Nome do arquivo [*.txt]: '))
            clientSocket.send((command + ' --' + fileName).encode('utf-8'))

        elif option == 6:
            command = 'excluir'
            fileName = str(input('Nome do arquivo [*.txt]: '))
            clientSocket.send((command + ' --' + fileName).encode('utf-8'))

        elif option == 0:
            print('Saindo...')
            clientSocket.close()
            exit()
            
        else:
            clearConsole()
            _ = input('Opção inválida.')
            break

        response = captureServerResponse()
        logServerResponse(response)
        
        while True:
            clientChoice = str(input(f'\nCONTINUAR NA OPÇÃO {option}?[S/N]: ')).upper()

            if clientChoice == 'S':
                break
            elif clientChoice == 'N':
                showInitialMenu = True
                clearConsole()
                break
            else:
                print('Apenas S ou N')
