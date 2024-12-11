INSERT INTO usuarios (nombre, email, user_password, Tipo_usuario) VALUES
('Admin', 'admin@example.com', 'password123', NULL), 
('Jugador1', 'jugador1@example.com', '12345', NULL),   
('Jugador2', 'jugador@example.com', '12345', NULL),     
('hola', 'hola@example.com', '1234', 'admin');          

INSERT INTO niveles (nombre_nivel, dificultad, creado_por) VALUES
('Nivel 1', 1, 4), 
('Nivel 2', 2, 4); 


INSERT INTO progresion (usuario_id, nivel_id, estado, fecha_inicio, fecha_completado) VALUES
(1, 1, 'finalizado', '2024-12-06 10:00:00', '2024-12-06 11:30:00'), 
(2, 1, 'en_proceso', '2024-12-06 12:00:00', NULL),                   
(3, 1, 'en_proceso', '2024-12-06 12:00:00', NULL);                   


INSERT INTO trivias (nivel_id, pregunta, respuesta, creado_por) VALUES 
(1, '¿Cuál es la capital de Francia?', 'París', 4),
(1, '¿En qué año comenzó la Segunda Guerra Mundial?', '1939', 4); 


CREATE OR REPLACE FUNCTION insert_progresion()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO progresion (usuario_id, nivel_id)
    VALUES (NEW.id, 1);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_insert_usuarios
AFTER INSERT ON usuarios
FOR EACH ROW
EXECUTE FUNCTION insert_progresion();
