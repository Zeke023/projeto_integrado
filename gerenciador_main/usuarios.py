from utils import gerar_chave_acesso, gerar_hash
from conexao import conexao, cursor
import getpass

def menu_usuarios(cursor):
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1. Ver Lista de Usuários")
        print("2. Alterar Usuário")
        print("3. Excluir Usuário")
        print("4. Adicionar Credencial a Usuário")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            listar_usuarios(cursor)
        elif opcao == '2':
            alterar_usuario(cursor)
        elif opcao == '3':
            excluir_usuario(cursor)
        elif opcao == '4':
            adicionar_credencial_usuario(cursor)
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

# Adicionar uma credencial à um usuário caso não tenha após o login
def adicionar_credencial_login(id_usuario, id_tipo):
    print("\n--- Adicionar Credencial a Usuário ---")

    documento = input("Documento (apenas números): ")
    chave_acesso = gerar_chave_acesso()

    cursor.execute("""
        INSERT INTO credenciais (
            id_usuario, documento, id_tipo, chave_acesso
        ) VALUES (%s, %s, %s, %s)
    """, (id_usuario, documento, id_tipo, chave_acesso))
    conexao.commit()

    print("Credencial adicionada com sucesso!")
    print(f"Chave de acesso gerada: {chave_acesso}")

# Listar usuários
def listar_usuarios(cursor):
    cursor.execute("""
        SELECT u.id_usuario, u.nome_usuario, u.email_usuario, t.nome_tipo, c.chave_acesso
        FROM usuarios u
        JOIN tipos_acesso t ON u.id_tipo = t.id_tipo
        LEFT JOIN credenciais c ON u.id_usuario = c.id_usuario
    """)
    usuarios = cursor.fetchall()

    print("\n--- Lista de Usuários ---")
    for u in usuarios:
        id_usuario, nome, email, tipo, chave = u
        chave_display = chave if chave else "Nenhuma"
        print(f"\nID: {id_usuario} | Nome: {nome}\nEmail: {email}\nTipo: {tipo} | Chave: {chave_display}")

# Alterar dados do usuário
def alterar_usuario(cursor):
    id_usuario = input("\nDigite o ID do usuário a ser alterado: ")

    # Verifica se é o administrador principal
    cursor.execute("SELECT prioridade_admin FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()

    if resultado and resultado[0] == 1:
        print("\nEste é o administrador principal e não pode ser alterado.")
        return

    print("\nO que deseja alterar?")
    print("1. Nome")
    print("2. Tipo de acesso")
    print("3. Email")
    print("4. Senha")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        novo_nome = input("\nNovo nome: ")
        cursor.execute("UPDATE usuarios SET nome_usuario = %s WHERE id_usuario = %s", (novo_nome, id_usuario))
        conexao.commit()

    elif opcao == '2':
        cursor.execute("SELECT id_tipo, nome_tipo FROM tipos_acesso")
        tipos = cursor.fetchall()
        print("Tipos disponíveis:")
        for tipo in tipos:
            print(f"{tipo[0]} - {tipo[1]}")
        novo_tipo = input("ID do novo tipo de acesso: ")
        cursor.execute("UPDATE usuarios SET id_tipo = %s WHERE id_usuario = %s", (novo_tipo, id_usuario))
        conexao.commit()
    elif opcao == '3':
        novo_email = input("Novo e-mail: ")
        cursor.execute("UPDATE usuarios SET email_usuario = %s WHERE id_usuario = %s", (novo_email, id_usuario))
        conexao.commit()
    elif opcao == '4':
        nova_senha = getpass.getpass("Digite a nova senha: ")
        nova_senha_hash = gerar_hash(nova_senha)
        cursor.execute("UPDATE usuarios SET senha_usuario = %s WHERE id_usuario = %s", (nova_senha_hash, id_usuario))
        conexao.commit()

    else:
        print("Opção inválida.")
        return

    print("\nUsuário atualizado com sucesso.")

# Excluir usuário
def excluir_usuario(cursor):
    id_usuario = input("\nDigite o ID do usuário a ser excluído: ")

    # Verificar se é o administrador principal
    cursor.execute("SELECT prioridade_admin FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()

    if resultado and resultado[0] == 1:
        print("\nEste é o administrador principal e não pode ser excluído.")
        return

    cursor.execute("DELETE FROM credenciais WHERE id_usuario = %s", (id_usuario,))
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    conexao.commit()

    print("\nUsuário excluído com sucesso.")

# Adicionar credencial manualmente
def adicionar_credencial_usuario(cursor):
    id_usuario = input("\nDigite o ID do usuário: ")

    # Verifica se já existe credencial
    cursor.execute("SELECT id_credencial FROM credenciais WHERE id_usuario = %s", (id_usuario,))
    if cursor.fetchone():
        print("\nUsuário já possui uma credencial.")
        return

    documento = input("\nDocumento (apenas números): ")

    # Busca tipo de acesso do usuário
    cursor.execute("SELECT id_tipo FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    tipo = cursor.fetchone()
    if not tipo:
        print("\nUsuário não encontrado.")
        return

    tipo_id = tipo[0]

    chave_acesso = gerar_chave_acesso()

    cursor.execute("""
        INSERT INTO credenciais (id_usuario, documento, id_tipo, chave_acesso)
        VALUES (%s, %s, %s, %s)
    """, (id_usuario, documento, tipo_id, chave_acesso))
    conexao.commit()

    print("Credencial criada com sucesso!")
    print(f"Chave de Acesso: {chave_acesso}")


# Cria um novo usuário
def cadastrar_usuario(cursor, conexao):
    print("\n--- CADASTRO ---")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")

    id_tipo = 2  # ID padrão de cadastro do tipo "Aluno"

    # Cadastrar o usuário
    cursor.execute("""
        INSERT INTO usuarios (nome_usuario, email_usuario, senha_usuario, id_tipo)
        VALUES (%s, %s, %s, %s)
    """, (nome, email, senha, id_tipo))
    conexao.commit()

    id_usuario = cursor.lastrowid
    
    # Criar a credencial para o novo usuário 
    print("\n--- Cadastro de Credencial ---")
    documento = input("Documento (CPF ou outro, apenas números): ")
    chave_acesso = gerar_chave_acesso()

    cursor.execute("SELECT id_tipo FROM tipos_acesso WHERE id_tipo = %s", (id_tipo,))
    id_tipo = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO credenciais (
            id_usuario, documento, id_tipo, chave_acesso
        ) VALUES (%s, %s, %s, %s)
    """, (id_usuario, documento, id_tipo, chave_acesso))
    conexao.commit()

    print("\nUsuário e credencial cadastrados com sucesso!")
    print(f"Chave de acesso gerada: {chave_acesso}")
