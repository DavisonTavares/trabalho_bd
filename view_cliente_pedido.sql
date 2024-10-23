CREATE OR REPLACE VIEW view_clientes_pedido AS
SELECT 
    c.id,
    c.nome,
    c.cpf,
    c.telefone,
    c.time,
    c.audiovisual,
    CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado, ', CEP: ', e.cep) AS endereco
FROM 
    cliente_cliente c
JOIN 
    endereco_endereco e ON c.endereco_id = e.id;
