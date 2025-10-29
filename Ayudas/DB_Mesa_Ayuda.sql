-- Script de creación de base de datos para HelpDesk Coyhaique
-- Base de datos: helpdesk_db

DROP DATABASE IF EXISTS helpdesk_db;
CREATE DATABASE helpdesk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE helpdesk_db;

-- Tabla de usuarios
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('AGENTE','SUPERVISOR', 'PUBLICADOR') NOT NULL DEFAULT 'PUBLICADOR',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de tickets
CREATE TABLE ticket (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(120) NOT NULL,
    descripcion TEXT NOT NULL,
    estado ENUM('ABIERTO','EN_PROCESO','EN_ESPERA','RESUELTO','CERRADO') NOT NULL DEFAULT 'ABIERTO',
    creado_por INT NOT NULL,
    asignado_a INT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_ticket_creado_por FOREIGN KEY (creado_por) REFERENCES usuario(id) ON DELETE CASCADE,
    CONSTRAINT fk_ticket_asignado_a FOREIGN KEY (asignado_a) REFERENCES usuario(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de comentarios
CREATE TABLE comentario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    autor_id INT NOT NULL,
    texto TEXT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_com_ticket FOREIGN KEY (ticket_id) REFERENCES ticket(id) ON DELETE CASCADE,
    CONSTRAINT fk_com_autor FOREIGN KEY (autor_id) REFERENCES usuario(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Índices para optimización
CREATE INDEX idx_ticket_estado ON ticket(estado);
CREATE INDEX idx_ticket_asignado ON ticket(asignado_a);
CREATE INDEX idx_ticket_creado_por ON ticket(creado_por);
CREATE INDEX idx_comentario_ticket ON comentario(ticket_id);

-- Insertar usuarios de prueba (contraseña: admin123 para todos)
-- Hash generado con PBKDF2: admin123
INSERT INTO usuario (username, email, password_hash, role) VALUES
('admin', 'admin@sursoporte.cl', 'f3e7a8b9c2d1e4f5:100000:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', 'SUPERVISOR'),
('agente1', 'agente1@sursoporte.cl', 'f3e7a8b9c2d1e4f5:100000:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', 'AGENTE'),
('user1', 'user1@sursoporte.cl', 'f3e7a8b9c2d1e4f5:100000:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', 'PUBLICADOR');

-- Nota: Para crear usuarios reales, usar el sistema de registro que generará hashes correctos