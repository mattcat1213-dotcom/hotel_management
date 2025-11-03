-- -----------------------------
-- Base de datos: hotel_db
-- -----------------------------
CREATE DATABASE IF NOT EXISTS hotel_db;
USE hotel_db;

-- -----------------------------
-- Tabla: users (para login/admin)
-- -----------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin','staff') DEFAULT 'staff'
);


-- -----------------------------
-- Tabla: clients
-- -----------------------------
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    email VARCHAR(50),
    direccion VARCHAR(100),
    pais VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'Activo'
);

-- -----------------------------
-- Tabla: rooms (habitaciones)
-- -----------------------------
CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) NOT NULL UNIQUE,
    tipo ENUM('Simple','Doble','Suite') NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    estado ENUM('Disponible','Ocupada','Mantenimiento') DEFAULT 'Disponible'
);

-- -----------------------------
-- Tabla: bookings (reservas)
-- -----------------------------
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    room_id INT NOT NULL,
    fecha_checkin DATE NOT NULL,
    fecha_checkout DATE NOT NULL,
    estado ENUM('Reservado','Cancelado','Finalizado') DEFAULT 'Reservado',
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);

-- -----------------------------
-- Tabla: payments (opcional)
-- -----------------------------
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha_pago DATE NOT NULL,
    metodo_pago ENUM('Efectivo','Tarjeta','Transferencia') DEFAULT 'Efectivo',
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);

-- Ejemplo de usuario admin
INSERT INTO users (username, password, role)
VALUES ('admin', 'admin123', 'admin');
