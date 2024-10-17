CREATE OR REPLACE PROCEDURE update_cliente_endereco(
    IN cliente_id UUID,
    IN nome VARCHAR,
    IN cpf VARCHAR,
    IN telefone VARCHAR,
    IN endereco_id int,
    IN rua VARCHAR,
    IN numero VARCHAR,
    IN bairro VARCHAR,
    IN cidade VARCHAR,
    IN estado VARCHAR,
    IN cep VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE cliente_cliente
    SET nome = nome,
        cpf = cpf,
        telefone = telefone
    WHERE id = cliente_id;

    UPDATE endereco_endereco
    SET rua = rua,
        numero = numero,
        bairro = bairro,
        cidade = cidade,
        estado = estado,
        cep = cep
    WHERE id = endereco_id;
END;
$$;
