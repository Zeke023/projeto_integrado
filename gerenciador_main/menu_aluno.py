import mysql.connector
from conexao import conexao, cursor
from utils import gerar_chave_acesso, gerar_hash
from datetime import datetime
from estado import usuario_logado



def menu_aluno(cursor):
    while True:
        print("\n--- Menu do Aluno ---")
        print("1. Perfil de Usuário")
        print("2. Eventos")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            menu_perfil_aluno(cursor)
        elif opcao == '2':
            menu_eventos_aluno(cursor)
        elif opcao == '0':
            break
        else:
            print("\nOpção inválida. Tente novamente.")


# ---------------------- PERFIL DO ALUNO ----------------------

def menu_perfil_aluno(cursor):
    while True:
        print("\n--- Perfil de Usuário ---")
        print("1. Ver informações de credencial")
        print("2. Inscrever visitante")
        print("3. Listar Visitantes.")
        print("4. Excluir visitante")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            ver_credencial(cursor)
        elif opcao == '2':
            inscrever_visitante(cursor, conexao)
        elif opcao == '3':
            listar_visitantes(cursor)
        elif opcao == '4':
            excluir_visitante(cursor)
        elif opcao == '0':
            break
        else:
            print("\nOpção inválida. Tente novamente.")


def ver_credencial(cursor):
    id_usuario = usuario_logado["id"]
    cursor.execute("""
        SELECT documento, chave_acesso, data_registro
        FROM credenciais
        WHERE id_usuario = %s
    """, (id_usuario,))
    credencial = cursor.fetchone()

    if credencial:
        documento, chave, data = credencial
        print("\n--- Credencial ---")
        print(f"Documento: {documento}")
        print(f"Chave de Acesso: {chave}")
        print(f"Data de Registro: {data}")
    else:
        print("\nNenhuma credencial encontrada.")


def inscrever_visitante(cursor, conexao):
    print("\n--- Inscrição de Visitante ---")
    nome = input("\nNome do visitante: ").strip()
    documento = input("Documento do visitante (CPF ou RG): ").strip()

    chave = gerar_chave_acesso()
    senha_hash = gerar_hash(documento)  # usa o documento como senha inicial
    id_responsavel = usuario_logado["id"]

    try:
        # Inserir visitante na tabela usuarios
        cursor.execute("""
            INSERT INTO usuarios (nome_usuario, email_usuario, senha_usuario, id_tipo, id_responsavel)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            nome,
            f"{documento}@visitante.com",  # email fictício
            senha_hash,                    # senha hash
            3,                             # tipo 'Visitante'
            id_responsavel                 # vínculo com quem cadastrou
        ))
        conexao.commit()

        id_visitante = cursor.lastrowid

        # Criar credencial do visitante
        cursor.execute("""
            INSERT INTO credenciais (id_usuario, documento, id_tipo, chave_acesso)
            VALUES (%s, %s, %s, %s)
        """, (
            id_visitante,
            documento,
            3,
            chave
        ))
        conexao.commit()

        print(f"\nVisitante cadastrado com sucesso!")
        print(f"Chave de acesso: {chave}")

    except mysql.connector.Error as erro:
        print("\nErro ao cadastrar visitante:", erro)



def listar_visitantes(cursor):
    id_responsavel = usuario_logado["id"]

    cursor.execute("""
        SELECT u.id_usuario, u.nome_usuario, c.documento
        FROM usuarios u
        JOIN credenciais c ON u.id_usuario = c.id_usuario
        WHERE u.id_tipo = 3 AND u.id_responsavel = %s
    """, (id_responsavel,))

    visitantes = cursor.fetchall()

    if not visitantes:
        print("\nVocê não possui visitantes cadastrados.")
        return

    print("\n--- Meus Visitantes ---")
    for v in visitantes:
        print(f"ID: {v[0]} | Nome: {v[1]} | Documento: {v[2]}")


def excluir_visitante(cursor):
    id_responsavel = usuario_logado["id"]

    cursor.execute("""
        SELECT u.id_usuario, u.nome_usuario, c.documento
        FROM usuarios u
        JOIN credenciais c ON u.id_usuario = c.id_usuario
        WHERE u.id_tipo = 3 AND u.id_responsavel = %s
    """, (id_responsavel,))

    visitantes = cursor.fetchall()

    if not visitantes:
        print("\nVocê não possui visitantes cadastrados.")
        return

    print("\n--- Meus Visitantes ---")
    for v in visitantes:
        print(f"ID: {v[0]} | Nome: {v[1]} | Documento: {v[2]}")

    id_visitante = input("Digite o ID do visitante para excluir: ")

    cursor.execute("DELETE FROM credenciais WHERE id_usuario = %s", (id_visitante,))
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_visitante,))

    print("Visitante excluído com sucesso.")


# ---------------------- EVENTOS DO ALUNO ----------------------

def menu_eventos_aluno(cursor):
    while True:
        print("\n--- Menu de Eventos ---")
        print("1. Lista de eventos")
        print("2. Inscrição em evento")
        print("3. Cancelar inscrição")
        print("4. Ver eventos inscritos")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            listar_eventos(cursor)
        elif opcao == '2':
            registrar_acesso_evento(cursor)
        elif opcao == '3':
            cancelar_inscricao_evento(cursor)
        elif opcao == '4':
            listar_eventos_inscritos(cursor)
        elif opcao == '0':
            break
        else:
            print("\nOpção inválida. Tente novamente.")


def listar_eventos(cursor):
    cursor.execute("""
        SELECT id_evento, nome_evento, data_evento, local, descricao
        FROM eventos
        WHERE ativo = TRUE
    """)
    eventos = cursor.fetchall()

    if not eventos:
        print("\nNenhum evento disponível.")
        return

    print("\n--- Eventos Ativos ---")
    for e in eventos:
        print(f"\nID: {e[0]} | Nome: {e[1]}\nData: {e[2]} | Local: {e[3]}\nDescrição: {e[4]}")


def registrar_acesso_evento(cursor):
    id_usuario = usuario_logado["id"]

    cursor.execute("SELECT id_evento, nome_evento FROM eventos WHERE ativo = TRUE")
    eventos = cursor.fetchall()

    if not eventos:
        print("\nNão há eventos disponíveis.")
        return

    print("\nEventos disponíveis:")
    for evento in eventos:
        print(f"{evento[0]} - {evento[1]}")

    id_evento = input("\nDigite o ID do evento: ")

    cursor.execute("SELECT id_credencial FROM credenciais WHERE id_usuario = %s", (id_usuario,))
    cred = cursor.fetchone()
    if not cred:
        print("\nVocê não possui uma credencial.")
        return

    id_credencial = cred[0]

    cursor.execute("""
        SELECT p.id_participacao
        FROM participacoes p
        JOIN acessos a ON p.id_acesso = a.id_acesso
        WHERE a.id_credencial = %s AND p.id_evento = %s
    """, (id_credencial, id_evento))
    ja_inscrito = cursor.fetchone()

    if ja_inscrito:
        print("\nVocê já está inscrito neste evento!")
        return

    data_hora = datetime.now()

    cursor.execute("""
        INSERT INTO acessos (id_credencial, id_tipo, data_hora)
        VALUES (%s, %s, %s)
    """, (id_credencial, usuario_logado["tipo_id"], data_hora))

    id_acesso = cursor.lastrowid

    cursor.execute("""
        INSERT INTO participacoes (id_acesso, id_evento, data_inscricao)
        VALUES (%s, %s, %s)
    """, (id_acesso, id_evento, data_hora))

    print("\nInscrição realizada com sucesso!")


def cancelar_inscricao_evento(cursor):
    id_usuario = usuario_logado["id"]

    cursor.execute("SELECT id_credencial FROM credenciais WHERE id_usuario = %s", (id_usuario,))
    cred = cursor.fetchone()

    if not cred:
        print("\nVocê não possui uma credencial.")
        return

    id_credencial = cred[0]

    cursor.execute("""
        SELECT p.id_participacao, e.nome_evento
        FROM participacoes p
        JOIN acessos a ON p.id_acesso = a.id_acesso
        JOIN eventos e ON p.id_evento = e.id_evento
        WHERE a.id_credencial = %s
    """, (id_credencial,))
    participacoes = cursor.fetchall()

    if not participacoes:
        print("\nVocê não está inscrito em nenhum evento.")
        return

    print("\n--- Inscrições ---")
    for p in participacoes:
        print(f"{p[0]} - {p[1]}")

    id_participacao = input("\nDigite o ID da participação que deseja cancelar: ")

    ids_validos = [str(p[0]) for p in participacoes]
    if id_participacao not in ids_validos:
        print("ID inválido.")
        return

    confirmar = input("\nDeseja realmente cancelar? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Cancelamento abortado.")
        return

    cursor.execute("DELETE FROM participacoes WHERE id_participacao = %s", (id_participacao,))
    print("Inscrição cancelada com sucesso.")


def listar_eventos_inscritos(cursor):
    id_usuario = usuario_logado["id"]

    cursor.execute("SELECT id_credencial FROM credenciais WHERE id_usuario = %s", (id_usuario,))
    cred = cursor.fetchone()

    if not cred:
        print("\nVocê não possui uma credencial.")
        return

    id_credencial = cred[0]

    cursor.execute("""
        SELECT e.id_evento, e.nome_evento, e.data_evento, e.local
        FROM participacoes p
        JOIN acessos a ON p.id_acesso = a.id_acesso
        JOIN eventos e ON p.id_evento = e.id_evento
        WHERE a.id_credencial = %s
    """, (id_credencial,))
    eventos = cursor.fetchall()

    if not eventos:
        print("\nVocê não está inscrito em nenhum evento.")
        return

    print("\n--- Eventos Inscritos ---")
    for e in eventos:
        print(f"ID: {e[0]} | Nome: {e[1]} | Data: {e[2]} | Local: {e[3]}")
