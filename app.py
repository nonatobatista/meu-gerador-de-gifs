import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
import io
import math
import random

# 1. Configuração da página web
st.set_page_config(page_title="Gerador de GIFs Pro", page_icon="🎨", layout="centered")

st.title("🎨 Gerador de GIFs - Versão Ultra Premium")
st.write("Crie animações profissionais com física de movimento, controle de velocidade e efeitos visuais avançados.")

# 2. Configurações de Interface (Painel Lateral para organizar melhor)
st.sidebar.header("🚀 Configurações Globais")

tamanho_saida = st.sidebar.slider("Tamanho do GIF (Pixels):", min_value=200, max_value=800, value=500, step=50)
velocidade_fps = st.sidebar.slider("Velocidade da Animação (FPS):", min_value=5, max_value=40, value=20, step=5)
tipo_fundo = st.sidebar.selectbox("Estilo do Fundo:", ["Cor Sólida", "Totalmente Transparente"])
cor_fundo = st.sidebar.color_picker("Escolha a cor do fundo:", "#1E1C18")

st.header("🎮 Elementos e Efeitos")
tipo_entrada = st.radio("O que você deseja animar?", ["Texto Personalizado", "Enviar uma Imagem"])

# Opções de efeitos avançados
combo_efeito = st.selectbox(
    "Escolha o Movimento Principal:",
    [
        "Apenas Pulsar (Zoom Suave)",
        "Girar + Pulsar (Clássico)", 
        "Gelatina Elástica (Física de Borracha)",
        "Tremor Estilo Meme (Glitch/Shake)",
        "Quicar (Bounce)",
        "Tornado Cósmico (Girar + Pulsar + Piscar)"
    ]
)

# Efeitos adicionais de luz e cor
st.subheader("Filtros Especiais")
col1, col2 = st.columns(2)
with col1:
    ativar_rainbow = st.checkbox("🌈 Efeito Arco-íris (Texto Dinâmico)")
with col2:
    ativar_neon = st.checkbox("✨ Ativar Brilho Neon (Glow)")

base_image = None
bg_color = (0, 0, 0, 0) if tipo_fundo == "Totalmente Transparente" else cor_fundo

# Converte FPS para milissegundos por frame (duration)
duracao_frame = int(1000 / velocidade_fps)

# --- MÓDULO 1: TEXTO PERSONALIZADO ---
if tipo_entrada == "Texto Personalizado":
    texto = st.text_input("Digite a palavra ou frase:", value="Python")
    cor_texto = st.color_picker("Escolha a cor base do texto:", "#FF4B4B")
    
    if texto:
        font = ImageFont.load_default()
        
        # Medição justa do texto
        canvas_medida = Image.new("RGBA", (2000, 500), (0, 0, 0, 0))
        draw_medida = ImageDraw.Draw(canvas_medida)
        bbox = draw_medida.textbbox((0, 0), texto, font=font)
        w_texto_base = max(bbox[2] - bbox[0], 1)
        h_texto_base = max(bbox[3] - bbox[1], 1)
        
        # Desenha o texto base
        img_texto_crua = Image.new("RGBA", (w_texto_base, h_texto_base), (0, 0, 0, 0))
        draw_cruo = ImageDraw.Draw(img_texto_crua)
        draw_cruo.text((-bbox[0], -bbox[1]), texto, fill=cor_texto, font=font)
        
        # Escala proporcional (80% para dar espaço aos novos movimentos)
        largura_alvo = int(tamanho_saida * 0.80)
        proporcao_escala = largura_alvo / w_texto_base
        
        novo_w = int(w_texto_base * proporcao_escala)
        novo_h = int(h_texto_base * proporcao_escala)
        
        if novo_h > int(tamanho_saida * 0.80):
            altura_alvo = int(tamanho_saida * 0.80)
            proporcao_escala = altura_alvo / h_texto_base
            novo_w = int(w_texto_base * proporcao_escala)
            novo_h = int(h_texto_base * proporcao_escala)
            
        img_texto_gigante = img_texto_crua.resize((novo_w, novo_h), Image.Resampling.BILINEAR)
        
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0,0,0,0))
        ox = (tamanho_saida - novo_w) // 2
        oy = (tamanho_saida - novo_h) // 2
        base_image.paste(img_texto_gigante, (ox, oy), img_texto_gigante)

# --- MÓDULO 2: IMAGEM TRADICIONAL ---
else:
    uploaded_file = st.file_uploader("Suba qualquer tipo de imagem...", type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"])
    if uploaded_file is not None:
        img_original = Image.open(uploaded_file).convert("RGBA")
        
        bbox = img_original.getbbox()
        if bbox:
            img_original = img_original.crop(bbox)
        
        largura_util, altura_util = img_original.size
        proporcao = min((tamanho_saida * 0.80) / largura_util, (tamanho_saida * 0.80) / altura_util)
        nova_l = int(largura_util * proporcao)
        nova_a = int(altura_util * proporcao)
        
        img_redimensionada = img_original.resize((nova_l, nova_a), Image.Resampling.LANCZOS)
        
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0,0,0,0))
        offset_x = (tamanho_saida - nova_l) // 2
        offset_y = (tamanho_saida - nova_a) // 2
        base_image.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)

# --- PROCESSAMENTO DOS FRAMES DA ANIMAÇÃO ---
if base_image is not None:
    st.subheader("Processando Animação...")
    
    largura_orig, altura_orig = base_image.size
    frames = []
    num_frames = 24  
    
    for i in range(num_frames):
        progresso = i / num_frames
        angulo_rad = progresso * 2 * math.pi
        
        # Cria cópia limpa do elemento para trabalhar o frame
        elemento_frame = base_image.copy()
        
        # --- FILTRO 1: RAINBOW (APENAS PARA TEXTO) ---
        if ativar_rainbow and tipo_entrada == "Texto Personalizado":
            # Altera a matiz (HSV) dinamicamente frame por frame
            fase_cor = int(progresso * 255)
            # Função matemática simples para gerar RGB do arco-íris
            r = int(math.sin(progresso * 2 * math.pi + 0) * 127 + 128)
            g = int(math.sin(progresso * 2 * math.pi + 2) * 127 + 128)
            b = int(math.sin(progresso * 2 * math.pi + 4) * 127 + 128)
            
            # Recolore o canal do texto substituindo os pixels visíveis
            dados = elemento_frame.getdata()
            novos_dados = [(r, g, b, item[3]) if item[3] > 0 else item for item in dados]
            elemento_frame.putdata(novos_dados)

        # --- APLICAÇÃO DOS MOVIMENTOS (FÍSICA) ---
        frame_final = Image.new("RGBA", (largura_orig, altura_orig), (0,0,0,0))
        shift_x, shift_y = 0, 0
        
        # 1. Rotação (Se selecionado)
        if combo_efeito in ["Girar + Pulsar (Clássico)", "Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            angulo = - (progresso * 360)
            elemento_frame = elemento_frame.rotate(angulo, resample=Image.BICUBIC)

        # 2. Zoom / Pulsação Padrão
        if combo_efeito in ["Apenas Pulsar (Zoom Suave)", "Girar + Pulsar (Clássico)", "Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            fator_escala = 0.90 + (math.sin(angulo_rad) * 0.10)
            nl = int(largura_orig * fator_escala)
            na = int(altura_orig * fator_escala)
            elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)
            
        # 3. Efeito Gelatina Elástica (Estica X enquanto encolhe Y)
        elif combo_efeito == "Gelatina Elástica (Física de Borracha)":
            fator_x = 1.0 + (math.sin(angulo_rad) * 0.15)
            fator_y = 1.0 - (math.sin(angulo_rad) * 0.15)
            nl = int(largura_orig * fator_x)
            na = int(altura_orig * fator_y)
            elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

        # 4. Efeito Quicar (Bounce)
        elif combo_efeito == "Quicar (Bounce)":
            # Valor absoluto do seno simula o quique no chão
            altura_pulo = int(abs(math.sin(angulo_rad)) * (tamanho_saida * 0.25))
            shift_y = - altura_pulo

        # 5. Tremor Estilo Meme (Glitch/Shake)
        elif combo_efeito == "Tremor Estilo Meme (Glitch/Shake)":
            shift_x = random.randint(-15, 15)
            shift_y = random.randint(-15, 15)

        # Cola o elemento modificado centralizado com seus respectivos desvios físicos
        nl, na = elemento_frame.size
        ox = (largura_orig - nl) // 2 + shift_x
        oy = (altura_orig - na) // 2 + shift_y
        frame_final.paste(elemento_frame, (ox, oy), elemento_frame)

        # --- FILTRO 2: BRILHO NEON (GLOW) ---
        if ativar_neon:
            # Cria silhueta borrada por trás do objeto
            brilho = frame_final.filter(ImageFilter.GaussianBlur(radius=12))
            # Intensifica o brilho mesclando camadas
            brilho_forte = Image.blend(brilho, frame_final, alpha=0.3)
            canvas_neon = Image.new("RGBA", (largura_orig, altura_orig), (0,0,0,0))
            canvas_neon.paste(brilho_forte, (0,0), brilho_forte)
            canvas_neon.paste(frame_final, (0,0), frame_final)
            frame_final = canvas_neon

        # --- EFEITO EXTRA DE BRILHO (PISCAR) ---
        if combo_efeito in ["Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            fator_brilho = 1.1 + (math.sin(angulo_rad) * 0.5)
            enhancer = ImageEnhance.Brightness(frame_final)
            frame_final = enhancer.enhance(fator_brilho)

        # --- COMPOSIÇÃO COM O FUNDO DEFINITIVO ---
        canvas_fundo = Image.new("RGBA", (largura_orig, altura_orig), bg_color)
        canvas_fundo.paste(frame_final, (0, 0), frame_final)
        frames.append(canvas_fundo)
        
    # Compilação do GIF usando a velocidade dinâmica escolhida
    gif_buffer = io.BytesIO()
    frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=duracao_frame,
        loop=0,
        disposal=2
    )
    gif_bytes = gif_buffer.getvalue()
    
    st.subheader("GIF Final Premium:")
    st.image(gif_bytes, width=tamanho_saida)
    
    nome_arquivo = "animacao_premium.gif"
    st.download_button(
        label=f"📥 Baixar GIF Customizado",
        data=gif_bytes,
        file_name=nome_arquivo,
        mime="image/gif"
    )
