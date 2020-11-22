import xmlrpc.client
import os

s = xmlrpc.client.ServerProxy('http://localhost:8000')

#print(s.criar('naruto.txt'))
#print(s.listar())
#print(s.escrever('naruto.txt', 'ola\nNaruto-kun'))
#print(s.ler('naruto.txt'))
#print(s.apagarConteudo('naruto.txt'))
#print(s.excluir("naruto.txt"))
print(s.ler('naruto.txt'))
#print(s.listar())