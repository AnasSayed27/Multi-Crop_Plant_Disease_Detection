import os
import json
import pandas as pd

json_path = 'models_assets/ab_experiment_comparison.json'
if not os.path.exists(json_path):
    json_path = '/content/drive/MyDrive/Potato_disease/models_assets/ab_experiment_comparison.json'

if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    a_rw = data['model_a']['realworld']['per_class_results']
    b_rw = data['model_b']['realworld']['per_class_results']
    
    rows = []
    for cls_name in sorted(a_rw.keys()):
        a_info = a_rw[cls_name]
        b_info = b_rw.get(cls_name, {'total_samples': a_info['total_samples'], 'correct': 0, 'accuracy': 0.0})
        
        n = a_info['total_samples']
        a_corr = a_info['correct']
        b_corr = b_info['correct']
        a_acc = a_info['accuracy'] * 100
        b_acc = b_info['accuracy'] * 100
        delta = b_acc - a_acc
        
        rows.append({
            'Class Name': cls_name,
            'Total Imgs': n,
            'Model A (Top-1)': f"{a_corr}/{n} ({a_acc:.1f}%)",
            'Model B (Top-1)': f"{b_corr}/{n} ({b_acc:.1f}%)",
            'Change (B - A)': f"{'+' if delta > 0 else ''}{delta:.1f}%",
            'Delta_Num': delta
        })
        
    df = pd.DataFrame(rows)
    print("=" * 95)
    print(" 236-IMAGE PLANTDOC REAL-WORLD BENCHMARK: MODEL A vs MODEL B PER-CLASS BREAKDOWN")
    print("=" * 95)
    print(df[['Class Name', 'Total Imgs', 'Model A (Top-1)', 'Model B (Top-1)', 'Change (B - A)']].to_string(index=False))
    print("=" * 95)
    
    # Summary of Improvements vs Regressions
    improved = df[df['Delta_Num'] > 0]
    worsened = df[df['Delta_Num'] < 0]
    unchanged = df[df['Delta_Num'] == 0]
    
    print(f"\n--- PERFORMANCE CATEGORIZATION ---")
    print(f"✅ Classes Improved by Model B ({len(improved)} classes):")
    for _, r in improved.iterrows():
        print(f"   • {r['Class Name']:<45}: {r['Model A (Top-1)']} -> {r['Model B (Top-1)']} ({r['Change (B - A)']})")
        
    print(f"\n⚠️ Classes Worsened by Model B ({len(worsened)} classes):")
    for _, r in worsened.iterrows():
        print(f"   • {r['Class Name']:<45}: {r['Model A (Top-1)']} -> {r['Model B (Top-1)']} ({r['Change (B - A)']})")
        
    print(f"\n➖ Classes Unchanged ({len(unchanged)} classes):")
    for _, r in unchanged.iterrows():
        print(f"   • {r['Class Name']:<45}: {r['Model A (Top-1)']}")
else:
    print(f"JSON comparison file not found at {json_path}")
