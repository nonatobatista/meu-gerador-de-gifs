import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter, ImageChops
import io
import math
import random
import os
import urllib.request
import colorsys
import numpy as np
import zipfile

# ============================================================================
# 1. CONFIGURAÇÃO INICIAL DA PÁGINA WEB
# ============================================================================
st.set_page_config(
    page_title="Gerador de GIFs Ultra Premium",
    page_icon="🎨",
    layout="centered"
)

# CSS customizado para deixar a interface mais premium
st.markdown("""
<style>
    /* Fundo escuro geral */
    .stApp { background: linear-gradient(135deg, #0a0e27 0%, #0d1b2a 100%); }
    
    /* Título com efeito glow */
    h1 { 
        background: linear-gradient(90deg, #00ff88, #00cfff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0,255,136,0.3);
        font-size: 2.2rem !important;
    }
    
    /* Sidebar mais escura */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        border-right: 1px solid #30363d;
    }
    
    /* Botões com brilho */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88, #00cfff);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        transition: all 0.3s;
        box-shadow: 0 0 20px rgba(0,255,136,0.4);
    }
    .stButton > button:hover {
        box-shadow: 0 0 40px rgba(0,255,136,0.8);
        transform: scale(1.02);
    }
    
    /* Cards de seção */
    .effect-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(0,255,136,0.2);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        backdrop-filter: blur(10px);
    }
    
    /* Badges de novidade */
    .badge-new {
        background: linear-gradient(135deg, #ff006e, #fb5607);
        color: white;
        font-size: 0.65rem;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 20px;
        margin-left: 6px;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Gerador de GIFs Ultra Premium")
st.markdown("**Versão 3.4 — Engine Absoluta de Textos** | Renderização multi-linhas matemática")

# ============================================================================
# 2. BARRA LATERAL - CONFIGURAÇÕES GLOBAIS
# ============================================================================
st.sidebar.header("🚀 Configurações Principais")

tamanho_saida = st.sidebar.slider("Resolução do GIF (Pixels):", 200, 1000, 600, 50)
velocidade_fps = st.sidebar.slider("Velocidade (FPS):", 10, 60, 30, 5)
num_frames_total = st.sidebar.slider("Duração (Número de Frames):", 12, 60, 30, 6)

tipo_fundo = st.sidebar.selectbox(
    "Estilo do Fundo:",
    [
        "Cor Sólida",
        "Totalmente Transparente",
        "Gradiente Radial Dinâmico",
        "Gradiente Linear Animado",
        "Padrão de Ruído (Noise)",
        "🆕 Fundo Estelar (Stars)",
        "🆕 Plasma Psicodélico",
    ]
)

cor_fundo_primaria = st.sidebar.color_picker("Cor Principal do Fundo:", "#0A0E27")
cor_fundo_secundaria = st.sidebar.color_picker("Cor Secundária (Gradientes):", "#1E3A8A")

# ============================================================================
# 3. MOVIMENTOS
# ============================================================================
st.sidebar.subheader("🎬 Efeitos de Movimento")

combo_efeito = st.sidebar.selectbox(
    "Movimento Principal:",
    [
        "Pulsar Suave (Respiração)",
        "Rotação Infinita",
        "Rotação + Pulsar (Clássico)",
        "Gelatina Elástica (Squash & Stretch)",
        "Tremor Caótico (Glitch)",
        "Quicar (Bounce Physics)",
        "Tornado Cósmico (Multi-Efeito)",
        "Onda Senoidal (Wave)",
        "Espiral Hipnótica",
        "Explosão e Implosão",
        "Balanço de Pêndulo",
        "Zoom In/Out Dramático",
        "🆕 Flutuação 3D (Float)",
        "🆕 Vibração Elétrica",
        "🆕 Órbita Dupla",
        "🆕 Bounce Realista (Quique + Squash)",
        "🆕 Rotação Cinematográfica",
        "🆕 Zoom Dramático In/Out Elástico",
    ]
)

intensidade_movimento = st.sidebar.slider("Intensidade do Movimento:", 0.1, 2.0, 1.0, 0.1)

# ============================================================================
# 4. EFEITOS VISUAIS
# ============================================================================
st.sidebar.subheader("✨ Efeitos Especiais")

ativar_rainbow = st.sidebar.checkbox("🌈 Arco-íris Dinâmico (Cores Rotativas)")
ativar_neon    = st.sidebar.checkbox("💡 Brilho Neon (Glow Intenso)")
ativar_particulas = st.sidebar.checkbox("⭐ Partículas Orbitais")
ativar_trail   = st.sidebar.checkbox("🌊 Rastro de Movimento (Motion Blur)")
ativar_sombra  = st.sidebar.checkbox("🌑 Sombra Dinâmica Projetada")
ativar_aberracao = st.sidebar.checkbox("📺 Aberração Cromática (RGB Split)")
ativar_scanlines = st.sidebar.checkbox("📟 Scanlines Retrô")
ativar_vinheta = st.sidebar.checkbox("🎞️ Vinheta Cinematográfica")
ativar_pulse_borda = st.sidebar.checkbox("⚡ Pulso de Borda (Border Pulse)")

if ativar_rainbow:
    velocidade_rainbow = st.sidebar.slider("Velocidade do Arco-íris:", 0.5, 3.0, 1.0, 0.1)
else:
    velocidade_rainbow = 1.0

if ativar_particulas:
    num_particulas = st.sidebar.slider("Número de Partículas:", 5, 50, 15, 5)
else:
    num_particulas = 15

st.sidebar.subheader("🔥 Efeitos NOVOS — Upgrade 3.0")

ativar_glow_pulsante = st.sidebar.checkbox("💥 Glow Pulsante (Neon Respiração)")
ativar_flicker       = st.sidebar.checkbox("🕯️ Flicker (Cintilação Cinematográfica)")
ativar_lightning     = st.sidebar.checkbox("⚡ Lightning (Relâmpagos)")
ativar_glitch_digital = st.sidebar.checkbox("👾 Glitch Digital (Distorção Pixel)")
ativar_heatwave      = st.sidebar.checkbox("🌊 Heatwave (Distorção de Calor)")
ativar_hologram      = st.sidebar.checkbox("🔵 Hologram (Linhas de Varredura + Cor)")
ativar_chromatic_flicker = st.sidebar.checkbox("🎨 Chromatic Flicker (RGB Trêmulo)")
ativar_dust_particles    = st.sidebar.checkbox("✨ Poeira Cósmica (Dust Particles)")
ativar_shockwave         = st.sidebar.checkbox("💫 Shockwave (Onda de Choque)")

if ativar_glow_pulsante:
    intensidade_glow = st.sidebar.slider("Intensidade do Glow:", 1.0, 5.0, 2.5, 0.5)
else:
    intensidade_glow = 2.5

if ativar_lightning:
    num_raios = st.sidebar.slider("Número de Raios:", 1, 6, 2, 1)
else:
    num_raios = 2

if ativar_glitch_digital:
    intensidade_glitch = st.sidebar.slider("Intensidade do Glitch:", 1, 10, 4, 1)
else:
    intensidade_glitch = 4

if ativar_dust_particles:
    num_dust = st.sidebar.slider("Quantidade de Poeira:", 20, 100, 40, 10)
else:
    num_dust = 40

# ============================================================================
# 5. PALETAS DE CORES
# ============================================================================
st.sidebar.subheader("🎨 Paletas de Cores")

paleta_escolhida = st.sidebar.selectbox(
    "Esquema de Cores:",
    [
        "Personalizado (Escolha Livre)",
        "Cyberpunk (Roxo/Rosa/Azul)",
        "Sunset (Laranja/Rosa/Roxo)",
        "Ocean (Azul/Verde/Ciano)",
        "Fire (Vermelho/Laranja/Amarelo)",
        "Neon Tokyo (Rosa/Azul/Verde)",
        "Pastel Dream (Tons Suaves)",
        "Monochrome (Preto e Branco)",
        "Tropical (Verde/Amarelo/Rosa)",
        "Galaxy (Roxo/Azul/Magenta)",
        "🆕 Acid Green (Verde Radioativo)",
        "🆕 Blood Moon (Vermelho/Preto)",
    ]
)

PALETAS = {
    "Cyberpunk (Roxo/Rosa/Azul)":        ["#8B00FF", "#FF00FF", "#00FFFF", "#FF1493"],
    "Sunset (Laranja/Rosa/Roxo)":         ["#FF6B35", "#FF8C42", "#FFA07A", "#FF69B4", "#9B59B6"],
    "Ocean (Azul/Verde/Ciano)":           ["#006994", "#0099CC", "#00CCCC", "#00FFB2", "#4ECDC4"],
    "Fire (Vermelho/Laranja/Amarelo)":    ["#FF0000", "#FF4500", "#FF6347", "#FF8C00", "#FFD700"],
    "Neon Tokyo (Rosa/Azul/Verde)":       ["#FF006E", "#FB5607", "#FFBE0B", "#8338EC", "#3A86FF"],
    "Pastel Dream (Tons Suaves)":         ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"],
    "Monochrome (Preto e Branco)":        ["#FFFFFF", "#CCCCCC", "#999999", "#666666", "#333333"],
    "Tropical (Verde/Amarelo/Rosa)":      ["#06FFA5", "#FFFB00", "#FF006E", "#00D9FF", "#8B00FF"],
    "Galaxy (Roxo/Azul/Magenta)":         ["#4A00E0", "#8E2DE2", "#DA22FF", "#9733EE", "#5B247A"],
    "🆕 Acid Green (Verde Radioativo)":   ["#00FF00", "#39FF14", "#7FFF00", "#ADFF2F", "#00FF7F"],
    "🆕 Blood Moon (Vermelho/Preto)":     ["#FF0000", "#CC0000", "#880000", "#FF4444", "#FF0033"],
}

# ============================================================================
# 6. ENTRADA DE CONTEÚDO 
# ============================================================================
st.header("🎮 Conteúdo para Animar")

tipo_entrada = st.radio(
    "Tipo de elemento:", 
    [
        "✍️ Texto Personalizado", 
        "🖼️ Imagem Única (Com Prévia)", 
        "🖼️ Múltiplas Imagens (Lote)"
    ]
)

if tipo_fundo == "Totalmente Transparente":
    bg_color = (0, 0, 0, 0)
else:
    hex_cor = cor_fundo_primaria.lstrip('#')
    bg_color = tuple(int(hex_cor[i:i+2], 16) for i in (0, 2, 4)) + (255,)

duracao_frame = int(1000 / velocidade_fps)

# ============================================================================
# 7. FUNÇÕES AUXILIARES MATRICIAIS
# ============================================================================
def hex_para_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def criar_fundo_gradiente(largura, altura, tipo, cor1, cor2, frame_atual, total_frames):
    img_array = np.zeros((altura, largura, 4), dtype=np.uint8)
    progresso = frame_atual / total_frames
    angulo = progresso * 2 * math.pi

    if tipo == "Gradiente Radial Dinâmico":
        centro_x, centro_y = largura // 2, altura // 2
        raio_max = math.sqrt(centro_x**2 + centro_y**2)
        offset_x = int(math.cos(angulo) * largura * 0.1)
        offset_y = int(math.sin(angulo) * altura * 0.1)
        for y in range(altura):
            for x in range(largura):
                dx = x - (centro_x + offset_x)
                dy = y - (centro_y + offset_y)
                distancia = math.sqrt(dx*dx + dy*dy)
                t = min(distancia / raio_max, 1.0)
                r = int(cor1[0] * (1-t) + cor2[0] * t)
                g = int(cor1[1] * (1-t) + cor2[1] * t)
                b = int(cor1[2] * (1-t) + cor2[2] * t)
                img_array[y, x] = [r, g, b, 255]

    elif tipo == "Gradiente Linear Animado":
        for y in range(altura):
            t = y / altura
            t = (t + math.sin(angulo) * 0.2) % 1.0
            r = int(cor1[0] * (1-t) + cor2[0] * t)
            g = int(cor1[1] * (1-t) + cor2[1] * t)
            b = int(cor1[2] * (1-t) + cor2[2] * t)
            img_array[y, :] = [r, g, b, 255]

    elif tipo == "Padrão de Ruído (Noise)":
        for y in range(altura):
            for x in range(largura):
                noise_val = (math.sin(x * 0.01 + angulo) * math.cos(y * 0.01 + angulo) * 0.5 + 0.5)
                r = int(cor1[0] * (1-noise_val) + cor2[0] * noise_val)
                g = int(cor1[1] * (1-noise_val) + cor2[1] * noise_val)
                b = int(cor1[2] * (1-noise_val) + cor2[2] * noise_val)
                img_array[y, x] = [r, g, b, 255]

    elif "Estelar" in tipo:
        img_array[:, :] = [5, 5, 20, 255]
        rng = np.random.default_rng(seed=42)
        num_estrelas = 200
        xs = rng.integers(0, largura, num_estrelas)
        ys = rng.integers(0, altura, num_estrelas)
        brilhos = rng.integers(150, 255, num_estrelas)
        for idx in range(num_estrelas):
            fase = (progresso * 2 * math.pi + idx * 0.3) % (2 * math.pi)
            alpha_e = int(brilhos[idx] * (0.5 + 0.5 * math.sin(fase)))
            alpha_e = max(0, min(255, alpha_e))
            img_array[ys[idx], xs[idx]] = [alpha_e, alpha_e, alpha_e, 255]
        for y in range(0, altura, 4):
            for x in range(0, largura, 4):
                n = math.sin(x * 0.008 + angulo) * math.cos(y * 0.008 + angulo * 0.7)
                if n > 0.3:
                    intensity = int((n - 0.3) * 100)
                    img_array[y:y+4, x:x+4] = [
                        min(255, img_array[y, x, 0] + intensity // 3),
                        min(255, img_array[y, x, 1] + intensity // 2),
                        min(255, img_array[y, x, 2] + intensity),
                        255
                    ]

    elif "Plasma" in tipo:
        for y in range(altura):
            for x in range(largura):
                v = math.sin(x * 0.02 + angulo)
                v += math.sin(y * 0.02 + angulo * 1.3)
                v += math.sin((x + y) * 0.01 + angulo * 0.7)
                v += math.sin(math.sqrt((x - largura/2)**2 + (y - altura/2)**2) * 0.03 + angulo)
                v = (v + 4) / 8
                h = v
                sat = 1.0
                val = 0.7 + v * 0.3
                r, g, b = colorsys.hsv_to_rgb(h, sat, val)
                img_array[y, x] = [int(r*255), int(g*255), int(b*255), 255]

    return Image.fromarray(img_array, mode='RGBA')

def desenhar_lightning(draw, x1, y1, x2, y2, cor, profundidade=4):
    if profundidade == 0:
        draw.line([(x1, y1), (x2, y2)], fill=cor + (200,), width=2)
        return
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    dx = x2 - x1
    dy = y2 - y1
    comprimento = math.sqrt(dx*dx + dy*dy) if (dx*dx + dy*dy) > 0 else 1
    perp_x = -dy / comprimento
    perp_y = dx / comprimento
    desvio = random.gauss(0, comprimento * 0.25)
    mx += perp_x * desvio
    my += perp_y * desvio
    desenhar_lightning(draw, x1, y1, mx, my, cor, profundidade - 1)
    desenhar_lightning(draw, mx, my, x2, y2, cor, profundidade - 1)

def aplicar_heatwave(img, intensidade, frame_idx):
    arr = np.array(img)
    altura, largura = arr.shape[:2]
    resultado = arr.copy()
    for y in range(altura):
        deslocamento = int(intensidade * math.sin(y * 0.05 + frame_idx * 0.3))
        if deslocamento > 0:
            resultado[y, deslocamento:, :] = arr[y, :largura-deslocamento, :]
            resultado[y, :deslocamento, :] = arr[y, 0:1, :]
        elif deslocamento < 0:
            resultado[y, :largura+deslocamento, :] = arr[y, -deslocamento:, :]
            resultado[y, largura+deslocamento:, :] = arr[y, -1:, :]
    return Image.fromarray(resultado, mode=img.mode)

def aplicar_hologram(frame, progresso, cor_holo=(0, 200, 255)):
    largura, altura = frame.size
    overlay = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    espaco = 4
    offset_scan = int(progresso * altura * 2) % espaco
    for y in range(offset_scan, altura, espaco):
        alpha_linha = random.randint(20, 60)
        draw.line([(0, y), (largura, y)], fill=cor_holo + (alpha_linha,))
    y_scan = int((math.sin(progresso * 2 * math.pi) * 0.5 + 0.5) * altura)
    for dy in range(-3, 4):
        if 0 <= y_scan + dy < altura:
            alpha = max(0, 120 - abs(dy) * 30)
            draw.line([(0, y_scan + dy), (largura, y_scan + dy)], fill=cor_holo + (alpha,))
    tint = Image.new("RGBA", (largura, altura), cor_holo + (25,))
    frame = Image.alpha_composite(frame, tint)
    frame = Image.alpha_composite(frame, overlay)
    return frame

def aplicar_glitch_digital(img, intensidade, seed):
    arr = np.array(img)
    altura, largura = arr.shape[:2]
    resultado = arr.copy()
    rng = random.Random(seed)
    num_blocos = intensidade * 3
    for _ in range(num_blocos):
        y_inicio = rng.randint(0, altura - 1)
        altura_bloco = rng.randint(2, max(3, altura // 20))
        y_fim = min(y_inicio + altura_bloco, altura)
        desloc = rng.randint(-largura // 8, largura // 8)
        if desloc > 0:
            resultado[y_inicio:y_fim, desloc:, :] = arr[y_inicio:y_fim, :largura-desloc, :]
            resultado[y_inicio:y_fim, :desloc, :] = arr[y_inicio:y_fim, 0:1, :]
        elif desloc < 0:
            resultado[y_inicio:y_fim, :largura+desloc, :] = arr[y_inicio:y_fim, -desloc:, :]
            resultado[y_inicio:y_fim, largura+desloc:, :] = arr[y_inicio:y_fim, -1:, :]
        if rng.random() > 0.7:
            resultado[y_inicio:y_fim, :, :3] = 255 - resultado[y_inicio:y_fim, :, :3]
    return Image.fromarray(resultado, mode=img.mode)

def aplicar_glow_pulsante(frame, progresso, intensidade_glow):
    pulso = 0.5 + 0.5 * math.sin(progresso * 2 * math.pi)
    fator = 0.5 + pulso * (intensidade_glow - 0.5)
    canvas = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    raios = [5, 12, 25, 40]
    alphas = [0.6, 0.4, 0.25, 0.15]
    for raio, alpha_mult in zip(raios, alphas):
        camada = frame.filter(ImageFilter.GaussianBlur(radius=raio * fator))
        enhancer = ImageEnhance.Brightness(camada)
        camada = enhancer.enhance(1.0 + fator * 0.5)
        enhancer_c = ImageEnhance.Color(camada)
        camada = enhancer_c.enhance(1.5 + fator * 0.5)
        dados = list(camada.getdata())
        dados_mod = [(r, g, b, min(255, int(a * alpha_mult))) for r, g, b, a in dados]
        camada.putdata(dados_mod)
        canvas = Image.alpha_composite(canvas, camada)
    canvas = Image.alpha_composite(canvas, frame)
    return canvas

def aplicar_dust_particles(frame, progresso, num_dust, seed_base):
    draw = ImageDraw.Draw(frame)
    largura, altura = frame.size
    for i in range(num_dust):
        rng = random.Random(seed_base + i * 137)
        base_x = rng.uniform(0, largura)
        base_y = rng.uniform(0, altura)
        fase_x = rng.uniform(0, 2 * math.pi)
        fase_y = rng.uniform(0, 2 * math.pi)
        vel_x = rng.uniform(0.3, 1.5)
        vel_y = rng.uniform(0.3, 1.5)
        amp = rng.uniform(5, 30)
        px = (base_x + math.sin(progresso * 2 * math.pi * vel_x + fase_x) * amp) % largura
        py = (base_y + math.cos(progresso * 2 * math.pi * vel_y + fase_y) * amp * 0.5) % altura
        tamanho = rng.uniform(0.5, 2.5)
        brilho = int(rng.uniform(100, 220) * (0.5 + 0.5 * math.sin(progresso * 2 * math.pi * 2 + i)))
        r = brilho
        g = brilho
        b = min(255, brilho + rng.randint(0, 50))
        alpha = int(brilho * 0.8)
        draw.ellipse([px - tamanho, py - tamanho, px + tamanho, py + tamanho], fill=(r, g, b, alpha))
    return frame

def aplicar_shockwave(frame, progresso):
    arr = np.array(frame, dtype=np.float32)
    altura, largura = arr.shape[:2]
    resultado = arr.copy()
    centro_x = largura / 2
    centro_y = altura / 2
    raio_onda = progresso * math.sqrt(centro_x**2 + centro_y**2) * 1.5
    espessura = 40
    for y in range(altura):
        for x in range(largura):
            dx = x - centro_x
            dy = y - centro_y
            dist = math.sqrt(dx*dx + dy*dy)
            diff = dist - raio_onda
            if abs(diff) < espessura:
                fator_desl = math.exp(-(diff**2) / (2 * (espessura/3)**2))
                desl = int(fator_desl * 10)
                if dist > 0:
                    nx = int(x + (dx / dist) * desl)
                    ny = int(y + (dy / dist) * desl)
                    nx = max(0, min(largura - 1, nx))
                    ny = max(0, min(altura - 1, ny))
                    resultado[y, x] = arr[ny, nx]
    return Image.fromarray(resultado.astype(np.uint8), mode=frame.mode)


# ============================================================================
# 9. GESTÃO DE DADOS COM TEXTO MATEMÁTICO ABSOLUTO
# ============================================================================
itens_para_processar = []

if tipo_entrada == "✍️ Texto Personalizado":
    # Uso do st.text_area permite que você use o ENTER livremente
    texto_input = st.text_area("Digite a frase (Use Enter se quiser pular linha):", value="SUPER\nOFERTA")
    
    # OPÇÃO DE DESTRUIÇÃO DE ESPAÇOS: Transforma frases horizontais em verticais automaticamente
    empilhar_palavras = st.checkbox("↕️ Empilhar Palavras (Força a quebra de linha em cada espaço)", value=True)
    
    cor_texto = st.color_picker("Cor base do texto:", "#00FF88")
    ativar_outline = st.checkbox("🔲 Adicionar Contorno no Texto")

    if ativar_outline:
        cor_outline = st.color_picker("Cor do Contorno:", "#000000")
        espessura_outline = st.slider("Espessura do Contorno:", 1, 10, 3)

    if texto_input:
        # PREPARAÇÃO MATRICIAL: Converte a string baseada na sua escolha
        if empilhar_palavras:
            texto_final = texto_input.replace(" ", "\n")
        else:
            texto_final = texto_input
            
        # Filtra linhas vazias geradas por excesso de espaços ou enters duplos
        linhas = [linha for linha in texto_final.split('\n') if linha.strip()]
        if not linhas:
            linhas = ["Vazio"]

        largura_alvo = int(tamanho_saida * 0.82)
        altura_alvo = int(tamanho_saida * 0.82)
        
        # Objeto temporário apenas para medir
        img_temp = Image.new("RGBA", (10, 10))
        draw_temp = ImageDraw.Draw(img_temp)
        font_final = None
        tamanho_fonte = 24

        # ENGINE DE DESCOBERTA DE ESCALA: Calcula a maior fonte que comporta TODAS as linhas juntas
        for f_size in range(24, 500, 4):
            font_teste = None
            for f_nome in ["Ubuntu-Bold.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial.ttf", "Helvetica.ttf"]:
                try:
                    font_teste = ImageFont.truetype(f_nome, f_size)
                    break
                except IOError:
                    continue
            if font_teste is None:
                try:
                    if not os.path.exists("Ubuntu-Bold.ttf"):
                        urllib.request.urlretrieve("https://github.com/google/fonts/raw/main/ofl/ubuntu/Ubuntu-Bold.ttf", "Ubuntu-Bold.ttf")
                    font_teste = ImageFont.truetype("Ubuntu-Bold.ttf", f_size)
                except Exception:
                    try: font_teste = ImageFont.load_default(size=f_size)
                    except TypeError: font_teste = ImageFont.load_default()

            max_w = 0
            total_h = 0
            espacamento = f_size * 0.15  # Gap de 15% entre as linhas empilhadas

            for linha in linhas:
                try:
                    bbox = draw_temp.textbbox((0, 0), linha, font=font_teste)
                    lw = bbox[2] - bbox[0]
                    lh = bbox[3] - bbox[1]
                except Exception:
                    lw, lh = font_teste.getsize(linha)
                
                if lw > max_w: max_w = lw
                total_h += lh + espacamento

            total_h -= espacamento # Tira o espaço extra da última linha

            # Se a altura total da pilha de blocos estourar o canvas, encerra a subida de tamanho
            if max_w > largura_alvo or total_h > altura_alvo:
                break
                
            font_final = font_teste
            tamanho_fonte = f_size

        if font_final is None:
            font_final = ImageFont.load_default()

        # RENDERIZAÇÃO MATEMÁTICA LINHA POR LINHA
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0, 0, 0, 0))
        draw_final = ImageDraw.Draw(base_image)

        total_h = 0
        alturas_linhas = []
        espacamento = tamanho_fonte * 0.15

        # Mede a altura exata do corpo da fonte final
        for linha in linhas:
            try:
                bbox = draw_final.textbbox((0, 0), linha, font=font_final)
                lh = bbox[3] - bbox[1]
            except Exception:
                _, lh = font_final.getsize(linha)
            alturas_linhas.append(lh)
            total_h += lh + espacamento
            
        total_h -= espacamento
        
        # Estabelece a origem Y (Topo do Bloco) para que fique no centro matemático do Canvas
        y_atual = (tamanho_saida - total_h) / 2

        # Pinta cada palavra individualmente recalculando o X
        for i, linha in enumerate(linhas):
            try:
                bbox = draw_final.textbbox((0, 0), linha, font=font_final)
                lw = bbox[2] - bbox[0]
            except Exception:
                lw, _ = font_final.getsize(linha)
            
            # Centraliza o X perfeitamente para ESTA palavra
            x_atual = (tamanho_saida - lw) / 2

            if ativar_outline:
                for offset_x in range(-espessura_outline, espessura_outline + 1):
                    for offset_y in range(-espessura_outline, espessura_outline + 1):
                        if offset_x != 0 or offset_y != 0:
                            draw_final.text((x_atual + offset_x, y_atual + offset_y), linha, fill=cor_outline, font=font_final)
            
            draw_final.text((x_atual, y_atual), linha, fill=cor_texto, font=font_final)
            
            y_atual += alturas_linhas[i] + espacamento
            
        itens_para_processar.append({"nome": "texto_animado.gif", "imagem": base_image})

elif tipo_entrada == "🖼️ Imagem Única (Com Prévia)":
    uploaded_file = st.file_uploader(
        "Envie uma imagem para renderização unitária:",
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Pré-visualização da Imagem Base", width=250)

        img_original = Image.open(uploaded_file).convert("RGBA")
        bbox = img_original.getbbox()
        if bbox: img_original = img_original.crop(bbox)

        largura_util, altura_util = img_original.size
        proporcao = min((tamanho_saida * 0.82) / largura_util, (tamanho_saida * 0.82) / altura_util)
        nova_l = int(largura_util * proporcao)
        nova_a = int(altura_util * proporcao)

        img_redimensionada = img_original.resize((nova_l, nova_a), Image.Resampling.LANCZOS)
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0, 0, 0, 0))
        offset_x = (tamanho_saida - nova_l) // 2
        offset_y = (tamanho_saida - nova_a) // 2
        base_image.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)
        
        itens_para_processar.append({"nome": uploaded_file.name, "imagem": base_image})

elif tipo_entrada == "🖼️ Múltiplas Imagens (Lote)":
    uploaded_files = st.file_uploader(
        "Envie duas ou mais imagens (Lote):",
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uf in uploaded_files:
            img_original = Image.open(uf).convert("RGBA")
            bbox = img_original.getbbox()
            if bbox: img_original = img_original.crop(bbox)

            largura_util, altura_util = img_original.size
            proporcao = min((tamanho_saida * 0.82) / largura_util, (tamanho_saida * 0.82) / altura_util)
            nova_l = int(largura_util * proporcao)
            nova_a = int(altura_util * proporcao)

            img_redimensionada = img_original.resize((nova_l, nova_a), Image.Resampling.LANCZOS)
            base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0, 0, 0, 0))
            offset_x = (tamanho_saida - nova_l) // 2
            offset_y = (tamanho_saida - nova_a) // 2
            base_image.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)
            
            itens_para_processar.append({"nome": uf.name, "imagem": base_image})

# ============================================================================
# 11. PROCESSAMENTO E GERAÇÃO DOS FRAMES
# ============================================================================
if itens_para_processar:
    st.write(f"⚙️ Renderizando {len(itens_para_processar)} animação(ões) premium...")
    
    gifs_processados = {}
    barra_prog_lote = st.progress(0)

    cores_paleta = []
    paleta_key = paleta_escolhida.replace("🆕 ", "")
    if paleta_key in PALETAS:
        cores_paleta = [hex_para_rgb(cor) for cor in PALETAS[paleta_key]]

    for idx, item in enumerate(itens_para_processar):
        nome_arquivo = item["nome"]
        base_img_atual = item["imagem"]
        largura_orig, altura_orig = base_img_atual.size
        frames = []
        
        st.write(f"⏳ Processando matriz: `{nome_arquivo}` ({idx+1}/{len(itens_para_processar)})")

        for i in range(num_frames_total):
            progresso = i / num_frames_total
            angulo_rad = progresso * 2 * math.pi

            elemento_frame = base_img_atual.copy()

            if ativar_rainbow:
                if tipo_entrada == "✍️ Texto Personalizado":
                    r = int(math.sin(progresso * 2 * math.pi * velocidade_rainbow + 0) * 127 + 128)
                    g = int(math.sin(progresso * 2 * math.pi * velocidade_rainbow + 2) * 127 + 128)
                    b = int(math.sin(progresso * 2 * math.pi * velocidade_rainbow + 4) * 127 + 128)
                    dados = elemento_frame.getdata()
                    novos_dados = [(r, g, b, item_px[3]) if item_px[3] > 0 else item_px for item_px in dados]
                    elemento_frame.putdata(novos_dados)
                else:
                    if cores_paleta:
                        idx_cor = int(progresso * len(cores_paleta)) % len(cores_paleta)
                        cor_tint = cores_paleta[idx_cor]
                        dados = elemento_frame.getdata()
                        novos_dados = []
                        for item_px in dados:
                            if item_px[3] > 0:
                                novos_dados.append((
                                    int(item_px[0] * cor_tint[0] / 255),
                                    int(item_px[1] * cor_tint[1] / 255),
                                    int(item_px[2] * cor_tint[2] / 255),
                                    item_px[3]
                                ))
                            else:
                                novos_dados.append(item_px)
                        elemento_frame.putdata(novos_dados)

            frame_final = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
            shift_x, shift_y = 0, 0
            aplicar_rotacao = False
            angulo_rotacao = 0

            efeito_limpo = combo_efeito.replace("🆕 ", "")

            if efeito_limpo in ["Rotação Infinita", "Rotação + Pulsar (Clássico)", "Tornado Cósmico (Multi-Efeito)"]:
                aplicar_rotacao = True
                angulo_rotacao = -(progresso * 360 * intensidade_movimento)
            elif efeito_limpo == "Espiral Hipnótica":
                aplicar_rotacao = True
                angulo_rotacao = -(progresso**2 * 720 * intensidade_movimento)

            if aplicar_rotacao:
                elemento_frame = elemento_frame.rotate(angulo_rotacao, resample=Image.BICUBIC, expand=False)

            if efeito_limpo in ["Pulsar Suave (Respiração)", "Rotação + Pulsar (Clássico)", "Tornado Cósmico (Multi-Efeito)"]:
                fator_escala = 1.0 + (math.sin(angulo_rad) * 0.15 * intensidade_movimento)
                nl = max(10, int(largura_orig * fator_escala))
                na = max(10, int(altura_orig * fator_escala))
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

            elif efeito_limpo == "Gelatina Elástica (Squash & Stretch)":
                fator_x = 1.0 + (math.sin(angulo_rad) * 0.25 * intensidade_movimento)
                fator_y = 1.0 - (math.sin(angulo_rad) * 0.25 * intensidade_movimento)
                nl = max(10, int(largura_orig * fator_x))
                na = max(10, int(altura_orig * fator_y))
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

            elif efeito_limpo == "Onda Senoidal (Wave)":
                amplitude = tamanho_saida * 0.15 * intensidade_movimento
                shift_x = int(math.sin(angulo_rad) * amplitude)
                shift_y = int(math.cos(angulo_rad) * amplitude * 0.5)

            elif efeito_limpo == "Quicar (Bounce Physics)":
                altura_pulo = abs(math.sin(angulo_rad)) * (tamanho_saida * 0.25 * intensidade_movimento)
                shift_y = -int(altura_pulo)
                if abs(math.sin(angulo_rad)) < 0.1:
                    nl = max(10, int(largura_orig * 1.2))
                    na = max(10, int(altura_orig * 0.8))
                    elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

            elif efeito_limpo == "Tremor Caótico (Glitch)":
                intensidade_shake = int(15 * intensidade_movimento)
                shift_x = random.randint(-intensidade_shake, intensidade_shake)
                shift_y = random.randint(-intensidade_shake, intensidade_shake)
                angulo_shake = random.uniform(-5, 5) * intensidade_movimento
                elemento_frame = elemento_frame.rotate(angulo_shake, resample=Image.BICUBIC)

            elif efeito_limpo == "Explosão e Implosão":
                fator = (1.0 + (progresso * 2) * 0.5 * intensidade_movimento) if progresso < 0.5 else (1.5 - ((progresso - 0.5) * 2) * 0.5 * intensidade_movimento)
                nl = max(10, int(largura_orig * fator))
                na = max(10, int(altura_orig * fator))
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

            elif efeito_limpo == "Balanço de Pêndulo":
                angulo_pendulo = math.sin(angulo_rad) * 45 * intensidade_movimento
                elemento_frame = elemento_frame.rotate(angulo_pendulo, resample=Image.BICUBIC)

            elif efeito_limpo == "Zoom In/Out Dramático":
                fator = 0.5 + abs(math.sin(angulo_rad)) * intensidade_movimento
                nl = max(10, int(largura_orig * fator))
                na = max(10, int(altura_orig * fator))
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

            elif efeito_limpo == "Flutuação 3D (Float)":
                amplitude = tamanho_saida * 0.1 * intensidade_movimento
                shift_x = int(math.sin(angulo_rad) * amplitude)
                shift_y = int(math.sin(angulo_rad * 2) * amplitude * 0.5)
                fator = 1.0 + math.sin(angulo_rad * 2) * 0.05 * intensidade_movimento
                nl = max(10, int(largura_orig * fator))
                na = max(10, int(altura_orig * fator))
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

            elif efeito_limpo == "Vibração Elétrica":
                freq = 6
                desl = int(math.sin(angulo_rad * freq * math.pi) * 8 * intensidade_movimento)
                shift_x = desl + random.randint(-2, 2)
                shift_y = int(math.cos(angulo_rad * freq * math.pi) * 4 * intensidade_movimento)
                ang_micro = math.sin(angulo_rad * freq) * 3 * intensidade_movimento
                elemento_frame = elemento_frame.rotate(ang_micro, resample=Image.BICUBIC)

            elif efeito_limpo == "Órbita Dupla":
                raio1 = tamanho_saida * 0.12 * intensidade_movimento
                raio2 = tamanho_saida * 0.05 * intensidade_movimento
                shift_x = int(math.cos(angulo_rad) * raio1 + math.cos(angulo_rad * 3) * raio2)
                shift_y = int(math.sin(angulo_rad) * raio1 + math.sin(angulo_rad * 3) * raio2)

            elif efeito_limpo == "Bounce Realista (Quique + Squash)":
                freq_bounce = 3
                t_norm = (progresso * freq_bounce * math.pi) % math.pi
                altura_quique = abs(math.sin(t_norm)) ** 0.7
                fator_squash_h = 1.0 + (1.0 - altura_quique) * 0.35 * intensidade_movimento
                fator_squash_v = 1.0 - (1.0 - altura_quique) * 0.25 * intensidade_movimento
                fator_stretch_h = 1.0 - altura_quique * 0.12 * intensidade_movimento
                fator_stretch_v = 1.0 + altura_quique * 0.15 * intensidade_movimento
                fator_h = fator_squash_h * fator_stretch_h
                fator_v = fator_squash_v * fator_stretch_v
                nl = max(10, int(largura_orig * fator_h))
                na = max(10, int(altura_orig * fator_v))
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)
                margem_chao = int(altura_orig * 0.05)
                y_chao = altura_orig - margem_chao - na
                amplitude_max = max(0, y_chao - int(altura_orig * 0.05))
                oy_bounce = y_chao - int(altura_quique * amplitude_max * intensidade_movimento)
                oy_bounce = max(int(altura_orig * 0.03), oy_bounce)
                shift_y = oy_bounce - ((altura_orig - na) // 2)

            elif efeito_limpo == "Rotação Cinematográfica":
                voltas = 3
                graus_totais = voltas * 360
                t = progresso
                if t < 0.5: t_ease = 4 * t * t * t
                else: t_ease = 1 - ((-2 * t + 2) ** 3) / 2
                angulo_rotacao_cin = -(t_ease * graus_totais * intensidade_movimento)
                elemento_frame = elemento_frame.rotate(angulo_rotacao_cin, resample=Image.BICUBIC, expand=False)
                velocidade_instantanea = abs(math.sin(progresso * math.pi))
                fator_zoom = 1.0 + velocidade_instantanea * 0.08 * intensidade_movimento
                nl = max(10, int(largura_orig * fator_zoom))
                na = max(10, int(altura_orig * fator_zoom))
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

            elif efeito_limpo == "Zoom Dramático In/Out Elástico":
                if progresso < 0.40:
                    t = progresso / 0.40
                    fator = 0.3 + (t * t * t) * 0.7
                elif progresso < 0.60:
                    t = (progresso - 0.40) / 0.20
                    fator = 1.0 + math.sin(t * math.pi) * 0.5
                elif progresso < 0.80:
                    t = (progresso - 0.60) / 0.20
                    fator = 1.0 - math.sin(t * math.pi) * 0.20
                else:
                    t = (progresso - 0.80) / 0.20
                    amplitude_mola = math.exp(-t * 4) * 0.10
                    fator = 1.0 + amplitude_mola * math.sin(t * math.pi * 6)
                fator *= intensidade_movimento * 0.7 + 0.3
                nl = max(10, int(largura_orig * fator))
                na = max(10, int(altura_orig * fator))
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

            nl, na = elemento_frame.size
            ox = (largura_orig - nl) // 2 + shift_x
            oy = (altura_orig - na) // 2 + shift_y
            frame_final.paste(elemento_frame, (ox, oy), elemento_frame)

            if ativar_sombra:
                sombra = Image.new("RGBA", elemento_frame.size, (0, 0, 0, 0))
                dados_sombra = [(0, 0, 0, item_px[3]) for item_px in elemento_frame.getdata()]
                sombra.putdata(dados_sombra)
                sombra = sombra.filter(ImageFilter.GaussianBlur(radius=15))
                offset_sx = int(math.cos(angulo_rad) * 20)
                offset_sy = int(math.sin(angulo_rad) * 20) + 30
                frame_com_sombra = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
                frame_com_sombra.paste(sombra, (ox + offset_sx, oy + offset_sy), sombra)
                frame_com_sombra.paste(frame_final, (0, 0), frame_final)
                frame_final = frame_com_sombra

            if ativar_particulas:
                draw_p = ImageDraw.Draw(frame_final)
                cx = largura_orig // 2
                cy = altura_orig // 2
                for p in range(num_particulas):
                    ang_p = (p / num_particulas) * 2 * math.pi + angulo_rad
                    raio_p = (tamanho_saida * 0.35) + math.sin(angulo_rad + p) * 30
                    px = cx + int(math.cos(ang_p) * raio_p)
                    py = cy + int(math.sin(ang_p) * raio_p)
                    tam_p = 3 + int(abs(math.sin(angulo_rad + p)) * 5)
                    if cores_paleta: cor_p = cores_paleta[p % len(cores_paleta)]
                    else:
                        hue = (p / num_particulas + progresso) % 1.0
                        cor_p = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0))
                    draw_p.ellipse([px - tam_p, py - tam_p, px + tam_p, py + tam_p], fill=cor_p + (200,))

            if ativar_trail and i > 0:
                frame_final = Image.blend(frames[-1].copy(), frame_final, alpha=0.7)

            if ativar_neon:
                brilho = frame_final.filter(ImageFilter.GaussianBlur(radius=20))
                brilho = ImageEnhance.Brightness(brilho).enhance(1.5)
                brilho = ImageEnhance.Color(brilho).enhance(2.0)
                canvas_neon = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
                canvas_neon.paste(brilho, (0, 0), brilho)
                canvas_neon.paste(frame_final, (0, 0), frame_final)
                frame_final = canvas_neon

            if ativar_aberracao:
                r_ch, g_ch, b_ch, a_ch = frame_final.split()
                offset_aberr = int(3 * intensidade_movimento)
                r_ch = ImageChops.offset(r_ch, offset_aberr, 0)
                b_ch = ImageChops.offset(b_ch, -offset_aberr, 0)
                frame_final = Image.merge("RGBA", (r_ch, g_ch, b_ch, a_ch))

            if ativar_pulse_borda:
                draw_b = ImageDraw.Draw(frame_final)
                esp_borda = int(5 + abs(math.sin(angulo_rad)) * 10)
                if cores_paleta: cor_b = cores_paleta[int(progresso * len(cores_paleta)) % len(cores_paleta)]
                else: cor_b = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(progresso, 1.0, 1.0))
                for t in range(esp_borda):
                    draw_b.rectangle([t, t, largura_orig - t - 1, altura_orig - t - 1], outline=cor_b + (150,))

            if efeito_limpo == "Tornado Cósmico (Multi-Efeito)":
                fator_b = 1.0 + (math.sin(angulo_rad * 2) * 0.3)
                frame_final = ImageEnhance.Brightness(frame_final).enhance(fator_b)
                if not ativar_rainbow:
                    dados = frame_final.getdata()
                    novos_dados = []
                    for item_px in dados:
                        if item_px[3] > 0:
                            h, s, v = colorsys.rgb_to_hsv(item_px[0]/255, item_px[1]/255, item_px[2]/255)
                            r_v, g_v, b_v = colorsys.hsv_to_rgb((h + progresso) % 1.0, s, v)
                            novos_dados.append((int(r_v*255), int(g_v*255), int(b_v*255), item_px[3]))
                        else: novos_dados.append(item_px)
                    frame_final.putdata(novos_dados)

            if ativar_scanlines:
                overlay_scan = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
                draw_scan = ImageDraw.Draw(overlay_scan)
                for y in range(0, altura_orig, 3):
                    draw_scan.line([(0, y), (largura_orig, y)], fill=(0, 0, 0, 50))
                frame_final = Image.alpha_composite(frame_final, overlay_scan)

            if ativar_vinheta:
                vinheta = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
                draw_v = ImageDraw.Draw(vinheta)
                cx_v, cy_v = largura_orig // 2, altura_orig // 2
                raio_max_v = math.sqrt(cx_v**2 + cy_v**2)
                for c in range(50):
                    raio_v = (c / 50) * raio_max_v * 1.2
                    draw_v.ellipse([cx_v - raio_v, cy_v - raio_v, cx_v + raio_v, cy_v + raio_v], fill=(0, 0, 0, int((c / 50) * 180)))
                frame_final = Image.alpha_composite(frame_final, vinheta)

            if ativar_glow_pulsante: frame_final = aplicar_glow_pulsante(frame_final, progresso, intensidade_glow)
            if ativar_flicker:
                rng_f = random.Random(i * 91 + 7)
                if progresso < 0.35:
                    fator_f = 0.90 + math.sin(progresso * 2 * math.pi * 1.5) * 0.10
                    if rng_f.random() > 0.95: fator_f = rng_f.uniform(0.4, 0.65)
                elif progresso < 0.65:
                    t_fase = (progresso - 0.35) / 0.30
                    fator_f = 0.80 + math.sin(progresso * 2 * math.pi * (2.0 + t_fase * 6.0)) * 0.20
                    if rng_f.random() > (1.0 - (0.05 + t_fase * 0.20)):
                        fator_f = rng_f.uniform(0.2, 0.5) if rng_f.random() > 0.5 else rng_f.uniform(1.2, 1.6)
                else:
                    fator_f = rng_f.uniform(1.3, 1.7) if i % 2 == 0 else rng_f.uniform(0.1, 0.4)
                    if i % 3 == 0: fator_f = rng_f.uniform(0.75, 0.95)
                frame_final = ImageEnhance.Brightness(frame_final).enhance(fator_f)
                intensidade_tremor = 1 + int(progresso * 3)
                if rng_f.random() > max(0.3, 0.8 - progresso * 0.7):
                    tremor_x = rng_f.randint(-intensidade_tremor, intensidade_tremor)
                    tremor_y = rng_f.randint(-max(1, intensidade_tremor // 2), max(1, intensidade_tremor // 2))
                    frame_temp = Image.new("RGBA", frame_final.size, (0, 0, 0, 0))
                    frame_temp.paste(frame_final, (tremor_x, tremor_y))
                    frame_final = frame_temp
                if progresso > 0.65 and i % 4 == 0:
                    frame_final = Image.alpha_composite(frame_final, Image.new("RGBA", frame_final.size, (255, 200, 100, 30)))

            if ativar_lightning:
                overlay_light = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
                draw_light = ImageDraw.Draw(overlay_light)
                cor_raios = [(255, 255, 255), (200, 200, 255), (255, 220, 100)]
                for r_idx in range(num_raios):
                    if (r_idx / num_raios + progresso * 2) % 1.0 < 0.15:
                        rng_r = random.Random(i * 100 + r_idx)
                        x_inicio = rng_r.randint(largura_orig // 4, 3 * largura_orig // 4)
                        cor_r = cor_raios[r_idx % len(cor_raios)]
                        for espessura in [6, 3, 1]:
                            desenhar_lightning(draw_light, x_inicio, 0, rng_r.randint(0, largura_orig), altura_orig, cor_r[:2] + (cor_r[2],), 3)
                frame_final = Image.alpha_composite(frame_final, overlay_light)

            if ativar_glitch_digital and random.Random(i * 777).random() > 0.5:
                frame_final = aplicar_glitch_digital(frame_final, intensidade_glitch, seed=i * 13 + 7)
            if ativar_heatwave: frame_final = aplicar_heatwave(frame_final, 4 * intensidade_movimento, i)
            if ativar_hologram:
                cor_h = cores_paleta[int(progresso * len(cores_paleta)) % len(cores_paleta)] if cores_paleta else (0, 200, 255)
                frame_final = aplicar_hologram(frame_final, progresso, cor_h)
            if ativar_chromatic_flicker:
                rng_cf = random.Random(i * 31)
                direcao = rng_cf.choice([-1, 1])
                r_ch, g_ch, b_ch, a_ch = frame_final.split()
                r_ch = ImageChops.offset(r_ch, rng_cf.randint(1, 6) * direcao, rng_cf.randint(-2, 2))
                b_ch = ImageChops.offset(b_ch, -rng_cf.randint(1, 6) * direcao, rng_cf.randint(-2, 2))
                if rng_cf.random() > 0.6: g_ch = ImageChops.offset(g_ch, rng_cf.randint(-2, 2), rng_cf.randint(-2, 2))
                frame_final = Image.merge("RGBA", (r_ch, g_ch, b_ch, a_ch))
            if ativar_dust_particles: frame_final = aplicar_dust_particles(frame_final, progresso, num_dust, seed_base=42)
            if ativar_shockwave: frame_final = aplicar_shockwave(frame_final, progresso)

            # COMPOSIÇÃO FINAL: Fundo + Frame
            cor1, cor2 = hex_para_rgb(cor_fundo_primaria), hex_para_rgb(cor_fundo_secundaria)
            if tipo_fundo in ["Gradiente Radial Dinâmico", "Gradiente Linear Animado", "Padrão de Ruído (Noise)", "🆕 Fundo Estelar (Stars)", "🆕 Plasma Psicodélico"]:
                canvas_fundo = criar_fundo_gradiente(largura_orig, altura_orig, tipo_fundo, cor1, cor2, i, num_frames_total)
            elif tipo_fundo == "Totalmente Transparente":
                canvas_fundo = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
            else:
                canvas_fundo = Image.new("RGBA", (largura_orig, altura_orig), bg_color)

            canvas_fundo.paste(frame_final, (0, 0), frame_final)
            frames.append(canvas_fundo)

        barra_prog_lote.progress((idx + 1) / len(itens_para_processar))

        gif_buffer = io.BytesIO()
        frames[0].save(
            gif_buffer,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=duracao_frame,
            loop=0,
            disposal=2,
            optimize=False
        )
        gifs_processados[nome_arquivo] = gif_buffer.getvalue()

    # ========================================================================
    # 12. EXIBIÇÃO E DOWNLOAD
    # ========================================================================
    st.success("✅ Processamento concluído com sucesso!")
    
    if len(gifs_processados) == 1:
        nome_arquivo, gif_bytes = list(gifs_processados.items())[0]
        st.subheader("🎬 Resultado Final Premium:")
        st.image(gif_bytes, width=tamanho_saida)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Resolução", f"{tamanho_saida}px")
        with col2: st.metric("Frames", f"{num_frames_total} @ {velocidade_fps}fps")
        with col3: st.metric("Tamanho", f"{len(gif_bytes)/1024:.1f} KB")

        st.download_button(
            label="📥 Baixar GIF Ultra Premium",
            data=gif_bytes,
            file_name=f"{nome_arquivo.rsplit('.', 1)[0]}_premium.gif",
            mime="image/gif",
            use_container_width=True
        )
    else:
        st.subheader("🎬 Prévia do Lote Gerado:")
        cols = st.columns(3)
        for i, (nome, gif_bytes) in enumerate(gifs_processados.items()):
            with cols[i % 3]:
                st.image(gif_bytes, caption=nome, use_container_width=True)
                
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for nome, gif_bytes in gifs_processados.items():
                nome_gif = f"{nome.rsplit('.', 1)[0]}_premium.gif"
                zip_file.writestr(nome_gif, gif_bytes)
                
        st.download_button(
            label=f"📥 Baixar Lote Completo ({len(gifs_processados)} GIFs) - Arquivo ZIP",
            data=zip_buffer.getvalue(),
            file_name="gifs_premium_lote.zip",
            mime="application/zip",
            use_container_width=True
        )

else:
    st.info("💡 Escolha uma opção e envie seu conteúdo acima para começar!")

# ============================================================================
# RODAPÉ
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>🎨 <b>Gerador de GIFs Ultra Premium</b> | <span style="color:#00ff88">Versão 3.4 — Engine Absoluta de Textos</span></p>
    <p>Processamento Inteligente • Previsão Integrada • Preservação Strict-Alpha RGBA</p>
</div>
""", unsafe_allow_html=True)
