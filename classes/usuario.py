import mysql.connector
import re

class Cadastrar_usuarios:
    """Classe para gerenciar o cadastro de usuários no banco de dados
    
    Atributos:
        __conexao: Objeto de conexão com o banco de dados (privado)
        __cursor: Cursor para executar comandos SQL (privado)
    """
    
    def __init__(self, conexao):
        """Inicializa a classe com a conexão ao banco de dados
        
        Args:
            conexao: Objeto de conexão MySQL
        """
        self.__conexao = conexao
        self.__cursor = conexao.cursor(dictionary=True)
        
    def __str__(self):
        """Retorna uma string legível com os principais atributos da classe"""
        return (
            "Cadastrar_usuarios(\n"
            f"  Conexão: {type(self.__conexao).__name__},\n"
            f"  Cursor: {type(self.__cursor).__name__}\n"
            ")"
        )
    
    def __validar_cpf(self, cpf):
        """Valida se o CPF contém exatamente 11 dígitos numéricos"""
        return len(cpf) == 11 and cpf.isdigit()
    
    def __validar_email(self, email):
        """Valida se o e-mail está em um formato aceitável"""
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)
    
    def cadastrar_usuario(self, nome, cpf, email):
        """Cadastra um novo usuário no sistema
        
        Args:
            nome: Nome completo do usuário
            cpf: CPF (apenas números)
            email: E-mail válido
            
        Returns:
            bool: True se cadastrado com sucesso, False caso contrário
        """
        if not self.__validar_cpf(cpf):
            print("Erro: CPF deve conter exatamente 11 dígitos numéricos")
            return False
            
        if not self.__validar_email(email):
            print("Erro: Formato de e-mail inválido")
            return False
            
        try:
            sql = """INSERT INTO usuarios 
                    (nome, cpf, email) 
                    VALUES (%s, %s, %s)"""
            self.__cursor.execute(sql, (nome, cpf, email))
            self.__conexao.commit()
            print("Usuário cadastrado com sucesso.")
            return True
        except mysql.connector.Error as erro:
            self.__conexao.rollback()
            if erro.errno == 1062:
                print("Erro: CPF já cadastrado no sistema!")
            else:
                print(f"Erro ao cadastrar usuário: {erro}")
            return False

    def listar_usuarios(self):
        """Lista todos os usuários cadastrados
        
        Returns:
            list: Lista de dicionários com os usuários
        """
        try:
            sql = "SELECT id, nome, cpf, email FROM usuarios"
            self.__cursor.execute(sql)
            return self.__cursor.fetchall()
        except mysql.connector.Error as erro:
            print(f"Erro ao listar usuários: {erro}")
            return []

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados"""
        self.__cursor.close()
        self.__conexao.close()
