# Sistema de Cadastro de Clientes e Contatos

Este é um sistema simples de cadastro de clientes e contatos desenvolvido em Python. O sistema permite gerenciar informações de clientes e seus contatos associados através de uma interface de linha de comando (CLI).

## Funcionalidades

- Cadastro de clientes (nome, email, telefone, endereço)
- Listagem de todos os clientes
- Edição de informações de clientes
- Exclusão de clientes
- Cadastro de múltiplos contatos para cada cliente
- Listagem de contatos por cliente
- Busca de clientes por nome ou email

## Estrutura do Projeto

```
Projeto_Integrador/
├── Documentacao/
│   ├── Requisitos.txt         # Requisitos funcionais e não funcionais
│   ├── Modelo_Logico.txt     # Modelo lógico do banco de dados
│   └── Script_SQL.sql        # Script para criação do banco de dados
├── Codigo/
│   └── sistema_clientes.py   # Implementação do sistema
└── README.md                 # Este arquivo
```

## Como Executar

1. Certifique-se de ter o Python 3.6 ou superior instalado
2. Navegue até a pasta do projeto:
   ```
   cd Projeto_Integrador/Codigo
   ```
3. Execute o sistema:
   ```
   python sistema_clientes.py
   ```

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