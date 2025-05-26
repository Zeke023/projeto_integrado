from auth import tela_login_cadastro
from conexao import conexao, cursor

if __name__ == "__main__":
    try:
        tela_login_cadastro(cursor, conexao)
    finally:
        cursor.close()
        conexao.close()