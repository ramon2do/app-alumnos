class IdentidadException(Exception): pass
class CorreoDuplicadoError(IdentidadException): pass
class CredencialesInvalidasError(IdentidadException): pass
class UsuarioInactivoError(IdentidadException): pass
