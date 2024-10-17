CREATE OR REPLACE FUNCTION update_cliente_endereco(
    cliente_id UUID,
    novo_nome VARCHAR,
    novo_cpf VARCHAR,
    novo_telefone VARCHAR,
    endereco_id INT,
    nova_rua VARCHAR,
    novo_numero VARCHAR,
    novo_bairro VARCHAR,
    nova_cidade VARCHAR,
    novo_estado VARCHAR,
    novo_cep VARCHAR
)
RETURNS VOID AS $$
BEGIN
    
    UPDATE cliente_cliente
    SET nome = novo_nome,
        cpf = novo_cpf,
        telefone = novo_telefone
    WHERE id = cliente_id;

    
    UPDATE endereco_endereco
    SET rua = nova_rua,
        numero = novo_numero,
        bairro = novo_bairro,
        cidade = nova_cidade,
        estado = novo_estado,
        cep = novo_cep
    WHERE id = endereco_id;
END;
$$ LANGUAGE plpgsql;
