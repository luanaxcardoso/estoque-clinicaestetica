SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `clinica_estetica` DEFAULT CHARACTER SET utf8;
USE `clinica_estetica`;

CREATE TABLE IF NOT EXISTS `clinica_estetica`.`usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(200) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `senha` VARCHAR(255) NOT NULL, 
  `nivel_de_acesso` ENUM('administrador', 'gerente', 'biomedico', 'esteticista', 'recepcionista') NOT NULL,
  `status` ENUM('S', 'N') NOT NULL DEFAULT 'S',
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `clinica_estetica`.`categorias` (
  `id_categoria` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(255) NOT NULL,
  `descricao` VARCHAR(255) NOT NULL, 
  PRIMARY KEY (`id_categoria`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `clinica_estetica`.`produtos` (
  `id_produto` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(255) NOT NULL,
  `descricao` VARCHAR(255) NOT NULL, 
  `quantidade` INT NOT NULL,
  `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `categorias_id_categoria` INT NOT NULL,
  PRIMARY KEY (`id_produto`), 
  INDEX `fk_produtos_categorias_idx` (`categorias_id_categoria` ASC) VISIBLE,
  CONSTRAINT `fk_produtos_categorias`
    FOREIGN KEY (`categorias_id_categoria`)
    REFERENCES `clinica_estetica`.`categorias` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `clinica_estetica`.`movimentacao` (
  `id_movimentacao` INT NOT NULL AUTO_INCREMENT,
  `tipo` ENUM('entrada', 'saida') NOT NULL,
  `quantidade` INT NOT NULL,
  `motivo` VARCHAR(255) NULL, 
  `data_movimentacao` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  `usuarios_id_usuario` INT NOT NULL,
  `produtos_id_produto` INT NOT NULL,
  PRIMARY KEY (`id_movimentacao`), 
  INDEX `fk_movimentacao_usuarios1_idx` (`usuarios_id_usuario` ASC) VISIBLE,
  INDEX `fk_movimentacao_produtos1_idx` (`produtos_id_produto` ASC) VISIBLE,
  CONSTRAINT `fk_movimentacao_usuarios1`
    FOREIGN KEY (`usuarios_id_usuario`)
    REFERENCES `clinica_estetica`.`usuarios` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movimentacao_produtos1`
    FOREIGN KEY (`produtos_id_produto`)
    REFERENCES `clinica_estetica`.`produtos` (`id_produto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE OR REPLACE VIEW view_movimentacoes_simples AS
SELECT 
    m.id_movimentacao,
    CASE m.tipo WHEN 'entrada' THEN '▲ Entrada' ELSE '▼ Saída' END AS tipo_formatado,
    m.quantidade,
    p.nome AS produto,
    CONCAT(u.nome, ' (', u.email, ')') AS responsavel,
    DATE_FORMAT(m.data_movimentacao, '%d/%m/%Y %H:%i') AS data_hora,
    m.motivo
FROM movimentacao m 
JOIN produtos p ON m.produtos_id_produto = p.id_produto
JOIN usuarios u ON m.usuarios_id_usuario = u.id_usuario
ORDER BY m.id_movimentacao DESC;

CREATE INDEX idx_movimentacao_produto ON movimentacao(produtos_id_produto);
CREATE INDEX idx_movimentacao_usuario ON movimentacao(usuarios_id_usuario);
CREATE INDEX idx_movimentacao_data ON movimentacao(data_movimentacao);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;