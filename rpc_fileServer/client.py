import xmlrpc.client
import os

s = xmlrpc.client.ServerProxy('http://localhost:8000')

'''
s.criar('naruto.txt')
s.criar("boruto.txt")
s.criar('hinata.txt')
s.criar('himawari.txt')
'''

#print(s.excluir("boruto.txt"))

s.editar('naruto.txt', 'ola')