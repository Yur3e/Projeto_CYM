CREATE DATABASE projeto_biblioteca; 

USE projeto_biblioteca;

CREATE TABLE livros (
	isbn VARCHAR(13) PRIMARY KEY NOT NULL,
	titulo VARCHAR(150) NOT NULL,
	autor VARCHAR(150) NOT NULL,
	ano YEAR,
	status_livro VARCHAR(10) NOT NULL /* Lembrar que (Coluna status (disponível ou emprestado)) */
);

CREATE TABLE usuarios (

	id int PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(150) NOT NULL,
	cpf VARCHAR(11) UNIQUE NOT NULL,
	email VARCHAR(128) NOT NULL

);

CREATE TABLE emprestimos (

	id int PRIMARY KEY AUTO_INCREMENT,
	livro_id VARCHAR(13),
	usuario_id int,
	data_emprestimo DATETIME NOT NULL,
	data_devolucao DATETIME NOT NULL,
	FOREIGN KEY (livro_id) REFERENCES livros(isbn),
	FOREIGN KEY (usuario_id) REFERENCES usuarios(id)

);


#================Seção de Testes================
#Visualizar:
SELECT * FROM livros; #para teste...
SELECT * FROM usuarios; #para teste...
SELECT * FROM emprestimos; #para teste...

#Deletar:
DROP TABLE livros; #para teste... (erro por conta da foreign key em emprestimos)
DROP TABLE usuarios; #para teste... (erro por conta da foreign key em emprestimos)
DROP TABLE emprestimos; #para teste...

