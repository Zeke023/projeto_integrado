from usuarios import menu_usuarios
from eventos import menu_eventos, gerar_relatorio_acessos
from visitante import ver_credencial, listar_eventos, registrar_acesso_evento, listar_eventos_inscritos
from menu_aluno import menu_aluno


def menu_admin(cursor):
    while True:
        print("\n--- Menu do Administrador ---")
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Eventos")
        print("3. Relatório de Acessos Gerais")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            menu_usuarios(cursor)
        elif opcao == '2':
            menu_eventos(cursor)
        elif opcao == '3':
            gerar_relatorio_acessos(cursor)
        elif opcao == '0':
            break
        else:
            print("\nOpção inválida. Tente novamente.")


def menu_aluno_principal(cursor):
    menu_aluno(cursor)


def menu_visitante(cursor):
    while True:
        print("\n--- Menu do Visitante ---\n")
        print("1. Ver minha credencial")
        print("2. Listar eventos")
        print("3. Inscrever-se em evento")
        print("4. Ver eventos inscritos")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            ver_credencial(cursor)
        elif opcao == '2':
            listar_eventos(cursor)
        elif opcao == '3':
            registrar_acesso_evento(cursor)
        elif opcao == '4':
            listar_eventos_inscritos(cursor)
        elif opcao == '0':
            break
        else:
            print("\nOpção inválida. Tente novamente.")
