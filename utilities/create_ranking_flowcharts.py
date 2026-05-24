#!/usr/bin/env python3
"""
Generate visual flowcharts for the ranking system
Creates two images:
1. Intelligent Multi-Factor Ranking System Flow
2. Ranking Metric Weights Distribution
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

def create_ranking_flow_diagram():
    """Create the ranking flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 16))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 20)
    ax.axis('off')
    
    # Title
    ax.text(5, 19.5, 'Intelligent Multi-Factor Ranking System Flow', 
            fontsize=18, fontweight='bold', ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#2C3E50', edgecolor='black', linewidth=2, alpha=0.9),
            color='white')
    
    # Helper function to draw boxes
    def draw_box(x, y, width, height, text, color, text_color='white'):
        box = FancyBboxPatch((x-width/2, y-height/2), width, height,
                            boxstyle="round,pad=0.1", 
                            facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, 
                fontweight='bold', color=text_color, wrap=True)
    
    def draw_arrow(x1, y1, x2, y2, style='->'):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle=style, mutation_scale=20, 
                               linewidth=2, color='black')
        ax.add_patch(arrow)
    
    # Start
    draw_box(5, 18, 2, 0.6, 'Start Market Bot', '#34495E')
    draw_arrow(5, 17.7, 5, 17.2)
    
    # PHASE 1
    draw_box(5, 16.7, 3.5, 0.7, 'PHASE 1: Data Collection', '#3498DB')
    draw_arrow(4, 16.35, 2.5, 15.8)
    draw_arrow(5, 16.35, 5, 15.8)
    draw_arrow(6, 16.35, 7.5, 15.8)
    
    # Stocks collection
    draw_box(2.5, 15.3, 1.8, 0.6, 'Stock 1:\nFetch Data', '#5DADE2')
    draw_box(5, 15.3, 1.8, 0.6, 'Stock 2:\nFetch Data', '#5DADE2')
    draw_box(7.5, 15.3, 1.8, 0.6, 'Stock N:\nFetch Data', '#5DADE2')
    
    draw_arrow(2.5, 15, 2.5, 14.2)
    draw_arrow(5, 15, 5, 14.2)
    draw_arrow(7.5, 15, 7.5, 14.2)
    
    # Data processing
    draw_box(2.5, 13.5, 1.8, 1.2, 'Market Data\nNews +\nSentiment\nAnalyst\nRatings', '#85C1E9', 'black')
    draw_box(5, 13.5, 1.8, 1.2, 'Market Data\nNews +\nSentiment\nAnalyst\nRatings', '#85C1E9', 'black')
    draw_box(7.5, 13.5, 1.8, 1.2, 'Market Data\nNews +\nSentiment\nAnalyst\nRatings', '#85C1E9', 'black')
    
    draw_arrow(2.5, 12.9, 3.5, 12.3)
    draw_arrow(5, 12.9, 5, 12.3)
    draw_arrow(7.5, 12.9, 6.5, 12.3)
    
    # Storage
    draw_box(5, 11.8, 3.5, 0.7, 'All Stocks Data Array\n[650+ stocks]', '#2ECC71')
    draw_arrow(5, 11.45, 5, 10.9)
    
    # PHASE 2
    draw_box(5, 10.4, 3.5, 0.7, 'PHASE 2: Intelligent Ranking', '#F39C12')
    draw_arrow(5, 10.05, 5, 9.6)
    
    # Normalization
    draw_box(5, 9.2, 2.5, 0.5, 'Normalize All Metrics\n(0-1 Scale)', '#F8C471', 'black')
    draw_arrow(5, 8.95, 5, 8.5)
    
    # Weights
    draw_box(5, 8.1, 2.5, 0.5, 'Apply Weighted Scoring', '#F8C471', 'black')
    draw_arrow(5, 7.85, 5, 7.4)
    
    # Metrics breakdown
    metrics_text = ('Market Cap 10%\nMomentum 20%\nVolume Surge 15%\n'
                   'Sentiment 15%\nScore 15%\nSignal 10%\n'
                   'News Sentiment 8%\nConsensus 5%\nRatings 2%')
    draw_box(5, 6.3, 2.8, 1.6, metrics_text, '#9B59B6')
    draw_arrow(5, 5.5, 5, 5.0)
    
    # Composite score
    draw_box(5, 4.6, 3, 0.5, 'Calculate Composite Score\n(0-100 for each stock)', '#F8C471', 'black')
    draw_arrow(5, 4.35, 5, 3.9)
    
    # Sort
    draw_box(5, 3.5, 2.2, 0.5, 'Sort by Score\n(Descending)', '#F8C471', 'black')
    draw_arrow(5, 3.25, 5, 2.8)
    
    # Assign ranks
    draw_box(5, 2.4, 2.2, 0.5, 'Assign Ranks\n(1 = Best)', '#F8C471', 'black')
    draw_arrow(5, 2.15, 5, 1.7)
    
    # PHASE 3
    draw_box(5, 1.2, 3.5, 0.7, 'PHASE 3: Send to Notion', '#27AE60')
    draw_arrow(4, 0.85, 2.5, 0.4)
    draw_arrow(5, 0.85, 5, 0.4)
    draw_arrow(6, 0.85, 7.5, 0.4)
    
    # Final output
    draw_box(2.5, -0.1, 1.8, 0.6, 'Rank 1:\nBest Stock', '#52BE80')
    draw_box(5, -0.1, 1.8, 0.6, 'Rank 2:\n2nd Best', '#52BE80')
    draw_box(7.5, -0.1, 1.8, 0.6, 'Rank N:\nLast Stock', '#52BE80')
    
    plt.tight_layout()
    plt.savefig('docs/Ranking_System_Flow.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: docs/Ranking_System_Flow.png")
    plt.close()

def create_weights_pie_chart():
    """Create the metric weights pie chart"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    
    # Data
    metrics = [
        'Momentum', 'Volume Surge', 'Sentiment', 'Investment Score',
        'Market Cap', 'Signal', 'News Sentiment', 'Analyst Consensus', 'Analyst Ratings'
    ]
    weights = [20, 15, 15, 15, 10, 10, 8, 5, 2]
    colors = ['#E74C3C', '#3498DB', '#9B59B6', '#F39C12', 
              '#1ABC9C', '#2ECC71', '#E67E22', '#95A5A6', '#34495E']
    
    # Create pie chart with explosion for top weights
    explode = [0.1 if w >= 15 else 0.05 for w in weights]
    
    wedges, texts, autotexts = ax.pie(weights, labels=metrics, autopct='%1.0f%%',
                                        colors=colors, explode=explode,
                                        startangle=90, textprops={'fontsize': 11, 'weight': 'bold'},
                                        pctdistance=0.85, labeldistance=1.15)
    
    # Enhance text
    for text in texts:
        text.set_fontsize(12)
        text.set_weight('bold')
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_weight('bold')
    
    # Title
    ax.set_title('Ranking Metric Weights Distribution\n(Total = 100%)', 
                 fontsize=16, fontweight='bold', pad=20,
                 bbox=dict(boxstyle='round,pad=0.8', facecolor='#2C3E50', 
                          edgecolor='black', linewidth=2),
                 color='white')
    
    # Equal aspect ratio
    ax.axis('equal')
    
    plt.tight_layout()
    plt.savefig('docs/Ranking_Weights_Distribution.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: docs/Ranking_Weights_Distribution.png")
    plt.close()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎨 Creating Ranking System Visualizations...")
    print("="*60 + "\n")
    
    create_ranking_flow_diagram()
    create_weights_pie_chart()
    
    print("\n" + "="*60)
    print("✅ All visualizations created successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. docs/Ranking_System_Flow.png")
    print("  2. docs/Ranking_Weights_Distribution.png")
    print("\n")
