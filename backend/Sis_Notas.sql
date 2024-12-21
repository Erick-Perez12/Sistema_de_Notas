-- Crear la base de datos
DROP DATABASE SisNotas;
CREATE DATABASE IF NOT EXISTS SisNotas;
USE SisNotas;

-- Tabla de usuarios
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL, -- Contraseña encriptada
    rol ENUM('administrador', 'profesor', 'estudiante') NOT NULL,
    cuenta_activa BOOLEAN DEFAULT TRUE, -- Indicador de si la cuenta está activa
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de notas
CREATE TABLE Notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    materia VARCHAR(100) NOT NULL,
    calificacion DECIMAL(5, 2) NOT NULL CHECK (calificacion >= 0 AND calificacion <= 20),
    semestre VARCHAR(20) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

-- Tabla de roles y permisos (para RBAC)
CREATE TABLE Roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE Permisos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_permiso VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE RolesPermisos (
    rol_id INT NOT NULL,
    permiso_id INT NOT NULL,
    PRIMARY KEY (rol_id, permiso_id),
    FOREIGN KEY (rol_id) REFERENCES Roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permiso_id) REFERENCES Permisos(id) ON DELETE CASCADE
);

-- Tabla de auditoría para registrar intentos de inicio de sesión
CREATE TABLE AuditoriaInicioSesion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    ip VARCHAR(45),
    exito BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

-- Inserción de cuentas de usuarios
INSERT INTO Usuarios (nombre, email, contrasena, rol, cuenta_activa) VALUES
('Admin1', 'admin1@universidad.edu', '$2b$12$.YVD5KN7NRt.UM0uztSu5uNM3WbsJjgw8Ql0plDJtQ504Oacw6RU.', 'administrador', TRUE),
('Admin2', 'admin2@universidad.edu', '$2b$12$lULyLr0riqrzgwAs971h8eeW3ov0GVXIzof8VWI4D5BV7VRpahtVa', 'administrador', TRUE),
('Profesor1', 'profesor1@universidad.edu', '$2b$12$ZmQQFNbI6EqYp0ReCwhAL..kjg1Rar/r.a0hHinLfiCn2TWApeA9G', 'profesor', TRUE),
('Profesor2', 'profesor2@universidad.edu', '$2b$12$DUYKtZHRB5dw9jJMGsjAF.5bLugafD8Qn7F4KUpIGi4HJktcevDL2', 'profesor', TRUE),
('Profesor3', 'profesor3@universidad.edu', '$2b$12$FK4LX7QgDTB63lMdjIim7uWg9937yTzaUq09wu03/C7NalMrkpQCW', 'profesor', TRUE),
('Estudiante1', 'estudiante1@universidad.edu', '$2b$12$UqNj/cmcq9TDUqnGX7jkKOho9FjiPcr3v7I/I3wogMh8U0J8KJJxe', 'estudiante', TRUE),
('Estudiante2', 'estudiante2@universidad.edu', '$2b$12$XMOOet47ZUUwLN1KfheEn.fHUMCCqCAQGT45bAPhIVKn.c3KyOQOu', 'estudiante', TRUE),
('Estudiante3', 'estudiante3@universidad.edu', '$2b$12$HxsPHk/BNdyXdthfnbon6eDBuHUXZUimx/rK7DaLvH5LMR.vOIAP6', 'estudiante', TRUE),
('Estudiante4', 'estudiante4@universidad.edu', '$2b$12$iNmOnV4hIzRLoXVJ6A21PumBYb7cEKqdVDy5SHEz9rimcAdOuRVoy', 'estudiante', TRUE),
('Estudiante5', 'estudiante5@universidad.edu', '$2b$12$cp7yHgLFLzm8DM.BYGsmp.fZWa9vOavxve/HFgJZZP2nMZaT842aS', 'estudiante', TRUE);

-- Inserción de notas para estudiantes
INSERT INTO Notas (estudiante_id, materia, calificacion, semestre) VALUES
(6, 'Matemáticas', 11.5, '2024-1'),
(6, 'Física', 14.0, '2024-1'),
(7, 'Química', 18.0, '2024-1'),
(7, 'Biología', 18.0, '2024-1'),
(8, 'Historia', 19.5, '2024-1'),
(8, 'Geografía', 10.0, '2024-1'),
(9, 'Inglés', 15.0, '2024-1'),
(9, 'Literatura', 15.0, '2024-1'),
(10, 'Arte', 15.0, '2024-1'),
(10, 'Música', 11.0, '2024-1');

-- Inserción de roles
INSERT INTO Roles (nombre_rol, descripcion) VALUES
('administrador', 'Acceso completo al sistema'),
('profesor', 'Acceso a la gestión de notas y estudiantes'),
('estudiante', 'Acceso a la consulta de sus notas');

-- Inserción de permisos
INSERT INTO Permisos (nombre_permiso, descripcion) VALUES
('ver_notas', 'Permiso para ver notas'),
('editar_notas', 'Permiso para editar notas'),
('gestionar_usuarios', 'Permiso para gestionar usuarios');

-- Asignación de permisos a roles
INSERT INTO RolesPermisos (rol_id, permiso_id) VALUES
(1, 1), -- Administrador puede ver notas
(1, 2), -- Administrador puede editar notas
(1, 3), -- Administrador puede gestionar usuarios
(2, 1), -- Profesor puede ver notas
(2, 2), -- Profesor puede editar notas
(3, 1); -- Estudiante puede ver notas

-- Inserción de auditoría
INSERT INTO AuditoriaInicioSesion (usuario_id, ip, exito) VALUES
(1, '192.168.1.1', TRUE),
(2, '192.168.1.2', TRUE),
(3, '192.168.1.3', FALSE),
(4, '192.168.1.4', TRUE),
(5, '192.168.1.5', FALSE);
