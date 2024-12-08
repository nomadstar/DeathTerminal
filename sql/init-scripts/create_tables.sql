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

CREATE TABLE Mapas (
    id SERIAL PRIMARY KEY, 
    mapa CHAR(100)[100]
    titulo CHAR(20) NOT NULL,
    descripcion CHAR(50) NOT NULL,
    elementos CHAR(1)[64],
    elementos_id INT[64]
);

CREATE TABLE Elementos (
    id SERIAL PRIMARY KEY, 
    nombre CHAR(20) NOT NULL,
    issteppable BOOLEAN NOT NULL,
    colides BOOLEAN NOT NULL,
    imageid INT
    );
