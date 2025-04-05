SELECT * FROM clinica_estetica.produtos;

-- Para ver os produtos e suas categorias por ordem de Id
SELECT p.id_produto, p.nome, p.quantidade, p.valor_unitario, c.nome AS categoria 
FROM produtos p JOIN categorias c ON p.categorias_id_categoria = c.id_categoria 
ORDER BY p.id_produto;

-- Para adicionar a coluna de valor unitario
ALTER TABLE `clinica_estetica`.`produtos` 
ADD COLUMN `valor_unitario` DECIMAL(10,2) NOT NULL DEFAULT 0.00 AFTER `quantidade`;

-- Para tualizar os primeiros produtos inseridos
UPDATE produtos 
SET valor_unitario = 89.90 
WHERE id_produto = 1;  

UPDATE produtos 
SET valor_unitario = 120.50 
WHERE id_produto = 2;   

-- Inserção de produtos representativos para cada categoria
INSERT INTO produtos (nome, descricao, quantidade, valor_unitario, categorias_id_categoria) VALUES
('Botox® Original', 'Toxina botulínica tipo A - frasco ', 15, 850.00, 1),
('Dysport®', 'Toxina botulínica tipo A - frasco 500U', 10, 1200.00, 2),
('Juvederm ', 'Preenchedor facial - 1ml', 20, 950.00, 3),
('Xylestesin', 'Creme anestésico 30g (lidocaína+prilocaína)', 25, 65.90, 4),
('Cocktail Revitalizante', 'Complexo vitamínico para mesoterapia - 10 ampolas', 18, 280.00, 5),
('Ácido Glicólico 10%', 'Sérum facial renovador celular - 30ml', 30, 120.50, 6),
('Agulha 30G 4mm', 'Caixa com 100 unidades para aplicação', 50, 45.00, 7),
('Cera Roll-On', 'Cera quente para depilação profissional - 500g', 22, 89.90, 8),
('Alcool 70%', 'Solução antisséptica - frasco 500ml', 40, 18.50, 9);

-- Para consulta de prdoutos e movimentacoes
SELECT 
    p.id_produto,
    p.nome AS produto,
    p.quantidade AS estoque_atual,
    COUNT(m.id_movimentacao) AS total_movimentacoes,
    SUM(CASE WHEN m.tipo = 'entrada' THEN m.quantidade ELSE 0 END) AS entradas,
    SUM(CASE WHEN m.tipo = 'saida' THEN m.quantidade ELSE 0 END) AS saidas
FROM 
    produtos p
LEFT JOIN 
    movimentacao m ON p.id_produto = m.produtos_id_produto
GROUP BY 
    p.id_produto
ORDER BY 
    p.id_produto;
    
-- Para mostrar os produtos, categorias, usuarios e movimentacoes
SELECT 
    p.id_produto,
    p.nome AS produto,
    c.nome AS categoria,
    p.quantidade AS estoque_atual,
    m.tipo AS tipo_movimentacao,
    m.quantidade AS quantidade_movimentada,
    DATE_FORMAT(m.data_movimentacao, '%d/%m/%Y %H:%i') AS data_movimentacao,
    u.nome AS responsavel
FROM 
    produtos p
JOIN 
    categorias c ON p.categorias_id_categoria = c.id_categoria
LEFT JOIN 
    movimentacao m ON p.id_produto = m.produtos_id_produto
LEFT JOIN 
    usuarios u ON m.usuarios_id_usuario = u.id_usuario
ORDER BY 
    p.id_produto, m.data_movimentacao DESC;

