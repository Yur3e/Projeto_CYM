from banco.bancoMysql import conectar_banco
from classes.livro import Cadastrar_livros
from classes.usuario import Cadastrar_usuarios
from classes.emprestimo import Cadastrar_emprestimos

# Projeto Biblioteca CYM - Equipe: Caio Henrique, José Yure, Marcelly Alves
# Fazendo conexão com o banco
projeto_biblioteca = conectar_banco()

# Verificando se a conexão foi concluída
if projeto_biblioteca is None:
    print("\nFalha ao conectar no banco. Encerrando o programa.")
    exit()

# Instanciando a classe e passando a conexão com nosso db
cadastro_livro = Cadastrar_livros(projeto_biblioteca)
cadastro_usuario = Cadastrar_usuarios(projeto_biblioteca)
cadastro_emprestimo = Cadastrar_emprestimos(projeto_biblioteca)

while True:
    print("\n==Menu de opções do Projeto Biblioteca==")
    print("\nOpção 1 - Cadastrar Livro")
    print("Opção 2 - Cadastrar Usuário")
    print("Opção 3 - Cadastrar Emprestimos")
    print("Opção 4 - Registrar Devolução")
    print("Opção 5 - Listagens")
    print("Opção 6 - Mostrar Atributos das Classes")
    print("Opção 7 - Apresentar Membros da Equipe")
    print("Opção 0 - Encerrar o sistema")
    
    opcao = int(input("\nDigite a sua opção de escolha: "))
    
    if opcao == 1: # Entrada de dados do livro
        isbn = str(input("\nDigite o ISBN do livro: "))
        titulo = str(input("Digite o título do livro: "))
        autor = str(input("Digite o nome do autor: "))
        ano = str(input("Digite o ano do livro: "))
        status = str(input("Digite o Status do livro: ")) # Disponível ou Emprestado
        
        # Executando cadastro de livro
        cadastro_livro.cadastrar_livro(isbn, titulo, autor, ano, status)   
        
    elif opcao == 2: # Entrada de dados do usuário
        nome = str(input("\nDigite seu nome: "))
        cpf = str(input("Digite o seu cpf: "))
        email = str(input("Digite o seu e-mail: "))
        
        # Executando cadastro de usuário
        cadastro_usuario.cadastrar_usuario(nome, cpf, email)     
        
    elif opcao == 3: # Registro de emprestimo
        livro_id = str(input("\nDigite o ID do livro: "))
        usuario_id = str(input("Digite o ID do usuário: "))
        data_emprestimo = str(input("Digite a data em que o emprestimo do livro está sendo realizado(Ano-Mês-Dia H:M:S): "))
    
        # Executando registro de emprestimo
        cadastro_emprestimo.cadastrar(livro_id, usuario_id, data_emprestimo)     
        
    elif opcao == 4: # Registro de devolução
        livro_id = str(input("\nDigite o ID do livro: "))
        usuario_id = str(input("Digite o ID do usuário: "))
        data_devolucao = str(input("Digite a data de devolução do emprestimo do livro(Ano-Mês-Dia H:M:S): "))
        
        # Executando registro de devolução
        cadastro_emprestimo.cadastrar_devolucao(livro_id, usuario_id, data_devolucao)
        
    elif opcao == 5: # Listagens 
        print("\n====Opções de Listagens====")
        print("\n1 - Listar livros disponíveis\n"
              +"2 - Listar livros emprestados (Livro e Usuário)\n"+
              "3 - Listar usuários\n"+
              "4 - Listar todos usuários que já realizaram emprestimos")
        
        op_list = int(input("\nDigite a opção de listagem: "))
            
        if op_list == 1: # Livros disponíveis
            livros = cadastro_livro.listar_livros("Disponível")
            print("\n=== Livros Disponíveis ===")
            for livro in livros:
                print(f"ISBN: {livro['isbn']} | Título: {livro['titulo']} | Autor: {livro['autor']} | Ano: {livro['ano']}")
                
        elif op_list == 2:  # Listar livros emprestados com usuários
            livros_emprestados = cadastro_livro.listar_livros_emprestados_com_usuarios()
            if livros_emprestados:
                print("\n=== Livros Emprestados ===")
                for livro in livros_emprestados:
                    print(f"\nLivro: {livro['titulo']} (ISBN: {livro['isbn']})")
                    print(f"Autor: {livro['autor']} | Ano: {livro['ano']}")
                    print(f"Emprestado para: {livro['usuario_nome']} (ID: {livro['usuario_id']})")
                    print(f"Data do empréstimo: {livro['data_emprestimo']}")
                    if livro['data_devolucao']:
                        print(f"Devolvido em: {livro['data_devolucao']}")
            else:
                print("\nNenhum livro emprestado no momento.")
                
        elif op_list == 3:  # Todos os usuários
            usuarios = cadastro_usuario.listar_usuarios()
            print("\n=== Todos os Usuários ===\n")
            for usuario in usuarios:
                print(f"ID: {usuario['id']} | Nome: {usuario['nome']} | CPF: {usuario['cpf']} | Email: {usuario['email']}")
                
        elif op_list == 4:
            print("\n=== Usuários que já realizaram empréstimos ===")
            usuarios = cadastro_emprestimo.listar_users_emprestestado()
            if usuarios:
                for usuario in usuarios:
                    print(f"ID: {usuario['id']} | Nome: {usuario['nome']} | CPF: {usuario['cpf']} | Email: {usuario['email']}")
            else:
                print("\nNenhum usuário encontrado.")
    
    elif opcao == 6:  # Opção para mostrar atributos das classes
        print("\n=== Atributos das Classes ===")
        print("\nCadastrar Livros:")
        print(cadastro_livro)
        print("\nCadastrar Usuários:")
        print(cadastro_usuario)
        print("\nCadastrar Empréstimos:")
        print(cadastro_emprestimo)
                
    elif opcao == 7: # Opção para mostrar o nome dos membros da equipe
        print("\nDesenvolvedores: Caio Henrique, José Yure, Marcelly Alves - Turma B de Ciência de Dados 2° período")
        
    elif opcao == 0: # Opção para encerrar o programa
        print("\nEncerrando o programa...")
        break

    else: # Caso nenhuma das opções anteriores, retornar opção inválida
        print("\nOpção inválida. Tente novamente.")

# Fechando conexões
cadastro_livro.fechar_conexao()
cadastro_usuario.fechar_conexao()
cadastro_emprestimo.fechar_conexao()