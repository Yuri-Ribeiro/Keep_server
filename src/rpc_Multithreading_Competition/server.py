from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn #Permite mais de uma requisição no mesmo método, fazendo nultiacessos 
from sys import exit

from time import sleep

from os import listdir, makedirs, remove
from os.path import isfile, join, exists

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

usuarios = list()
def autenticarUsuario(usuario):
    if usuario not in usuarios:
        usuarios.append(usuario)
        print(usuarios)
        return True
    return False

def removerUsuario(usuario):
     for usuarioAux in usuarios:
        if usuarioAux == usuario:
            usuarios.remove(usuario)
            print(usuarios)
            return True

locked_files = dict()
locking = list()
def bloquearArquivo(nome_arquivo, usuario):
    locked_files['arquivo'] = nome_arquivo
    locked_files['usuario'] = usuario
    locking.append(locked_files.copy())
    print(locking)

def desbloquearArquivo(nome_arquivo, usuario):
    for file in locking:
        if file['arquivo'] == nome_arquivo:
            if file['usuario'] == usuario:
                locking.remove(file)


def estadoDoArquivo(nome_arquivo, usuario):
    for index in range(0, len(locking)):
        if locking[index]['arquivo'] == nome_arquivo:
            if locking[index]['usuario'] == usuario:
                print(f'{nome_arquivo} LOCKED')
                return 'LOCKED'
            print(f'{usuario} NOT_THE_USER')
            return 'NOT_THE_USER'
    print(f'{nome_arquivo} UNLOCKED')
    return 'UNLOCKED'


def buscarArquivoDeTexto(nome_arquivo):
    path = 'files'
    dir = listdir(path)

    for file in dir:
        if file == nome_arquivo:
            return f'{nome_arquivo}'
        sleep(1)
    return False

def criarArquivoDeTexto(nome_arquivo):
    path = 'files'
    print(f'Solicitado criação de {nome_arquivo}...' )
    if buscarArquivoDeTexto(nome_arquivo) != False:
        return f'{nome_arquivo} já existe'
    print(f'criando arquivo {nome_arquivo}...' )
    sleep(5)
    arquivo = open(f'{path}/{nome_arquivo}', 'w+')
    arquivo.close()
    return f'{nome_arquivo} foi criado!'


def escreverArquivoDeTexto(nome_arquivo, texto, usuario):
    path = 'files'

    if texto != '#':
        arquivo = open(f'{path}/{nome_arquivo}', "a")
        arquivo.writelines(texto)
        arquivo.write('\n')
        arquivo.close()
    else:
        desbloquearArquivo(nome_arquivo, usuario)
    return True

def apagarConteudoArquivoDeTexto(nome_arquivo, usuario):
    path = 'files'
    if buscarArquivoDeTexto(nome_arquivo) != False:
        estado = estadoDoArquivo(nome_arquivo, usuario)
        if estado == 'NOT_THE_USER':
            return 'Em uso' 
        arquivo = open(f'{path}/{nome_arquivo}', "w")
        arquivo.close()
        return f'{nome_arquivo} sem texto'
    return f'{nome_arquivo} não ncontrado'

def lerArquivodeTexto(nome_arquivo, usuario):
    path = 'files'
    if buscarArquivoDeTexto(nome_arquivo) != False:
        estado = estadoDoArquivo(nome_arquivo, usuario)
        if estado == 'NOT_THE_USER':
            return 'Em uso'
        arquivo = open(f'{path}/{nome_arquivo}', "r")
        return arquivo.read()
    return f'{nome_arquivo} não encontrado'

def excluirArquivoDeTexto(nome_arquivo, usuario):
    path = 'files'

    if buscarArquivoDeTexto(nome_arquivo) != False:
        estado = estadoDoArquivo(nome_arquivo, usuario)
        if estado == 'NOT_THE_USER':
            return 'Em uso'
        else:
            print('Removendo...')
            remove(f'{path}/{nome_arquivo}')
            print(locking)
            return 'Arquivo removido!'
    return f'{nome_arquivo} não encontrado'


def listarArquivos():
    path = 'files'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

def run_server(host="localhost", port=8000):
    server_addr = (host, port)
    server = SimpleThreadedXMLRPCServer(server_addr, allow_none=True)
    
    #Manipular Usuários
    server.register_function(autenticarUsuario, 'autenticarUsuario')
    server.register_function(removerUsuario, 'removerUsuario')
    
    #Bloqueio de arquivos
    server.register_function(bloquearArquivo, 'bloquear')
    server.register_function(desbloquearArquivo, 'desbloquear')
    server.register_function(estadoDoArquivo, 'estadoArquivo')

    #Registro de funções de manipulação de arquivos
    server.register_function(buscarArquivoDeTexto, 'buscar')
    server.register_function(criarArquivoDeTexto, 'criar')
    server.register_function(escreverArquivoDeTexto, 'escrever')
    server.register_function(apagarConteudoArquivoDeTexto, 'apagarConteudo')
    server.register_function(excluirArquivoDeTexto, 'excluir')
    server.register_function(lerArquivodeTexto, 'ler')
    server.register_function(listarArquivos, 'listar')

    print("Servidor iniciando...")
    print(f'Ouvindo em {host} na porta {port}')

    server.serve_forever()


if __name__ == '__main__':
    try:
        if not exists('files'):
            makedirs('files')
        run_server()
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo adm...")