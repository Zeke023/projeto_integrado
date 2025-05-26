from datetime import datetime

# Menu de eventos
def menu_eventos(cursor):
    while True:
        print("\n--- Menu de Gerenciamento de Eventos ---")
        print("1. Inserir Evento")
        print("2. Listar Eventos")
        print("3. Relatório de Acessos por Evento")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            inserir_evento(cursor)
        elif opcao == '2':
            listar_eventos(cursor)
        elif opcao == '3':
            relatorio_acessos_evento(cursor)
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Inserir um novo evento
def inserir_evento(cursor):
    print("\n--- Inserir Novo Evento ---")
    nome = input("Nome do evento: ").strip()
    descricao = input("Descrição: ").strip()
    data_evento = input("Data do evento (YYYY-MM-DD): ").strip()
    local = input("Local: ").strip()

    try:
        cursor.execute("""
            INSERT INTO eventos (nome_evento, descricao, data_evento, local, ativo)
            VALUES (%s, %s, %s, %s, TRUE)
        """, (nome, descricao, data_evento, local))
        print("Evento cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir evento: {e}")

# Listar eventos cadastrados
def listar_eventos(cursor):
    print("\n--- Lista de Eventos ---")
    cursor.execute("""
        SELECT id_evento, nome_evento, data_evento, local, descricao, ativo
        FROM eventos
        ORDER BY data_evento
    """)
    eventos = cursor.fetchall()

    if not eventos:
        print("Nenhum evento encontrado.")
        return

    for evento in eventos:
        status = "Ativo" if evento[4] else "Inativo"
        print(f"\nID: {evento[0]} | Nome: {evento[1]}\nData: {evento[2]} | Local: {evento[3]}\nDescrição: {evento[4]}\nStatus: {status}")

# Relatório de acessos por evento
def relatorio_acessos_evento(cursor):
    print("\n--- Relatório de Acessos por Evento ---")
    cursor.execute("""
        SELECT e.id_evento, e.nome_evento, COUNT(p.id_participacao) AS total_participacoes
        FROM eventos e
        LEFT JOIN participacoes p ON e.id_evento = p.id_evento
        GROUP BY e.id_evento, e.nome_evento
        ORDER BY e.data_evento;
    """)
    resultados = cursor.fetchall()

    if resultados:
        for r in resultados:
            print(f"ID: {r[0]} | Evento: {r[1]} | Total de Participações: {r[2]}")
    else:
        print("Nenhum evento encontrado para gerar relatório.")

# Relatório geral de acessos (todos os acessos registrados no sistema)
def gerar_relatorio_acessos(cursor):
    print("\n--- Relatório Geral de Acessos ---")
    cursor.execute("""
        SELECT a.id_acesso, c.id_credencial, a.data_hora, t.nome_tipo
        FROM acessos a
        JOIN credenciais c ON a.id_credencial = c.id_credencial
        JOIN tipos_acesso t ON a.id_tipo = t.id_tipo
        ORDER BY a.data_hora DESC
    """)
    acessos = cursor.fetchall()

    if acessos:
        for acesso in acessos:
            print(f"ID Acesso: {acesso[0]} | Credencial: {acesso[1]} | Data/Hora: {acesso[2]} | Tipo: {acesso[3]}")
    else:
        print("Nenhum acesso encontrado.")
