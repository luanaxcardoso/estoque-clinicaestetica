SELECT * FROM clinica_estetica.movimentacao;

-- Para mostrar a view ordenada pelo id
SELECT * FROM view_movimentacoes_simples 
ORDER BY id_movimentacao ASC  
LIMIT 50;


-- Para ver quais usuários fizeram movimentações
SELECT u.nome, u.email, COUNT(m.id_movimentacao) as total_movimentacoes
FROM usuarios u
LEFT JOIN movimentacao m ON u.id_usuario = m.usuarios_id_usuario
GROUP BY u.id_usuario
ORDER BY total_movimentacoes DESC;

-- Para ver os detalhes das movimentações por usuário (com produtos)
SELECT 
    u.nome as usuario,
    u.nivel_de_acesso,
    m.tipo,
    m.quantidade,
    p.nome as produto,
    DATE_FORMAT(m.data_movimentacao, '%d/%m/%Y') as data
FROM usuarios u
JOIN movimentacao m ON u.id_usuario = m.usuarios_id_usuario
JOIN produtos p ON m.produtos_id_produto = p.id_produto
ORDER BY m.data_movimentacao DESC;

-- Ver o usuário com mais movimentações que a média
SELECT u.nome, COUNT(m.id_movimentacao) as movimentacoes
FROM usuarios u
JOIN movimentacao m ON u.id_usuario = m.usuarios_id_usuario
GROUP BY u.id_usuario
HAVING movimentacoes > (
    SELECT AVG(contagem) 
    FROM (
        SELECT COUNT(*) as contagem
        FROM movimentacao
        GROUP BY usuarios_id_usuario
    ) as subquery
);

