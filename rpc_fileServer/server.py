from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from os import listdir
from os.path import isfile, join
from os import remove

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()

    def criarArquivoDeTexto(nome_arquivo):
        path = 'files'
        dir = listdir(path)

        for file in dir:
            if file == nome_arquivo:
                return f'{nome_arquivo} já existe'
        arquivo = open(f'{path}/{nome_arquivo}', 'w+')
        arquivo.close()
        return f'{nome_arquivo} foi criado!'
    server.register_function(criarArquivoDeTexto, 'criar')

    def editarArquivoDeTexto(arquivo, texto):
        path = 'files'
        arquivo = open(f'{path}/{arquivo}', "a")
        arquivo.write(texto)
        arquivo.close()
    server.register_function(editarArquivoDeTexto, 'editar')

    def lerArquivodeTexto(arquivo):
        path = 'files'
        arquivo = open(f'{path}/{arquivo}', "r")
        return arquivo.read()
    server.register_function(lerArquivodeTexto, 'ler')

    def excluirArquivoDeTexto(arquivo):
        path = 'files'
        dir = listdir(path)

        for file in dir:
            if file == arquivo:
                remove(f'{path}/{file}')
                return 'Arquivo removido!'
        return 'Não encontrado'
    server.register_function(excluirArquivoDeTexto, 'excluir')

    def listarArquivos():
        path = 'files'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return files
    server.register_function(listarArquivos, 'listar')

    # Run the server's main loop
    server.serve_forever()