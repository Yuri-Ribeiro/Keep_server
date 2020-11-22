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

    def escreverArquivoDeTexto(nome_arquivo, texto):
        path = 'files'
        dir = listdir(path)

        for file in dir:
            if file == nome_arquivo:
                if texto != "#":
                    arquivo = open(f'{path}/{nome_arquivo}', "a")
                    arquivo.writelines(texto)
                    arquivo.write('\n')
                    arquivo.close()
                    return ''
                else:
                    return f'{nome_arquivo} editado!'
        
        return f'{nome_arquivo} não ncontrado'
    server.register_function(escreverArquivoDeTexto, 'escrever')

    def apagarConteudoArquivoDeTexto(nome_arquivo):
        path = 'files'
        dir = listdir(path)

        for file in dir:
            if file == nome_arquivo:
                arquivo = open(f'{path}/{nome_arquivo}', "w")
                arquivo.close()
                return f'{nome_arquivo} sem texto'
        return f'{nome_arquivo} não ncontrado'
    server.register_function(apagarConteudoArquivoDeTexto, 'apagarConteudo')

    def lerArquivodeTexto(nome_arquivo):
        path = 'files'
        dir = listdir(path)

        for file in dir:
            if file == nome_arquivo:
                arquivo = open(f'{path}/{nome_arquivo}', "r")
                return arquivo.read()
        return f'{nome_arquivo} não encontrado'
    server.register_function(lerArquivodeTexto, 'ler')

    def excluirArquivoDeTexto(nome_arquivo):
        path = 'files'
        dir = listdir(path)

        for file in dir:
            if file == nome_arquivo:
                remove(f'{path}/{file}')
                return 'Arquivo removido!'
        return f'{nome_arquivo} não encontrado'
    server.register_function(excluirArquivoDeTexto, 'excluir')

    def listarArquivos():
        path = 'files'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return files
    server.register_function(listarArquivos, 'listar')

    # Run the server's main loop
    server.serve_forever()