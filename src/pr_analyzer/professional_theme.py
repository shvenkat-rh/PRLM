"""
Professional Theme Configuration for GitHub PR Analytics Platform
Centralized styling and theme management for consistent enterprise appearance
"""

# Professional Color Palette
COLORS = {
    # Primary brand colors
    'primary': '#667eea',
    'primary_dark': '#5a67d8',
    'secondary': '#764ba2',
    
    # Status colors
    'success': '#22c55e',
    'success_light': '#dcfce7',
    'success_border': '#16a34a',
    
    'info': '#3b82f6',
    'info_light': '#dbeafe',
    'info_border': '#2563eb',
    
    'warning': '#f59e0b',
    'warning_light': '#fef3c7',
    'warning_border': '#d97706',
    
    'error': '#ef4444',
    'error_light': '#fee2e2',
    'error_border': '#dc2626',
    
    # Neutral colors
    'text_primary': '#1a202c',
    'text_secondary': '#4a5568',
    'text_muted': '#64748b',
    
    'background': '#ffffff',
    'background_secondary': '#f8fafc',
    'background_tertiary': '#f1f5f9',
    
    'border': '#e2e8f0',
    'border_light': '#f1f5f9',
    
    # Gradient backgrounds
    'gradient_primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'gradient_success': 'linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%)',
    'gradient_info': 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
    'gradient_warning': 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
    'gradient_error': 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)',
    'gradient_card': 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
    'gradient_page': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)'
}

# Typography settings
TYPOGRAPHY = {
    'font_family': "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    'font_sizes': {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem'
    },
    'font_weights': {
        'light': '300',
        'normal': '400',
        'medium': '500',
        'semibold': '600',
        'bold': '700'
    },
    'line_heights': {
        'tight': '1.25',
        'snug': '1.375',
        'normal': '1.5',
        'relaxed': '1.625',
        'loose': '2'
    }
}

# Spacing and layout
SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem',
    'base': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
    '2xl': '3rem',
    '3xl': '4rem'
}

# Border radius values
BORDER_RADIUS = {
    'sm': '4px',
    'base': '8px',
    'lg': '12px',
    'xl': '16px',
    'full': '9999px'
}

# Shadow definitions
SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'base': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)'
}

# Component-specific styles
COMPONENTS = {
    'card': {
        'background': COLORS['gradient_card'],
        'border': f"1px solid {COLORS['border']}",
        'border_radius': BORDER_RADIUS['lg'],
        'shadow': SHADOWS['md'],
        'padding': SPACING['xl']
    },
    'button_primary': {
        'background': COLORS['gradient_primary'],
        'color': COLORS['background'],
        'border': 'none',
        'border_radius': BORDER_RADIUS['base'],
        'padding': f"{SPACING['sm']} {SPACING['lg']}",
        'font_weight': TYPOGRAPHY['font_weights']['semibold'],
        'shadow': SHADOWS['md']
    },
    'input': {
        'border': f"2px solid {COLORS['border']}",
        'border_radius': BORDER_RADIUS['base'],
        'padding': SPACING['sm'],
        'background': COLORS['background']
    },
    'status_success': {
        'background': COLORS['gradient_success'],
        'border': f"1px solid {COLORS['success_border']}",
        'color': COLORS['success_border'],
        'border_radius': BORDER_RADIUS['base'],
        'padding': SPACING['base']
    },
    'status_info': {
        'background': COLORS['gradient_info'],
        'border': f"1px solid {COLORS['info_border']}",
        'color': COLORS['info_border'],
        'border_radius': BORDER_RADIUS['base'],
        'padding': SPACING['base']
    },
    'status_warning': {
        'background': COLORS['gradient_warning'],
        'border': f"1px solid {COLORS['warning_border']}",
        'color': COLORS['warning_border'],
        'border_radius': BORDER_RADIUS['base'],
        'padding': SPACING['base']
    },
    'status_error': {
        'background': COLORS['gradient_error'],
        'border': f"1px solid {COLORS['error_border']}",
        'color': COLORS['error_border'],
        'border_radius': BORDER_RADIUS['base'],
        'padding': SPACING['base']
    }
}

# Streamlit theme configuration
STREAMLIT_CONFIG = {
    'theme.base': 'light',
    'theme.primaryColor': COLORS['primary'],
    'theme.backgroundColor': COLORS['background'],
    'theme.secondaryBackgroundColor': COLORS['background_secondary'],
    'theme.textColor': COLORS['text_primary']
}

# Animation and transition settings
ANIMATIONS = {
    'transition_fast': '0.15s ease',
    'transition_base': '0.3s ease',
    'transition_slow': '0.5s ease',
    'hover_transform': 'translateY(-2px)',
    'hover_shadow': SHADOWS['lg']
}

def get_status_style(status_type):
    """Get styling for status components"""
    status_styles = {
        'success': COMPONENTS['status_success'],
        'info': COMPONENTS['status_info'],
        'warning': COMPONENTS['status_warning'],
        'error': COMPONENTS['status_error']
    }
    return status_styles.get(status_type, status_styles['info'])

def create_metric_card_style():
    """Generate CSS for metric cards"""
    return f"""
    .metric-card {{
        background: {COMPONENTS['card']['background']};
        border: {COMPONENTS['card']['border']};
        border-radius: {COMPONENTS['card']['border_radius']};
        padding: {COMPONENTS['card']['padding']};
        box-shadow: {COMPONENTS['card']['shadow']};
        transition: {ANIMATIONS['transition_base']};
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card:hover {{
        transform: {ANIMATIONS['hover_transform']};
        box-shadow: {ANIMATIONS['hover_shadow']};
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: {COLORS['gradient_primary']};
    }}
    """

def create_professional_css():
    """Generate complete professional CSS"""
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {{
            font-family: {TYPOGRAPHY['font_family']};
            background: {COLORS['gradient_page']};
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        .main-header {{
            font-size: {TYPOGRAPHY['font_sizes']['5xl']};
            font-weight: {TYPOGRAPHY['font_weights']['bold']};
            color: {COLORS['text_primary']};
            text-align: center;
            margin: {SPACING['xl']} 0 {SPACING['base']} 0;
            background: {COLORS['gradient_primary']};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.025em;
        }}
        
        .sub-header {{
            font-size: {TYPOGRAPHY['font_sizes']['lg']};
            color: {COLORS['text_secondary']};
            text-align: center;
            margin-bottom: {SPACING['3xl']};
            font-weight: {TYPOGRAPHY['font_weights']['normal']};
            line-height: {TYPOGRAPHY['line_heights']['relaxed']};
        }}
        
        {create_metric_card_style()}
        
        .metric-value {{
            font-size: {TYPOGRAPHY['font_sizes']['4xl']};
            font-weight: {TYPOGRAPHY['font_weights']['bold']};
            color: {COLORS['text_primary']};
            margin: 0;
            line-height: {TYPOGRAPHY['line_heights']['tight']};
        }}
        
        .metric-label {{
            font-size: {TYPOGRAPHY['font_sizes']['sm']};
            color: {COLORS['text_muted']};
            margin: {SPACING['sm']} 0 0 0;
            font-weight: {TYPOGRAPHY['font_weights']['medium']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .status-success {{
            background: {COMPONENTS['status_success']['background']};
            border: {COMPONENTS['status_success']['border']};
            border-radius: {COMPONENTS['status_success']['border_radius']};
            padding: {COMPONENTS['status_success']['padding']};
            margin: {SPACING['base']} 0;
            color: {COMPONENTS['status_success']['color']};
            font-weight: {TYPOGRAPHY['font_weights']['medium']};
        }}
        
        .status-info {{
            background: {COMPONENTS['status_info']['background']};
            border: {COMPONENTS['status_info']['border']};
            border-radius: {COMPONENTS['status_info']['border_radius']};
            padding: {COMPONENTS['status_info']['padding']};
            margin: {SPACING['base']} 0;
            color: {COMPONENTS['status_info']['color']};
            font-weight: {TYPOGRAPHY['font_weights']['medium']};
        }}
        
        .status-warning {{
            background: {COMPONENTS['status_warning']['background']};
            border: {COMPONENTS['status_warning']['border']};
            border-radius: {COMPONENTS['status_warning']['border_radius']};
            padding: {COMPONENTS['status_warning']['padding']};
            margin: {SPACING['base']} 0;
            color: {COMPONENTS['status_warning']['color']};
            font-weight: {TYPOGRAPHY['font_weights']['medium']};
        }}
        
        .status-error {{
            background: {COMPONENTS['status_error']['background']};
            border: {COMPONENTS['status_error']['border']};
            border-radius: {COMPONENTS['status_error']['border_radius']};
            padding: {COMPONENTS['status_error']['padding']};
            margin: {SPACING['base']} 0;
            color: {COMPONENTS['status_error']['color']};
            font-weight: {TYPOGRAPHY['font_weights']['medium']};
        }}
        
        .stButton > button {{
            background: {COMPONENTS['button_primary']['background']};
            color: {COMPONENTS['button_primary']['color']};
            border: {COMPONENTS['button_primary']['border']};
            border-radius: {COMPONENTS['button_primary']['border_radius']};
            padding: {COMPONENTS['button_primary']['padding']};
            font-weight: {COMPONENTS['button_primary']['font_weight']};
            font-size: {TYPOGRAPHY['font_sizes']['sm']};
            width: 100%;
            transition: {ANIMATIONS['transition_base']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: {COMPONENTS['button_primary']['shadow']};
        }}
        
        .stButton > button:hover {{
            transform: {ANIMATIONS['hover_transform']};
            box-shadow: {ANIMATIONS['hover_shadow']};
        }}
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            border: {COMPONENTS['input']['border']};
            border-radius: {COMPONENTS['input']['border_radius']};
            padding: {COMPONENTS['input']['padding']};
            font-size: {TYPOGRAPHY['font_sizes']['sm']};
            background: {COMPONENTS['input']['background']};
            transition: {ANIMATIONS['transition_fast']};
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: {COLORS['primary']};
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .section-header {{
            font-size: {TYPOGRAPHY['font_sizes']['xl']};
            font-weight: {TYPOGRAPHY['font_weights']['semibold']};
            color: {COLORS['text_primary']};
            margin: {SPACING['xl']} 0 {SPACING['base']} 0;
            padding-bottom: {SPACING['sm']};
            border-bottom: 2px solid {COLORS['border']};
        }}
        
        .analytics-container {{
            background: {COLORS['background']};
            border-radius: {BORDER_RADIUS['lg']};
            padding: {SPACING['xl']};
            box-shadow: {SHADOWS['md']};
            margin: {SPACING['base']} 0;
            border: 1px solid {COLORS['border']};
        }}
        
        .professional-footer {{
            background: {COLORS['gradient_primary']};
            color: {COLORS['background']};
            padding: {SPACING['xl']};
            border-radius: {BORDER_RADIUS['lg']};
            margin: {SPACING['3xl']} 0 {SPACING['base']} 0;
            text-align: center;
        }}
        
        .stProgress > div > div > div > div {{
            background: {COLORS['gradient_primary']};
            border-radius: {BORDER_RADIUS['sm']};
        }}
        
        @media (max-width: 768px) {{
            .main-header {{
                font-size: {TYPOGRAPHY['font_sizes']['3xl']};
            }}
            
            .metric-card {{
                padding: {SPACING['base']};
            }}
            
            .metric-value {{
                font-size: {TYPOGRAPHY['font_sizes']['3xl']};
            }}
        }}
    </style>
    """ 