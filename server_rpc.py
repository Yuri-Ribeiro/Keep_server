from xmlrpc.server import SimpleXMLRPCServer

port = 8001

def autenticarUsuario(userID):
    if(userID == 122 or userID == 123):
        return "Usuário autenticado!"
    else:
        return "Usuário não encontrado :("

server = SimpleXMLRPCServer(("localhost", port))
print("Servidor do keeper rodando na porta %i..." %(port))
server.register_function(autenticarUsuario, "autenticarUsuario")
server.serve_forever()