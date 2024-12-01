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
    fecha_completado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
