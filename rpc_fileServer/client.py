import xmlrpc.client
import os

s = xmlrpc.client.ServerProxy('http://localhost:8000')

#print(s.criar('naruto.txt'))
#print(s.criar('boruto.txt'))
#print(s.criar('naruto.txt'))
#print(s.excluir("naruto.txt"))
#s.editar('naruto.txt', 'ola\nNaruto-kun')
#print(s.ler('naruto.txt'))