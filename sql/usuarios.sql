SELECT * FROM clinica_estetica.usuarios;

INSERT INTO usuarios (nome, email, senha, nivel_de_acesso, status) VALUES
('Jeniffer Araujo', 'jeniffer@gmail.com', '65852', 'biomedico', 'S'),
('Amanda Silva', 'amanda@gmail.com', '568426', 'gerente', 'S'),
('Talita Correa', 'talita@gmail.com', '69856', 'administrador', 'S'),
('Ana Oliveira', 'ana@gmail.com', '995789', 'recepcionista', 'S'),
('Maria Cecilia', 'maria@gmail.com', '65853', 'esteticista', 'S');

-- Atualizar os usuarios com a senha em hash
UPDATE usuarios SET senha = SHA2('65852', 256) WHERE email = 'jeniffer@gmail.com';
UPDATE usuarios SET senha = SHA2('568426', 256) WHERE email = 'amanda@gmail.com';
UPDATE usuarios SET senha = SHA2('69856', 256) WHERE email = 'talita@gmail.com';
UPDATE usuarios SET senha = SHA2('995789', 256) WHERE email = 'ana@gmail.com';
UPDATE usuarios SET senha = SHA2('65853', 256) WHERE email = 'maria@gmail.com';

-- Para adicionar um novo usuario já com a senha em hash
INSERT INTO usuarios (nome, email, senha, nivel_de_acesso, status)
VALUES ('Frederico Augusto', 'frederico@email.com', SHA2('69856356', 256), 'biomedico', 'S');

-- Para selecionar os usuarios por nivel de acesso
SELECT * FROM usuarios WHERE nivel_de_acesso = 'recepcionista';
SELECT * FROM usuarios WHERE nivel_de_acesso = 'gerente';
SELECT * FROM usuarios WHERE nivel_de_acesso = 'administrador';

-- Para mostrar usuário por nivel de acesso do maior para o menor
SELECT nivel_de_acesso, COUNT(*) as total_usuarios
FROM usuarios
GROUP BY nivel_de_acesso
ORDER BY total_usuarios DESC;

-- Para verificar se há emails duplicados 
SELECT email, COUNT(*) as duplicados
FROM usuarios
GROUP BY email
HAVING duplicados > 1;


SELECT * FROM usuarios ORDER BY id_usuario;


