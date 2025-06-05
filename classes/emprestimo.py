import mysql.connector

class Cadastrar_emprestimos:
    """Classe para gerenciar empréstimos no sistema
    
    Atributos privados:
        __conexao: Objeto de conexão com o banco de dados
        __cursor: Cursor para executar comandos SQL
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
            "Cadastrar_emprestimos(\n"
            f"  Conexão: {type(self.__conexao).__name__},\n"
            f"  Cursor: {type(self.__cursor).__name__}\n"
            ")"
        )
    
    def listar_users_emprestestado(self):
        """Lista usuários que já realizaram empréstimos
        
        Returns:
            list: Usuários com empréstimos registrados (id, nome, cpf, email)
            None: Em caso de erro
        """
        try:
            sql = """SELECT DISTINCT u.id, u.nome, u.cpf, u.email 
                     FROM usuarios u 
                     JOIN emprestimos e ON u.id = e.usuario_id"""
            self.__cursor.execute(sql)
            return self.__cursor.fetchall()
            
        except mysql.connector.Error as erro:
            print(f"Erro ao listar usuários com empréstimos: {erro}")
            return None

    def __verificar_livro(self, livro_id):
        """Verifica se o livro está disponível
        
        Args:
            livro_id (str): ISBN do livro
        
        Returns:
            dict ou None: Dados do livro se disponível, None caso contrário
        """
        sql = "SELECT isbn FROM livros WHERE isbn = %s AND status_livro = 'Disponível'"
        self.__cursor.execute(sql, (livro_id,))
        return self.__cursor.fetchone()
    
    def __verificar_usuario(self, usuario_id):
        """Verifica se o usuário existe
        
        Args:
            usuario_id (int): ID do usuário
        
        Returns:
            dict ou None: Dados do usuário se existir, None caso contrário
        """
        sql = "SELECT id FROM usuarios WHERE id = %s"
        self.__cursor.execute(sql, (usuario_id,))
        return self.__cursor.fetchone()
    
    def cadastrar(self, livro_id, usuario_id, data_emprestimo):
        """Registra um novo empréstimo
        
        Args:
            livro_id (str): ISBN do livro
            usuario_id (int): ID do usuário
            data_emprestimo (str): Data e hora do empréstimo no formato 'YYYY-MM-DD HH:MM:SS'
        
        Returns:
            bool: True se o empréstimo for registrado, False caso contrário
        """
        if not self.__verificar_livro(livro_id):
            print("Erro: Livro não disponível ou não encontrado")
            return False
            
        if not self.__verificar_usuario(usuario_id):
            print("Erro: Usuário não encontrado")
            return False
            
        try:
            sql = """INSERT INTO emprestimos 
                    (livro_id, usuario_id, data_emprestimo)
                    VALUES (%s, %s, %s)"""
            self.__cursor.execute(sql, (livro_id, usuario_id, data_emprestimo))
            
            # Atualiza status do livro para "Emprestado"
            update_sql = "UPDATE livros SET status_livro = 'Emprestado' WHERE isbn = %s"
            self.__cursor.execute(update_sql, (livro_id,))
            
            self.__conexao.commit()
            print("Empréstimo registrado com sucesso!")
            return True
        except mysql.connector.Error as erro:
            self.__conexao.rollback()
            print(f"Erro ao registrar empréstimo: {erro}")
            return False

    def cadastrar_devolucao(self, livro_id, usuario_id, data_devolucao):
        """Registra a devolução de um livro emprestado
        
        Args:
            livro_id (str): ISBN do livro
            usuario_id (int): ID do usuário
            data_devolucao (str): Data e hora da devolução no formato 'YYYY-MM-DD HH:MM:SS'
        
        Returns:
            bool: True se devolução registrada, False caso contrário
        """
        try:
            # Verifica se existe empréstimo ativo para este livro e usuário
            sql_check = """SELECT id FROM emprestimos 
                          WHERE livro_id = %s AND usuario_id = %s 
                          AND data_devolucao IS NULL"""
            self.__cursor.execute(sql_check, (livro_id, usuario_id))
            if not self.__cursor.fetchone():
                print("Erro: Não existe empréstimo ativo para este livro e usuário")
                return False
            
            # Atualiza data de devolução
            sql_update = """UPDATE emprestimos 
                            SET data_devolucao = %s 
                            WHERE livro_id = %s AND usuario_id = %s 
                            AND data_devolucao IS NULL"""
            self.__cursor.execute(sql_update, (data_devolucao, livro_id, usuario_id))
            
            # Atualiza status do livro para "Disponível"
            update_sql = "UPDATE livros SET status_livro = 'Disponível' WHERE isbn = %s"
            self.__cursor.execute(update_sql, (livro_id,))
            
            self.__conexao.commit()
            print("Devolução registrada com sucesso!")
            return True
        except mysql.connector.Error as erro:
            self.__conexao.rollback()
            print(f"Erro ao registrar devolução: {erro}")
            return False

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados"""
        self.__cursor.close()
        self.__conexao.close()
