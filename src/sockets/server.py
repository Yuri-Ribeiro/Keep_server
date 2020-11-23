import socket
from datetime import datetime

from os import listdir
from os.path import isfile, join
from os import remove

host = ''
port = 7005

myAddress = (host, port)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(myAddress)
serverSocket.listen(10)

print('Servidor inicializado.')
print('Aguardando conexao com cliente...')
connection, cliente = serverSocket.accept()
print('Cliente conectado.')

# otherIP = input("IP do cliente: ")
otherIP = '127.0.0.1'
otherPort = 7008
otherAddress = (otherIP, otherPort)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(otherAddress)

def filesListToString(filesList):  
    filesName = ""  
    
    for fileName in filesList:  
        filesName +=  fileName + '; '
    
    return filesName

#listar
def index():
    path = 'files'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    filesName = filesListToString(files).replace('.gitignore; ', '')

    return filesName

#buscar
def search(fileName):
        path = 'files'
        dir = listdir(path)

        for file in dir:
            if file == fileName:
                return f'{fileName}'
        return 'Não encontrado.'

#criar
def store(fileName):
    path = 'files'

    if search(fileName) != 'Não encontrado.':
        return f'{fileName} já existe.'
    arquivo = open(f'{path}/{fileName}', 'w+')
    arquivo.close()
    return f'{fileName} foi criado.'

#escrever
def writeContent(fileName, content):
    path = 'files'
    
    if search(fileName) != 'Não encontrado.':
        if content != '#':
            arquivo = open(f'{path}/{fileName}', "a")
            arquivo.writelines(content)
            arquivo.close()
        return f'{fileName} alterado com sucesso.'
    return f'{fileName} não encontrado.'

#apagarConteudo
def deleteContent(fileName):
    path = 'files'
    if search(fileName) != 'Não encontrado.':
        arquivo = open(f'{path}/{fileName}', "w")
        arquivo.close()
        return f'{fileName} sem texto.'
    return f'{fileName} não encontrado.'

#apagarConteudo
def show(fileName):
    path = 'files'
    if search(fileName) != 'Não encontrado.':
        arquivo = open(f'{path}/{fileName}', "r")
        return arquivo.read() or 'Arquivo vazio.'
    return f'{fileName} não encontrado.'

#excluir
def delete(fileName):
    path = 'files'
    if search(fileName) != 'Não encontrado.':
        remove(f'{path}/{fileName}')
        return 'Arquivo removido.'
    return f'{fileName} não encontrado.'

while True:
    print( "aguardando comando..." )

    receive = connection.recv(1024).decode("utf-8")
    command, *args = receive.split(' --')
    message = 'Nenhuma ação realizada.'

    if command == 'buscar':
        fileName = args[0]
        message = search(fileName)
    elif command == 'criar':
        fileName = args[0]
        message = store(fileName)
    elif command == 'escrever':
        fileName = args[0]
        content = args[1]
        message = writeContent(fileName, content)
    elif command == 'apagarConteudo':
        fileName = args[0]
        message = deleteContent(fileName)
    elif command == 'ler':
        fileName = args[0]
        message = show(fileName)
    elif command == 'excluir':
        fileName = args[0]
        message = delete(fileName)
    elif command == 'listar':
        message = index()

    currentyTime = datetime.now().strftime('%H:%M:%S')
    print( currentyTime + " - " + command + " executado." )

    clientSocket.send((message).encode('utf-8'))
