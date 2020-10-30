import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy:
    print(proxy.autenticarUsuario(122))
    print(proxy.autenticarUsuario(130))
