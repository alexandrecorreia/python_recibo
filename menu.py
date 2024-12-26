from main import *

gerador = Gerador(Recibo)

def menu():
    print('\n')
    print('#-' * 30 + '\n')
    print('--- Menu GERADOR RECIBOS ---')
    print('[1]  Cadastrar Recibo')
    print('[2]  Listar Todos'    )
    print('[3]  Imprimir Recibo' )
    print('[11] Sair\n')
    print('#-' * 30 + '\n')

    while True:
        try:
            escolha = int(input('Digite aqui a opcao escolhida : '))
            while escolha not in range(1, 12):
                print('Opção inválida!')
                escolha = int(input('Digite aqui a opcao escolhida : '))
            break
        except ValueError:
            print('Opção inválida!')
                  
    match(escolha):
        case 1:
            gerador.cadastrar_recibo()

        case 2:
            gerador.listar()

        case 3:
            gerador.imprimir_numero_recibo(
                input('\n--- Informe o NUMERO DO RECIBO --- : ')
            )
        case 11:
            input('Programa finalizado!')
            quit()

while True:
    menu()
            