import mysql.connector
import os
import hashlib
import random
import string
from dotenv import load_dotenv

load_dotenv()


def conectar_mysql():
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conexao.cursor()
    return conexao, cursor


def gerar_chave_acesso(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))


def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def verificar_senha(senha_inserida, senha_armazenada):
    senha_hash = gerar_hash(senha_inserida)
    return senha_hash == senha_armazenada or senha_inserida == senha_armazenada
