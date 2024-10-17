
CREATE OR REPLACE VIEW view_clientes AS
SELECT 
	c.id,
    c.nome,
    c.telefone,
    CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado, ', CEP: ', e.cep) AS endereco
FROM 
    cliente_cliente c
JOIN 
    endereco_endereco e ON c.endereco_id = e.id;
