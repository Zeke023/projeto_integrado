from conexao import conexao, cursor
from estado import usuario_logado
from menus import menu_admin, menu_aluno_principal, menu_visitante
from utils import gerar_hash, verificar_senha
from usuarios import adicionar_credencial_login, cadastrar_usuario
import getpass

conexao, cursor


def login_usuario(cursor, conexao):
    print("\n--- LOGIN ---\n")
    email = input("Email: ")
    senha = getpass.getpass("Senha: ")

    cursor.execute("""
        SELECT u.id_usuario, u.nome_usuario, u.senha_usuario, t.id_tipo, t.nome_tipo
        FROM usuarios u
        JOIN tipos_acesso t ON u.id_tipo = t.id_tipo
        WHERE u.email_usuario = %s
    """, (email,))

    resultado = cursor.fetchone()

    if resultado:
        id_usuario, nome, senha_armazenada, id_tipo, tipo_nome = resultado

        if verificar_senha(senha, senha_armazenada):
            senha_hash = gerar_hash(senha)
            if senha_armazenada != senha_hash:
                cursor.execute(
                    "UPDATE usuarios SET senha_usuario = %s WHERE id_usuario = %s",
                    (senha_hash, id_usuario)
                )

            usuario_logado["id"] = id_usuario
            usuario_logado["nome"] = nome
            usuario_logado["tipo_id"] = id_tipo
            usuario_logado["tipo"] = tipo_nome

            # Verificar se possui credencial
            cursor.execute("SELECT id_credencial FROM credenciais WHERE id_usuario = %s", (id_usuario,))
            credencial = cursor.fetchone()

            if not credencial:
                print("\nVocê ainda não possui uma credencial. Direcionando para criação...")
                adicionar_credencial_login(id_usuario, id_tipo)

            print(f"\nBem-vindo, {nome} ({tipo_nome})!")

            if tipo_nome.lower() == "administrador":
                menu_admin(cursor)
            elif tipo_nome.lower() == "aluno":
                menu_aluno_principal(cursor)
            elif tipo_nome.lower() == "visitante":
                menu_visitante(cursor)
            else:
                print("Tipo de usuário não reconhecido.")

        else:
            print("\nSenha incorreta.")
    else:
        print("\nUsuário não encontrado.")


def tela_login_cadastro(cursor, conexao):
    while True:
        print("\n--- BEM VINDO A KEYMANAGER! ---")
        print("\n--- Menu Inicial ---")
        print("1. Login")
        print("2. Cadastro")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            login_usuario(cursor, conexao)
        elif opcao == '2':
            cadastrar_usuario(cursor, conexao)
        elif opcao == '0':
            print("Sistema encerrado!")
            break
        else:
            print("Opção inválida. Tente novamente.")
