from db_config import get_db_connection
from mysql.connector import Error

def verificar_estrutura():
    """Verifica se o banco de dados e as tabelas foram criados corretamente."""
    conn = get_db_connection()
    if not conn:
        print("❌ Erro: Não foi possível conectar ao banco de dados!")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar tabelas
        cursor.execute("SHOW TABLES")
        tabelas = cursor.fetchall()
        tabelas = [t[0] for t in tabelas]
        
        print("\n=== Verificação da Estrutura do Banco de Dados ===")
        print("\n1. Conexão com o Banco:")
        print("✅ Conexão estabelecida com sucesso!")
        
        print("\n2. Tabelas Encontradas:")
        if 'cliente' in tabelas:
            print("✅ Tabela 'cliente' encontrada")
        else:
            print("❌ Tabela 'cliente' não encontrada!")
        
        if 'contato' in tabelas:
            print("✅ Tabela 'contato' encontrada")
        else:
            print("❌ Tabela 'contato' não encontrada!")
        
        print("\n3. Estrutura das Tabelas:")
        
        # Verificar estrutura da tabela cliente
        cursor.execute("DESCRIBE cliente")
        colunas_cliente = {row[0]: row[1] for row in cursor.fetchall()}
        print("\nTabela 'cliente':")
        print(f"✅ id_cliente: {colunas_cliente.get('id_cliente', '❌ Não encontrado')}")
        print(f"✅ nome: {colunas_cliente.get('nome', '❌ Não encontrado')}")
        print(f"✅ email: {colunas_cliente.get('email', '❌ Não encontrado')}")
        print(f"✅ telefone: {colunas_cliente.get('telefone', '❌ Não encontrado')}")
        print(f"✅ endereco: {colunas_cliente.get('endereco', '❌ Não encontrado')}")
        
        # Verificar estrutura da tabela contato
        cursor.execute("DESCRIBE contato")
        colunas_contato = {row[0]: row[1] for row in cursor.fetchall()}
        print("\nTabela 'contato':")
        print(f"✅ id_contato: {colunas_contato.get('id_contato', '❌ Não encontrado')}")
        print(f"✅ id_cliente: {colunas_contato.get('id_cliente', '❌ Não encontrado')}")
        print(f"✅ nome: {colunas_contato.get('nome', '❌ Não encontrado')}")
        print(f"✅ telefone: {colunas_contato.get('telefone', '❌ Não encontrado')}")
        print(f"✅ email: {colunas_contato.get('email', '❌ Não encontrado')}")
        print(f"✅ tipo: {colunas_contato.get('tipo', '❌ Não encontrado')}")
        
        # Verificar chaves estrangeiras
        cursor.execute("""
            SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'contato'
            AND REFERENCED_TABLE_NAME IS NOT NULL
            AND TABLE_SCHEMA = 'sistema_clientes'
        """)
        fks = cursor.fetchall()
        
        print("\n4. Relacionamentos:")
        if any(fk[0] == 'id_cliente' and fk[1] == 'cliente' for fk in fks):
            print("✅ Chave estrangeira configurada corretamente entre contato e cliente")
        else:
            print("❌ Chave estrangeira não encontrada ou mal configurada!")
        
        return True
        
    except Error as e:
        print(f"\n❌ Erro ao verificar estrutura: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def testar_operacoes():
    """Testa as operações CRUD básicas no banco de dados."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        print("\n=== Teste de Operações CRUD ===")
        
        # CREATE - Inserir cliente teste
        print("\n1. Testando INSERT:")
        cursor.execute("""
            INSERT INTO cliente (nome, email, telefone, endereco)
            VALUES ('Cliente Teste', 'teste@teste.com', '123456789', 'Endereço Teste')
        """)
        id_cliente = cursor.lastrowid
        print("✅ INSERT em 'cliente' funcionou!")
        
        # Inserir contato teste
        cursor.execute("""
            INSERT INTO contato (id_cliente, nome, telefone, email, tipo)
            VALUES (%s, 'Contato Teste', '987654321', 'contato@teste.com', 'pessoal')
        """, (id_cliente,))
        print("✅ INSERT em 'contato' funcionou!")
        
        # READ - Selecionar dados
        print("\n2. Testando SELECT:")
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        if cliente:
            print("✅ SELECT em 'cliente' funcionou!")
        
        cursor.execute("SELECT * FROM contato WHERE id_cliente = %s", (id_cliente,))
        contato = cursor.fetchone()
        if contato:
            print("✅ SELECT em 'contato' funcionou!")
        
        # UPDATE - Atualizar dados
        print("\n3. Testando UPDATE:")
        cursor.execute("""
            UPDATE cliente 
            SET nome = 'Cliente Teste Atualizado'
            WHERE id_cliente = %s
        """, (id_cliente,))
        print("✅ UPDATE em 'cliente' funcionou!")
        
        # DELETE - Limpar dados de teste
        print("\n4. Testando DELETE:")
        cursor.execute("DELETE FROM contato WHERE id_cliente = %s", (id_cliente,))
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
        print("✅ DELETE funcionou!")
        
        conn.commit()
        return True
        
    except Error as e:
        print(f"\n❌ Erro ao testar operações: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Iniciando verificação do banco de dados...\n")
    if verificar_estrutura():
        print("\nEstrutura do banco de dados está correta!")
        print("\nIniciando testes de operações CRUD...")
        if testar_operacoes():
            print("\n✅ Todos os testes completados com sucesso!")
            print("\nO sistema está pronto para uso!")
        else:
            print("\n❌ Falha nos testes de operações!")
    else:
        print("\n❌ Falha na verificação da estrutura!") 