# Sistema de Cadastro de Clientes e Contatos

Este é um sistema simples de cadastro de clientes e contatos desenvolvido em Python. O sistema permite gerenciar informações de clientes e seus contatos associados, inicialmente com armazenamento em memória e posteriormente migrado para um banco de dados MySQL.

## Funcionalidades

- **Cadastro de Clientes**: Adicionar novos clientes com nome, email, telefone e endereço.
- **Listagem de Clientes**: Listar todos os clientes cadastrados.
- **Edição de Clientes**: Atualizar informações de clientes existentes.
- **Exclusão de Clientes**: Remover clientes do sistema.
- **Cadastro de Contatos**: Adicionar múltiplos contatos para cada cliente.
- **Listagem de Contatos**: Listar contatos associados a um cliente.
- **Busca de Clientes**: Buscar clientes por nome ou email.

## Estrutura do Projeto

```
Projeto_Integrador/
├── Codigo/
│   ├── sistema_clientes.py       # Implementação do sistema (CLI)
│   ├── sistema_clientes_gui.py   # Implementação da interface gráfica (GUI)
│   ├── db_config.py              # Configurações de conexão com o MySQL
│   └── verificar_banco.py        # Script para testar o banco de dados
├── Documentacao/
│   ├── Requisitos.txt            # Requisitos funcionais e não funcionais
│   ├── Modelo_Logico.txt         # Modelo lógico do banco de dados
│   └── Script_SQL.sql            # Script para criação do banco de dados
├── .gitignore                    # Arquivo para ignorar arquivos no Git
├── requirements.txt              # Dependências do projeto
└── README.md                     # Este arquivo
```

## Como Executar

### Pré-requisitos

1. **Python 3.6 ou superior** instalado.
2. **MySQL** configurado (pode ser via XAMPP ou outro servidor MySQL).
3. **HeidiSQL** ou outra ferramenta para gerenciar o banco de dados.

### Instalação das Dependências

Instale as dependências do projeto usando o arquivo `requirements.txt`:

```powershell
pip install -r requirements.txt
```

### Configuração do Banco de Dados

1. Execute o script SQL (`Script_SQL.sql`) no MySQL para criar o banco de dados e as tabelas.
2. Configure as credenciais de conexão no arquivo `db_config.py`.

### Executando o Sistema

#### Versão CLI (Linha de Comando)

1. Navegue até a pasta `Codigo`:
   ```powershell
   cd Codigo
   ```
2. Execute o sistema:
   ```powershell
   python sistema_clientes.py
   ```

#### Versão GUI (Interface Gráfica)

1. Navegue até a pasta `Codigo`:
   ```powershell
   cd Codigo
   ```
2. Execute a interface gráfica:
   ```powershell
   python sistema_clientes_gui.py
   ```

## Dependências

As principais dependências do projeto são:

- `mysql-connector-python==8.0.32`: Biblioteca para conexão com o MySQL.
- `python-dotenv==1.0.0`: Biblioteca para gerenciar variáveis de ambiente (opcional, se usado).

## Próximas Etapas

- Melhorias na interface gráfica (GUI).
- Adição de relatórios e exportação de dados.
- Implementação de autenticação de usuários.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Utilização

Ao iniciar o sistema, você verá um menu com as seguintes opções:

1. Cadastrar novo cliente
2. Listar clientes
3. Editar cliente
4. Excluir cliente
5. Cadastrar contato para cliente
6. Listar contatos de um cliente
7. Buscar clientes
0. Sair

Escolha a opção desejada digitando o número correspondente e siga as instruções na tela.

## Observações

- Esta é a primeira etapa do projeto, utilizando armazenamento em memória
- Na próxima etapa, será implementada a persistência em banco de dados
- Os dados são mantidos apenas durante a execução do programa

## Próximas Etapas

- Implementação do banco de dados MySQL
- Migração dos dados para persistência em banco
- Adição de novas funcionalidades
- Melhorias na interface do usuário 