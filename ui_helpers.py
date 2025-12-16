"""
Helper functions untuk styling dan visualisasi
"""

def get_risk_badge_html(risk_category):
    """Generate HTML badge untuk kategori risiko"""
    if risk_category == 'Low Risk':
        return '<span class="risk-badge risk-low">🟢 LOW RISK</span>'
    elif risk_category == 'Medium Risk':
        return '<span class="risk-badge risk-medium">🟡 MEDIUM RISK</span>'
    else:
        return '<span class="risk-badge risk-high">🔴 HIGH RISK</span>'

def format_number(number):
    """Format angka dengan separator ribuan"""
    return f"{number:,.0f}".replace(',', '.')

def get_score_color(score):
    """Dapatkan warna berdasarkan skor"""
    if score >= 70:
        return '#10b981'  # Green
    elif score >= 40:
        return '#f59e0b'  # Orange
    else:
        return '#ef4444'  # Red

def create_metric_card(title, value, subtitle, icon, color):
    """Buat HTML card untuk metrics"""
    return f"""
    <div style='background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); 
                border-left: 4px solid {color}; transition: transform 0.3s ease;'>
        <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;'>
            <span style='font-size: 2rem;'>{icon}</span>
            <span style='color: {color}; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;'>{title}</span>
        </div>
        <h2 style='margin: 0.5rem 0; color: #1e293b; font-size: 2.5rem; font-weight: 700;'>{value}</h2>
        <p style='margin: 0; color: #64748b; font-size: 0.9rem;'>{subtitle}</p>
    </div>
    """

def create_info_box(message, box_type='info'):
    """Buat info box dengan styling"""
    icons = {
        'info': '💡',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }
    
    colors = {
        'info': {'bg': '#d1ecf1', 'border': '#17a2b8', 'text': '#0c5460'},
        'success': {'bg': '#d4edda', 'border': '#28a745', 'text': '#155724'},
        'warning': {'bg': '#fff3cd', 'border': '#ffc107', 'text': '#856404'},
        'error': {'bg': '#f8d7da', 'border': '#dc3545', 'text': '#721c24'}
    }
    
    c = colors.get(box_type, colors['info'])
    icon = icons.get(box_type, '💡')
    
    return f"""
    <div style='padding: 1.25rem; border-radius: 12px; background: {c["bg"]};
                border-left: 4px solid {c["border"]}; color: {c["text"]};
                font-weight: 500; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
        {icon} {message}
    </div>
    """

def create_progress_bar(value, max_value=100, color='#667eea'):
    """Buat progress bar"""
    percentage = (value / max_value) * 100
    return f"""
    <div style='background: #e2e8f0; border-radius: 10px; overflow: hidden; height: 8px;'>
        <div style='background: {color}; width: {percentage}%; height: 100%; 
                    transition: width 0.3s ease;'></div>
    </div>
    """

def create_stat_card(label, value, change=None, change_type='increase'):
    """Buat stat card dengan optional change indicator"""
    change_html = ''
    if change is not None:
        arrow = '↑' if change_type == 'increase' else '↓'
        color = '#10b981' if change_type == 'increase' else '#ef4444'
        change_html = f"<span style='color: {color}; font-size: 0.85rem;'>{arrow} {change}%</span>"
    
    return f"""
    <div style='background: white; padding: 1.25rem; border-radius: 12px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
        <p style='margin: 0; color: #64748b; font-size: 0.85rem;'>{label}</p>
        <div style='display: flex; align-items: baseline; justify-content: space-between; margin-top: 0.5rem;'>
            <h3 style='margin: 0; color: #1e293b; font-size: 1.75rem; font-weight: 700;'>{value}</h3>
            {change_html}
        </div>
    </div>
    """

def create_timeline_item(date, title, description, icon='📌'):
    """Buat item timeline"""
    return f"""
    <div style='display: flex; gap: 1rem; margin-bottom: 1.5rem;'>
        <div style='flex-shrink: 0;'>
            <div style='width: 40px; height: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 50%; display: flex; align-items: center; justify-content: center;
                        font-size: 1.2rem; box-shadow: 0 4px 6px rgba(102,126,234,0.3);'>
                {icon}
            </div>
        </div>
        <div style='flex-grow: 1;'>
            <p style='margin: 0; color: #64748b; font-size: 0.8rem;'>{date}</p>
            <h4 style='margin: 0.25rem 0; color: #1e293b;'>{title}</h4>
            <p style='margin: 0.25rem 0 0 0; color: #64748b; font-size: 0.9rem;'>{description}</p>
        </div>
    </div>
    """

def create_feature_card(icon, title, description):
    """Buat feature card"""
    return f"""
    <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.07); text-align: center;
                transition: transform 0.3s ease; cursor: pointer;'
         onmouseover='this.style.transform="translateY(-8px)"; this.style.boxShadow="0 12px 24px rgba(0,0,0,0.15)"'
         onmouseout='this.style.transform="translateY(0)"; this.style.boxShadow="0 4px 6px rgba(0,0,0,0.07)"'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>{icon}</div>
        <h3 style='margin: 0 0 0.5rem 0; color: #1e293b;'>{title}</h3>
        <p style='margin: 0; color: #64748b; font-size: 0.9rem;'>{description}</p>
    </div>
    """

def get_gradient_background(color1='#667eea', color2='#764ba2'):
    """Generate gradient background"""
    return f"background: linear-gradient(135deg, {color1} 0%, {color2} 100%);"
