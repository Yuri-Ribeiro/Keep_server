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

    def editarArquivoDeTexto(arquivo, texto):
        arquivo = open(arquivo, "a")
        arquivo.write(texto)
        arquivo.close()
    server.register_function(editarArquivoDeTexto, 'editar')

    def lerArquivodeTexto(arquivo):
        arquivo = open(arquivo, "r")
        return arquivo.readline()
    server.register_function(lerArquivodeTexto, 'ler')

    def listarArquivos():
        path = 'files'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return files
    server.register_function(listarArquivos, 'listar')

    def criarArquivoDeTexto(nome_arquivo):
        try:
            arquivo = open(f'files/{nome_arquivo}', 'r+')
        except FileNotFoundError:
            arquivo = open(f'files/{nome_arquivo}', 'w+')
            arquivo.writelines(u'Arquivo criado pois nao existia')
        arquivo.close()
    server.register_function(criarArquivoDeTexto, 'criar')

    def excluirArquivoDeTexto(arquivo):
        path = 'files'
        dir = listdir(path)

        for file in dir:
            if file == arquivo:
                remove(f'files/{file}')
                return 'Arquivo removido!'
        return 'Não encontrado'
    server.register_function(excluirArquivoDeTexto, 'excluir')

    # Run the server's main loop
    server.serve_forever()