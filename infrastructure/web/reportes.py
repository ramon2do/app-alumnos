import io, os
from flask import Blueprint, render_template, request, send_file, current_app
from utils.decorators import login_required
from infrastructure.container import container
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import openpyxl
from openpyxl.drawing.image import Image as OpenpyxlImage

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes_bp.route('/')
@login_required
def index():
    ofertas = container.oferta_repo.listar_todas()
    selected_oferta_id = request.args.get('oferta_id', type=int)
    inscritos = []
    oferta_seleccionada = None
    
    if selected_oferta_id:
        inscritos = container.inscripcion_repo.listar_por_oferta_detalle(selected_oferta_id)
        oferta_seleccionada = container.oferta_repo.buscar_por_id(selected_oferta_id)
        
    return render_template('reportes/index.html', ofertas=ofertas, inscritos=inscritos, selected_oferta_id=selected_oferta_id, oferta_seleccionada=oferta_seleccionada)

# --- Dentro de pdf_alumnos ---
@reportes_bp.route('/pdf/alumnos')
@login_required
def pdf_alumnos():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = [Paragraph("Reporte General de Alumnos", getSampleStyleSheet()['Title'])]
    
    # Añadir cabecera "Foto"
    data = [["Foto", "Cédula", "Nombre", "Correo", "WhatsApp"]]
    
    for a in container.alumno_repo.listar_todos():
        img_element = ""
        if a.foto_carnet:
            # Ruta absoluta local de la imagen para ReportLab
            img_path = os.path.join(current_app.root_path, a.foto_carnet.lstrip('/'))
            if os.path.exists(img_path):
                img_element = Image(img_path, width=30, height=30)
        
        data.append([img_element, str(a.cedula), a.nombre_completo, a.correo.value, a.whatsapp.value])
        
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')), 
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Alumnos.pdf", mimetype='application/pdf')

@reportes_bp.route('/excel/alumnos')
@login_required
def excel_alumnos():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Alumnos"
    
    # Encabezados
    ws.append(["Foto", "Tipo Cédula", "Nro Cédula", "Nombres", "Apellidos", "Correo", "WhatsApp"])
    ws.row_dimensions[1].height = 25
    
    for row_idx, a in enumerate(container.alumno_repo.listar_todos(), start=2):
        ws.row_dimensions[row_idx].height = 50 # Dar espacio vertical para la imagen
        ws.append(["", a.tipo_cedula, a.nro_cedula, a.nombres, a.apellidos, a.correo.value, a.whatsapp.value])
        
        if a.foto_carnet:
            img_path = os.path.join(current_app.root_path, a.foto_carnet.lstrip('/'))
            if os.path.exists(img_path):
                img = OpenpyxlImage(img_path)
                img.width = 50
                img.height = 50
                # Inserta la imagen en la primera columna (A) de la fila actual
                ws.add_image(img, f"A{row_idx}")
                
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Alumnos.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# --- Dentro de pdf_profesores ---
@reportes_bp.route('/pdf/profesores')
@login_required
def pdf_profesores():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = [Paragraph("Reporte General de Profesores", getSampleStyleSheet()['Title'])]
    
    data = [["Foto", "Cédula", "Nombre", "Área", "Correo", "WhatsApp"]]
    for p in container.profesor_repo.listar_todos():
        img_element = ""
        if p.foto_carnet:
            img_path = os.path.join(current_app.root_path, p.foto_carnet.lstrip('/'))
            if os.path.exists(img_path):
                img_element = Image(img_path, width=30, height=30)
                
        data.append([img_element, str(p.cedula), p.nombre_completo, p.area_conocimiento, p.correo.value, p.whatsapp.value])
        
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')), 
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Profesores.pdf", mimetype='application/pdf')

@reportes_bp.route('/excel/profesores')
@login_required
def excel_profesores():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Profesores"
    
    ws.append(["Foto", "Tipo Cédula", "Nro Cédula", "Nombres", "Apellidos", "Área", "Correo", "WhatsApp"])
    ws.row_dimensions[1].height = 25
    
    for row_idx, p in enumerate(container.profesor_repo.listar_todos(), start=2):
        ws.row_dimensions[row_idx].height = 50
        ws.append(["", p.tipo_cedula, p.nro_cedula, p.nombres, p.apellidos, p.area_conocimiento, p.correo.value, p.whatsapp.value])
        
        if p.foto_carnet:
            img_path = os.path.join(current_app.root_path, p.foto_carnet.lstrip('/'))
            if os.path.exists(img_path):
                img = OpenpyxlImage(img_path)
                img.width = 50
                img.height = 50
                ws.add_image(img, f"A{row_idx}")
                
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Profesores.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# 3. Reporte de Ofertas Académicas (PDF)
@reportes_bp.route('/pdf/ofertas')
@login_required
def pdf_ofertas():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = [Paragraph("Reporte de Ofertas Académicas", getSampleStyleSheet()['Title'])]
    data = [["ID", "Oferta", "Tipo", "Precio ($)", "Cuotas"]]
    for o in container.oferta_repo.listar_todas():
        data.append([str(o.id), o.oferta_academica, o.tipo, f"${o.precio_en_divisas.valor:.2f}", f"{o.nro_partes_cuotas}x${o.cada_una_de_en_divisas:.2f}"])
    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')), ('TEXTCOLOR', (0,0), (-1,0), colors.white)]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="OfertasAcademicas.pdf", mimetype='application/pdf')

# 3. Reporte de Ofertas Académicas (Excel)
@reportes_bp.route('/excel/ofertas')
@login_required
def excel_ofertas():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["ID", "Oferta Académica", "Tipo", "Precio Total ($)", "Nro Cuotas", "Monto Cuota ($)"])
    for o in container.oferta_repo.listar_todas():
        ws.append([o.id, o.oferta_academica, o.tipo, o.precio_en_divisas.valor, o.nro_partes_cuotas, o.cada_una_de_en_divisas])
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="OfertasAcademicas.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# --- 4. Reporte de Inscripciones por Oferta (PDF) ---
@reportes_bp.route('/pdf/inscripciones/<int:oferta_id>')
@login_required
def pdf_inscripciones(oferta_id):
    oferta = container.oferta_repo.buscar_por_id(oferta_id)
    inscritos = container.inscripcion_repo.listar_por_oferta_detalle(oferta_id)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    title = f"Reporte de Inscritos - {oferta.oferta_academica if oferta else 'Oferta'}"
    elements = [Paragraph(title, getSampleStyleSheet()['Title'])]
    
    # Añadimos la columna "Foto"
    data = [["Foto", "Cédula", "Alumno", "Profesor", "Horario", "Duración", "Frecuencia"]]
    
    for i in inscritos:
        img_element = ""
        if i.get('FotoCarnet'):
            img_path = os.path.join(current_app.root_path, i['FotoCarnet'].lstrip('/'))
            if os.path.exists(img_path):
                img_element = Image(img_path, width=30, height=30)
                
        data.append([img_element, str(i['AlumnoCedula']), i['AlumnoNombre'], i['ProfesorNombre'], i['Horario'], i['Duracion'], i['Frecuencia']])
    
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')), 
        ('TEXTCOLOR', (0,0), (-1,0), colors.white), 
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    
    # Limpiar y formatear el nombre de la oferta para el archivo
    nombre_oferta = oferta.oferta_academica.replace(' ', '_').replace('/', '-') if oferta else f"oferta_{oferta_id}"
    nombre_archivo = f"Inscritos_{nombre_oferta}.pdf"
    
    return send_file(buffer, as_attachment=True, download_name=nombre_archivo, mimetype='application/pdf')

# --- 5. Reporte de Inscripciones por Oferta (Excel) ---
@reportes_bp.route('/excel/inscripciones/<int:oferta_id>')
@login_required
def excel_inscripciones(oferta_id):
    oferta = container.oferta_repo.buscar_por_id(oferta_id)
    inscritos = container.inscripcion_repo.listar_por_oferta_detalle(oferta_id)
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inscritos"
    
    ws.append(["Foto", "Cédula Alumno", "Nombre Alumno", "Profesor", "Horario", "Duración", "Frecuencia", "Fecha Inscripción"])
    ws.row_dimensions[1].height = 25
    
    for row_idx, i in enumerate(inscritos, start=2):
        ws.row_dimensions[row_idx].height = 50
        ws.append(["", i['AlumnoCedula'], i['AlumnoNombre'], i['ProfesorNombre'], i['Horario'], i['Duracion'], i['Frecuencia'], i['Fecha_Inscripcion']])
        
        if i.get('FotoCarnet'):
            img_path = os.path.join(current_app.root_path, i['FotoCarnet'].lstrip('/'))
            if os.path.exists(img_path):
                img = OpenpyxlImage(img_path)
                img.width = 50
                img.height = 50
                ws.add_image(img, f"A{row_idx}")
                
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    # Formatear el nombre de la oferta para el archivo Excel
    nombre_oferta = oferta.oferta_academica.replace(' ', '_').replace('/', '-') if oferta else f"oferta_{oferta_id}"
    filename = f"Inscritos_{nombre_oferta}.xlsx"
    
    return send_file(
        buffer, 
        as_attachment=True, 
        download_name=filename, 
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
