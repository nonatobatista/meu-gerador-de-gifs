import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
import io
import math
import random
import os
import urllib.request

# 1. Configuração da página web
st.set_page_config(page_title="Gerador de GIFs Pro", page_icon="🎨", layout="centered")

st.title("🎨 Gerador de GIFs - Versão Premium Continental")
st.write("Crie animações profissionais com renderização nativa de alta definição.")

# 2. Configurações de Interface (Painel Lateral)
st.sidebar.header("🚀 Configurações Globais")

tamanho_saida = st.sidebar.slider("Tamanho do GIF (Pixels):", min_value=200, max_value=800, value=500, step=50)
velocidade_fps = st.sidebar.slider("Velocidade da Animação (FPS):", min_value=5, max_value=40, value=20, step=5)
tipo_fundo = st.sidebar.selectbox("Estilo do Fundo:", ["Cor Sólida", "Totalmente Transparente"])
cor_fundo = st.sidebar.color_picker("Escolha a cor do fundo:", "#1E1C18")

# Opções de efeitos avançados na barra lateral
combo_efeito = st.sidebar.selectbox(
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

st.sidebar.subheader("Filtros Especiais")
ativar_rainbow = st.sidebar.checkbox("🌈 Efeito Arco-íris (Texto Dinâmico)")
ativar_neon = st.sidebar.checkbox("✨ Ativar Brilho Neon (Glow)")

# 3. Painel Central - Entradas do Usuário
st.header("🎮 O que você deseja animar?")
tipo_entrada = st.radio("Escolha o tipo de elemento:", ["Texto Personalizado", "Enviar uma Imagem"])

base_image = None
bg_color = (0, 0, 0, 0) if tipo_fundo == "Totalmente Transparente" else cor_fundo
duracao_frame = int(1000 / velocidade_fps) # Linha corrigida aqui!

# --- MÓDULO 1: TEXTO PERSONALIZADO (VETORIAL DIRETO NATIVO) ---
if tipo_entrada == "Texto Personalizado":
    texto = st.text_input("Digite a palavra ou frase:", value="Python")
    cor_texto = st.color_picker("Escolha a cor base do texto:", "#FF4B4B")
    
    if texto:
        largura_alvo = int(tamanho_saida * 0.82)
        altura_alvo = int(tamanho_saida * 0.82)
        
        img_temp = Image.new("RGBA", (10, 10))
        draw_temp = ImageDraw.Draw(img_temp)
        
        font_final = None
        tamanho_fonte = 24
        
        # Encontra o maior tamanho de fonte estável que cabe perfeitamente na tela
        for f_size in range(24, 400, 4):
            font_teste = None
            
            # Passo 1: Tenta buscar fontes nativas comuns do Linux/Windows
            for f_nome in ["Ubuntu-Bold.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial.ttf", "Helvetica.ttf"]:
                try:
                    font_teste = ImageFont.truetype(f_nome, f_size)
                    break
                except IOError:
                    continue
            
            # Passo 2: Se não houver fontes locais, tenta o download preventivo
            if font_teste is None:
                try:
                    if not os.path.exists("Ubuntu-Bold.ttf"):
                        urllib.request.urlretrieve("https://github.com/google/fonts/raw/main/ofl/ubuntu/Ubuntu-Bold.ttf", "Ubuntu-Bold.ttf")
                    font_teste = ImageFont.truetype("Ubuntu-Bold.ttf", f_size)
                except Exception:
                    # Passo 3: Em último caso absoluto, usa a fonte interna do Pillow escalável
                    try:
                        font_teste = ImageFont.load_default(size=f_size)
                    except TypeError:
                        font_teste = ImageFont.load_default()
            
            # Medição com tratamento robusto
            try:
                bbox = draw_temp.textbbox((0, 0), texto, font=font_teste, anchor="mm")
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
            except Exception:
                bbox = draw_temp.textbbox((0, 0), texto, font=font_teste)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                
            if w > largura_alvo or h > altura_alvo:
                break
                
            font_final = font_teste
            tamanho_fonte = f_size
        
        if font_final is None:
            font_final = ImageFont.load_default()

        # Cria a imagem base vazia e renderiza o texto vetorial em alta definição
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0, 0, 0, 0))
        draw_final = ImageDraw.Draw(base_image)
        
        centro_x = tamanho_saida // 2
        centro_y = tamanho_saida // 2
        
        # Renderização estável livre de cortes
        try:
            draw_final.text((centro_x, centro_y), texto, fill=cor_texto, font=font_final, anchor="mm")
        except Exception:
            bbox = draw_final.textbbox((0, 0), texto, font=font_final)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            ox = (tamanho_saida - w) // 2
            oy = (tamanho_saida - h) // 2
            draw_final.text((ox, oy), texto, fill=cor_texto, font=font_final)

# --- MÓDULO 2: IMAGEM TRADICIONAL ---
else:
    uploaded_file = st.file_uploader("Suba qualquer tipo de imagem...", type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"])
    if uploaded_file is not None:
        img_original = Image.open(uploaded_file).convert("RGBA")
        
        bbox = img_original.getbbox()
        if bbox:
            img_original = img_original.crop(bbox)
        
        largura_util, altura_util = img_original.size
        proporcao = min((tamanho_saida * 0.82) / largura_util, (tamanho_saida * 0.82) / altura_util)
        nova_l = int(largura_util * proporcao)
        nova_a = int(altura_util * proporcao)
        
        img_redimensionada = img_original.resize((nova_l, nova_a), Image.Resampling.LANCZOS)
        
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0, 0, 0, 0))
        offset_x = (tamanho_saida - nova_l) // 2
        offset_y = (tamanho_saida - nova_a) // 2
        base_image.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)

# --- PROCESSAMENTO DOS FRAMES DA ANIMAÇÃO ---
if base_image is not None:
    st.write("⚙️ Processando Animação...")
    largura_orig, altura_orig = base_image.size
    frames = []
    num_frames = 24  
    
    for i in range(num_frames):
        progresso = i / num_frames
        angulo_rad = progresso * 2 * math.pi
        
        elemento_frame = base_image.copy()
        
        # --- FILTRO 1: RAINBOW ---
        if ativar_rainbow and tipo_entrada == "Texto Personalizado":
            r = int(math.sin(progresso * 2 * math.pi + 0) * 127 + 128)
            g = int(math.sin(progresso * 2 * math.pi + 2) * 127 + 128)
            b = int(math.sin(progresso * 2 * math.pi + 4) * 127 + 128)
            
            dados = elemento_frame.getdata()
            novos_dados = [(r, g, b, item[3]) if item[3] > 0 else item for item in dados]
            elemento_frame.putdata(novos_dados)

        # --- APLICAÇÃO DOS MOVIMENTOS ---
        frame_final = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
        shift_x, shift_y = 0, 0
        
        if combo_efeito in ["Girar + Pulsar (Clássico)", "Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            angulo = - (progresso * 360)
            elemento_frame = elemento_frame.rotate(angulo, resample=Image.BICUBIC)

        if combo_efeito in ["Apenas Pulsar (Zoom Suave)", "Girar + Pulsar (Clássico)", "Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            fator_escala = 0.90 + (math.sin(angulo_rad) * 0.10)
            nl = int(largura_orig * fator_escala)
            na = int(altura_orig * fator_escala)
            elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)
            
        elif combo_efeito == "Gelatina Elástica (Física de Borracha)":
            fator_x = 1.0 + (math.sin(angulo_rad) * 0.12)
            fator_y = 1.0 - (math.sin(angulo_rad) * 0.12)
            nl = int(largura_orig * fator_x)
            na = int(altura_orig * fator_y)
            elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)

        elif combo_efeito == "Quicar (Bounce)":
            altura_pulo = int(abs(math.sin(angulo_rad)) * (tamanho_saida * 0.20))
            shift_y = - altura_pulo

        elif combo_efeito == "Tremor Estilo Meme (Glitch/Shake)":
            shift_x = random.randint(-10, 10)
            shift_y = random.randint(-10, 10)

        nl, na = elemento_frame.size
        ox = (largura_orig - nl) // 2 + shift_x
        oy = (altura_orig - na) // 2 + shift_y
        frame_final.paste(elemento_frame, (ox, oy), elemento_frame)

        # --- FILTRO 2: BRILHO NEON ---
        if ativar_neon:
            brilho = frame_final.filter(ImageFilter.GaussianBlur(radius=10))
            brilho_forte = Image.blend(brilho, frame_final, alpha=0.3)
            canvas_neon = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
            canvas_neon.paste(brilho_forte, (0, 0), brilho_forte)
            canvas_neon.paste(frame_final, (0, 0), frame_final)
            frame_final = canvas_neon

        if combo_efeito in ["Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            fator_brilho = 1.1 + (math.sin(angulo_rad) * 0.4)
            enhancer = ImageEnhance.Brightness(frame_final)
            frame_final = enhancer.enhance(fator_brilho)

        canvas_fundo = Image.new("RGBA", (largura_orig, altura_orig), bg_color)
        canvas_fundo.paste(frame_final, (0, 0), frame_final)
        frames.append(canvas_fundo)
        
    # Compila o GIF final de alta definição
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
    
    st.download_button(
        label="📥 Baixar GIF Customizado",
        data=gif_bytes,
        file_name="animacao_premium.gif",
        mime="image/gif"
    )
else:
    st.info("💡 Digite um texto acima ou envie uma imagem para ver seu GIF rodar liso!")
