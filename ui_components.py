import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st

def create_animated_metric(value, title, color="#667eea", prefix="", suffix=""):
    """Create an animated metric display"""
    
    fig = go.Figure()
    
    # Create animated number
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = value,
        title = {"text": title, "font": {"size": 24, "color": color}},
        number = {"font": {"size": 48, "color": color}, "prefix": prefix, "suffix": suffix},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        height=200,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def create_compatibility_gauge(score, title="Compatibility Score"):
    """Create a beautiful gauge chart for scores"""
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 24, 'color': '#2c3e50'}},
        delta = {'reference': 70, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "darkblue", 'tickfont': {'size': 14}},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#ff6b6b'},
                {'range': [30, 60], 'color': '#feca57'},
                {'range': [60, 80], 'color': '#48dbfb'},
                {'range': [80, 100], 'color': '#0be881'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#2c3e50", 'family': "Poppins"}
    )
    
    return fig

def create_skill_radar_chart(skills_data):
    """Create a radar chart for skills analysis"""
    
    # Process skills data for radar chart
    if not skills_data:
        return create_empty_chart("No skills data available")
    
    # Group skills by category and calculate average confidence
    categories = {}
    for skill in skills_data:
        category = skill.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(skill.get('confidence', 0))
    
    # Calculate average confidence per category
    radar_data = []
    for category, confidences in categories.items():
        avg_confidence = sum(confidences) / len(confidences)
        radar_data.append({'category': category, 'confidence': avg_confidence})
    
    if not radar_data:
        return create_empty_chart("No skill categories found")
    
    df = pd.DataFrame(radar_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=df['confidence'],
        theta=df['category'],
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.2)',
        line=dict(color='rgba(102, 126, 234, 0.8)', width=3),
        marker=dict(color='rgba(102, 126, 234, 1)', size=8),
        name='Skill Proficiency'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(255,255,255,0.1)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color='#2c3e50'),
                gridcolor='rgba(102, 126, 234, 0.3)'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#2c3e50'),
                gridcolor='rgba(102, 126, 234, 0.3)'
            ),
        ),
        showlegend=False,
        title=dict(
            text="Skills by Category",
            x=0.5,
            font=dict(size=18, color='#2c3e50', family='Poppins')
        ),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_skills_treemap(skills_data):
    """Create a treemap visualization for skills"""
    
    if not skills_data:
        return create_empty_chart("No skills data available")
    
    # Prepare data for treemap
    categories = {}
    for skill in skills_data:
        category = skill.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(skill)
    
    # Create hierarchical data
    treemap_data = []
    colors = px.colors.qualitative.Set3
    
    for i, (category, skills) in enumerate(categories.items()):
        for skill in skills:
            treemap_data.append({
                'ids': f"{category}-{skill['name']}",
                'labels': skill['name'],
                'parents': category,
                'values': skill.get('confidence', 50),
                'color': colors[i % len(colors)]
            })
        
        # Add category parent
        treemap_data.append({
            'ids': category,
            'labels': category,
            'parents': '',
            'values': 0,
            'color': colors[i % len(colors)]
        })
    
    df = pd.DataFrame(treemap_data)
    
    fig = go.Figure(go.Treemap(
        ids=df['ids'],
        labels=df['labels'],
        parents=df['parents'],
        values=df['values'],
        branchvalues="total",
        marker=dict(
            colorscale='Viridis',
            cmid=50,
            colorbar=dict(thickness=20, title="Confidence")
        ),
        textinfo="label+value",
        textfont=dict(size=12, color='white', family='Poppins'),
        hovertemplate='<b>%{label}</b><br>Confidence: %{value}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Skills Distribution",
            x=0.5,
            font=dict(size=18, color='#2c3e50', family='Poppins')
        ),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_keyword_comparison_chart(job_analysis):
    """Create a comparison chart for matching vs missing keywords"""
    
    if not job_analysis:
        return create_empty_chart("No job analysis data available")
    
    matching = len(job_analysis.get('matching_keywords', []))
    missing = len(job_analysis.get('missing_keywords', []))
    
    fig = go.Figure()
    
    # Add matching keywords bar
    fig.add_trace(go.Bar(
        name='Matching Keywords',
        x=['Keywords'],
        y=[matching],
        marker_color='rgba(11, 232, 129, 0.8)',
        text=[f'{matching} keywords'],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Poppins')
    ))
    
    # Add missing keywords bar
    fig.add_trace(go.Bar(
        name='Missing Keywords',
        x=['Keywords'],
        y=[missing],
        marker_color='rgba(255, 107, 107, 0.8)',
        text=[f'{missing} keywords'],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Poppins')
    ))
    
    fig.update_layout(
        title=dict(
            text="Keyword Match Analysis",
            x=0.5,
            font=dict(size=18, color='#2c3e50', family='Poppins')
        ),
        barmode='stack',
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(title='Number of Keywords', titlefont=dict(color='#2c3e50')),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_progress_chart(scores):
    """Create a progress chart showing different score categories"""
    
    categories = list(scores.keys())
    values = list(scores.values())
    
    # Create color scale
    colors = ['#ff6b6b' if v < 50 else '#feca57' if v < 70 else '#0be881' for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(50, 50, 50, 0.8)', width=1)
        ),
        text=[f'{v}%' for v in values],
        textposition='inside',
        textfont=dict(color='white', size=12, family='Poppins')
    ))
    
    fig.update_layout(
        title=dict(
            text="Performance Metrics",
            x=0.5,
            font=dict(size=18, color='#2c3e50', family='Poppins')
        ),
        xaxis=dict(
            title='Score (%)',
            range=[0, 100],
            titlefont=dict(color='#2c3e50'),
            tickfont=dict(color='#2c3e50')
        ),
        yaxis=dict(
            titlefont=dict(color='#2c3e50'),
            tickfont=dict(color='#2c3e50')
        ),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig

def create_experience_timeline(experience_data):
    """Create a timeline visualization for experience"""
    
    if not experience_data:
        return create_empty_chart("No experience data available")
    
    fig = go.Figure()
    
    # Sample timeline data - in real implementation, this would parse the resume
    timeline_data = [
        {'role': 'Senior Developer', 'company': 'Tech Corp', 'start': '2022-01', 'end': '2023-12', 'duration': 24},
        {'role': 'Junior Developer', 'company': 'StartUp Inc', 'start': '2020-06', 'end': '2021-12', 'duration': 18},
        {'role': 'Intern', 'company': 'Big Company', 'start': '2020-01', 'end': '2020-05', 'duration': 5}
    ]
    
    colors = ['#667eea', '#764ba2', '#f093fb']
    
    for i, exp in enumerate(timeline_data):
        fig.add_trace(go.Scatter(
            x=[exp['start'], exp['end']],
            y=[exp['role'], exp['role']],
            mode='lines+markers+text',
            line=dict(color=colors[i % len(colors)], width=8),
            marker=dict(size=12, color=colors[i % len(colors)]),
            text=[f"{exp['company']}<br>{exp['duration']} months", ""],
            textposition="top center",
            textfont=dict(size=10, color='#2c3e50', family='Poppins'),
            name=exp['role'],
            showlegend=False
        ))
    
    fig.update_layout(
        title=dict(
            text="Career Timeline",
            x=0.5,
            font=dict(size=18, color='#2c3e50', family='Poppins')
        ),
        xaxis=dict(
            title='Timeline',
            titlefont=dict(color='#2c3e50'),
            tickfont=dict(color='#2c3e50')
        ),
        yaxis=dict(
            titlefont=dict(color='#2c3e50'),
            tickfont=dict(color='#2c3e50')
        ),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_word_cloud_chart(keywords):
    """Create a word cloud-style chart using plotly"""
    
    if not keywords:
        return create_empty_chart("No keywords available")
    
    # Convert keywords to DataFrame
    if isinstance(keywords[0], tuple):
        df = pd.DataFrame(keywords, columns=['word', 'frequency'])
    else:
        df = pd.DataFrame(keywords, columns=['word'])
        df['frequency'] = range(len(keywords), 0, -1)
    
    # Create bubble chart as word cloud alternative
    fig = px.scatter(
        df.head(20), 
        x=np.random.randn(min(20, len(df))), 
        y=np.random.randn(min(20, len(df))),
        size='frequency',
        color='frequency',
        hover_name='word',
        text='word',
        color_continuous_scale='Viridis',
        size_max=40
    )
    
    fig.update_traces(
        textposition='middle center',
        textfont=dict(size=12, family='Poppins', color='white')
    )
    
    fig.update_layout(
        title=dict(
            text="Key Terms Visualization",
            x=0.5,
            font=dict(size=18, color='#2c3e50', family='Poppins')
        ),
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False, title=''),
        yaxis=dict(showgrid=False, showticklabels=False, title=''),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_sentiment_gauge(sentiment_data):
    """Create a sentiment analysis gauge"""
    
    if not sentiment_data:
        return create_empty_chart("No sentiment data available")
    
    polarity = sentiment_data.get('polarity', 0)
    # Convert polarity (-1 to 1) to 0-100 scale
    sentiment_score = (polarity + 1) * 50
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Resume Tone", 'font': {'size': 20, 'color': '#2c3e50'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#ff6b6b'},
                {'range': [30, 70], 'color': '#feca57'},
                {'range': [70, 100], 'color': '#0be881'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#2c3e50", 'family': "Poppins"}
    )
    
    return fig

def create_empty_chart(message="No data available"):
    """Create an empty chart with a message"""
    
    fig = go.Figure()
    
    fig.add_annotation(
        x=0.5,
        y=0.5,
        text=message,
        showarrow=False,
        font=dict(size=16, color='#2c3e50', family='Poppins'),
        xref="paper",
        yref="paper"
    )
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    
    return fig

def create_animated_counter(target_value, duration=2000):
    """Create an animated counter component"""
    
    # This would be implemented with JavaScript in a real application
    # For now, we'll return the static value
    return target_value

def create_skill_proficiency_chart(skills):
    """Create a horizontal bar chart for skill proficiency"""
    
    if not skills:
        return create_empty_chart("No skills data available")
    
    # Take top 10 skills
    top_skills = skills[:10]
    
    skill_names = [skill['name'] for skill in top_skills]
    confidences = [skill['confidence'] for skill in top_skills]
    
    # Create color gradient
    colors = [f'rgba({255-int(c*2.55)}, {int(c*2.55)}, 100, 0.8)' for c in confidences]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=skill_names,
        x=confidences,
        orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(50, 50, 50, 0.8)', width=1)),
        text=[f'{c}%' for c in confidences],
        textposition='inside',
        textfont=dict(color='white', size=11, family='Poppins')
    ))
    
    fig.update_layout(
        title=dict(
            text="Top Skills Proficiency",
            x=0.5,
            font=dict(size=18, color='#2c3e50', family='Poppins')
        ),
        xaxis=dict(
            title='Confidence (%)',
            range=[0, 100],
            titlefont=dict(color='#2c3e50'),
            tickfont=dict(color='#2c3e50')
        ),
        yaxis=dict(
            titlefont=dict(color='#2c3e50'),
            tickfont=dict(color='#2c3e50')
        ),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig