import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import io
import math

# 1. Configuração da página web
st.set_page_config(page_title="Gerador de GIFs Pro", page_icon="🎨", layout="centered")

st.title("Gerador de GIFs - Alta Definição Garantida")
st.write("O conteúdo agora utiliza um mecanismo de renderização independente de fontes do sistema.")

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

tamanho_saida = st.slider("Escolha o tamanho do GIF (Pixels de Largura/Altura):", min_value=200, max_value=800, value=600, step=50)

tipo_fundo = st.selectbox("Estilo do Fundo do GIF:", ["Cor Sólida (Escolha abaixo)", "Totalmente Transparente"])
cor_fundo = st.color_picker("Escolha a cor do fundo:", "#1E1C18")

base_image = None
bg_color = (0, 0, 0, 0) if tipo_fundo == "Totalmente Transparente" else cor_fundo

# --- MÓDULO 1: TEXTO PERSONALIZADO (CÁLCULO DE RESOLUÇÃO SEGURO) ---
if tipo_entrada == "Texto Personalizado":
    texto = st.text_input("Digite a palavra ou frase:", value="Python")
    cor_texto = st.color_picker("Escolha a cor do texto:", "#FF4B4B")
    
    if texto:
        # Usamos uma fonte alternativa do Pillow que permite alteração de escala interna de forma confiável
        try:
            # Tenta carregar uma fonte padrão escalável embutida no Pillow
            font = ImageFont.load_default(size=100)
        except TypeError:
            # Caso a versão instalada do Pillow seja antiga e não aceite o argumento 'size',
            # criamos uma instância básica para o cálculo proporcional
            font = ImageFont.load_default()

        # Cria uma imagem temporária para medir o tamanho do texto base
        canvas_medida = Image.new("RGBA", (2000, 500), (0, 0, 0, 0))
        draw_medida = ImageDraw.Draw(canvas_medida)
        bbox = draw_medida.textbbox((0, 0), texto, font=font)
        w_texto_base = max(bbox[2] - bbox[0], 1)
        h_texto_base = max(bbox[3] - bbox[1], 1)
        
        # Desenha o texto base de forma bem justa em sua própria superfície
        img_texto_crua = Image.new("RGBA", (w_texto_base, h_texto_base), (0, 0, 0, 0))
        draw_cruo = ImageDraw.Draw(img_texto_crua)
        draw_cruo.text((-bbox[0], -bbox[1]), texto, fill=cor_texto, font=font)
        
        # Define a proporção matemática para esticar até 85% do tamanho escolhido no Slider
        largura_alvo = int(tamanho_saida * 0.85)
        proporcao_escala = largura_alvo / w_texto_base
        
        novo_w = int(w_texto_base * proporcao_escala)
        novo_h = int(h_texto_base * proporcao_escala)
        
        # Ajusta caso a altura ultrapasse os limites verticais da imagem quadrada
        if novo_h > int(tamanho_saida * 0.85):
            altura_alvo = int(tamanho_saida * 0.85)
            proporcao_escala = altura_alvo / h_texto_base
            novo_w = int(w_texto_base * proporcao_escala)
            novo_h = int(h_texto_base * proporcao_escala)
            
        # O pulo do gato: Faz o redimensionamento mantendo uma boa interpolação linear
        img_texto_gigante = img_texto_crua.resize((novo_w, novo_h), Image.Resampling.BILINEAR)
        
        # Cria o canvas final com a cor escolhida e centraliza o texto gerado
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), bg_color)
        ox = (tamanho_saida - novo_w) // 2
        oy = (tamanho_saida - novo_h) // 2
        base_image.paste(img_texto_gigante, (ox, oy), img_texto_gigante)

# --- MÓDULO 2: IMAGEM TRADICIONAL (PREENCHIMENTO TOTAL) ---
else:
    uploaded_file = st.file_uploader("Suba qualquer tipo de imagem...", type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"])
    if uploaded_file is not None:
        img_original = Image.open(uploaded_file).convert("RGBA")
        
        bbox = img_original.getbbox()
        if bbox:
            img_original = img_original.crop(bbox)
        
        largura_util, altura_util = img_original.size
        proporcao = min((tamanho_saida * 0.90) / largura_util, (tamanho_saida * 0.90) / altura_util)
        nova_l = int(largura_util * proporcao)
        nova_a = int(altura_util * proporcao)
        
        img_redimensionada = img_original.resize((nova_l, nova_a), Image.Resampling.LANCZOS)
        
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), bg_color)
        offset_x = (tamanho_saida - nova_l) // 2
        offset_y = (tamanho_saida - nova_a) // 2
        base_image.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)

# --- PROCESSAMENTO DA ANIMAÇÃO ---
if base_image is not None:
    st.subheader("Visualização Base:")
    st.image(base_image, width=tamanho_saida)
    
    st.write("Renderizando frames...")
    
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
            
        # --- EFEITO 2: PULSAÇÃO / ESCALA CALIBRADA ---
        if combo_efeito in ["Girar + Pulsar (Zoom) [Recomendado]", "Pulsar + Piscar Forte (Escala + Brilho)", "Tornado Cósmico (Girar + Pulsar + Piscar)"]:
            fator_escala = 0.90 + (math.sin(progresso * 2 * math.pi) * 0.10)
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
            fator_brilho = 1.1 + (math.sin(progresso * 2 * math.pi) * 0.5)
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
    
    st.subheader("GIF Final Gerado:")
    st.image(gif_bytes, width=tamanho_saida)
    
    nome_arquivo = "texto_correto.gif" if tipo_entrada == "Texto Personalizado" else "imagem_correta.gif"
    st.download_button(
        label=f"📥 Baixar GIF em {tamanho_saida}x{tamanho_saida}px",
        data=gif_bytes,
        file_name=nome_arquivo,
        mime="image/gif"
    )
