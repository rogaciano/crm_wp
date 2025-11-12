-- Script para corrigir encoding UTF-8 no MySQL
-- Execute no phpMyAdmin ou console MySQL

USE crm_db;

-- Alterar charset do banco de dados
ALTER DATABASE crm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Alterar charset da tabela de estágios
ALTER TABLE crm_estagiofunil CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Limpar dados antigos
DELETE FROM crm_estagiofunil;

-- Reinserir dados com acentuação correta
INSERT INTO crm_estagiofunil (nome, ordem, tipo, cor, data_criacao) VALUES
('Prospecção', 1, 'ABERTO', '#3B82F6', NOW()),
('Qualificação', 2, 'ABERTO', '#8B5CF6', NOW()),
('Proposta', 3, 'ABERTO', '#EC4899', NOW()),
('Negociação', 4, 'ABERTO', '#F59E0B', NOW()),
('Fechado - Ganho', 5, 'GANHO', '#10B981', NOW()),
('Fechado - Perdido', 6, 'PERDIDO', '#EF4444', NOW());

-- Verificar se foi inserido corretamente
SELECT * FROM crm_estagiofunil;
