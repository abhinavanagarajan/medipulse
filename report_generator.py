import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os
import io

class StressReportGenerator:
    def __init__(self, csv_file='sensor_data.csv'):
        self.data = pd.read_csv(csv_file)
        self.data['Timestamp'] = pd.to_datetime(self.data['Timestamp'])
        self.report_dir = os.path.join('mediplus-lite', 'reports')
        os.makedirs(self.report_dir, exist_ok=True)

    def calculate_statistics(self):
        stats = {
            'Heart Rate': {
                'Max': self.data['HeartRate'].max(),
                'Min': self.data['HeartRate'].min(),
                'Average': self.data['HeartRate'].mean()
            },
            'GSR': {
                'Max': self.data['GSR'].max(),
                'Min': self.data['GSR'].min(),
                'Average': self.data['GSR'].mean()
            },
            'Cortisol': {
                'Max': self.data['Cortisol'].max(),
                'Min': self.data['Cortisol'].min(),
                'Average': self.data['Cortisol'].mean(),
                'High Count': len(self.data[self.data['Cortisol'] >= 17]),
                'Medium Count': len(self.data[(self.data['Cortisol'] >= 10) & (self.data['Cortisol'] < 17)]),
                'Normal Count': len(self.data[self.data['Cortisol'] < 10])
            }
        }
        return stats

    def create_graphs(self):
        # Create figures for each metric
        graphs = []
        metrics = ['HeartRate', 'GSR', 'Cortisol']
        
        for metric in metrics:
            plt.figure(figsize=(8, 4))
            plt.plot(self.data['Timestamp'], self.data[metric])
            plt.title(f'{metric} Over Time')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save to bytes buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)
            graphs.append(img_buffer)
            plt.close()
            
        return graphs

    def generate_pdf(self):
        doc = SimpleDocTemplate(
            os.path.join(self.report_dir, 'report.pdf'),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        
        # Content elements
        elements = []
        
        # Title
        elements.append(Paragraph("Patient Stress & Cortisol Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Statistics
        stats = self.calculate_statistics()
        stats_data = []
        
        # Add statistics tables
        for metric, values in stats.items():
            stats_data.append([Paragraph(f"<b>{metric} Statistics</b>", styles['Normal'])])
            for key, value in values.items():
                stats_data.append([f"{key}: {value:.2f}"])
        
        stats_table = Table(stats_data, colWidths=[400])
        stats_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 20))
        
        # Add graphs
        graphs = self.create_graphs()
        for i, graph in enumerate(['Heart Rate', 'GSR', 'Cortisol']):
            elements.append(Paragraph(f"{graph} Trend", styles['Heading2']))
            elements.append(Image(graphs[i], width=6*inch, height=3*inch))
            elements.append(Spacer(1, 20))
        
        # Conclusion for psychiatrists
        elements.append(Paragraph("Analysis for Psychiatrists", styles['Heading2']))
        
        conclusion_text = f"""
        Based on the recorded data:
        - Patient showed high stress levels ({stats['Cortisol']['High Count']} instances)
        - Average cortisol level: {stats['Cortisol']['Average']:.2f} μg/dL
        - Highest recorded cortisol: {stats['Cortisol']['Max']:.2f} μg/dL
        - GSR readings indicate {self._analyze_gsr_trend()} trend
        
        Recommendations:
        1. Monitor stress patterns during peak cortisol periods
        2. Consider stress management techniques
        3. Regular follow-up assessments recommended
        """
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        
        # Generate PDF
        doc.build(elements)
        return os.path.join(self.report_dir, 'report.pdf')

    def _analyze_gsr_trend(self):
        # Simple trend analysis
        first_half = self.data['GSR'][:len(self.data)//2].mean()
        second_half = self.data['GSR'][len(self.data)//2:].mean()
        
        if second_half > first_half * 1.1:
            return "an increasing stress"
        elif second_half < first_half * 0.9:
            return "a decreasing stress"
        return "a stable stress"

if __name__ == "__main__":
    report_gen = StressReportGenerator()
    report_path = report_gen.generate_pdf()
    print(f"Report generated at: {report_path}")
