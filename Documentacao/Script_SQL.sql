-- Criação do banco de dados
CREATE DATABASE sistema_clientes;

-- Tabela CLIENTE
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(20),
    endereco TEXT
);

-- Tabela CONTATO
CREATE TABLE contato (
    id_contato INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    tipo VARCHAR(50),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
); 