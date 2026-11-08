from utils.notifications import enviar_correo, enviar_whatsapp

class AlumnoRegistradoHandler:
    @staticmethod
    def handle(event):
        mensaje = f"¡Bienvenido a AppAlumnos!\nTu usuario es: {event.usuario_generado}\nTu clave temporal es: {event.contrasena_generada}"
        
        # 1. Envío de Correo Real (SMTP)
        enviar_correo(
            event.correo, 
            "Bienvenido a AppAlumnos", 
            mensaje
        )
        
        # 2. Envío de WhatsApp vía Whapi.cloud
        enviar_whatsapp(
            event.whatsapp, 
            mensaje
        )