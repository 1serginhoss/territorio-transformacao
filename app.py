"""
Território em Transformação - Dashboard de Planejamento Territorial e Gestão Sustentável
Análise do Uso da Terra e Recursos Naturais em Santa Luzia - MA
"""

import streamlit as st
import geemap.foliumap as geemap
import ee
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import folium
import base64

# ============================================================================
# CONFIGURAÇÃO INICIAL
# ============================================================================
st.set_page_config(
    page_title="Território em Transformação | Planejamento Territorial",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS - LIMPO E PROFISSIONAL
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(160deg, #f0f4f8 0%, #e8edf4 50%, #dce4ed 100%);
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.90);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 28px 32px;
        margin: 12px 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 48px rgba(0, 0, 0, 0.06);
    }
    
    .hero-title {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #1a2a1a !important;
        text-align: center;
        line-height: 1.2;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .hero-title .highlight {
        background: linear-gradient(135deg, #1a472a, #2d8a4e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #4a5a4a !important;
        font-size: 0.9rem;
        font-weight: 400;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #1a472a, #2d8a4e);
        color: #FFFFFF !important;
        padding: 4px 20px;
        border-radius: 30px;
        font-size: 0.55rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
    }
    
    .hero-meta {
        display: inline-block;
        background: rgba(26, 42, 26, 0.04);
        padding: 3px 14px;
        border-radius: 20px;
        font-size: 0.6rem;
        color: #4a5a4a !important;
        border: 1px solid rgba(26, 42, 26, 0.06);
    }
    
    .kpi-card {
        background: rgba(255, 255, 255, 0.92);
        border-radius: 14px;
        padding: 16px 14px;
        text-align: center;
        border: 1px solid rgba(26, 42, 26, 0.06);
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        border-color: rgba(26, 42, 26, 0.1);
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1a2a1a !important;
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    
    .kpi-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #5a6a5a !important;
        font-weight: 600;
        margin-top: 2px;
    }
    
    .kpi-icon {
        font-size: 1.4rem;
        margin-bottom: 2px;
    }
    
    .kpi-trend {
        font-size: 0.5rem;
        margin-top: 4px;
        padding: 2px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .trend-up {
        background: rgba(45, 138, 78, 0.12);
        color: #1a472a;
    }
    
    .trend-down {
        background: rgba(212, 39, 30, 0.1);
        color: #b71c1c;
    }
    
    .trend-stable {
        background: rgba(255, 193, 7, 0.12);
        color: #b8860b;
    }
    
    .chart-card {
        background: rgba(255, 255, 255, 0.92);
        border-radius: 16px;
        padding: 20px 20px 16px 20px;
        border: 1px solid rgba(26, 42, 26, 0.06);
        box-shadow: 0 2px 16px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .chart-card:hover {
        border-color: rgba(26, 42, 26, 0.1);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.05);
    }
    
    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1a2a1a !important;
        margin: 16px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .section-title .icon {
        font-size: 1.1rem;
        opacity: 0.7;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(175deg, #0d1f12 0%, #152a1a 50%, #0f1f14 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04);
        padding: 6px 0;
        min-width: 220px !important;
        max-width: 260px !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    .sidebar-header {
        background: rgba(255, 255, 255, 0.04);
        padding: 16px 16px 12px 16px;
        border-radius: 14px;
        margin-bottom: 14px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }
    
    .sidebar-header .badge {
        font-size: 0.45rem;
        opacity: 0.4;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .sidebar-header .title {
        font-size: 1rem;
        font-weight: 700;
        margin: 4px 0 2px 0;
        color: #FFFFFF !important;
        letter-spacing: -0.2px;
    }
    
    .sidebar-header .sub {
        font-size: 0.55rem;
        opacity: 0.4;
        font-weight: 300;
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .sidebar-section-title {
        font-size: 0.5rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin: 12px 0 6px 0;
        padding: 0 2px;
    }
    
    .year-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 5px;
        margin: 4px 0 8px 0;
    }
    
    .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 6px 4px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        font-size: 0.75rem !important;
        height: 42px !important;
        width: 100% !important;
        text-align: center !important;
        line-height: 1.2 !important;
        min-height: 42px !important;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
        transform: translateY(-1px);
        color: #FFFFFF !important;
    }
    
    .ano-indicador {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 6px 12px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.03);
        margin: 4px 0 10px 0;
    }
    
    .ano-indicador .label {
        font-size: 0.4rem;
        opacity: 0.3;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .ano-indicador .valor {
        font-size: 1.4rem;
        font-weight: 700;
        color: #9FE870 !important;
        margin-top: 0px;
        letter-spacing: -0.5px;
    }
    
    .impact-card {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 10px 12px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        margin: 4px 0;
    }
    
    .impact-card .impact-label {
        font-size: 0.65rem;
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .impact-card .impact-value {
        font-size: 1rem;
        font-weight: 700;
        color: #FFFFFF !important;
    }
    
    .impact-card .impact-desc {
        font-size: 0.5rem;
        color: rgba(255, 255, 255, 0.3) !important;
    }
    
    .footer {
        text-align: center;
        padding: 12px;
        border-top: 1px solid rgba(26, 42, 26, 0.04);
        color: #6a7a6a !important;
        font-size: 0.55rem;
        letter-spacing: 0.5px;
    }
    
    .footer strong {
        color: #2a3a2a !important;
    }
    
    .progress-container {
        margin: 4px 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
        color: #3a4a3a !important;
        margin-bottom: 2px;
    }
    
    .progress-label strong {
        color: #1a2a1a !important;
    }
    
    .progress-bar {
        height: 3px;
        background: rgba(26, 42, 26, 0.06);
        border-radius: 2px;
        overflow: hidden;
    }
    
    .progress-bar .fill {
        height: 100%;
        border-radius: 2px;
        transition: width 0.8s ease;
    }
    
    @media (max-width: 768px) {
        .main-container {
            padding: 16px;
            margin: 10px 8px;
        }
        .hero-title {
            font-size: 1.4rem !important;
        }
        .kpi-value {
            font-size: 1.2rem;
        }
        [data-testid="stSidebar"] {
            min-width: 160px !important;
            max-width: 180px !important;
        }
        .stButton > button {
            height: 36px !important;
            min-height: 36px !important;
            font-size: 0.65rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÃO PARA CARREGAR LOGO
# ============================================================================
def get_image_base64(path, width=120):
    try:
        if os.path.exists(path):
            with open(path, "rb") as image_file:
                data = base64.b64encode(image_file.read()).decode()
            return f'<img src="data:image/png;base64,{data}" width="{width}">'
    except:
        pass
    return None

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================
# ============================================================================
# INICIALIZAÇÃO DO EARTH ENGINE COM SECRETS
# ============================================================================
@st.cache_resource
def init_earth_engine():
    try:
        # Tentar usar secrets (para produção no Streamlit Cloud)
        if hasattr(st, 'secrets') and "EE_ACCOUNT" in st.secrets:
            credentials = ee.ServiceAccountCredentials(
                st.secrets["EE_ACCOUNT"],
                st.secrets["EE_PRIVATE_KEY"]
            )
            ee.Initialize(credentials)
            st.sidebar.success("✅ Earth Engine autenticado com secrets!")
            return True
        else:
            # Tentar autenticação normal (desenvolvimento local)
            ee.Initialize(project='ee-serginss-459118')
            st.sidebar.success("✅ Earth Engine autenticado localmente!")
            return True
    except Exception as e:
        st.sidebar.warning(f"⚠️ Earth Engine offline: {str(e)[:100]}")
        return False

ee_initialized = init_earth_engine()

# ============================================================================
# CONFIGURAÇÃO DAS CLASSES - CORES OFICIAIS MAPBIOMAS
# ============================================================================
CLASS_CONFIG = {
    'names': {
        1: "🌳 Floresta",
        2: "🌾 Formação Natural",
        3: "🚜 Agropecuária",
        4: "🏙️ Área Urbana",
        5: "💧 Água",
        6: "❓ Outros"
    },
    'colors': {
        "🌳 Floresta": "#1f8d49",
        "🌾 Formação Natural": "#d6bc74",
        "🚜 Agropecuária": "#FFFFB2",
        "🏙️ Área Urbana": "#d4271e",
        "💧 Água": "#2532e4",
        "❓ Outros": "#cccccc"
    },
    'class_mapping': {
        1:1,3:1,4:1,5:1,6:1,49:1,
        10:2,11:2,12:2,32:2,29:2,50:2,
        14:3,15:3,18:3,19:3,20:3,35:3,36:3,39:3,40:3,41:3,46:3,47:3,48:3,62:3,9:3,21:3,
        22:4,23:4,24:4,25:4,30:4,
        26:5,33:5,31:5,
        27:6,
    },
    'mapbiomas_palette': [
        "#1f8d49","#1f8d49","#1f8d49","#7dc975","#04381d","#026975",
        "#1f8d49","#1f8d49","#7a5900","#ad975a","#519799","#d6bc74",
        "#ad975a","#FFFFB2","#edde8e","#FFFFB2","#FFFFB2","#E974ED",
        "#C27BA0","#db7093","#ffefc3","#d4271e","#ffa07a","#d4271e",
        "#db4d4f","#0000FF","#ffffff","#0000FF","#ffaa5f","#9c0027",
        "#091077","#fc81f4","#2532e4","#cccccc"
    ]
}

# ============================================================================
# ANOS DISPONÍVEIS
# ============================================================================
ANOS_DISPONIVEIS = [1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]
ANOS_COMPLETOS = [1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]

# ============================================================================
# CARREGAR GEOJSON
# ============================================================================
@st.cache_data
def load_geojson():
    try:
        with open('assets/municipios_ma.geojson', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for feature in data['features']:
            nome = feature['properties'].get('NM_MUNICIP', '') or feature['properties'].get('nome', '')
            if 'SANTA LUZIA' in nome.upper():
                return data, feature
        return data, None
    except:
        return None, None

geojson_data, santa_luzia_feature = load_geojson()

def get_geometry():
    if santa_luzia_feature:
        return ee.Geometry(santa_luzia_feature['geometry'])
    return ee.Geometry.Rectangle([-45.8, -4.3, -45.2, -3.9])

geometry = get_geometry()

# ============================================================================
# CARREGAR MAPBIOMAS
# ============================================================================
mapbiomas_image = None
if ee_initialized:
    try:
        mapbiomas_image = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_integration_v2')
    except:
        pass

# ============================================================================
# FUNÇÃO DE CÁLCULO
# ============================================================================
@st.cache_data(ttl=3600)
def calculate_statistics(years, selected_codes):
    if not ee_initialized or mapbiomas_image is None:
        return get_demo_data(years, selected_codes)
    
    stats = []
    for year in years:
        try:
            band = f'classification_{year}'
            
            area_total = ee.Image.pixelArea().clip(geometry).reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=geometry,
                scale=100,
                maxPixels=1e11
            ).getInfo().get('area', 0) / 1e6
            
            for class_code in selected_codes:
                orig_codes = [k for k, v in CLASS_CONFIG['class_mapping'].items() if v == class_code]
                if orig_codes:
                    mask = mapbiomas_image.select(band).eq(orig_codes[0])
                    for code in orig_codes[1:]:
                        mask = mask.Or(mapbiomas_image.select(band).eq(code))
                    
                    area = ee.Image.pixelArea().updateMask(mask).clip(geometry).reduceRegion(
                        reducer=ee.Reducer.sum(),
                        geometry=geometry,
                        scale=100,
                        maxPixels=1e11
                    ).getInfo().get('area', 0) / 1e6
                    
                    stats.append({
                        'Ano': year,
                        'Classe': class_code,
                        'Nome': CLASS_CONFIG['names'][class_code],
                        'Área (km²)': round(area, 2),
                        'Percentual (%)': round((area / area_total * 100), 1) if area_total > 0 else 0
                    })
        except:
            continue
    
    if not stats:
        return get_demo_data(years, selected_codes)
    return pd.DataFrame(stats)

def get_demo_data(years, selected_codes):
    demo_data = []
    for year in years:
        fator = (year - 1985) / 39 if year > 1985 else 0
        valores = {
            1: 850 * (1 - fator * 0.35),
            2: 380 * (1 - fator * 0.15),
            3: 150 * (1 + fator * 1.8),
            4: 20 * (1 + fator * 2.5),
            5: 25,
            6: 25
        }
        total = sum(valores.values())
        for code in selected_codes:
            area = valores.get(code, 0)
            demo_data.append({
                'Ano': year,
                'Classe': code,
                'Nome': CLASS_CONFIG['names'][code],
                'Área (km²)': round(area, 2),
                'Percentual (%)': round((area / total * 100), 1)
            })
    return pd.DataFrame(demo_data)

# ============================================================================
# FUNÇÃO ÍNDICE DE SUSTENTABILIDADE
# ============================================================================
def calculate_sustainability_index(df, ano):
    dados_ano = df[df['Ano'] == ano]
    if dados_ano.empty:
        return 0, "Indisponível"
    
    pesos = {
        "🌳 Floresta": 100,
        "🌾 Formação Natural": 80,
        "💧 Água": 90,
        "🚜 Agropecuária": 40,
        "🏙️ Área Urbana": 20,
        "❓ Outros": 30
    }
    
    total_area = dados_ano['Área (km²)'].sum()
    if total_area == 0:
        return 0, "Indisponível"
    
    indice = 0
    for _, row in dados_ano.iterrows():
        peso = pesos.get(row['Nome'], 30)
        proporcao = row['Área (km²)'] / total_area
        indice += peso * proporcao
    
    if indice >= 70:
        classificacao = "🟢 Sustentável"
    elif indice >= 50:
        classificacao = "🟡 Moderado"
    elif indice >= 30:
        classificacao = "🟠 Atenção"
    else:
        classificacao = "🔴 Crítico"
    
    return round(indice, 1), classificacao

# ============================================================================
# HEADER COM LOGO
# ============================================================================

# Cabeçalho com logo
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    logo = get_image_base64("assets/logo_principal.png", 160)
    if logo:
        st.markdown(f'<div style="text-align: center; margin-top: 8px;">{logo}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center; font-size: 40px; margin-top: 8px;">🌿</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center;">
        <span class="hero-badge">🌿 Planejamento Territorial · Gestão Sustentável</span>
        <h1 class="hero-title">
            <span class="highlight">Território</span> em Transformação
        </h1>
        <p class="hero-subtitle">
            Análise do Uso da Terra e Recursos Naturais em Santa Luzia - MA
        </p>
        <div style="display: flex; justify-content: center; gap: 8px; margin-top: 6px; flex-wrap: wrap;">
            <span class="hero-meta">📍 Santa Luzia - MA</span>
            <span class="hero-meta">📊 1985-2024</span>
            <span class="hero-meta">🗺️ MapBiomas Coleção 10</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="badge">🌿 Planejamento Territorial</div>
        <div class="title">Território em Transformação</div>
        <div class="sub">Gestão Sustentável · Santa Luzia - MA</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section-title">📅 Período de Análise</div>', unsafe_allow_html=True)
    
    if 'selected_years' not in st.session_state:
        st.session_state.selected_years = [2024]
    
    st.markdown('<div class="year-grid">', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, ano in enumerate(ANOS_DISPONIVEIS):
        col_idx = idx % 3
        with cols[col_idx]:
            is_active = ano == st.session_state.selected_years[0]
            if st.button(
                str(ano),
                key=f"ano_{ano}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.selected_years = [ano]
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    ano_atual = st.session_state.selected_years[0]
    st.markdown(f"""
    <div class="ano-indicador">
        <div class="label">Ano em análise</div>
        <div class="valor">{ano_atual}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section-title">🗺️ Classes de Cobertura</div>', unsafe_allow_html=True)
    
    all_classes = list(CLASS_CONFIG['names'].values())
    selected_names = st.multiselect(
        "Selecione as classes",
        options=all_classes,
        default=all_classes,
        label_visibility="collapsed"
    )
    
    name_to_code = {v: k for k, v in CLASS_CONFIG['names'].items()}
    selected_codes = [name_to_code[n] for n in selected_names]
    
    # Painel de Impacto
    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">📊 Painel de Impacto</div>', unsafe_allow_html=True)
    
    df_temp = calculate_statistics(ANOS_DISPONIVEIS, selected_codes)
    if not df_temp.empty:
        dados_ano = df_temp[df_temp['Ano'] == ano_atual]
        dados_1985 = df_temp[df_temp['Ano'] == 1985]
        
        if not dados_ano.empty and not dados_1985.empty:
            agro_atual = dados_ano[dados_ano['Nome'] == "🚜 Agropecuária"]['Área (km²)'].sum()
            agro_1985 = dados_1985[dados_1985['Nome'] == "🚜 Agropecuária"]['Área (km²)'].sum()
            mudanca_agro = agro_atual - agro_1985
            
            agua_atual = dados_ano[dados_ano['Nome'] == "💧 Água"]['Área (km²)'].sum()
            agua_1985 = dados_1985[dados_1985['Nome'] == "💧 Água"]['Área (km²)'].sum()
            mudanca_agua = agua_atual - agua_1985
            
            urbano_atual = dados_ano[dados_ano['Nome'] == "🏙️ Área Urbana"]['Área (km²)'].sum()
            urbano_1985 = dados_1985[dados_1985['Nome'] == "🏙️ Área Urbana"]['Área (km²)'].sum()
            mudanca_urbano = urbano_atual - urbano_1985
            
            st.markdown(f"""
            <div class="impact-card">
                <div class="impact-label">🚜 Expansão Agropecuária</div>
                <div class="impact-value">{'+' if mudanca_agro > 0 else ''}{mudanca_agro:.1f} km²</div>
                <div class="impact-desc">Pressão sobre recursos naturais</div>
            </div>
            <div class="impact-card">
                <div class="impact-label">💧 Variação Hídrica</div>
                <div class="impact-value">{'+' if mudanca_agua > 0 else ''}{mudanca_agua:.1f} km²</div>
                <div class="impact-desc">Disponibilidade de água</div>
            </div>
            <div class="impact-card">
                <div class="impact-label">🏙️ Crescimento Urbano</div>
                <div class="impact-value">{'+' if mudanca_urbano > 0 else ''}{mudanca_urbano:.1f} km²</div>
                <div class="impact-desc">Expansão da infraestrutura</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# CARREGAR DADOS
# ============================================================================
ano_atual = st.session_state.selected_years[0]

with st.spinner("🔄 Carregando dados territoriais..."):
    df = calculate_statistics(ANOS_COMPLETOS, selected_codes)

if df.empty:
    st.warning("⚠️ Nenhum dado disponível. Verifique a conexão com o Earth Engine.")
    st.stop()

# ============================================================================
# CONTAINER PRINCIPAL
# ============================================================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ============================================================================
# KPIs
# ============================================================================
dados_ano = df[df['Ano'] == ano_atual]

if not dados_ano.empty:
    agro_val = dados_ano[dados_ano['Nome'] == "🚜 Agropecuária"]['Área (km²)'].sum()
    agua_val = dados_ano[dados_ano['Nome'] == "💧 Água"]['Área (km²)'].sum()
    urbano_val = dados_ano[dados_ano['Nome'] == "🏙️ Área Urbana"]['Área (km²)'].sum()
    
    indice_sust, classificacao = calculate_sustainability_index(df, ano_atual)
    
    st.markdown('<div class="section-title"><span class="icon">📊</span> Indicadores Territoriais</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🌾</div>
            <div class="kpi-value">{agro_val:.0f}</div>
            <div class="kpi-label">Área Agropecuária</div>
            <div class="kpi-trend trend-up">↑ Expansão</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💧</div>
            <div class="kpi-value">{agua_val:.0f}</div>
            <div class="kpi-label">Corpos D'água</div>
            <div class="kpi-trend trend-down">↓ Redução</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🏘️</div>
            <div class="kpi-value">{urbano_val:.0f}</div>
            <div class="kpi-label">Área Urbanizada</div>
            <div class="kpi-trend trend-up">↑ Crescimento</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">♻️</div>
            <div class="kpi-value">{indice_sust}</div>
            <div class="kpi-label">Índice de Sustentabilidade</div>
            <div class="kpi-trend trend-stable">{classificacao}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# DISTRIBUIÇÃO ATUAL
# ============================================================================
st.markdown('<div class="section-title"><span class="icon">📊</span> Distribuição da Cobertura do Solo</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    fig_pie = px.pie(
        dados_ano,
        names="Nome",
        values="Área (km²)",
        color="Nome",
        color_discrete_map=CLASS_CONFIG['colors'],
        hole=0.4,
        height=400
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=12, color='#1a2a1a'),
        marker=dict(line=dict(color='white', width=2))
    )
    fig_pie.update_layout(
        showlegend=False,
        font=dict(family='Inter'),
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown("#### Detalhamento")
    for _, row in dados_ano.iterrows():
        pct = row['Percentual (%)']
        nome = row['Nome']
        color = CLASS_CONFIG['colors'][nome]
        area = row['Área (km²)']
        
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-label">
                <span>{nome}</span>
                <span><strong>{pct:.1f}%</strong></span>
            </div>
            <div class="progress-bar">
                <div class="fill" style="width: {pct}%; background: {color};"></div>
            </div>
            <div style="font-size: 0.6rem; color: #5a6a5a; margin-top: -2px;">{area:.1f} km²</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# EVOLUÇÃO TEMPORAL
# ============================================================================
st.markdown('<div class="section-title"><span class="icon">📈</span> Evolução Temporal da Paisagem</div>', unsafe_allow_html=True)

fig_evol = go.Figure()

cores_grafico = {
    "🚜 Agropecuária": "#FFFFB2",
    "💧 Água": "#2532e4",
    "🏙️ Área Urbana": "#d4271e",
    "🌳 Floresta": "#1f8d49",
    "🌾 Formação Natural": "#d6bc74"
}

for classe in ['🚜 Agropecuária', '💧 Água', '🏙️ Área Urbana', '🌳 Floresta', '🌾 Formação Natural']:
    dados_classe = df[df['Nome'] == classe]
    if not dados_classe.empty:
        fig_evol.add_trace(go.Scatter(
            x=dados_classe['Ano'],
            y=dados_classe['Área (km²)'],
            mode='lines+markers',
            name=classe,
            line=dict(color=cores_grafico.get(classe, '#888'), width=2.5),
            marker=dict(size=7)
        ))

fig_evol.update_layout(
    height=380,
    font=dict(family='Inter', size=11, color='#3a4a3a'),
    xaxis=dict(
        title="Ano",
        tickmode='linear',
        dtick=5,
        gridcolor='rgba(0,0,0,0.04)',
        showgrid=True,
        color='#3a4a3a'
    ),
    yaxis=dict(
        title="Área (km²)",
        gridcolor='rgba(0,0,0,0.04)',
        showgrid=True,
        color='#3a4a3a'
    ),
    hovermode='x unified',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=10, b=20, l=40, r=10),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(size=10)
    )
)

st.plotly_chart(fig_evol, use_container_width=True)

st.markdown("---")

# ============================================================================
# MAPA
# ============================================================================
st.markdown('<div class="section-title"><span class="icon">🗺️</span> Mapeamento do Território</div>', unsafe_allow_html=True)

if ee_initialized and mapbiomas_image is not None:
    try:
        m = geemap.Map(center=[-4.1, -45.5], zoom=11)
        
        band = f'classification_{ano_atual}'
        image = mapbiomas_image.select(band).clip(geometry)
        
        m.addLayer(
            image,
            {
                'min': 1,
                'max': 34,
                'palette': CLASS_CONFIG['mapbiomas_palette']
            },
            f"MapBiomas {ano_atual}"
        )
        
        outline = ee.FeatureCollection([ee.Feature(geometry)])
        m.addLayer(
            outline,
            {'color': '#FF0000', 'width': 2.5, 'fillColor': '00000000'},
            '📍 Santa Luzia'
        )
        
        legend_html = """
        <div style="position: fixed; bottom: 30px; right: 30px; background: rgba(255,255,255,0.95); 
                    padding: 10px 14px; border-radius: 10px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    font-family: 'Inter', sans-serif; font-size: 9px; z-index: 1000;
                    border: 1px solid rgba(0,0,0,0.06);">
            <strong style="font-size: 10px; color: #1a2a1a;">🌿 Legenda</strong><br><br>
            <span style="background: #1f8d49; display: inline-block; width: 10px; height: 10px; border-radius: 2px;"></span>
            <span style="color: #1a2a1a;"> Floresta</span><br>
            <span style="background: #d6bc74; display: inline-block; width: 10px; height: 10px; border-radius: 2px;"></span>
            <span style="color: #1a2a1a;"> Formação Natural</span><br>
            <span style="background: #FFFFB2; display: inline-block; width: 10px; height: 10px; border-radius: 2px;"></span>
            <span style="color: #1a2a1a;"> Agropecuária</span><br>
            <span style="background: #d4271e; display: inline-block; width: 10px; height: 10px; border-radius: 2px;"></span>
            <span style="color: #1a2a1a;"> Área Urbana</span><br>
            <span style="background: #2532e4; display: inline-block; width: 10px; height: 10px; border-radius: 2px;"></span>
            <span style="color: #1a2a1a;"> Água</span><br>
            <br>
            <span style="color: #FF0000;">⬤</span>
            <span style="color: #1a2a1a;"> Limite Municipal</span>
        </div>
        """
        
        m.add_child(folium.Element(legend_html))
        m.to_streamlit(height=480)
        
    except Exception as e:
        st.error(f"Erro no mapa: {e}")
        st.info("💡 Dica: Certifique-se de que o ano selecionado está disponível (1985-2024)")
else:
    st.warning("Mapa indisponível - Earth Engine offline")

st.markdown("---")

# ============================================================================
# PAINEL DE IMPACTO
# ============================================================================
st.markdown('<div class="section-title"><span class="icon">📊</span> Painel de Impacto Territorial</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

dados_1985 = df[df['Ano'] == 1985]
dados_2024 = df[df['Ano'] == 2024]

if not dados_1985.empty and not dados_2024.empty:
    agro_1985 = dados_1985[dados_1985['Nome'] == "🚜 Agropecuária"]['Área (km²)'].sum()
    agro_2024 = dados_2024[dados_2024['Nome'] == "🚜 Agropecuária"]['Área (km²)'].sum()
    
    agua_1985 = dados_1985[dados_1985['Nome'] == "💧 Água"]['Área (km²)'].sum()
    agua_2024 = dados_2024[dados_2024['Nome'] == "💧 Água"]['Área (km²)'].sum()
    
    urbano_1985 = dados_1985[dados_1985['Nome'] == "🏙️ Área Urbana"]['Área (km²)'].sum()
    urbano_2024 = dados_2024[dados_2024['Nome'] == "🏙️ Área Urbana"]['Área (km²)'].sum()
    
    with col1:
        mudanca_agro = agro_2024 - agro_1985
        pct_agro = (mudanca_agro / agro_1985 * 100) if agro_1985 > 0 else 0
        st.markdown(f"""
        <div class="chart-card">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 1.3rem;">🚜</span>
                <div>
                    <div style="font-weight: 700; color: #1a2a1a; font-size: 0.9rem;">Expansão Agropecuária</div>
                    <div style="font-size: 0.65rem; color: #5a6a5a;">1985 → 2024</div>
                </div>
            </div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #e8822a;">+{mudanca_agro:.0f} km²</div>
            <div style="font-size: 0.75rem; color: #4a5a4a;">Aumento de {pct_agro:.1f}%</div>
            <div style="margin-top: 6px; padding: 6px 10px; background: rgba(232, 130, 42, 0.08); border-radius: 6px; font-size: 0.65rem; color: #4a5a4a;">
                ⚠️ Pressão crescente sobre recursos naturais
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        mudanca_agua = agua_2024 - agua_1985
        pct_agua = (mudanca_agua / agua_1985 * 100) if agua_1985 > 0 else 0
        st.markdown(f"""
        <div class="chart-card">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 1.3rem;">💧</span>
                <div>
                    <div style="font-weight: 700; color: #1a2a1a; font-size: 0.9rem;">Alteração Hídrica</div>
                    <div style="font-size: 0.65rem; color: #5a6a5a;">1985 → 2024</div>
                </div>
            </div>
            <div style="font-size: 1.8rem; font-weight: 800; color: {'#2568b4' if mudanca_agua > 0 else '#d4271e'};">{'+' if mudanca_agua > 0 else ''}{mudanca_agua:.0f} km²</div>
            <div style="font-size: 0.75rem; color: #4a5a4a;">Variação de {pct_agua:.1f}%</div>
            <div style="margin-top: 6px; padding: 6px 10px; background: rgba(37, 104, 180, 0.08); border-radius: 6px; font-size: 0.65rem; color: #4a5a4a;">
                {'🟢 Estabilidade hídrica' if mudanca_agua > 0 else '🔴 Redução da disponibilidade hídrica'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        mudanca_urbano = urbano_2024 - urbano_1985
        pct_urbano = (mudanca_urbano / urbano_1985 * 100) if urbano_1985 > 0 else 0
        st.markdown(f"""
        <div class="chart-card">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 1.3rem;">🏘️</span>
                <div>
                    <div style="font-weight: 700; color: #1a2a1a; font-size: 0.9rem;">Crescimento Urbano</div>
                    <div style="font-size: 0.65rem; color: #5a6a5a;">1985 → 2024</div>
                </div>
            </div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #d4271e;">+{mudanca_urbano:.0f} km²</div>
            <div style="font-size: 0.75rem; color: #4a5a4a;">Crescimento de {pct_urbano:.1f}%</div>
            <div style="margin-top: 6px; padding: 6px 10px; background: rgba(212, 39, 30, 0.08); border-radius: 6px; font-size: 0.65rem; color: #4a5a4a;">
                🏙️ Alteração do território com expansão urbana
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# DADOS E EXPORTAÇÃO
# ============================================================================
with st.expander("📋 Dados Completos e Exportação", expanded=False):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.dataframe(df, use_container_width=True, height=250)
    
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados (CSV)",
            data=csv,
            file_name=f"territorio_transformacao_{ano_atual}.csv",
            mime="text/csv"
        )
        
        st.markdown("""
        <div style="background: rgba(255,255,255,0.5); padding: 8px; border-radius: 8px; margin-top: 8px; border: 1px solid rgba(0,0,0,0.04);">
            <div style="font-size: 0.5rem; color: #6a7a6a; text-transform: uppercase; letter-spacing: 1px;">📊 Metadados</div>
            <div style="font-size: 0.55rem; color: #7a8a7a; line-height: 1.6;">
                Fonte: MapBiomas Coleção 10<br>
                Resolução: 30m<br>
                Período: 1985-2024
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

st.markdown(f"""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 2px;">
        <span>🌿 Planejamento Territorial</span>
        <span style="opacity: 0.2;">|</span>
        <span>🌱 Gestão Sustentável</span>
        <span style="opacity: 0.2;">|</span>
        <span>📊 MapBiomas Coleção 10</span>
    </div>
    <div>
        <strong>Território em Transformação</strong> — Santa Luzia - MA
    </div>
    <div style="margin-top: 2px; opacity: 0.5;">
        Centro Educa Mais José Mariano Muniz · Análise de Uso da Terra e Recursos Naturais
    </div>
    <div style="margin-top: 2px; opacity: 0.3;">
        {datetime.now().strftime('%d/%m/%Y às %H:%M')}
    </div>
</div>
""", unsafe_allow_html=True)