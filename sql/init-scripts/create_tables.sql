CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(25),
    email VARCHAR(25) UNIQUE,
    Tipo_usuario VARCHAR(25),
    user_password VARCHAR(25),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE niveles (
    id SERIAL PRIMARY KEY,
    nombre_nivel VARCHAR(25),
    dificultad INT
);

CREATE TABLE progresion (
    usuario_id INT REFERENCES usuarios(id),
    nivel_id INT REFERENCES niveles(id),
    fecha_completado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (usuario_id, nivel_id)
);

CREATE TABLE publicaciones (
    id SERIAL PRIMARY KEY, 
    tema VARCHAR(10) NOT NULL,                         
    mensaje TEXT NOT NULL,                          
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE, -- Si se elimina un usuario, se eliminan sus publicaciones
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);
CREATE TABLE trivias (
    id SERIAL PRIMARY KEY,
    nivel_id INT REFERENCES niveles(id) ON DELETE CASCADE, -- Relación con el nivel
    pregunta TEXT NOT NULL, -- La pregunta de la trivia
    respuesta TEXT NOT NULL, -- La respuesta correcta
    creado_por INT REFERENCES usuarios(id) ON DELETE SET NULL, -- Administrador que creó la trivia
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de creación
);
