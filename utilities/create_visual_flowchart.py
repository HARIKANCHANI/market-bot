#!/usr/bin/env python3
"""
Create visual flowchart diagram using matplotlib
No external dependencies required (uses matplotlib which should be available)
"""

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
    import matplotlib.lines as mlines
except ImportError:
    print("❌ Matplotlib not found!")
    print("Installing matplotlib...")
    import subprocess
    subprocess.run(["pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def create_flowchart():
    """Create professional flowchart diagram"""
    
    print("=" * 60)
    print("🎨 Creating Visual Data Flow Diagram")
    print("=" * 60)
    print()
    
    # Create figure with high DPI for presentations
    fig, ax = plt.subplots(1, 1, figsize=(14, 20), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 20)
    ax.axis('off')
    
    # Title
    ax.text(7, 19.5, 'Market Bot - Complete Data Flow', 
            ha='center', va='top', fontsize=20, fontweight='bold', color='#2C3E50')
    ax.text(7, 19, 'Step-by-Step Processing Pipeline for 675 NSE Stocks',
            ha='center', va='top', fontsize=12, color='#7F8C8D', style='italic')
    
    # Helper function to create boxes
    def box(x, y, w, h, text, color='#3498DB', text_color='white', shape='rect'):
        if shape == 'ellipse':
            ellipse = patches.Ellipse((x+w/2, y+h/2), w, h, 
                                      facecolor=color, edgecolor='#2C3E50', linewidth=2)
            ax.add_patch(ellipse)
        elif shape == 'diamond':
            points = [[x+w/2, y], [x+w, y+h/2], [x+w/2, y+h], [x, y+h/2]]
            diamond = patches.Polygon(points, facecolor=color, edgecolor='#2C3E50', linewidth=2)
            ax.add_patch(diamond)
        else:  # rectangle
            rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                  facecolor=color, edgecolor='#2C3E50', linewidth=2)
            ax.add_patch(rect)
        
        # Add text
        ax.text(x+w/2, y+h/2, text, ha='center', va='center',
                fontsize=9, color=text_color, weight='bold', wrap=True)
    
    # Helper function for arrows
    def arrow(x1, y1, x2, y2, label='', color='#2C3E50'):
        arr = FancyArrowPatch((x1, y1), (x2, y2),
                              arrowstyle='->', mutation_scale=20, linewidth=2,
                              color=color, connectionstyle="arc3,rad=0")
        ax.add_patch(arr)
        if label:
            mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
            ax.text(mid_x+0.2, mid_y, label, fontsize=8, color=color, weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Row positions
    y = 18
    step_h = 0.6
    gap = 0.4
    
    # START
    box(5.5, y, 3, step_h, '▶ START\nBot Execution', color='#27AE60', shape='ellipse')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    # Phase 1: Initialization
    box(2, y-0.2, 10, 0.5, '━━━ PHASE 1: INITIALIZATION ━━━', color='#34495E', text_color='white')
    y -= 0.8
    
    box(5.5, y, 3, step_h, '1. Load Config\nTokens, DB ID', color='#3498DB')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    box(5.5, y, 3, step_h, '2. Load Stocks\n675 NSE Tickers', color='#3498DB')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    # Phase 2: Loop Start
    box(2, y-0.2, 10, 0.5, '━━━ PHASE 2: STOCK ITERATION ━━━', color='#34495E', text_color='white')
    y -= 0.8
    
    box(5, y, 4, step_h+0.2, '3. FOR EACH STOCK\n(Rank 1-675)', color='#9B59B6', shape='diamond', text_color='white')
    y -= (step_h + gap + 0.2)
    arrow(7, y+gap+0.2, 7, y+step_h+gap/2+0.2)
    
    # Phase 3: Data Fetching
    box(2, y-0.2, 10, 0.5, '━━━ PHASE 3: DATA FETCHING ━━━', color='#34495E', text_color='white')
    y -= 0.8
    
    box(5.5, y, 3, step_h, '4. Fetch Price Data\nyfinance (6mo)', color='#F39C12')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    box(5, y, 4, step_h+0.2, '5. Data Available?', color='#E74C3C', shape='diamond', text_color='white')
    y_decision = y
    y -= (step_h + gap + 0.4)
    
    # Left path: YES (Data exists)
    box(0.5, y_decision-4, 2, 0.4, 'YES (~450)', color='#27AE60', text_color='white')
    arrow(5, y_decision+0.3, 2.5, y_decision+0.1, 'Data\nExists', color='#27AE60')
    
    # Phase 4: Processing (Left side)
    box(0, y_decision-0.8, 3, 0.45, 'PROCESSING PATH', color='#16A085', text_color='white')
    
    box(0.5, y_decision-1.4, 2, step_h, '6. Calculate\nMomentum', color='#E67E22')
    arrow(1.5, y_decision-1.4, 1.5, y_decision-0.8-0.45)
    
    box(0.5, y_decision-2.1, 2, step_h, '7. Calculate\nVolume Surge', color='#E67E22')
    arrow(1.5, y_decision-2.1, 1.5, y_decision-1.4)
    
    box(0.5, y_decision-2.8, 2, step_h, '8. Fetch News\n70+ sources', color='#F39C12')
    arrow(1.5, y_decision-2.8, 1.5, y_decision-2.1)
    
    box(0.5, y_decision-3.5, 2, step_h, '9. Sentiment\nFinBERT/Keywords', color='#1ABC9C')
    arrow(1.5, y_decision-3.5, 1.5, y_decision-2.8)
    
    box(0.5, y_decision-4.2, 2, step_h, '10. Classify\nNews Type', color='#1ABC9C')
    arrow(1.5, y_decision-4.2, 1.5, y_decision-3.5)
    
    box(0.5, y_decision-4.9, 2, step_h, '11. Analyst\nRatings (50+)', color='#F39C12')
    arrow(1.5, y_decision-4.9, 1.5, y_decision-4.2)
    
    # Right path: NO (No data - NA)
    box(11.5, y_decision-4, 2, 0.4, 'NO (~225)', color='#E74C3C', text_color='white')
    arrow(9, y_decision+0.3, 11.5, y_decision+0.1, 'No\nData', color='#E74C3C')
    
    box(10.5, y_decision-0.8, 3, 0.45, 'NA VALUE PATH', color='#95A5A6', text_color='white')
    box(11, y_decision-1.5, 2, step_h, '12. Set Default\nNA Values', color='#BDC3C7', text_color='#2C3E50')
    arrow(12, y_decision-1.5, 12, y_decision-0.8-0.45)
    
    # Paths merge at calculation
    y_merge = y_decision - 5.5
    arrow(2.5, y_decision-4.9, 5.5, y_merge+0.5)
    arrow(11, y_decision-1.5, 8.5, y_merge+0.5)
    
    # Phase 6: Calculation
    box(2, y_merge-0.2, 10, 0.5, '━━━ PHASE 6: CALCULATION ━━━', color='#34495E', text_color='white')
    y = y_merge - 0.8
    
    box(5.5, y, 3, step_h, '13. Calculate Signal\n🚀👀😴❄️', color='#9B59B6', text_color='white')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    box(5.5, y, 3, step_h, '14. Calculate Score\nComposite', color='#9B59B6', text_color='white')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    # Phase 7: Notion Update
    box(2, y-0.2, 10, 0.5, '━━━ PHASE 7: NOTION UPDATE ━━━', color='#34495E', text_color='white')
    y -= 0.8
    
    box(5.5, y, 3, step_h, '15. Build Payload\n16 Columns', color='#E67E22')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    box(5.5, y, 3, step_h, '16. POST to Notion\nCreate/Update', color='#D35400')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    box(5, y, 4, step_h+0.2, '17. Success?', color='#E74C3C', shape='diamond', text_color='white')
    y_success = y
    y -= (step_h + gap + 0.4)
    
    # Success/Error paths
    arrow(5, y_success+0.3, 3.5, y_success-0.3, 'YES\n97%', color='#27AE60')
    box(2, y_success-0.8, 2, step_h, '✓ Log Success', color='#27AE60', text_color='white')
    
    arrow(9, y_success+0.3, 10.5, y_success-0.3, 'NO\n3%', color='#E74C3C')
    box(10, y_success-0.8, 2, step_h, '✗ Log Error', color='#E74C3C', text_color='white')
    
    # Merge back
    y_merge2 = y_success - 1.4
    arrow(3, y_success-0.8, 7, y_merge2+0.3)
    arrow(11, y_success-0.8, 7, y_merge2+0.3)
    
    # More stocks?
    box(5, y_merge2, 4, step_h+0.2, '18. More Stocks?', color='#E74C3C', shape='diamond', text_color='white')
    
    # Loop back arrow
    arrow(9, y_merge2+0.5, 13, y_merge2+0.5, '', color='#3498DB')
    ax.annotate('', xy=(13, 10), xytext=(13, y_merge2+0.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='#3498DB'))
    ax.annotate('', xy=(5, 10), xytext=(13, 10),
                arrowprops=dict(arrowstyle='->', lw=2, color='#3498DB'))
    ax.text(13.5, (10+y_merge2+0.5)/2, 'YES\nNext Stock', fontsize=8, color='#3498DB', weight='bold')
    
    # NO - Continue to end
    y = y_merge2 - (step_h + gap + 0.4)
    arrow(7, y+gap+0.4, 7, y+step_h+gap/2)
    ax.text(6.5, y+gap+0.2, 'NO', fontsize=8, color='#27AE60', weight='bold')
    
    # Phase 8: Completion
    box(2, y+0.1, 10, 0.5, '━━━ PHASE 8: COMPLETION ━━━', color='#34495E', text_color='white')
    y -= 0.6
    
    box(5.5, y, 3, step_h, '19. Print Stats\nSuccess/Failed', color='#3498DB')
    y -= (step_h + gap)
    arrow(7, y+gap, 7, y+step_h+gap/2)
    
    # END
    box(5.5, y, 3, step_h, '◼ END\nExecution Complete', color='#C0392B', shape='ellipse', text_color='white')
    
    # Legend
    legend_y = 1.5
    ax.text(1, legend_y+0.5, 'LEGEND:', fontsize=10, weight='bold', color='#2C3E50')
    box(1, legend_y, 1.5, 0.3, 'Config/Init', color='#3498DB')
    box(2.8, legend_y, 1.5, 0.3, 'API Call', color='#F39C12')
    box(4.6, legend_y, 1.5, 0.3, 'Processing', color='#E67E22')
    box(6.4, legend_y, 1.5, 0.3, 'Calculation', color='#9B59B6', text_color='white')
    box(8.2, legend_y, 1.5, 0.3, 'Decision', color='#E74C3C', text_color='white')
    box(10, legend_y, 1.5, 0.3, 'Sentiment', color='#1ABC9C', text_color='white')
    
    plt.tight_layout()
    
    # Save
    output_file = 'DATA_FLOW_DIAGRAM.png'
    print(f"💾 Saving diagram to {output_file}...")
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Created: {output_file}")
    print(f"📏 Resolution: 300 DPI (High quality)")
    print(f"📐 Format: PNG (Presentation-ready)")
    print(f"📊 Size: ~14x20 inches")
    
    return output_file

if __name__ == "__main__":
    try:
        output = create_flowchart()
        print()
        print("🎉 Success!")
        print(f"📁 File: {output}")
        print()
        print("Opening image...")
        import os
        os.system(f"start {output}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
