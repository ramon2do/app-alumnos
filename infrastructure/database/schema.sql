CREATE TABLE IF NOT EXISTS tbl_usuarios (
    Id INTEGER PRIMARY KEY AUTOINCREMENT, Nombre TEXT NOT NULL, Correo TEXT NOT NULL UNIQUE, Contrasena TEXT NOT NULL, Tipo_Usuario TEXT NOT NULL, Estatus TEXT NOT NULL DEFAULT 'Activo'
);
CREATE TABLE IF NOT EXISTS tbl_alumnos (
    Id INTEGER PRIMARY KEY AUTOINCREMENT, Tipo_Cedula TEXT NOT NULL, Nro_Cedula TEXT NOT NULL, Nombres TEXT NOT NULL, Apellidos TEXT NOT NULL, Genero TEXT NOT NULL, Fecha_Nacimiento TEXT NOT NULL, WhatsApp TEXT NOT NULL, Correo TEXT NOT NULL UNIQUE, Foto_Cedula TEXT NOT NULL, Foto_Carnet TEXT NOT NULL, Id_Usuario INTEGER,
    UNIQUE(Tipo_Cedula, Nro_Cedula)
);
CREATE TABLE IF NOT EXISTS tbl_profesores (
    Id INTEGER PRIMARY KEY AUTOINCREMENT, Tipo_Cedula TEXT NOT NULL, Nro_Cedula TEXT NOT NULL, Nombres TEXT NOT NULL, Apellidos TEXT NOT NULL, Genero TEXT NOT NULL, Fecha_Nacimiento TEXT NOT NULL, Area_Conocimiento TEXT NOT NULL, WhatsApp TEXT NOT NULL, Correo TEXT NOT NULL UNIQUE, Foto_Cedula TEXT NOT NULL, Foto_Carnet TEXT NOT NULL,
    UNIQUE(Tipo_Cedula, Nro_Cedula)
);
CREATE TABLE IF NOT EXISTS tbl_horarios (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Horario TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS tbl_duracion (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Duracion TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS tbl_frecuencia (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Frecuencia TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS tbl_ofertas_academicas (
    Id INTEGER PRIMARY KEY AUTOINCREMENT, Oferta_Academica TEXT NOT NULL UNIQUE, Tipo TEXT NOT NULL, Precio_en_Divisas REAL NOT NULL, NroPartesCuotas INTEGER NOT NULL, CadaUnaDe_En_divisas REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS tbl_inscripciones (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Alumno INTEGER NOT NULL,
    Id_Oferta INTEGER NOT NULL,
    Id_Profesor INTEGER NOT NULL,
    Id_Horario INTEGER NOT NULL,
    Id_Duracion INTEGER NOT NULL,
    Id_Frecuencia INTEGER NOT NULL,
    Fecha_Inscripcion TEXT NOT NULL,
    FOREIGN KEY(Id_Alumno) REFERENCES tbl_alumnos(Id),
    FOREIGN KEY(Id_Oferta) REFERENCES tbl_ofertas_academicas(Id),
    FOREIGN KEY(Id_Profesor) REFERENCES tbl_profesores(Id),
    FOREIGN KEY(Id_Horario) REFERENCES tbl_horarios(Id),
    FOREIGN KEY(Id_Duracion) REFERENCES tbl_duracion(Id),
    FOREIGN KEY(Id_Frecuencia) REFERENCES tbl_frecuencia(Id)
);
