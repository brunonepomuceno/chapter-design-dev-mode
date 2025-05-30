import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from collections import Counter
from data_processor import SurveyDataProcessor

class PDFReportGenerator:
    def __init__(self):
        self.data_processor = SurveyDataProcessor()
        self.primary_blue = HexColor('#007AFF')
        self.text_primary = HexColor('#1D1D1F')
        self.text_secondary = HexColor('#6E6E73')
        
    def create_chart_image(self, chart_type, data, filename):
        """Create chart images for the PDF"""
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('white')
        
        if chart_type == 'ide_preferences':
            bars = ax.bar(data.keys(), data.values(), color='#007AFF', alpha=0.8)
            ax.set_title('IDEs Mais Utilizadas', fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel('Número de Desenvolvedores', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            
        elif chart_type == 'satisfaction':
            colors = ['#EF4444', '#F97316', '#EAB308', '#22C55E', '#10B981']
            labels = [f'Rating {k}' for k in data.keys()]
            pie_result = ax.pie(data.values(), labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title('Satisfação com Dev Mode do Figma', fontsize=16, fontweight='bold', pad=20)
            
        elif chart_type == 'feedback':
            likes_data = data['likes']
            dislikes_data = data['dislikes']
            
            all_labels = list(likes_data.keys()) + list(dislikes_data.keys())
            all_values = list(likes_data.values()) + [-v for v in dislikes_data.values()]
            colors = ['#10B981'] * len(likes_data) + ['#EF4444'] * len(dislikes_data)
            
            bars = ax.barh(all_labels, all_values, color=colors)
            ax.set_title('Feedback sobre Handoffs', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Menções (Verde = Gostam, Vermelho = Não Gostam)', fontsize=12)
            ax.axvline(x=0, color='black', linewidth=0.5)
            
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filename
    
    def generate_pdf_report(self):
        """Generate comprehensive PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        # Get data
        survey_data = self.data_processor.get_survey_insights()
        chart_data = self.data_processor.get_chart_data()
        feedback_themes = self.data_processor.get_feedback_themes()
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            textColor=self.text_primary,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=self.text_secondary,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=20,
            spaceAfter=12,
            textColor=self.text_primary,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            textColor=self.text_primary,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        
        # Title page
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("Resultado da pesquisa sobre Dev Mode", title_style))
        story.append(Paragraph("Feedback dos desenvolvedores para melhoria contínua", subtitle_style))
        story.append(Spacer(1, 1*inch))
        
        # Executive Summary
        story.append(Paragraph("Resumo Executivo", heading_style))
        story.append(Paragraph(f"""
        Esta pesquisa foi realizada com <b>{survey_data['total_responses']}</b> desenvolvedores frontend em <b>{survey_data['survey_date']}</b>, 
        com o objetivo de avaliar os processos de handoff, preferências de ferramentas e a eficácia do Dev Mode do Figma. 
        Os resultados mostram uma satisfação média de <b>{survey_data['avg_satisfaction']}</b> com o Dev Mode, 
        com <b>{survey_data['top_ide'][0]}</b> sendo a IDE mais utilizada por <b>{survey_data['top_ide'][1]}</b> desenvolvedores.
        """, body_style))
        
        story.append(PageBreak())
        
        # Methodology
        story.append(Paragraph("Metodologia", heading_style))
        story.append(Paragraph(f"""
        A coleta de dados focou em identificar pontos de melhoria nos processos atuais e entender as necessidades 
        dos desenvolvedores para otimizar a colaboração entre design e desenvolvimento. Foram coletadas 
        <b>{survey_data['total_responses']}</b> respostas através de questionário estruturado abordando:
        <br/>• Preferências de IDEs e ferramentas
        <br/>• Avaliação do Dev Mode do Figma
        <br/>• Aspectos positivos e negativos dos handoffs
        <br/>• Sugestões de melhorias
        """, body_style))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Create and add charts
        chart_files = []
        
        # IDE Chart
        ide_file = 'temp_ide_chart.png'
        self.create_chart_image('ide_preferences', chart_data['ide_chart']['labels'], ide_file)
        ide_data_dict = dict(zip(chart_data['ide_chart']['labels'], chart_data['ide_chart']['data']))
        self.create_chart_image('ide_preferences', ide_data_dict, ide_file)
        chart_files.append(ide_file)
        
        story.append(Paragraph("IDEs Mais Utilizadas", heading_style))
        story.append(RLImage(ide_file, width=5*inch, height=3.75*inch))
        story.append(Spacer(1, 0.3*inch))
        
        # Satisfaction Chart
        satisfaction_file = 'temp_satisfaction_chart.png'
        satisfaction_data_dict = dict(zip(chart_data['satisfaction_chart']['labels'], chart_data['satisfaction_chart']['data']))
        self.create_chart_image('satisfaction', satisfaction_data_dict, satisfaction_file)
        chart_files.append(satisfaction_file)
        
        story.append(Paragraph("Satisfação com Dev Mode do Figma", heading_style))
        story.append(RLImage(satisfaction_file, width=5*inch, height=3.75*inch))
        story.append(Spacer(1, 0.3*inch))
        
        # Feedback Chart
        feedback_file = 'temp_feedback_chart.png'
        self.create_chart_image('feedback', feedback_themes, feedback_file)
        chart_files.append(feedback_file)
        
        story.append(Paragraph("Análise de Feedback", heading_style))
        story.append(RLImage(feedback_file, width=5*inch, height=3.75*inch))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(PageBreak())
        
        # Key Insights
        story.append(Paragraph("Insights Principais", heading_style))
        
        insights_data = [
            ['Aspecto', 'Resultado', 'Impacto'],
            ['IDE Dominante', f"{survey_data['top_ide'][0]} ({survey_data['top_ide'][1]} devs)", 'Padronização de ferramentas'],
            ['Aspecto Mais Valorizado', f"{survey_data['top_like'][0]} ({survey_data['top_like'][1]} menções)", 'Foco em comunicação clara'],
            ['Principal Desafio', f"{survey_data['top_dislike'][0]} ({survey_data['top_dislike'][1]} menções)", 'Área prioritária de melhoria'],
            ['Satisfação Dev Mode', f"Nota {survey_data['avg_satisfaction']}/5", 'Boa aceitação da ferramenta']
        ]
        
        insights_table = Table(insights_data)
        insights_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(insights_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Developer Quotes
        if survey_data.get('quotes'):
            story.append(Paragraph("Depoimentos dos Desenvolvedores", heading_style))
            for quote in survey_data['quotes']:
                story.append(Paragraph(f'<i>"{quote["text"]}"</i>', body_style))
                story.append(Paragraph(f'<b>— {quote["name"]}</b>', body_style))
                story.append(Spacer(1, 0.2*inch))
        
        # Next Steps
        story.append(Paragraph("Próximos Passos", heading_style))
        next_steps = [
            "Implementar melhorias na documentação de edge cases nos handoffs",
            "Criar sessões de treinamento para otimização do Dev Mode do Figma", 
            "Estabelecer padrões mais claros para especificações de telas e componentes",
            "Desenvolver processo de feedback contínuo entre design e desenvolvimento",
            "Organizar workshops mensais de alinhamento e melhores práticas"
        ]
        
        for i, step in enumerate(next_steps, 1):
            story.append(Paragraph(f"<b>{i}.</b> {step}", body_style))
        
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"<b>Relatório gerado em:</b> {datetime.now().strftime('%d de %B de %Y')}", body_style))
        
        # Build PDF
        doc.build(story)
        
        # Clean up temporary files
        for file in chart_files:
            try:
                os.remove(file)
            except:
                pass
                
        buffer.seek(0)
        return buffer