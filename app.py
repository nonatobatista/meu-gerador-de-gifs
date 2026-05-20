import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import io
import math
import os
import urllib.request

# 1. Configuração da página web
st.set_page_config(page_title="Gerador de GIFs Pro", page_icon="🎨", layout="centered")

st.title("🎨 Gerador de GIFs - Resolução Máxima Garantida")
st.write("Suba uma imagem ou digite um texto. Sistema com correção automática de fontes em nuvem.")

# FUNÇÃO ADICIONAL: Garante que uma fonte robusta exista no servidor do Streamlit
@st.cache_data
def baixar_fonte_reserva():
    caminho_local_fonte = "fonte_reserva.ttf"
    if not os.path.exists(caminho_local_fonte):
        # Baixa a fonte DejaVuSans-Bold diretamente do repositório público oficial do Debian/GNU
        url_fonte = "https://github.com/matomo-org/component-dejavu-sans/raw/master/DejaVuSans-Bold.ttf"
        try:
            urllib.request.urlretrieve(url_fonte, caminho_local_fonte)
        except Exception:
            return None
    return caminho_local_fonte

# Baixa a fonte se necessário
font_path_servidor = baixar_fonte_reserva()

# 2. Configurações de Interface
tipo_entrada = st.radio("O que você deseja animar?", ["Texto Personalizado", "Enviar uma Imagem"])

combo_efeito = st.selectbox(
    "Escolha o Combo de Efeitos:",
    [
        "Girar + Pulsar (Zoom) [Recomendado]", 
        "Pulsar + Piscar Forte (Escala + Brilho)",
        "Tornado Cósmico (Girar + Pulsar + Piscar)"
    ]
)

# Controle de tamanho dinâmico via interface
tamanho_saida = st.slider("Escolha o tamanho do GIF (Pixels de Largura/Altura):", min_value=200, max_value=800, value=500, step=50)

# Controle de fundo para evitar problemas de renderização de transparência
tipo_fundo = st.selectbox("Estilo do Fundo do GIF:", ["Totalmente Transparente", "Cor Sólida (Escolha abaixo)"])
cor_fundo = st.color_picker("Escolha a cor do fundo (Se selecionou Cor Sólida):", "#1E1C18")

base_image = None
bg_color = (0, 0, 0, 0) if tipo_fundo == "Totalmente Transparente" else cor_fundo

# --- MÓDULO 1: GERAR IMAGEM A PARTIR DE TEXTO (MAXIMIZADO REAL) ---
if tipo_entrada == "Texto Personalizado":
    texto = st.text_input("Digite a palavra ou frase:", value="Python")
    cor_texto = st.color_picker("Escolha a cor do texto:", "#FF4B4B")
    
    if texto:
        # Define o caminho da fonte utilizando a fonte baixada como prioridade absoluta
        if font_path_servidor and os.path.exists(font_path_servidor):
            font_path = font_path_servidor
        elif os.name == 'nt':  # Backup caso esteja rodando local no Windows
            caminho_windows = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arialbd.ttf')
            font_path = caminho_windows if os.path.exists(caminho_windows) else None
        else:
            font_path = None

        # Cria a tela final baseada no tamanho do Slider
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), bg_color)
        draw = ImageDraw.Draw(base_image)

        # Algoritmo de crescimento dinâmico da fonte
        tamanho_fonte = 10
        largura_alvo = int(tamanho_saida * 0.88)  # Ocupar até 88% da largura da tela
        altura_alvo = int(tamanho_saida * 0.88)
        font = ImageFont.load_default()

        if font_path:
            while True:
                try:
                    font_teste = ImageFont.truetype(font_path, tamanho_fonte)
                    bbox = draw.textbbox((0, 0), texto, font=font_teste)
                    w = bbox[2] - bbox[0]
                    h = bbox[3] - bbox[1]
                    
                    if w >= largura_alvo or h >= altura_alvo or tamanho_fonte > 400:
                        break
                    font = font_teste
                    tamanho_fonte += 2
                except Exception:
                    break

        # Centralização milimétrica do texto maximizado
        bbox = draw.textbbox((0, 0), texto, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (tamanho_saida - text_width) // 2
        y = (tamanho_saida - text_height) // 2
        
        draw.text((x, y), texto, fill=cor_texto, font=font)

# --- MÓDULO 2: ENTRADA DE IMAGEM TRADICIONAL (COM AUTO-CROP) ---
else:
    uploaded_file = st.file_uploader(
        "Suba qualquer tipo de imagem...", 
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"]
    )
    if uploaded_file is not None:
        img_original = Image.open(uploaded_file).convert("RGBA")
        
        # Corta as bordas inúteis
        bbox = img_original.getbbox()
        if bbox:
            img_original = img_original.crop(bbox)
        
        # Força a imagem a se expandir preenchendo 85% do tamanho selecionado
        largura_util, altura_util = img_original.size
        proporcao = min((tamanho_saida * 0.85) / largura_util, (tamanho_saida * 0.85) / altura_util)
        nova_l = int(largura_util * proporcao)
        nova_a = int(altura_util * proporcao)
        
        img_redimensionada = img_original.resize((nova_l, nova_a), Image.Resampling.LANCZOS)
        
        # Cria o canvas final no tamanho do Slider e centraliza a imagem nele
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), bg_color)
        offset_x = (tamanho_saida - nova_l) // 2
        offset_y = (tamanho_saida - nova_a) // 2
        base_image.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)

# --- PROCESSAMENTO DA ANIMAÇÃO ---
if base_image is not None:
    st.subheader("Visualização Base:")
    st.image(base_image, width=tamanho_saida)
    
    st.write("Renderizando frames em alta resolução...")
    
    largura_orig, altura_orig = base_image.size
    frames = []
    num_frames = 24  
    
    for i in range(num_frames):
        progresso = i / num_frames
        
        # --- EFEITO 1: ROTAÇÃO ---
        if combo_efeito in ["Girar + Pulsar (Zoom) [Recomendado]", "Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            angulo = - (progresso * 360)
            frame_atual = base_image.rotate(angulo, resample=Image.BICUBIC)
            if tipo_fundo != "Totalmente Transparente":
                bg_frame = Image.new("RGBA", base_image.size, bg_color)
                bg_frame.paste(frame_atual, (0,0), frame_atual)
                frame_atual = bg_frame
        else:
            frame_atual = base_image.copy()
            
        # --- EFEITO 2: PULSAÇÃO / ESCALA ---
        if combo_efeito in ["Girar + Pulsar (Zoom) [Recomendado]", "Pulsar + Piscar Forte (Escala + Brilho)", "Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            fator_escala = 0.85 + (math.sin(progresso * 2 * math.pi) * 0.15)
            nova_largura = int(largura_orig * fator_escala)
            nova_altura = int(altura_orig * fator_escala)
            
            img_redimensionada = frame_atual.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
            
            frame_final = Image.new("RGBA", (largura_orig, altura_orig), bg_color)
            offset_x = (largura_orig - nova_largura) // 2
            offset_y = (altura_orig - nova_altura) // 2
            frame_final.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)
            frame_atual = frame_final
            
        # --- EFEITO 3: BRILHO ---
        if combo_efeito in ["Pulsar + Piscar Forte (Escala + Brilho)", "Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            fator_brilho = 1.2 + (math.sin(progresso * 2 * math.pi) * 0.6)
            enhancer = ImageEnhance.Brightness(frame_atual)
            frame_atual = enhancer.enhance(fator_brilho)
            
        frames.append(frame_atual)
        
    # Compilação do GIF
    gif_buffer = io.BytesIO()
    frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=45,
        loop=0,
        disposal=2
    )
    gif_bytes = gif_buffer.getvalue()
    
    # Exibição e Download
    st.subheader("GIF Final Gerado:")
    st.image(gif_bytes, width=tamanho_saida)
    
    nome_arquivo = "texto_maximizado.gif" if tipo_entrada == "Texto Personalizado" else "imagem_maximizada.gif"
    st.download_button(
        label=f"📥 Baixar GIF em {tamanho_saida}x{tamanho_saida}px",
        data=gif_bytes,
        file_name=nome_arquivo,
        mime="image/gif"
    )
