"""
Module de génération de graphiques pour Sécurité 360
Utilise Plotly pour créer des visualisations interactives
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
from utils.config import COLORS, PLOTLY_LAYOUT, PLOTLY_CONFIG

def create_conformity_gauge(percentage: float, title: str = "Taux de conformité") -> go.Figure:
    """
    Crée un graphique en ligne simple identique au style du dashboard existant
    
    Args:
        percentage: Pourcentage de conformité actuel
        title: Titre du graphique
    
    Returns:
        Figure Plotly
    """
    import pandas as pd
    import plotly.express as px
    
    # Données simulées d'évolution (même style que le graphique existant)
    trend_data = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
        'Score': [65, 68, 72, 75, 78, percentage]
    })
    
    # Créer le graphique avec plotly express (lignes droites)
    fig = px.line(trend_data, x='Mois', y='Score', 
                  title="", 
                  line_shape='linear',  # Changé de 'spline' à 'linear' pour des lignes droites
                  markers=True)
    
    # Appliquer exactement le même style que le graphique existant
    fig.update_traces(line_color=COLORS['primary'], marker_size=8)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=COLORS['text'],
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=40),  # Augmenter la marge du bas pour le pourcentage
        annotations=[
            dict(
                text=f"<b>Taux actuel: {percentage:.1f}%</b>",
                x=0.5,
                y=-0.01,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14, color=COLORS['primary']),
                xanchor="center"
            )
        ]
    )
    fig.add_hline(y=80, line_dash="dash", line_color=COLORS['success'], 
                  annotation_text="Objectif ISO 27001")
    
    return fig

def create_conformity_pie_chart(stats: Dict) -> go.Figure:
    """
    Crée un diagramme circulaire de la conformité
    
    Args:
        stats: Dictionnaire des statistiques de conformité
    
    Returns:
        Figure Plotly
    """
    labels = ['Conforme', 'Largement conforme', 'Partiellement conforme', 'Faiblement conforme', 'Non conforme']
    values = [
        stats.get('conforme', 0),
        stats.get('largement_conforme', 0),
        stats.get('partiellement_conforme', 0),
        stats.get('faiblement_conforme', 0),
        stats.get('non_conforme', 0)
    ]
    colors = [COLORS['success'], '#16a34a', COLORS['warning'], '#dc2626', COLORS['danger']]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors, line=dict(color=COLORS['background'], width=2)),
        textfont=dict(size=14, color='white'),
        textposition='inside',
        textinfo='label+percent'
    )])
    
    layout = {**PLOTLY_LAYOUT}
    layout.update({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)'
    })
    
    fig.update_layout(
        **layout,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(color=COLORS['text'])
        ),
        height=300
    )
    
    return fig

def create_category_bar_chart(criteres: List[Dict]) -> go.Figure:
    """
    Crée un graphique linéaire par catégorie
    
    Args:
        criteres: Liste des critères
    
    Returns:
        Figure Plotly
    """
    categories = {}
    statuts_list = ['Conforme', 'Largement conforme', 'Partiellement conforme', 'Faiblement conforme', 'Non conforme']
    
    for critere in criteres:
        cat = critere['categorie']
        statut = critere['statut']
        if cat not in categories:
            categories[cat] = {s: 0 for s in statuts_list}
        categories[cat][statut] = categories[cat].get(statut, 0) + 1
    
    cat_names = list(categories.keys())
    conforme = [categories[cat]['Conforme'] for cat in cat_names]
    largement = [categories[cat]['Largement conforme'] for cat in cat_names]
    partiel = [categories[cat]['Partiellement conforme'] for cat in cat_names]
    faiblement = [categories[cat]['Faiblement conforme'] for cat in cat_names]
    non_conforme = [categories[cat]['Non conforme'] for cat in cat_names]
    
    fig = go.Figure()
    
    # Ligne Conforme
    fig.add_trace(go.Scatter(
        name='Conforme',
        x=cat_names,
        y=conforme,
        mode='lines+markers',
        line=dict(color=COLORS['success'], width=3),
        marker=dict(size=10, color=COLORS['success'], symbol='circle'),
        fill='tozeroy',
        fillcolor=f"rgba(16, 185, 129, 0.1)"
    ))
    
    # Ligne Largement conforme
    fig.add_trace(go.Scatter(
        name='Largement conforme',
        x=cat_names,
        y=largement,
        mode='lines+markers',
        line=dict(color='#16a34a', width=3),
        marker=dict(size=10, color='#16a34a', symbol='triangle-up'),
        fill='tozeroy',
        fillcolor=f"rgba(22, 163, 74, 0.1)"
    ))
    
    # Ligne Partiellement conforme
    fig.add_trace(go.Scatter(
        name='Partiellement conforme',
        x=cat_names,
        y=partiel,
        mode='lines+markers',
        line=dict(color=COLORS['warning'], width=3),
        marker=dict(size=10, color=COLORS['warning'], symbol='square'),
        fill='tozeroy',
        fillcolor=f"rgba(245, 158, 11, 0.1)"
    ))
    
    # Ligne Faiblement conforme
    fig.add_trace(go.Scatter(
        name='Faiblement conforme',
        x=cat_names,
        y=faiblement,
        mode='lines+markers',
        line=dict(color='#dc2626', width=3),
        marker=dict(size=10, color='#dc2626', symbol='triangle-down'),
        fill='tozeroy',
        fillcolor=f"rgba(220, 38, 38, 0.1)"
    ))
    
    # Ligne Non conforme
    fig.add_trace(go.Scatter(
        name='Non conforme',
        x=cat_names,
        y=non_conforme,
        mode='lines+markers',
        line=dict(color=COLORS['danger'], width=3),
        marker=dict(size=10, color=COLORS['danger'], symbol='diamond'),
        fill='tozeroy',
        fillcolor=f"rgba(239, 68, 68, 0.1)"
    ))
    
    # Créer un layout personnalisé en fusionnant PLOTLY_LAYOUT avec nos paramètres spécifiques
    layout = {**PLOTLY_LAYOUT}
    layout.update({
        'xaxis_title': 'Catégorie',
        'yaxis_title': 'Nombre de critères',
        'legend': {
            'orientation': 'v',
            'yanchor': 'top',
            'y': 0.98,
            'xanchor': 'right',
            'x': 0.98,
            'bgcolor': 'rgba(30, 41, 59, 0.8)',
            'bordercolor': COLORS['text_secondary'],
            'borderwidth': 1,
            'font': {'color': COLORS['text'], 'size': 11}
        },
        'hovermode': 'x unified',
        'height': 450,
        'margin': {'l': 60, 'r': 20, 't': 40, 'b': 60}
    })
    fig.update_layout(**layout)
    
    return fig

def create_audit_timeline(audits: List[Dict]) -> go.Figure:
    """
    Crée une chronologie des audits
    
    Args:
        audits: Liste des audits
    
    Returns:
        Figure Plotly
    """
    if not audits:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun audit disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text_secondary'])
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=300)
        return fig
    
    dates = [audit['date_audit'] for audit in audits]
    scores = [audit['score'] if audit['score'] else 0 for audit in audits]
    titres = [audit['titre'] for audit in audits]
    
    fig = go.Figure(data=go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        marker=dict(
            size=12,
            color=scores,
            colorscale=[[0, COLORS['danger']], [0.5, COLORS['warning']], [1, COLORS['success']]],
            showscale=True,
            colorbar=dict(title=dict(text="Score", font=dict(color=COLORS['text'])))
        ),
        line=dict(color=COLORS['info'], width=3),
        text=titres,
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Score: %{y:.1f}%<extra></extra>'
    ))
    
    # Créer un layout personnalisé en fusionnant PLOTLY_LAYOUT avec nos paramètres spécifiques
    layout = {**PLOTLY_LAYOUT}
    layout.update({
        'title': {'text': 'Évolution des scores d\'audit', 'font': {'size': 18, 'color': COLORS['text']}},
        'xaxis_title': 'Date',
        'yaxis_title': 'Score (%)',
        'yaxis': dict(range=[0, 100], gridcolor='rgba(148, 163, 184, 0.1)', zerolinecolor='rgba(148, 163, 184, 0.1)'),
        'height': 400
    })
    fig.update_layout(**layout)
    
    return fig

def create_directive_effectiveness_chart(directives: List[Dict]) -> go.Figure:
    """
    Crée un graphique d'efficacité des directives
    
    Args:
        directives: Liste des directives
    
    Returns:
        Figure Plotly
    """
    if not directives:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune directive disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text_secondary'])
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=300)
        return fig
    
    efficacite_counts = {}
    for directive in directives:
        eff = directive.get('efficacite', 'Moyenne')
        efficacite_counts[eff] = efficacite_counts.get(eff, 0) + 1
    
    labels = list(efficacite_counts.keys())
    values = list(efficacite_counts.values())
    
    colors_map = {
        'Élevée': COLORS['success'],
        'Moyenne': COLORS['info'],
        'Faible': COLORS['warning'],
        'À améliorer': COLORS['danger']
    }
    bar_colors = [colors_map.get(label, COLORS['info']) for label in labels]
    
    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker_color=bar_colors,
        text=values,
        textposition='outside',
        textfont=dict(size=14, color=COLORS['text'])
    )])
    
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title={'text': 'Efficacité des directives', 'font': {'size': 18, 'color': COLORS['text']}},
        xaxis_title='Niveau d\'efficacité',
        yaxis_title='Nombre de directives',
        height=400
    )
    
    return fig

def create_radial_category_chart(stats_by_category: Dict) -> go.Figure:
    """
    Crée un graphique en barres horizontales avec pourcentages par catégorie
    
    Args:
        stats_by_category: Statistiques par catégorie
    
    Returns:
        Figure Plotly
    """
    categories = list(stats_by_category.keys())
    percentages = [stats_by_category[cat]['percentage'] for cat in categories]
    
    # Déterminer la couleur de chaque barre en fonction du pourcentage
    colors = []
    for pct in percentages:
        if pct >= 80:
            colors.append(COLORS['success'])
        elif pct >= 50:
            colors.append(COLORS['warning'])
        else:
            colors.append(COLORS['danger'])
    
    fig = go.Figure()
    
    # Créer les barres horizontales
    fig.add_trace(go.Bar(
        y=categories,
        x=percentages,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color=COLORS['background'], width=2)
        ),
        text=[f'{pct}%' for pct in percentages],
        textposition='outside',
        textfont=dict(size=14, color=COLORS['text'], family='Arial, sans-serif', weight='bold'),
        hovertemplate='<b>%{y}</b><br>Conformité: %{x:.1f}%<extra></extra>'
    ))
    
    # Créer un layout personnalisé en fusionnant PLOTLY_LAYOUT avec nos paramètres spécifiques
    layout = {**PLOTLY_LAYOUT}
    layout.update({
        'xaxis': {
            'range': [0, 105],  # Un peu plus que 100 pour laisser de la place aux labels
            'ticksuffix': '%',
            'gridcolor': 'rgba(148, 163, 184, 0.2)',
            'tickfont': {'color': COLORS['text']},
            'showgrid': True,
            'zerolinecolor': 'rgba(148, 163, 184, 0.1)'
        },
        'yaxis': {
            'tickfont': {'color': COLORS['text'], 'size': 12},
            'showgrid': False,
            'gridcolor': 'rgba(148, 163, 184, 0.1)',
            'zerolinecolor': 'rgba(148, 163, 184, 0.1)'
        },
        'showlegend': False,
        'height': 400,
        'margin': {'l': 20, 'r': 60, 't': 40, 'b': 40}
    })
    fig.update_layout(**layout)
    
    return fig

def create_heatmap_conformity(criteres: List[Dict]) -> go.Figure:
    """
    Crée une heatmap de conformité
    
    Args:
        criteres: Liste des critères
    
    Returns:
        Figure Plotly
    """
    # Organiser les données par catégorie et code
    categories = ['Organisationnelle', 'Personnel', 'Physique', 'Technologique']
    
    data_matrix = []
    codes = []
    
    for cat in categories:
        cat_criteres = [c for c in criteres if c['categorie'] == cat][:10]  # Limiter à 10 pour la lisibilité
        if cat_criteres:
            for c in cat_criteres:
                codes.append(c['code'])
                if c['statut'] == 'Conforme':
                    data_matrix.append([cat, 100])
                elif c['statut'] == 'Partiellement conforme':
                    data_matrix.append([cat, 50])
                else:
                    data_matrix.append([cat, 0])
    
    if not data_matrix:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text_secondary'])
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=300)
        return fig
    
    z_values = [[dm[1]] for dm in data_matrix]
    
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        y=codes,
        x=['Conformité'],
        colorscale=[[0, COLORS['danger']], [0.5, COLORS['warning']], [1, COLORS['success']]],
        showscale=True,
        colorbar=dict(title=dict(text="Score", font=dict(color=COLORS['text'])))
    ))
    
    # Créer un layout personnalisé en fusionnant PLOTLY_LAYOUT avec nos paramètres spécifiques
    layout = {**PLOTLY_LAYOUT}
    layout.update({
        'title': {'text': 'Carte de conformité des critères', 'font': {'size': 18, 'color': COLORS['text']}},
        'height': max(400, len(codes) * 25),
        'yaxis': dict(tickfont=dict(size=10), gridcolor='rgba(148, 163, 184, 0.1)', zerolinecolor='rgba(148, 163, 184, 0.1)')
    })
    fig.update_layout(**layout)
    
    return fig