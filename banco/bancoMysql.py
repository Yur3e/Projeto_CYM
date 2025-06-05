import mysql.connector

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="SENHA",  # Senha do localhost
            database="projeto_biblioteca"
        )
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro na conexão com o banco de dados: {erro}")
        return None
