#!/usr/bin/env python3
"""
Create visual flowchart diagram for Market Bot data flow
Exports as PNG image for presentations
"""

try:
    from graphviz import Digraph
    import os
except ImportError:
    print("❌ Required library not found!")
    print("\nPlease install:")
    print("  pip install graphviz")
    print("\nAlso install Graphviz system package:")
    print("  Windows: choco install graphviz")
    print("  Or download from: https://graphviz.org/download/")
    exit(1)

def create_data_flow_diagram():
    """Create comprehensive data flow diagram"""
    
    print("=" * 60)
    print("🎨 Creating Data Flow Diagram")
    print("=" * 60)
    print()
    
    # Create new directed graph
    dot = Digraph(comment='Market Bot Data Flow', format='png')
    dot.attr(rankdir='TB', size='12,16', dpi='300')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='9')
    
    # Start/End nodes
    dot.node('START', 'START\nBot Execution', shape='ellipse', fillcolor='#90EE90', fontsize='12', style='filled')
    dot.node('END', 'END\nExecution Complete', shape='ellipse', fillcolor='#FFB6C1', fontsize='12', style='filled')
    
    # Phase 1: Initialization
    dot.node('INIT', 'Load Configuration\n(Tokens, Database ID)', fillcolor='#87CEEB')
    dot.node('STOCKS', 'Load Stock List\n(675 NSE Stocks)', fillcolor='#87CEEB')
    
    # Phase 2: Loop
    dot.node('LOOP', 'For Each Stock\n(Rank 1-675)', fillcolor='#DDA0DD', shape='diamond')
    
    # Phase 3: Data Fetching
    dot.node('FETCH', 'Fetch Price Data\n(yfinance 6mo)', fillcolor='#FFD700')
    dot.node('CHECK', 'Data Available?', fillcolor='#FF6347', shape='diamond')
    
    # Path A: Data Available
    dot.node('MOM', 'Calculate Momentum\n(6-month return)', fillcolor='#FFA07A')
    dot.node('VOL', 'Calculate Volume Surge\n(vs 20-day avg)', fillcolor='#FFA07A')
    dot.node('NEWS', 'Fetch News\n(70+ sources AI / 2 Lite)', fillcolor='#FFD700')
    dot.node('SENT', 'Analyze Sentiment\n(FinBERT AI / Keywords)', fillcolor='#98FB98')
    dot.node('TYPE', 'Classify News Type\n(Earnings, Product, etc.)', fillcolor='#98FB98')
    dot.node('ANALYST', 'Fetch Analyst Ratings\n(50+ sources)', fillcolor='#FFD700')
    
    # Path B: No Data
    dot.node('NA', 'Set NA Values\n(Default data)', fillcolor='#D3D3D3')
    
    # Calculation Phase
    dot.node('SIGNAL', 'Calculate Signal\n(🚀/👀/😴/❄️)', fillcolor='#DDA0DD')
    dot.node('SCORE', 'Calculate Score\n(Composite)', fillcolor='#DDA0DD')
    
    # Notion Update
    dot.node('PAYLOAD', 'Build Notion Payload\n(16 columns)', fillcolor='#FFE4B5')
    dot.node('API', 'POST to Notion API\n(Create/Update Page)', fillcolor='#FFA500')
    dot.node('SUCCESS', 'API Success?', fillcolor='#FF6347', shape='diamond')
    dot.node('LOG_OK', 'Log Success', fillcolor='#90EE90')
    dot.node('LOG_ERR', 'Log Error', fillcolor='#FF6347')
    
    # More stocks?
    dot.node('MORE', 'More Stocks?', fillcolor='#FF6347', shape='diamond')
    dot.node('STATS', 'Print Statistics\n(Success/Failed counts)', fillcolor='#87CEEB')
    
    # Connect nodes - Main flow
    dot.edge('START', 'INIT', label='1')
    dot.edge('INIT', 'STOCKS', label='2')
    dot.edge('STOCKS', 'LOOP', label='3')
    dot.edge('LOOP', 'FETCH', label='4')
    dot.edge('FETCH', 'CHECK', label='5')
    
    # Path A: Data exists
    dot.edge('CHECK', 'MOM', label='YES\n(~450 stocks)', color='green', fontcolor='green')
    dot.edge('MOM', 'VOL', label='6')
    dot.edge('VOL', 'NEWS', label='7')
    dot.edge('NEWS', 'SENT', label='8')
    dot.edge('SENT', 'TYPE', label='9')
    dot.edge('TYPE', 'ANALYST', label='10')
    dot.edge('ANALYST', 'SIGNAL', label='11')
    
    # Path B: No data
    dot.edge('CHECK', 'NA', label='NO\n(~225 stocks)', color='red', fontcolor='red')
    dot.edge('NA', 'SIGNAL', label='12')
    
    # Continue to scoring
    dot.edge('SIGNAL', 'SCORE', label='13')
    dot.edge('SCORE', 'PAYLOAD', label='14')
    dot.edge('PAYLOAD', 'API', label='15')
    dot.edge('API', 'SUCCESS', label='16')
    
    # Success/Error paths
    dot.edge('SUCCESS', 'LOG_OK', label='YES\n(~97%)', color='green', fontcolor='green')
    dot.edge('SUCCESS', 'LOG_ERR', label='NO\n(~3%)', color='red', fontcolor='red')
    
    # Back to loop
    dot.edge('LOG_OK', 'MORE', label='17')
    dot.edge('LOG_ERR', 'MORE', label='18')
    
    # Loop or finish
    dot.edge('MORE', 'LOOP', label='YES', color='blue', fontcolor='blue')
    dot.edge('MORE', 'STATS', label='NO', color='green', fontcolor='green')
    dot.edge('STATS', 'END', label='19')
    
    # Render
    print("📊 Generating flowchart...")
    output_file = 'DATA_FLOW_DIAGRAM'
    dot.render(output_file, cleanup=True)
    
    print(f"✅ Created: {output_file}.png")
    print(f"📏 Size: High resolution (300 DPI)")
    print(f"📐 Format: PNG (presentation-ready)")
    
    return f"{output_file}.png"

if __name__ == "__main__":
    try:
        output = create_data_flow_diagram()
        print()
        print("🎉 Success!")
        print(f"📁 File: {output}")
        print()
        print("Opening image...")
        os.system(f"start {output}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure Graphviz is installed:")
        print("  choco install graphviz")
        print("  OR download from: https://graphviz.org/download/")
