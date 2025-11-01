"""
Module de génération de rapports PDF pour Sécurité 360
Utilise ReportLab pour créer des rapports professionnels
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import Dict, List
import io

class PDFGenerator:
    def __init__(self):
        """Initialise le générateur PDF"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configure les styles personnalisés"""
        # Style de titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Style de sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Style de texte normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        # Style pour le pied de page
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
    
    def generate_conformity_report(self, stats: Dict, criteres: List[Dict], filename: str = None) -> bytes:
        """
        Génère un rapport de conformité complet
        
        Args:
            stats: Statistiques de conformité
            criteres: Liste des critères
            filename: Nom du fichier (optionnel)
        
        Returns:
            Contenu PDF en bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # En-tête du rapport
        story.append(Paragraph("RAPPORT DE CONFORMITÉ ISO 27001", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*cm))
        
        # Informations générales
        date_rapport = datetime.now().strftime('%d/%m/%Y à %H:%M')
        story.append(Paragraph(f"<b>Date du rapport:</b> {date_rapport}", self.styles['CustomBody']))
        story.append(Paragraph(f"<b>Système:</b> Sécurité 360", self.styles['CustomBody']))
        story.append(Spacer(1, 1*cm))
        
        # Résumé exécutif
        story.append(Paragraph("RÉSUMÉ EXÉCUTIF", self.styles['CustomSubtitle']))
        
        taux_conformite = stats.get('taux_conformite', 0)
        total = stats.get('total', 0)
        conforme = stats.get('conforme', 0)
        partiel = stats.get('partiellement_conforme', 0)
        non_conforme = stats.get('non_conforme', 0)
        
        summary_data = [
            ['Indicateur', 'Valeur'],
            ['Taux de conformité global', f"{taux_conformite}%"],
            ['Total de critères évalués', str(total)],
            ['Critères conformes', str(conforme)],
            ['Critères partiellement conformes', str(partiel)],
            ['Critères non conformes', str(non_conforme)]
        ]
        
        summary_table = Table(summary_data, colWidths=[10*cm, 6*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 1*cm))
        
        # Analyse par catégorie
        story.append(Paragraph("ANALYSE PAR CATÉGORIE", self.styles['CustomSubtitle']))
        
        categories = {}
        for critere in criteres:
            cat = critere['categorie']
            if cat not in categories:
                categories[cat] = {'conforme': 0, 'partiel': 0, 'non_conforme': 0, 'total': 0}
            categories[cat]['total'] += 1
            if critere['statut'] == 'Conforme':
                categories[cat]['conforme'] += 1
            elif critere['statut'] == 'Partiellement conforme':
                categories[cat]['partiel'] += 1
            else:
                categories[cat]['non_conforme'] += 1
        
        cat_data = [['Catégorie', 'Conforme', 'Partiel', 'Non conforme', 'Total', 'Taux (%)']]
        for cat, values in categories.items():
            taux = round((values['conforme'] / values['total'] * 100) if values['total'] > 0 else 0, 1)
            cat_data.append([
                cat,
                str(values['conforme']),
                str(values['partiel']),
                str(values['non_conforme']),
                str(values['total']),
                f"{taux}%"
            ])
        
        cat_table = Table(cat_data, colWidths=[5*cm, 2*cm, 2*cm, 2.5*cm, 2*cm, 2.5*cm])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ]))
        
        story.append(cat_table)
        story.append(PageBreak())
        
        # Détail des critères non conformes
        story.append(Paragraph("CRITÈRES NON CONFORMES", self.styles['CustomSubtitle']))
        
        non_conformes = [c for c in criteres if c['statut'] == 'Non conforme']
        
        if non_conformes:
            nc_data = [['Code', 'Titre', 'Catégorie']]
            for critere in non_conformes[:20]:  # Limiter à 20 pour la lisibilité
                nc_data.append([
                    critere['code'],
                    critere['titre'][:40] + '...' if len(critere['titre']) > 40 else critere['titre'],
                    critere['categorie']
                ])
            
            nc_table = Table(nc_data, colWidths=[2*cm, 10*cm, 4*cm])
            nc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(nc_table)
        else:
            story.append(Paragraph("Aucun critère non conforme. Félicitations!", self.styles['CustomBody']))
        
        story.append(Spacer(1, 1*cm))
        
        # Recommandations
        story.append(Paragraph("RECOMMANDATIONS", self.styles['CustomSubtitle']))
        
        if taux_conformite < 50:
            recommandation = "Le taux de conformité est critique. Il est impératif de mettre en place un plan d'action prioritaire pour traiter les critères non conformes."
        elif taux_conformite < 80:
            recommandation = "Le taux de conformité est moyen. Un effort supplémentaire est nécessaire pour atteindre un niveau de conformité satisfaisant."
        else:
            recommandation = "Le taux de conformité est bon. Continuez les efforts pour maintenir et améliorer ce niveau."
        
        story.append(Paragraph(recommandation, self.styles['CustomBody']))
        story.append(Spacer(1, 0.5*cm))
        
        recommendations = [
            "Établir un calendrier de revue des critères non conformes",
            "Affecter des responsables pour chaque mesure corrective",
            "Documenter toutes les actions entreprises",
            "Planifier des audits de suivi réguliers",
            "Former le personnel aux exigences ISO 27001"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
        
        story.append(Spacer(1, 2*cm))
        
        # Pied de page
        story.append(Paragraph("_" * 80, self.styles['Footer']))
        story.append(Paragraph(
            f"Rapport généré par Sécurité 360 - {date_rapport}",
            self.styles['Footer']
        ))
        story.append(Paragraph(
            "Document confidentiel - ISO 27001",
            self.styles['Footer']
        ))
        
        # Construction du PDF
        doc.build(story)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    def generate_audit_report(self, audit: Dict, criteres: List[Dict]) -> bytes:
        """
        Génère un rapport d'audit
        
        Args:
            audit: Données de l'audit
            criteres: Liste des critères évalués
        
        Returns:
            Contenu PDF en bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # En-tête
        story.append(Paragraph("RAPPORT D'AUDIT INTERNE", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*cm))
        
        # Informations de l'audit
        story.append(Paragraph(f"<b>Titre:</b> {audit['titre']}", self.styles['CustomBody']))
        story.append(Paragraph(f"<b>Date d'audit:</b> {audit['date_audit']}", self.styles['CustomBody']))
        story.append(Paragraph(f"<b>Auditeur:</b> {audit['auditeur']}", self.styles['CustomBody']))
        story.append(Paragraph(f"<b>Statut:</b> {audit['statut']}", self.styles['CustomBody']))
        story.append(Paragraph(f"<b>Score global:</b> {audit.get('score', 0)}%", self.styles['CustomBody']))
        story.append(Spacer(1, 1*cm))
        
        # Commentaires
        if audit.get('commentaires'):
            story.append(Paragraph("COMMENTAIRES", self.styles['CustomSubtitle']))
            story.append(Paragraph(audit['commentaires'], self.styles['CustomBody']))
            story.append(Spacer(1, 1*cm))
        
        # Résultats détaillés
        story.append(Paragraph("RÉSULTATS DÉTAILLÉS", self.styles['CustomSubtitle']))
        
        # Construction du PDF
        doc.build(story)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data