from estado import usuario_logado
from conexao import conexao, cursor
from datetime import datetime


def listar_eventos(cursor):
    cursor.execute("""
        SELECT id_evento, nome_evento, data_evento, local, descricao
        FROM eventos
        WHERE ativo = TRUE
    """)
    eventos = cursor.fetchall()

    if not eventos:
        print("Não há eventos disponíveis no momento.")
        return

    print("\n--- Eventos Disponíveis ---")
    for evento in eventos:
        print(f"\nID: {evento[0]} | Nome: {evento[1]}\nData: {evento[2]} | Local: {evento[3]}\nDescrição: {evento[4]}")


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
        print("\n--- Minha Credencial ---")
        print(f"Documento: {documento}")
        print(f"Chave de Acesso: {chave}")
        print(f"Data de Registro: {data}")
    else:
        print("Credencial não encontrada.")


def registrar_acesso_evento(cursor):
    id_usuario = usuario_logado["id"]

    cursor.execute("SELECT id_evento, nome_evento, data_evento FROM eventos WHERE ativo = TRUE")
    eventos = cursor.fetchall()

    if not eventos:
        print("Não há eventos disponíveis.")
        return

    print("\n--- Eventos Disponíveis ---")
    for evento in eventos:
        print(f"{evento[0]} - {evento[1]} ({evento[2]})")

    id_evento = input("Digite o ID do evento para participar: ").strip()

    cursor.execute("SELECT id_credencial FROM credenciais WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()

    if not resultado:
        print("Credencial não encontrada.")
        return

    id_credencial = resultado[0]

    cursor.execute("""
        SELECT p.id_participacao
        FROM participacoes p
        JOIN acessos a ON p.id_acesso = a.id_acesso
        WHERE a.id_credencial = %s AND p.id_evento = %s
    """, (id_credencial, id_evento))

    if cursor.fetchone():
        print("Você já está inscrito neste evento.")
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

    print("Inscrição realizada com sucesso!")

    conexao.commit()


def listar_eventos_inscritos(cursor):
    id_usuario = usuario_logado["id"]

    cursor.execute("SELECT id_credencial FROM credenciais WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()

    if not resultado:
        print("Credencial não encontrada.")
        return

    id_credencial = resultado[0]

    cursor.execute("""
        SELECT e.id_evento, e.nome_evento, e.data_evento, e.local
        FROM participacoes p
        JOIN acessos a ON p.id_acesso = a.id_acesso
        JOIN eventos e ON p.id_evento = e.id_evento
        WHERE a.id_credencial = %s
    """, (id_credencial,))

    eventos = cursor.fetchall()

    if not eventos:
        print("Você não está inscrito em nenhum evento.")
        return

    print("\n--- Meus Eventos Inscritos ---")
    for evento in eventos:
        print(f"\nID: {evento[0]} | Nome: {evento[1]}\nData: {evento[2]} | Local: {evento[3]}")
