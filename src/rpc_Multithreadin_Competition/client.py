import xmlrpc.client



if __name__=='__main__':
    s = xmlrpc.client.ServerProxy("http://localhost:8000/", allow_none=True)
    
    nome_arquivo = ''
    op = ''
    
    try:
        usuario = str(input('Digite nome de identificação: '))
        autenticar = s.autenticarUsuario(usuario)
        if autenticar == True:

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
                    print('Aguarde..')
                    print(s.criar(nome_arquivo))
                    
                elif op == 3:
                    nome_arquivo = str(input('Nome do arquivo [*.txt]: '))    
                    print(s.ler(nome_arquivo, usuario))

                elif op == 4:
                    nome_arquivo = str(input('Nome do arquivo [*.txt]: '))
                    buscarArquivo = s.buscar(nome_arquivo)
                    if buscarArquivo != False:
                        if s.estadoArquivo(nome_arquivo, usuario) != 'UNLOCKED':
                            print("Em uso")
                    
                        else:
                            s.bloquear(nome_arquivo, usuario)
                            print('(Digite \'#\' na última linha para ecerrar)Conteúdo a ser inserido:\n')
                            while True:
                                texto = str(input(''))
                                arquivo_encontrado = s.escrever(nome_arquivo, texto, usuario)
                                if arquivo_encontrado == True:
                                    if texto == '#':
                                        print(f'----{nome_arquivo} editado!----')
                                        break
                    else:
                        print(f'{nome_arquivo} não encontado!')

                elif op == 5:
                    nome_arquivo = str(input('Nome do arquivo [*.txt]: '))
                    print(s.apagarConteudo(nome_arquivo, usuario))

                elif op == 6:
                    nome_arquivo = str(input('Nome do arquivo [*.txt]: '))
                    print(s.excluir(nome_arquivo, usuario))
                                        
                elif op == 0:
                    print('Saindo...')
                    s.removerUsuario(usuario)
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
        else:
            print('Usuário já existe')
    except KeyboardInterrupt:
        print(nome_arquivo)
        if nome_arquivo != '':
            if s.estadoArquivo(nome_arquivo, usuario) != 'UNLOCKED':
                s.desbloquear(nome_arquivo, usuario)
        s.removerUsuario(usuario)
        print("\nCliente foi encerrado...")
    except ConnectionRefusedError:
        print('Nenhum servidor foi encontrado!')