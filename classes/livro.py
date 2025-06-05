import mysql.connector

class Cadastrar_livros:
    """Classe para gerenciar o cadastro de livros no banco de dados
    
    Atributos privados:
        __conexao: Objeto de conexão com o banco de dados
        __cursor: Cursor para executar comandos SQL
    """
    
    def __init__(self, conexao):
        """Inicializa a classe com a conexão ao banco de dados
        
        Args:
            conexao: Objeto de conexão MySQL
        """
        self.__conexao = conexao  # Atributo privado
        self.__cursor = conexao.cursor(dictionary=True)  # Atributo privado
        
    def __str__(self):
        "Retorna todos os atributos da classe como string"
        return str(vars(self))
    
    def __validar_status(self, status):
        """Método PRIVADO para validar status do livro
        
        Args:
            status: Status a ser validado
            
        Returns:
            bool: True se status for válido, False caso contrário
        """
        return status in ["Disponível", "Emprestado"]
    
    def cadastrar_livro(self, isbn, titulo, autor, ano, status):
        """Método PÚBLICO para cadastrar um novo livro
        
        Args:
            isbn: Código ISBN do livro
            titulo: Título do livro
            autor: Autor do livro
            ano: Ano de publicação
            status: Status do livro
            
        Returns:
            bool: True se cadastro foi bem-sucedido, False caso contrário
        """
        if not self.__validar_status(status):
            print("Erro: Status deve ser 'Disponível' ou 'Emprestado'")
            return False
            
        try:
            sql = """INSERT INTO livros 
                    (isbn, titulo, autor, ano, status_livro) 
                    VALUES (%s, %s, %s, %s, %s)"""
            valores = (isbn, titulo, autor, ano, status)
            
            self.__cursor.execute(sql, valores)
            self.__conexao.commit()
            return True
        except mysql.connector.Error as erro:
            self.__conexao.rollback()
            print(f"Erro ao cadastrar livro: {erro}")
            return False

    def listar_livros(self, status=None):
        """Método PÚBLICO para listar livros
        
        Args:
            status: None para todos os livros ou status específico
            
        Returns:
            list: Lista de dicionários com os livros
        """
        try:
            if status:
                if not self.__validar_status(status):
                    return []
                
                sql = "SELECT * FROM livros WHERE status_livro = %s"
                self.__cursor.execute(sql, (status,))
            else:
                sql = "SELECT * FROM livros"
                self.__cursor.execute(sql)
                
            return self.__cursor.fetchall()
        except mysql.connector.Error as erro:
            print(f"Erro ao listar livros: {erro}")
            return []
    
    def listar_livros_emprestados_com_usuarios(self):
        """Lista livros emprestados com informações dos usuários
        
        Returns:
            list: Lista de dicionários com:
                - Dados do livro
                - Dados do usuário
                - Datas do empréstimo
        """
        try:
            sql = """SELECT 
                        l.isbn, l.titulo, l.autor, l.ano,
                        u.id as usuario_id, u.nome as usuario_nome, 
                        e.data_emprestimo, e.data_devolucao
                    FROM livros l
                    JOIN emprestimos e ON l.isbn = e.livro_id
                    JOIN usuarios u ON e.usuario_id = u.id
                    WHERE l.status_livro = 'Emprestado'"""
            
            self.__cursor.execute(sql)
            return self.__cursor.fetchall()
            
        except mysql.connector.Error as erro:
            print(f"Erro ao listar livros emprestados: {erro}")
            return []

    def fechar_conexao(self):
        """Método PÚBLICO para fechar a conexão"""
        self.__cursor.close()
        self.__conexao.close()