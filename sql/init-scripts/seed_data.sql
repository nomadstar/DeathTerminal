INSERT INTO usuarios (nombre, email, user_password) VALUES
('Admin', 'admin@example.com', 'password123'),
('Jugador1', 'jugador1@example.com', '12345');

INSERT INTO niveles (nombre_nivel, dificultad) VALUES
('Nivel 1', 1),
('Nivel 2', 2);

INSERT INTO usuarios (nombre, email, user_password, Tipo_usuario) VALUES
('hola', 'hola@example.com', '1234', 'admin');

INSERT INTO progresion (usuario_id, nivel_id, fecha_completado) VALUES
(1, 1, CURRENT_TIMESTAMP), -- Admin completó Nivel 1
(2, 2, CURRENT_TIMESTAMP); -- Jugador1 completó Nivel 2

