from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame
from io import BytesIO

class PDFGenerator:
    @staticmethod
    def generate_pdf(letters, group_name=None):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        
        # Configurações de estilo
        styles = getSampleStyleSheet()
        style_normal = styles['Normal']
        
        # Cabeçalho
        pdf.setFont("Helvetica-Bold", 16)
        title = f"Cartas para {group_name}" if group_name else "Todas as Minhas Cartas"
        pdf.drawString(100, 800, title)
        
        # Conteúdo
        y_position = 750
        for idx, letter in enumerate(letters, 1):
            text = f"<b>Carta #{idx}</b> ({letter['sentiment']})<br/>{letter['content']}"
            p = Paragraph(text, style_normal)
            
            frame = Frame(50, y_position - 200, 500, 200, showBoundary=0)
            frame.add(p, pdf)
            
            y_position -= 220
            if y_position < 100:
                pdf.showPage()
                y_position = 750
        
        pdf.save()
        buffer.seek(0)
        return buffer