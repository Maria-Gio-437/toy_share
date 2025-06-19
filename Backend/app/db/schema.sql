-- CRIAÇÃO DA TABELA USUÁRIOS --
DROP TABLE IF EXISTS Usuario;

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    telefone TEXT,      -- Campo opcional (pode ser NULL)
    endereco TEXT,      -- Campo opcional (pode ser NULL)
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);