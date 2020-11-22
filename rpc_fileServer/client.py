import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

#print(s.criar('naruto.txt'))
#print(s.listar())
#print(s.escrever('naruto.txt', 'ola\nNaruto-kun'))
#print(s.ler('naruto.txt'))
#print(s.apagarConteudo('naruto.txt'))
#print(s.excluir("naruto.txt"))
#print(s.listar())


print('--------------SISTEMA DE ARQUIVOS DE TEXTO--------------')
print("""ESCOLHA UMA OPÇÃO:
        [1] LISTAR ARQUIVOS 
        [2] CRIAR ARQUIVO
        [3] LER CONTEÚDO DE ARQUIVO
        [4] ESCREVER CONTEÚDO EM ARQUIVO
        [5] APAGAR CONTEÚDO DE ARQUIVO
        [6] APAGAR ARQUIVO
        [0] SAIR
        """
        )
try:
    op = int(input("\n\nQUAL OPÇÃO?: "))
except ValueError:
    op = 'INVÁLIDA'

while True:

    if op == 1:
        print(s.listar())

    elif op == 2:
        nome_arquivo = str(input('Nome do arquivo [*.txt]:'))
        print(s.criar(nome_arquivo))

    elif op == 3:
        nome_arquivo = str(input('Nome do arquivo [*.txt]: '))
        print(s.ler(nome_arquivo))

    elif op == 4:
        nome_arquivo = str(input('Nome do arquivo [*.txt]: '))
        if s.buscar(nome_arquivo) != False:
            print('(Digite \'#\' na última linha para ecerrar)Conteúdo a ser inserido:\n')
            while True:
                texto = str(input(''))
                arquivo_encontrado = s.escrever(nome_arquivo, texto)
                if arquivo_encontrado == True:
                    if texto == '#':
                        print(f'----{nome_arquivo} editado!----')
                        break
        else:
            print(f'{nome_arquivo} não encontado!')

    elif op == 5:
        nome_arquivo = str(input('Nome do arquivo [*.txt]: '))
        print(s.apagarConteudo(nome_arquivo))

    elif op == 6:
        nome_arquivo = str(input('Nome do arquivo [*.txt]: '))
        print(s.excluir(nome_arquivo))

    elif op == 0:
        print('Saindo...')
        break
        
    else:
        print('-Opção inválida')
        op = 'INVÁLIDA'
    
    while True:
        continuar = str(input(f'\nCONTINUAR NA OPÇÃO {op}?[S/N]: ')).upper()
        if continuar == "S":
            break
        elif continuar == "N":
            print('\n\n'+'-'*28)
            try:
                op = int(input("ESCOLHA NOVAMENTE A OPÇÃO: "))
                print('-'*28)
            except ValueError:
                op = 'INVÁLIDA'
            break 
        else:
            print('Apenas S ou N')
    
    