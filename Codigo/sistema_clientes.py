#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema de Cadastro de Clientes e Contatos - Versão Inicial
Este módulo implementa um sistema simples de cadastro de clientes e seus contatos,
utilizando estruturas de dados em memória (listas e dicionários).
"""

# Estruturas de dados temporárias (serão substituídas pelo banco de dados)
clientes = []
contatos = []

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
    
    # Verificar se o email já existe
    if any(c["email"] == email for c in clientes):
        print("Este email já está cadastrado!")
        return
    
    telefone = input("Telefone: ").strip()
    endereco = input("Endereço: ").strip()
    
    cliente = {
        "id": len(clientes) + 1,
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "endereco": endereco
    }
    
    clientes.append(cliente)
    print("\nCliente cadastrado com sucesso!")

def listar_clientes():
    """Lista todos os clientes cadastrados."""
    print("\n=== LISTA DE CLIENTES ===")
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    
    for cliente in clientes:
        print(f"\nID: {cliente['id']}")
        print(f"Nome: {cliente['nome']}")
        print(f"Email: {cliente['email']}")
        print(f"Telefone: {cliente['telefone']}")
        print(f"Endereço: {cliente['endereco']}")
        print("-" * 40)

def editar_cliente():
    """Edita as informações de um cliente existente."""
    listar_clientes()
    if not clientes:
        return
    
    try:
        id_cliente = int(input("\nID do cliente a editar: "))
        cliente = next((c for c in clientes if c["id"] == id_cliente), None)
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        print("\nDeixe em branco para manter o valor atual")
        nome = input(f"Nome ({cliente['nome']}): ").strip() or cliente['nome']
        email_temp = input(f"Email ({cliente['email']}): ").strip() or cliente['email']
        
        # Verificar se o novo email já existe em outro cliente
        if email_temp != cliente['email'] and any(c["email"] == email_temp for c in clientes):
            print("Este email já está cadastrado para outro cliente!")
            return
        
        telefone = input(f"Telefone ({cliente['telefone']}): ").strip() or cliente['telefone']
        endereco = input(f"Endereço ({cliente['endereco']}): ").strip() or cliente['endereco']
        
        cliente.update({
            "nome": nome,
            "email": email_temp,
            "telefone": telefone,
            "endereco": endereco
        })
        
        print("\nCliente atualizado com sucesso!")
    except ValueError:
        print("ID inválido! Digite um número inteiro.")

def excluir_cliente():
    """Exclui um cliente do sistema."""
    global clientes, contatos
    
    listar_clientes()
    if not clientes:
        return
    
    try:
        id_cliente = int(input("\nID do cliente a excluir: "))
        cliente = next((c for c in clientes if c["id"] == id_cliente), None)
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        # Verificar se o cliente possui contatos
        contatos_cliente = [c for c in contatos if c["id_cliente"] == id_cliente]
        if contatos_cliente:
            print(f"\nAtenção: Este cliente possui {len(contatos_cliente)} contato(s).")
            confirmacao = input("Deseja realmente excluir o cliente e seus contatos? (s/N): ").lower()
            if confirmacao != 's':
                print("Operação cancelada.")
                return
        
        clientes = [c for c in clientes if c["id"] != id_cliente]
        contatos = [c for c in contatos if c["id_cliente"] != id_cliente]
        print("\nCliente e seus contatos foram excluídos com sucesso!")
    except ValueError:
        print("ID inválido! Digite um número inteiro.")

def cadastrar_contato():
    """Cadastra um novo contato para um cliente."""
    listar_clientes()
    if not clientes:
        return
    
    try:
        id_cliente = int(input("\nID do cliente para cadastrar contato: "))
        cliente = next((c for c in clientes if c["id"] == id_cliente), None)
        
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
        
        contato = {
            "id": len(contatos) + 1,
            "id_cliente": id_cliente,
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "tipo": tipo
        }
        
        contatos.append(contato)
        print("\nContato cadastrado com sucesso!")
    except ValueError:
        print("ID inválido! Digite um número inteiro.")

def listar_contatos_cliente():
    """Lista todos os contatos de um cliente específico."""
    listar_clientes()
    if not clientes:
        return
    
    try:
        id_cliente = int(input("\nID do cliente para listar contatos: "))
        cliente = next((c for c in clientes if c["id"] == id_cliente), None)
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        contatos_cliente = [c for c in contatos if c["id_cliente"] == id_cliente]
        
        print(f"\n=== CONTATOS DE {cliente['nome'].upper()} ===")
        if not contatos_cliente:
            print("Nenhum contato cadastrado para este cliente.")
        else:
            for contato in contatos_cliente:
                print(f"\nID: {contato['id']}")
                print(f"Nome: {contato['nome']}")
                print(f"Telefone: {contato['telefone']}")
                print(f"Email: {contato['email']}")
                print(f"Tipo: {contato['tipo']}")
                print("-" * 30)
    except ValueError:
        print("ID inválido! Digite um número inteiro.")

def buscar_clientes():
    """Busca clientes por nome ou email."""
    if not clientes:
        print("\nNenhum cliente cadastrado.")
        return
    
    termo = input("\nDigite o nome ou email para buscar: ").strip().lower()
    if not termo:
        print("Digite um termo de busca válido!")
        return
    
    resultados = [
        c for c in clientes
        if termo in c['nome'].lower() or termo in c['email'].lower()
    ]
    
    print("\n=== RESULTADOS DA BUSCA ===")
    if not resultados:
        print("Nenhum cliente encontrado.")
    else:
        for cliente in resultados:
            print(f"\nID: {cliente['id']}")
            print(f"Nome: {cliente['nome']}")
            print(f"Email: {cliente['email']}")
            print(f"Telefone: {cliente['telefone']}")
            print(f"Endereço: {cliente['endereco']}")
            print("-" * 40)

def main():
    """Função principal que executa o loop do programa."""
    print("Bem-vindo ao Sistema de Cadastro de Clientes e Contatos!")
    
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