#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema de Cadastro de Clientes e Contatos - Versão MySQL
Este módulo implementa um sistema de cadastro de clientes e seus contatos,
utilizando MySQL como banco de dados.
"""

from db_config import get_db_connection
from mysql.connector import Error

def menu_principal():
    """Exibe o menu principal e retorna a opção escolhida pelo usuário."""
    print("\n=== SISTEMA DE CADASTRO DE CLIENTES ===")
    print("1. Cadastrar novo cliente")
    print("2. Listar clientes")
    print("3. Editar cliente")
    print("4. Excluir cliente")
    print("5. Cadastrar contato para cliente")
    print("6. Listar contatos de um cliente")
    print("7. Buscar clientes")
    print("0. Sair")
    return input("\nEscolha uma opção: ")

def cadastrar_cliente():
    """Cadastra um novo cliente no sistema."""
    print("\n=== NOVO CLIENTE ===")
    nome = input("Nome: ").strip()
    while not nome:
        print("O nome é obrigatório!")
        nome = input("Nome: ").strip()
    
    email = input("Email: ").strip()
    while not email:
        print("O email é obrigatório!")
        email = input("Email: ").strip()
    
    telefone = input("Telefone: ").strip()
    endereco = input("Endereço: ").strip()
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """INSERT INTO cliente (nome, email, telefone, endereco) 
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (nome, email, telefone, endereco))
        conn.commit()
        print("\nCliente cadastrado com sucesso!")
    except Error as e:
        if "Duplicate entry" in str(e):
            print("Este email já está cadastrado!")
        else:
            print(f"Erro ao cadastrar cliente: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_clientes():
    """Lista todos os clientes cadastrados."""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cliente")
        clientes = cursor.fetchall()
        
        print("\n=== LISTA DE CLIENTES ===")
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return
        
        for cliente in clientes:
            print(f"\nID: {cliente['id_cliente']}")
            print(f"Nome: {cliente['nome']}")
            print(f"Email: {cliente['email']}")
            print(f"Telefone: {cliente['telefone']}")
            print(f"Endereço: {cliente['endereco']}")
            print("-" * 40)
    except Error as e:
        print(f"Erro ao listar clientes: {e}")
    finally:
        cursor.close()
        conn.close()

def editar_cliente():
    """Edita as informações de um cliente existente."""
    listar_clientes()
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        id_cliente = int(input("\nID do cliente a editar: "))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        print("\nDeixe em branco para manter o valor atual")
        nome = input(f"Nome ({cliente['nome']}): ").strip() or cliente['nome']
        email_temp = input(f"Email ({cliente['email']}): ").strip() or cliente['email']
        telefone = input(f"Telefone ({cliente['telefone']}): ").strip() or cliente['telefone']
        endereco = input(f"Endereço ({cliente['endereco']}): ").strip() or cliente['endereco']
        
        sql = """UPDATE cliente 
                SET nome = %s, email = %s, telefone = %s, endereco = %s 
                WHERE id_cliente = %s"""
        cursor.execute(sql, (nome, email_temp, telefone, endereco, id_cliente))
        conn.commit()
        
        print("\nCliente atualizado com sucesso!")
    except ValueError:
        print("ID inválido! Digite um número inteiro.")
    except Error as e:
        if "Duplicate entry" in str(e):
            print("Este email já está cadastrado para outro cliente!")
        else:
            print(f"Erro ao atualizar cliente: {e}")
    finally:
        cursor.close()
        conn.close()

def excluir_cliente():
    """Exclui um cliente do sistema."""
    listar_clientes()
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        id_cliente = int(input("\nID do cliente a excluir: "))
        
        cursor = conn.cursor(dictionary=True)
        
        # Verificar se o cliente existe
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (id_cliente,))
        if not cursor.fetchone():
            print("Cliente não encontrado!")
            return
        
        # Verificar se o cliente possui contatos
        cursor.execute("SELECT COUNT(*) as total FROM contato WHERE id_cliente = %s", (id_cliente,))
        total_contatos = cursor.fetchone()['total']
        
        if total_contatos > 0:
            print(f"\nAtenção: Este cliente possui {total_contatos} contato(s).")
            confirmacao = input("Deseja realmente excluir o cliente e seus contatos? (s/N): ").lower()
            if confirmacao != 's':
                print("Operação cancelada.")
                return
            
            # Excluir contatos primeiro (devido à chave estrangeira)
            cursor.execute("DELETE FROM contato WHERE id_cliente = %s", (id_cliente,))
        
        # Excluir o cliente
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        
        print("\nCliente e seus contatos foram excluídos com sucesso!")
    except ValueError:
        print("ID inválido! Digite um número inteiro.")
    except Error as e:
        print(f"Erro ao excluir cliente: {e}")
    finally:
        cursor.close()
        conn.close()

def cadastrar_contato():
    """Cadastra um novo contato para um cliente."""
    listar_clientes()
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        id_cliente = int(input("\nID do cliente para cadastrar contato: "))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nome FROM cliente WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        print(f"\n=== NOVO CONTATO PARA {cliente['nome'].upper()} ===")
        nome = input("Nome do contato: ").strip()
        while not nome:
            print("O nome do contato é obrigatório!")
            nome = input("Nome do contato: ").strip()
        
        telefone = input("Telefone: ").strip()
        email = input("Email: ").strip()
        
        tipo = input("Tipo (pessoal/comercial): ").strip().lower()
        while tipo not in ['pessoal', 'comercial']:
            print("Tipo inválido! Digite 'pessoal' ou 'comercial'")
            tipo = input("Tipo (pessoal/comercial): ").strip().lower()
        
        sql = """INSERT INTO contato (id_cliente, nome, telefone, email, tipo) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (id_cliente, nome, telefone, email, tipo))
        conn.commit()
        
        print("\nContato cadastrado com sucesso!")
    except ValueError:
        print("ID inválido! Digite um número inteiro.")
    except Error as e:
        print(f"Erro ao cadastrar contato: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_contatos_cliente():
    """Lista todos os contatos de um cliente específico."""
    listar_clientes()
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        id_cliente = int(input("\nID do cliente para listar contatos: "))
        
        cursor = conn.cursor(dictionary=True)
        
        # Verificar se o cliente existe
        cursor.execute("SELECT nome FROM cliente WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        # Buscar contatos do cliente
        cursor.execute("SELECT * FROM contato WHERE id_cliente = %s", (id_cliente,))
        contatos = cursor.fetchall()
        
        print(f"\n=== CONTATOS DE {cliente['nome'].upper()} ===")
        if not contatos:
            print("Nenhum contato cadastrado para este cliente.")
        else:
            for contato in contatos:
                print(f"\nID: {contato['id_contato']}")
                print(f"Nome: {contato['nome']}")
                print(f"Telefone: {contato['telefone']}")
                print(f"Email: {contato['email']}")
                print(f"Tipo: {contato['tipo']}")
                print("-" * 30)
    except ValueError:
        print("ID inválido! Digite um número inteiro.")
    except Error as e:
        print(f"Erro ao listar contatos: {e}")
    finally:
        cursor.close()
        conn.close()

def buscar_clientes():
    """Busca clientes por nome ou email."""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        termo = input("\nDigite o nome ou email para buscar: ").strip()
        if not termo:
            print("Digite um termo de busca válido!")
            return
        
        cursor = conn.cursor(dictionary=True)
        sql = """SELECT * FROM cliente 
                 WHERE nome LIKE %s OR email LIKE %s"""
        termo_busca = f"%{termo}%"
        cursor.execute(sql, (termo_busca, termo_busca))
        resultados = cursor.fetchall()
        
        print("\n=== RESULTADOS DA BUSCA ===")
        if not resultados:
            print("Nenhum cliente encontrado.")
        else:
            for cliente in resultados:
                print(f"\nID: {cliente['id_cliente']}")
                print(f"Nome: {cliente['nome']}")
                print(f"Email: {cliente['email']}")
                print(f"Telefone: {cliente['telefone']}")
                print(f"Endereço: {cliente['endereco']}")
                print("-" * 40)
    except Error as e:
        print(f"Erro ao buscar clientes: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    """Função principal que executa o loop do programa."""
    print("Bem-vindo ao Sistema de Cadastro de Clientes e Contatos!")
    
    # Testar conexão com o banco de dados
    conn = get_db_connection()
    if not conn:
        print("Não foi possível conectar ao banco de dados. Verifique se o MySQL está rodando.")
        return
    conn.close()
    
    while True:
        opcao = menu_principal()
        
        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            editar_cliente()
        elif opcao == "4":
            excluir_cliente()
        elif opcao == "5":
            cadastrar_contato()
        elif opcao == "6":
            listar_contatos_cliente()
        elif opcao == "7":
            buscar_clientes()
        elif opcao == "0":
            print("\nObrigado por usar o sistema!")
            break
        else:
            print("\nOpção inválida! Por favor, tente novamente.")

if __name__ == "__main__":
    main() 