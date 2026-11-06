from utils.notifications import enviar_correo, enviar_whatsapp
class AlumnoRegistradoHandler:
    @staticmethod
    def handle(event):
        enviar_correo(event.correo, "Bienvenido a AppAlumnos", f"Usuario: {event.usuario_generado} Clave: {event.contrasena_generada}")
        enviar_whatsapp(event.whatsapp, f"Bienvenido! Usuario: {event.usuario_generado} Clave: {event.contrasena_generada}")
