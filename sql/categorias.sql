select * from categorias;

-- Para listar por id
SELECT * FROM categorias WHERE id_categoria = 1;

-- Buscar categorias por parte do nome 'depil'
SELECT * FROM categorias WHERE nome LIKE '%depil%';

-- Mostrar produtos por categoria
SELECT c.nome AS categoria,
    COUNT(p.id_produto) AS total_produtos
FROM categorias c
LEFT JOIN produtos p ON c.id_categoria = p.categorias_id_categoria
GROUP BY c.id_categoria
ORDER BY total_produtos DESC;

-- Mostrar categorias sem produtos cadastrados
SELECT c.*
FROM categorias c
LEFT JOIN produtos p ON c.id_categoria = p.categorias_id_categoria
WHERE p.id_produto IS NULL;

-- Para listar o total
SELECT COUNT(*) AS total_categorias FROM categorias;

-- Para listar as 5 primeiras
SELECT * FROM categorias LIMIT 5 OFFSET 0;

