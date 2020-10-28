import xmlrpc.client

s = xmlrpc.client.ServerProxy('localhost:8001')
print(s.pow(2,3))  # Returns 2**3 = 8
# print(s.add(2,3))  # Returns 5
# print(s.print("Olá, 10 anos!"))  # Returns 5*2 = 10

# Print list of available methods
# print(s.system.listMethods())
