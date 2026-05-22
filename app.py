import streamlit as st  # Biblioteca para criar interface web interativa
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter  # Biblioteca para manipulação de imagens
import io  # Para trabalhar com bytes na memória (salvar GIF sem criar arquivo)
import math  # Funções matemáticas (seno, cosseno, pi, etc)
import random  # Para gerar números aleatórios (efeitos de shake, partículas)
import os  # Para verificar se arquivos existem no sistema
import urllib.request  # Para baixar fontes da internet
import colorsys  # Para converter entre sistemas de cores (RGB, HSV, etc)
import numpy as np  # Para cálculos matriciais avançados (gradientes, transformações)

# ============================================================================
# 1. CONFIGURAÇÃO INICIAL DA PÁGINA WEB
# ============================================================================
st.set_page_config(
    page_title="Gerador de GIFs Ultra Premium",  # Título que aparece na aba do navegador
    page_icon="🎨",  # Ícone que aparece na aba
    layout="centered"  # Layout centralizado (opções: "centered" ou "wide")
)

# Título principal visível na página
st.title("🎨 Gerador de GIFs Ultra Premium - Edição Continental")
st.write("Crie animações cinematográficas com efeitos de Hollywood e renderização 4K.")

# ============================================================================
# 2. BARRA LATERAL - CONFIGURAÇÕES GLOBAIS
# ============================================================================
st.sidebar.header("🚀 Configurações Principais")

# Slider: controle deslizante para escolher valores numéricos
tamanho_saida = st.sidebar.slider(
    "Resolução do GIF (Pixels):",  # Texto que aparece acima do slider
    min_value=200,  # Valor mínimo permitido
    max_value=1000,  # Valor máximo permitido
    value=600,  # Valor padrão inicial
    step=50  # Incremento ao mover (pula de 50 em 50)
)

# Controla quantos quadros por segundo (quanto maior, mais suave)
velocidade_fps = st.sidebar.slider(
    "Velocidade (FPS):",
    min_value=10,
    max_value=60,
    value=30,
    step=5
)

# Controla quantos frames totais terá o GIF (quanto mais, mais longa a animação)
num_frames_total = st.sidebar.slider(
    "Duração (Número de Frames):",
    min_value=12,
    max_value=60,
    value=30,
    step=6
)

# Selectbox: menu dropdown para escolher entre opções
tipo_fundo = st.sidebar.selectbox(
    "Estilo do Fundo:",
    [
        "Cor Sólida",
        "Totalmente Transparente",
        "Gradiente Radial Dinâmico",
        "Gradiente Linear Animado",
        "Padrão de Ruído (Noise)"
    ]
)

# Color picker: seletor de cor (retorna string hexadecimal como "#FF0000")
cor_fundo_primaria = st.sidebar.color_picker("Cor Principal do Fundo:", "#0A0E27")
cor_fundo_secundaria = st.sidebar.color_picker("Cor Secundária (Gradientes):", "#1E3A8A")

# ============================================================================
# 3. SEÇÃO DE MOVIMENTOS E ANIMAÇÕES
# ============================================================================
st.sidebar.subheader("🎬 Efeitos de Movimento")

# Lista expandida de efeitos de movimento
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
        "Zoom In/Out Dramático"
    ]
)

# Slider para controlar a intensidade do efeito (0.0 a 2.0)
intensidade_movimento = st.sidebar.slider(
    "Intensidade do Movimento:",
    min_value=0.1,
    max_value=2.0,
    value=1.0,
    step=0.1
)

# ============================================================================
# 4. EFEITOS VISUAIS AVANÇADOS
# ============================================================================
st.sidebar.subheader("✨ Efeitos Especiais")

# Checkboxes: caixas de seleção (True/False)
ativar_rainbow = st.sidebar.checkbox("🌈 Arco-íris Dinâmico (Cores Rotativas)")
ativar_neon = st.sidebar.checkbox("💡 Brilho Neon (Glow Intenso)")
ativar_particulas = st.sidebar.checkbox("⭐ Partículas Orbitais")
ativar_trail = st.sidebar.checkbox("🌊 Rastro de Movimento (Motion Blur)")
ativar_sombra = st.sidebar.checkbox("🌑 Sombra Dinâmica Projetada")
ativar_aberracao = st.sidebar.checkbox("📺 Aberração Cromática (RGB Split)")
ativar_scanlines = st.sidebar.checkbox("📟 Scanlines Retrô")
ativar_vinheta = st.sidebar.checkbox("🎞️ Vinheta Cinematográfica")
ativar_pulse_borda = st.sidebar.checkbox("⚡ Pulso de Borda (Border Pulse)")

# Controle de intensidade para efeitos de cor
if ativar_rainbow:
    velocidade_rainbow = st.sidebar.slider(
        "Velocidade do Arco-íris:",
        min_value=0.5,
        max_value=3.0,
        value=1.0,
        step=0.1
    )

# Controle de intensidade para partículas
if ativar_particulas:
    num_particulas = st.sidebar.slider(
        "Número de Partículas:",
        min_value=5,
        max_value=50,
        value=15,
        step=5
    )

# ============================================================================
# 5. PALETAS DE CORES PREDEFINIDAS
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
        "Galaxy (Roxo/Azul/Magenta)"
    ]
)

# Dicionário: estrutura que armazena pares chave-valor
# Cada paleta tem uma lista de cores em formato hexadecimal
PALETAS = {
    "Cyberpunk (Roxo/Rosa/Azul)": ["#8B00FF", "#FF00FF", "#00FFFF", "#FF1493"],
    "Sunset (Laranja/Rosa/Roxo)": ["#FF6B35", "#FF8C42", "#FFA07A", "#FF69B4", "#9B59B6"],
    "Ocean (Azul/Verde/Ciano)": ["#006994", "#0099CC", "#00CCCC", "#00FFB2", "#4ECDC4"],
    "Fire (Vermelho/Laranja/Amarelo)": ["#FF0000", "#FF4500", "#FF6347", "#FF8C00", "#FFD700"],
    "Neon Tokyo (Rosa/Azul/Verde)": ["#FF006E", "#FB5607", "#FFBE0B", "#8338EC", "#3A86FF"],
    "Pastel Dream (Tons Suaves)": ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"],
    "Monochrome (Preto e Branco)": ["#FFFFFF", "#CCCCCC", "#999999", "#666666", "#333333"],
    "Tropical (Verde/Amarelo/Rosa)": ["#06FFA5", "#FFFB00", "#FF006E", "#00D9FF", "#8B00FF"],
    "Galaxy (Roxo/Azul/Magenta)": ["#4A00E0", "#8E2DE2", "#DA22FF", "#9733EE", "#5B247A"]
}

# ============================================================================
# 6. ENTRADA DE CONTEÚDO (TEXTO OU IMAGEM)
# ============================================================================
st.header("🎮 Conteúdo para Animar")

# Radio buttons: escolha única entre opções
tipo_entrada = st.radio(
    "Tipo de elemento:",
    ["✍️ Texto Personalizado", "🖼️ Enviar Imagem"]
)

# Variável que vai armazenar a imagem base a ser animada
base_image = None

# Calcula cor de fundo baseada na escolha do usuário
# Tupla RGBA: (Red, Green, Blue, Alpha) onde Alpha é transparência (0-255)
if tipo_fundo == "Totalmente Transparente":
    bg_color = (0, 0, 0, 0)  # Totalmente transparente
else:
    # Converte string hexadecimal "#RRGGBB" para tupla (R, G, B)
    # [1:] remove o "#" do início
    # int(hex[i:i+2], 16) converte cada par de caracteres hex para número decimal
    hex_cor = cor_fundo_primaria.lstrip('#')
    bg_color = tuple(int(hex_cor[i:i+2], 16) for i in (0, 2, 4)) + (255,)  # Adiciona alpha=255

# Calcula duração de cada frame em milissegundos
# Se FPS=30, cada frame dura 1000/30 ≈ 33ms
duracao_frame = int(1000 / velocidade_fps)

# ============================================================================
# 7. FUNÇÃO AUXILIAR: CONVERTER HEX PARA RGB
# ============================================================================
def hex_para_rgb(hex_color):
    """
    Converte cor hexadecimal (#RRGGBB) para tupla RGB (R, G, B)
    
    Parâmetros:
        hex_color (str): Cor em formato "#RRGGBB"
    
    Retorna:
        tuple: Tupla com 3 valores (R, G, B) de 0 a 255
    
    Exemplo:
        hex_para_rgb("#FF0000") retorna (255, 0, 0) - vermelho puro
    """
    hex_color = hex_color.lstrip('#')  # Remove "#" se existir
    # Divide a string em 3 pares e converte cada um de hexadecimal para decimal
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# ============================================================================
# 8. FUNÇÃO AUXILIAR: CRIAR GRADIENTE DE FUNDO
# ============================================================================
def criar_fundo_gradiente(largura, altura, tipo, cor1, cor2, frame_atual, total_frames):
    """
    Cria imagem com fundo gradiente animado
    
    Parâmetros:
        largura (int): Largura da imagem em pixels
        altura (int): Altura da imagem em pixels
        tipo (str): Tipo de gradiente ("radial", "linear", "noise")
        cor1 (tuple): Cor inicial RGB
        cor2 (tuple): Cor final RGB
        frame_atual (int): Número do frame atual (para animação)
        total_frames (int): Total de frames (para calcular progresso)
    
    Retorna:
        Image: Imagem PIL com o gradiente
    """
    # Cria array numpy (matriz) de pixels inicialmente preta
    # Shape (altura, largura, 4) = cada pixel tem 4 valores RGBA
    img_array = np.zeros((altura, largura, 4), dtype=np.uint8)
    
    # Calcula progresso da animação (0.0 a 1.0)
    progresso = frame_atual / total_frames
    angulo = progresso * 2 * math.pi  # Converte para radianos (0 a 2π)
    
    if tipo == "Gradiente Radial Dinâmico":
        # Cria gradiente circular do centro para as bordas
        centro_x, centro_y = largura // 2, altura // 2
        raio_max = math.sqrt(centro_x**2 + centro_y**2)  # Distância máxima do centro
        
        # Offset animado: o centro do gradiente se move em círculo
        offset_x = int(math.cos(angulo) * largura * 0.1)
        offset_y = int(math.sin(angulo) * altura * 0.1)
        
        # Loop por cada pixel da imagem
        for y in range(altura):
            for x in range(largura):
                # Calcula distância do pixel até o centro (com offset animado)
                dx = x - (centro_x + offset_x)
                dy = y - (centro_y + offset_y)
                distancia = math.sqrt(dx*dx + dy*dy)
                
                # Normaliza distância (0.0 = centro, 1.0 = borda)
                t = min(distancia / raio_max, 1.0)
                
                # Interpola linearmente entre cor1 e cor2
                # t=0 → 100% cor1, t=1 → 100% cor2
                r = int(cor1[0] * (1-t) + cor2[0] * t)
                g = int(cor1[1] * (1-t) + cor2[1] * t)
                b = int(cor1[2] * (1-t) + cor2[2] * t)
                
                img_array[y, x] = [r, g, b, 255]
    
    elif tipo == "Gradiente Linear Animado":
        # Gradiente que vai de cima para baixo, com rotação animada
        angulo_grad = progresso * 360  # Ângulo em graus
        
        for y in range(altura):
            # Calcula posição vertical normalizada (0.0 a 1.0)
            t = y / altura
            
            # Adiciona oscilação baseada no ângulo
            t = (t + math.sin(angulo) * 0.2) % 1.0
            
            # Interpola cores
            r = int(cor1[0] * (1-t) + cor2[0] * t)
            g = int(cor1[1] * (1-t) + cor2[1] * t)
            b = int(cor1[2] * (1-t) + cor2[2] * t)
            
            # Preenche a linha inteira com essa cor
            img_array[y, :] = [r, g, b, 255]
    
    elif tipo == "Padrão de Ruído (Noise)":
        # Cria padrão de ruído Perlin-like (simplificado)
        for y in range(altura):
            for x in range(largura):
                # Gera valor pseudo-aleatório baseado na posição + tempo
                # Usa seno para criar padrão suave
                noise_val = (
                    math.sin(x * 0.01 + angulo) * 
                    math.cos(y * 0.01 + angulo) * 
                    0.5 + 0.5  # Normaliza para 0.0-1.0
                )
                
                # Interpola cores baseado no ruído
                r = int(cor1[0] * (1-noise_val) + cor2[0] * noise_val)
                g = int(cor1[1] * (1-noise_val) + cor2[1] * noise_val)
                b = int(cor1[2] * (1-noise_val) + cor2[2] * noise_val)
                
                img_array[y, x] = [r, g, b, 255]
    
    # Converte array numpy de volta para imagem PIL
    return Image.fromarray(img_array, mode='RGBA')

# ============================================================================
# 9. MÓDULO DE TEXTO PERSONALIZADO (RENDERIZAÇÃO VETORIAL)
# ============================================================================
if tipo_entrada == "✍️ Texto Personalizado":
    # Input de texto: caixa onde usuário digita
    texto = st.text_input("Digite o texto:", value="PYTHON")
    
    # Color picker para cor do texto
    cor_texto = st.color_picker("Cor base do texto:", "#00FF88")
    
    # Checkbox para ativar texto com outline (contorno)
    ativar_outline = st.checkbox("🔲 Adicionar Contorno no Texto")
    if ativar_outline:
        cor_outline = st.color_picker("Cor do Contorno:", "#000000")
        espessura_outline = st.slider("Espessura do Contorno:", 1, 10, 3)
    
    if texto:  # Só executa se o usuário digitou algo
        # Calcula área útil (82% do tamanho total, deixando margem)
        largura_alvo = int(tamanho_saida * 0.82)
        altura_alvo = int(tamanho_saida * 0.82)
        
        # Cria imagem temporária pequena só para medir texto
        img_temp = Image.new("RGBA", (10, 10))
        draw_temp = ImageDraw.Draw(img_temp)  # Objeto para desenhar
        
        font_final = None  # Vai armazenar a fonte escolhida
        tamanho_fonte = 24  # Tamanho inicial
        
        # Loop para encontrar o maior tamanho de fonte que cabe
        # range(início, fim, passo) - testa de 24 até 500, pulando de 4 em 4
        for f_size in range(24, 500, 4):
            font_teste = None
            
            # TENTATIVA 1: Procura fontes instaladas no sistema
            # Lista de fontes comuns em Linux/Windows
            for f_nome in ["Ubuntu-Bold.ttf", "DejaVuSans-Bold.ttf", 
                          "LiberationSans-Bold.ttf", "Arial.ttf", "Helvetica.ttf"]:
                try:
                    font_teste = ImageFont.truetype(f_nome, f_size)
                    break  # Encontrou! Sai do loop interno
                except IOError:
                    continue  # Não achou, tenta a próxima
            
            # TENTATIVA 2: Baixa fonte do GitHub se necessário
            if font_teste is None:
                try:
                    # Verifica se já baixou antes
                    if not os.path.exists("Ubuntu-Bold.ttf"):
                        # urllib.request.urlretrieve baixa arquivo da internet
                        urllib.request.urlretrieve(
                            "https://github.com/google/fonts/raw/main/ofl/ubuntu/Ubuntu-Bold.ttf",
                            "Ubuntu-Bold.ttf"
                        )
                    font_teste = ImageFont.truetype("Ubuntu-Bold.ttf", f_size)
                except Exception:
                    # TENTATIVA 3: Usa fonte padrão do Pillow
                    try:
                        font_teste = ImageFont.load_default(size=f_size)
                    except TypeError:
                        font_teste = ImageFont.load_default()
            
            # Mede o tamanho que o texto vai ocupar com essa fonte
            try:
                # textbbox retorna (x1, y1, x2, y2) - caixa delimitadora do texto
                # anchor="mm" = middle-middle (centro)
                bbox = draw_temp.textbbox((0, 0), texto, font=font_teste, anchor="mm")
                w = bbox[2] - bbox[0]  # Largura = x2 - x1
                h = bbox[3] - bbox[1]  # Altura = y2 - y1
            except Exception:
                # Fallback para versões antigas do Pillow
                bbox = draw_temp.textbbox((0, 0), texto, font=font_teste)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
            
            # Se o texto ficou maior que o espaço disponível, para o loop
            if w > largura_alvo or h > altura_alvo:
                break
            
            # Se chegou aqui, o texto ainda cabe - salva essa fonte
            font_final = font_teste
            tamanho_fonte = f_size
        
        # Garantia: se não achou nenhuma fonte, usa a padrão
        if font_final is None:
            font_final = ImageFont.load_default()
        
        # Agora cria a imagem base real com o texto renderizado
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0, 0, 0, 0))
        draw_final = ImageDraw.Draw(base_image)
        
        # Calcula centro da imagem
        centro_x = tamanho_saida // 2  # Operador // faz divisão inteira
        centro_y = tamanho_saida // 2
        
        # Desenha contorno (outline) se ativado
        if ativar_outline:
            # Desenha o texto várias vezes em posições levemente deslocadas
            # Isso cria efeito de contorno grosso
            for offset_x in range(-espessura_outline, espessura_outline + 1):
                for offset_y in range(-espessura_outline, espessura_outline + 1):
                    if offset_x != 0 or offset_y != 0:  # Não desenha no centro ainda
                        try:
                            draw_final.text(
                                (centro_x + offset_x, centro_y + offset_y),
                                texto,
                                fill=cor_outline,
                                font=font_final,
                                anchor="mm"
                            )
                        except:
                            pass
        
        # Desenha o texto principal por cima do contorno
        try:
            draw_final.text(
                (centro_x, centro_y),
                texto,
                fill=cor_texto,
                font=font_final,
                anchor="mm"
            )
        except Exception:
            # Fallback para versões antigas sem suporte a anchor
            bbox = draw_final.textbbox((0, 0), texto, font=font_final)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            ox = (tamanho_saida - w) // 2
            oy = (tamanho_saida - h) // 2
            draw_final.text((ox, oy), texto, fill=cor_texto, font=font_final)

# ============================================================================
# 10. MÓDULO DE IMAGEM ENVIADA PELO USUÁRIO
# ============================================================================
else:
    # File uploader: permite usuário enviar arquivo
    uploaded_file = st.file_uploader(
        "Envie uma imagem:",
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"]
    )
    
    if uploaded_file is not None:
        # Abre imagem e converte para RGBA (Red, Green, Blue, Alpha)
        # RGBA garante suporte a transparência
        img_original = Image.open(uploaded_file).convert("RGBA")
        
        # Remove pixels completamente transparentes das bordas
        # getbbox() retorna (x1, y1, x2, y2) da área com conteúdo visível
        bbox = img_original.getbbox()
        if bbox:
            img_original = img_original.crop(bbox)  # Recorta para essa área
        
        # Pega dimensões da imagem
        largura_util, altura_util = img_original.size
        
        # Calcula proporção para redimensionar mantendo aspect ratio
        # min() garante que a imagem caiba tanto em largura quanto altura
        proporcao = min(
            (tamanho_saida * 0.82) / largura_util,
            (tamanho_saida * 0.82) / altura_util
        )
        
        # Calcula novas dimensões
        nova_l = int(largura_util * proporcao)
        nova_a = int(altura_util * proporcao)
        
        # Redimensiona com filtro LANCZOS (alta qualidade, evita pixelização)
        img_redimensionada = img_original.resize(
            (nova_l, nova_a),
            Image.Resampling.LANCZOS
        )
        
        # Cria canvas vazio do tamanho final
        base_image = Image.new("RGBA", (tamanho_saida, tamanho_saida), (0, 0, 0, 0))
        
        # Calcula posição para centralizar a imagem
        offset_x = (tamanho_saida - nova_l) // 2
        offset_y = (tamanho_saida - nova_a) // 2
        
        # Cola a imagem redimensionada no centro
        # O terceiro parâmetro usa a própria imagem como máscara de transparência
        base_image.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)

# ============================================================================
# 11. PROCESSAMENTO E GERAÇÃO DOS FRAMES DA ANIMAÇÃO
# ============================================================================
if base_image is not None:  # Só executa se temos uma imagem base
    st.write("⚙️ Renderizando animação premium...")
    
    # Pega dimensões da imagem base
    largura_orig, altura_orig = base_image.size
    
    # Lista que vai armazenar todos os frames do GIF
    frames = []
    
    # Prepara cores da paleta escolhida
    cores_paleta = []
    if paleta_escolhida != "Personalizado (Escolha Livre)":
        # Converte cores hexadecimais da paleta para RGB
        cores_paleta = [hex_para_rgb(cor) for cor in PALETAS[paleta_escolhida]]
    
    # ========================================================================
    # LOOP PRINCIPAL: Gera cada frame da animação
    # ========================================================================
    for i in range(num_frames_total):
        # Calcula progresso (0.0 no primeiro frame, 1.0 no último)
        progresso = i / num_frames_total
        
        # Converte progresso em ângulo de 0 a 2π (ciclo completo)
        angulo_rad = progresso * 2 * math.pi
        
        # Copia a imagem base (evita modificar o original)
        elemento_frame = base_image.copy()
        
        # ====================================================================
        # FILTRO 1: EFEITO ARCO-ÍRIS (Muda cor do elemento)
        # ====================================================================
        if ativar_rainbow:
            if tipo_entrada == "✍️ Texto Personalizado":
                # Gera cores RGB usando funções seno defasadas
                # Cada componente (R, G, B) oscila em frequência diferente
                r = int(math.sin(progresso * 2 * math.pi * velocidade_rainbow + 0) * 127 + 128)
                g = int(math.sin(progresso * 2 * math.pi * velocidade_rainbow + 2) * 127 + 128)
                b = int(math.sin(progresso * 2 * math.pi * velocidade_rainbow + 4) * 127 + 128)
                
                # Pega todos os pixels da imagem como lista de tuplas
                dados = elemento_frame.getdata()
                
                # Substitui cor de cada pixel não-transparente
                # List comprehension: cria nova lista baseada na antiga
                novos_dados = [
                    (r, g, b, item[3]) if item[3] > 0 else item 
                    for item in dados
                ]
                # item[3] é o canal alpha (transparência)
                # Se alpha > 0 (visível), aplica nova cor mantendo alpha
                # Se alpha = 0 (transparente), mantém como está
                
                # Atualiza pixels da imagem
                elemento_frame.putdata(novos_dados)
            else:
                # Para imagens, aplica tint colorido
                # Converte para HSV, modifica matiz (hue), volta para RGB
                if cores_paleta:
                    # Escolhe cor da paleta de forma cíclica
                    idx_cor = int(progresso * len(cores_paleta)) % len(cores_paleta)
                    cor_tint = cores_paleta[idx_cor]
                    
                    # Aplica tint multiplicando canais RGB
                    dados = elemento_frame.getdata()
                    novos_dados = []
                    for item in dados:
                        if item[3] > 0:
                            # Multiplica cada canal pela cor do tint (normalizada)
                            novo_r = int(item[0] * cor_tint[0] / 255)
                            novo_g = int(item[1] * cor_tint[1] / 255)
                            novo_b = int(item[2] * cor_tint[2] / 255)
                            novos_dados.append((novo_r, novo_g, novo_b, item[3]))
                        else:
                            novos_dados.append(item)
                    elemento_frame.putdata(novos_dados)
        
        # ====================================================================
        # APLICAÇÃO DOS MOVIMENTOS E TRANSFORMAÇÕES
        # ====================================================================
        
        # Cria canvas vazio onde vamos colocar o elemento transformado
        frame_final = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
        
        # Variáveis de deslocamento (para movimentos de translação)
        shift_x, shift_y = 0, 0
        
        # Variável que controla se aplicamos rotação
        aplicar_rotacao = False
        angulo_rotacao = 0
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Rotação
        # --------------------------------------------------------------------
        if combo_efeito in ["Rotação Infinita", "Rotação + Pulsar (Clássico)", 
                            "Tornado Cósmico (Multi-Efeito)"]:
            aplicar_rotacao = True
            # Rotação completa (360 graus) no sentido anti-horário
            angulo_rotacao = -(progresso * 360 * intensidade_movimento)
        
        elif combo_efeito == "Espiral Hipnótica":
            aplicar_rotacao = True
            # Rotação acelerada (quadrática)
            angulo_rotacao = -(progresso**2 * 720 * intensidade_movimento)
        
        # Aplica rotação se necessário
        if aplicar_rotacao:
            elemento_frame = elemento_frame.rotate(
                angulo_rotacao,
                resample=Image.BICUBIC,  # Interpolação de alta qualidade
                expand=False  # Não expande canvas
            )
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Pulsar (Zoom in/out)
        # --------------------------------------------------------------------
        if combo_efeito in ["Pulsar Suave (Respiração)", "Rotação + Pulsar (Clássico)", 
                            "Tornado Cósmico (Multi-Efeito)"]:
            # Fator de escala oscila entre 0.85 e 1.15
            # math.sin(angulo_rad) varia de -1 a +1
            fator_escala = 1.0 + (math.sin(angulo_rad) * 0.15 * intensidade_movimento)
            
            # Calcula novas dimensões
            nl = int(largura_orig * fator_escala)
            na = int(altura_orig * fator_escala)
            
            # Garante dimensões mínimas
            nl = max(nl, 10)
            na = max(na, 10)
            
            # Redimensiona elemento
            elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Gelatina Elástica (Squash & Stretch)
        # --------------------------------------------------------------------
        elif combo_efeito == "Gelatina Elástica (Squash & Stretch)":
            # Largura e altura oscilam em direções opostas
            # Quando fica mais largo, fica mais baixo (conserva área aproximadamente)
            fator_x = 1.0 + (math.sin(angulo_rad) * 0.25 * intensidade_movimento)
            fator_y = 1.0 - (math.sin(angulo_rad) * 0.25 * intensidade_movimento)
            
            nl = int(largura_orig * fator_x)
            na = int(altura_orig * fator_y)
            nl = max(nl, 10)
            na = max(na, 10)
            
            elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Onda Senoidal
        # --------------------------------------------------------------------
        elif combo_efeito == "Onda Senoidal (Wave)":
            # Move horizontalmente em padrão de onda
            amplitude = tamanho_saida * 0.15 * intensidade_movimento
            shift_x = int(math.sin(angulo_rad) * amplitude)
            
            # Move verticalmente em padrão de onda defasado
            shift_y = int(math.cos(angulo_rad) * amplitude * 0.5)
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Quicar (Bounce)
        # --------------------------------------------------------------------
        elif combo_efeito == "Quicar (Bounce Physics)":
            # Simula física de quique
            # abs(sin) cria padrão de quique (sempre positivo)
            altura_pulo = abs(math.sin(angulo_rad)) * (tamanho_saida * 0.25 * intensidade_movimento)
            shift_y = -int(altura_pulo)
            
            # Squash quando toca o chão (compressão vertical)
            if abs(math.sin(angulo_rad)) < 0.1:  # Perto do chão
                fator_squash = 0.8
                nl = int(largura_orig * 1.2)  # Mais largo
                na = int(altura_orig * fator_squash)  # Mais baixo
                elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Tremor Caótico (Glitch/Shake)
        # --------------------------------------------------------------------
        elif combo_efeito == "Tremor Caótico (Glitch)":
            # Deslocamento aleatório em X e Y
            intensidade_shake = int(15 * intensidade_movimento)
            shift_x = random.randint(-intensidade_shake, intensidade_shake)
            shift_y = random.randint(-intensidade_shake, intensidade_shake)
            
            # Rotação aleatória pequena
            angulo_shake = random.uniform(-5, 5) * intensidade_movimento
            elemento_frame = elemento_frame.rotate(angulo_shake, resample=Image.BICUBIC)
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Explosão e Implosão
        # --------------------------------------------------------------------
        elif combo_efeito == "Explosão e Implosão":
            # Primeira metade: expande (explosão)
            # Segunda metade: contrai (implosão)
            if progresso < 0.5:
                fator = 1.0 + (progresso * 2) * 0.5 * intensidade_movimento
            else:
                fator = 1.5 - ((progresso - 0.5) * 2) * 0.5 * intensidade_movimento
            
            nl = int(largura_orig * fator)
            na = int(altura_orig * fator)
            nl = max(nl, 10)
            na = max(na, 10)
            elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Balanço de Pêndulo
        # --------------------------------------------------------------------
        elif combo_efeito == "Balanço de Pêndulo":
            # Oscila como pêndulo (-45° a +45°)
            angulo_pendulo = math.sin(angulo_rad) * 45 * intensidade_movimento
            elemento_frame = elemento_frame.rotate(angulo_pendulo, resample=Image.BICUBIC)
        
        # --------------------------------------------------------------------
        # MOVIMENTO: Zoom In/Out Dramático
        # --------------------------------------------------------------------
        elif combo_efeito == "Zoom In/Out Dramático":
            # Zoom exponencial (mais dramático que linear)
            # Vai de 0.5x a 1.5x
            fator = 0.5 + abs(math.sin(angulo_rad)) * intensidade_movimento
            nl = int(largura_orig * fator)
            na = int(altura_orig * fator)
            nl = max(nl, 10)
            na = max(na, 10)
            elemento_frame = elemento_frame.resize((nl, na), Image.Resampling.LANCZOS)
        
        # ====================================================================
        # Centraliza o elemento transformado no canvas
        # ====================================================================
        nl, na = elemento_frame.size
        ox = (largura_orig - nl) // 2 + shift_x
        oy = (altura_orig - na) // 2 + shift_y
        
        # Cola elemento no frame final
        frame_final.paste(elemento_frame, (ox, oy), elemento_frame)
        
        # ====================================================================
        # EFEITO: Sombra Dinâmica Projetada
        # ====================================================================
        if ativar_sombra:
            # Cria versão da sombra (imagem preta com mesma forma)
            sombra = Image.new("RGBA", elemento_frame.size, (0, 0, 0, 0))
            
            # Copia canal alpha do elemento para criar silhueta preta
            dados_elemento = elemento_frame.getdata()
            dados_sombra = [(0, 0, 0, item[3]) for item in dados_elemento]
            sombra.putdata(dados_sombra)
            
            # Desfoca a sombra
            sombra = sombra.filter(ImageFilter.GaussianBlur(radius=15))
            
            # Calcula posição da sombra (offset baseado no movimento)
            offset_sombra_x = int(math.cos(angulo_rad) * 20)
            offset_sombra_y = int(math.sin(angulo_rad) * 20) + 30  # Sempre abaixo
            
            # Posiciona sombra
            pos_sombra_x = ox + offset_sombra_x
            pos_sombra_y = oy + offset_sombra_y
            
            # Cria novo frame com sombra atrás do elemento
            frame_com_sombra = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
            frame_com_sombra.paste(sombra, (pos_sombra_x, pos_sombra_y), sombra)
            frame_com_sombra.paste(frame_final, (0, 0), frame_final)
            frame_final = frame_com_sombra
        
        # ====================================================================
        # EFEITO: Partículas Orbitais
        # ====================================================================
        if ativar_particulas:
            draw_particulas = ImageDraw.Draw(frame_final)
            centro_x = largura_orig // 2
            centro_y = altura_orig // 2
            
            # Desenha várias partículas em órbita
            for p in range(num_particulas):
                # Cada partícula tem ângulo diferente
                angulo_particula = (p / num_particulas) * 2 * math.pi + angulo_rad
                
                # Raio de órbita varia
                raio_orbit = (tamanho_saida * 0.35) + math.sin(angulo_rad + p) * 30
                
                # Calcula posição da partícula
                px = centro_x + int(math.cos(angulo_particula) * raio_orbit)
                py = centro_y + int(math.sin(angulo_particula) * raio_orbit)
                
                # Tamanho da partícula varia com movimento
                tamanho_part = 3 + int(abs(math.sin(angulo_rad + p)) * 5)
                
                # Cor da partícula (usa paleta se disponível)
                if cores_paleta:
                    cor_part = cores_paleta[p % len(cores_paleta)]
                else:
                    # Cor arco-íris se não tiver paleta
                    hue = (p / num_particulas + progresso) % 1.0
                    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                    cor_part = tuple(int(c * 255) for c in rgb)
                
                # Desenha círculo da partícula
                draw_particulas.ellipse(
                    [px - tamanho_part, py - tamanho_part, 
                     px + tamanho_part, py + tamanho_part],
                    fill=cor_part + (200,)  # Alpha 200 (semi-transparente)
                )
        
        # ====================================================================
        # EFEITO: Rastro de Movimento (Motion Blur)
        # ====================================================================
        if ativar_trail and i > 0:
            # Mistura frame atual com frame anterior
            # Cria efeito de rastro/ghost
            frame_anterior = frames[-1].copy()  # Pega último frame da lista
            
            # Blend: combina duas imagens com peso
            # alpha=0.7 significa 70% frame atual + 30% anterior
            frame_final = Image.blend(frame_anterior, frame_final, alpha=0.7)
        
        # ====================================================================
        # EFEITO: Brilho Neon (Glow)
        # ====================================================================
        if ativar_neon:
            # Cria versão borrada da imagem
            brilho = frame_final.filter(ImageFilter.GaussianBlur(radius=20))
            
            # Aumenta intensidade do brilho
            enhancer_brilho = ImageEnhance.Brightness(brilho)
            brilho = enhancer_brilho.enhance(1.5)
            
            # Aumenta saturação do brilho
            enhancer_sat = ImageEnhance.Color(brilho)
            brilho = enhancer_sat.enhance(2.0)
            
            # Sobrepõe brilho com imagem original
            # Modo 'screen' cria efeito aditivo (ilumina)
            canvas_neon = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
            canvas_neon.paste(brilho, (0, 0), brilho)
            canvas_neon.paste(frame_final, (0, 0), frame_final)
            frame_final = canvas_neon
        
        # ====================================================================
        # EFEITO: Aberração Cromática (RGB Split)
        # ====================================================================
        if ativar_aberracao:
            # Separa canais RGB e desloca cada um
            r, g, b, a = frame_final.split()
            
            # Desloca canal vermelho para direita
            offset_aberr = int(3 * intensidade_movimento)
            r = ImageChops.offset(r, offset_aberr, 0)
            
            # Desloca canal azul para esquerda
            b = ImageChops.offset(b, -offset_aberr, 0)
            
            # Recompõe imagem com canais deslocados
            frame_final = Image.merge("RGBA", (r, g, b, a))
        
        # ====================================================================
        # EFEITO: Pulso de Borda (Border Pulse)
        # ====================================================================
        if ativar_pulse_borda:
            draw_borda = ImageDraw.Draw(frame_final)
            
            # Espessura da borda oscila
            espessura_borda = int(5 + abs(math.sin(angulo_rad)) * 10)
            
            # Cor da borda (usa paleta ou branco)
            if cores_paleta:
                idx_cor = int(progresso * len(cores_paleta)) % len(cores_paleta)
                cor_borda = cores_paleta[idx_cor]
            else:
                # Cor arco-íris
                hue = progresso
                rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                cor_borda = tuple(int(c * 255) for c in rgb)
            
            # Desenha retângulo de borda
            for t in range(espessura_borda):
                draw_borda.rectangle(
                    [t, t, largura_orig - t - 1, altura_orig - t - 1],
                    outline=cor_borda + (150,)  # Alpha 150
                )
        
        # ====================================================================
        # EFEITO ESPECIAL: Tornado Cósmico
        # ====================================================================
        if combo_efeito == "Tornado Cósmico (Multi-Efeito)":
            # Pulso de brilho sincronizado
            fator_brilho = 1.0 + (math.sin(angulo_rad * 2) * 0.3)
            enhancer = ImageEnhance.Brightness(frame_final)
            frame_final = enhancer.enhance(fator_brilho)
            
            # Rotação de matiz (hue rotation)
            if not ativar_rainbow:  # Evita conflito com rainbow
                dados = frame_final.getdata()
                novos_dados = []
                for item in dados:
                    if item[3] > 0:  # Pixel visível
                        # Converte RGB para HSV
                        r, g, b = item[0] / 255, item[1] / 255, item[2] / 255
                        h, s, v = colorsys.rgb_to_hsv(r, g, b)
                        
                        # Rotaciona matiz
                        h = (h + progresso) % 1.0
                        
                        # Converte de volta para RGB
                        r, g, b = colorsys.hsv_to_rgb(h, s, v)
                        novos_dados.append((
                            int(r * 255), int(g * 255), int(b * 255), item[3]
                        ))
                    else:
                        novos_dados.append(item)
                frame_final.putdata(novos_dados)
        
        # ====================================================================
        # EFEITO: Scanlines Retrô
        # ====================================================================
        if ativar_scanlines:
            # Cria overlay de linhas horizontais
            overlay_scan = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
            draw_scan = ImageDraw.Draw(overlay_scan)
            
            # Desenha linhas a cada 3 pixels
            for y in range(0, altura_orig, 3):
                # Linha preta semi-transparente
                draw_scan.line([(0, y), (largura_orig, y)], fill=(0, 0, 0, 50))
            
            # Sobrepõe scanlines
            frame_final = Image.alpha_composite(frame_final, overlay_scan)
        
        # ====================================================================
        # EFEITO: Vinheta Cinematográfica
        # ====================================================================
        if ativar_vinheta:
            # Cria gradiente radial escuro nas bordas
            vinheta = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
            draw_vinheta = ImageDraw.Draw(vinheta)
            
            centro_x = largura_orig // 2
            centro_y = altura_orig // 2
            raio_max = math.sqrt(centro_x**2 + centro_y**2)
            
            # Desenha círculos concêntricos cada vez mais escuros
            num_circulos = 50
            for c in range(num_circulos):
                raio = (c / num_circulos) * raio_max * 1.2
                # Alpha aumenta conforme se afasta do centro
                alpha_vin = int((c / num_circulos) * 180)
                
                draw_vinheta.ellipse(
                    [centro_x - raio, centro_y - raio,
                     centro_x + raio, centro_y + raio],
                    fill=(0, 0, 0, alpha_vin)
                )
            
            # Sobrepõe vinheta
            frame_final = Image.alpha_composite(frame_final, vinheta)
        
        # ====================================================================
        # Composição Final: Adiciona Fundo
        # ====================================================================
        
        # Cria fundo baseado no tipo escolhido
        if tipo_fundo in ["Gradiente Radial Dinâmico", "Gradiente Linear Animado", 
                          "Padrão de Ruído (Noise)"]:
            # Cria fundo gradiente animado
            cor1 = hex_para_rgb(cor_fundo_primaria)
            cor2 = hex_para_rgb(cor_fundo_secundaria)
            canvas_fundo = criar_fundo_gradiente(
                largura_orig, altura_orig, tipo_fundo, 
                cor1, cor2, i, num_frames_total
            )
        elif tipo_fundo == "Totalmente Transparente":
            # Fundo transparente
            canvas_fundo = Image.new("RGBA", (largura_orig, altura_orig), (0, 0, 0, 0))
        else:
            # Fundo cor sólida
            canvas_fundo = Image.new("RGBA", (largura_orig, altura_orig), bg_color)
        
        # Compõe fundo + frame final
        canvas_fundo.paste(frame_final, (0, 0), frame_final)
        
        # Adiciona frame completo à lista
        frames.append(canvas_fundo)
    
    # ========================================================================
    # 12. COMPILAÇÃO E SALVAMENTO DO GIF
    # ========================================================================
    
    st.write("💾 Compilando GIF final...")
    
    # BytesIO: buffer de memória que simula um arquivo
    # Permite salvar GIF sem criar arquivo no disco
    gif_buffer = io.BytesIO()
    
    # Salva o GIF
    frames[0].save(
        gif_buffer,  # Destino (buffer na memória)
        format="GIF",  # Formato do arquivo
        save_all=True,  # Salvar todos os frames (não só o primeiro)
        append_images=frames[1:],  # Lista de frames adicionais (do 2º em diante)
        duration=duracao_frame,  # Duração de cada frame em milissegundos
        loop=0,  # 0 = loop infinito, 1 = roda uma vez, 2 = duas vezes, etc
        disposal=2,  # Método de descarte: 2 = restaura ao fundo (evita artefatos)
        optimize=False  # True compacta mais, mas demora (False = mais rápido)
    )
    
    # Pega bytes do GIF do buffer
    gif_bytes = gif_buffer.getvalue()
    
    # ========================================================================
    # 13. EXIBIÇÃO E DOWNLOAD
    # ========================================================================
    
    st.success("✅ GIF criado com sucesso!")
    st.subheader("🎬 Resultado Final Premium:")
    
    # Mostra o GIF na página
    st.image(gif_bytes, width=tamanho_saida)
    
    # Informações técnicas
    st.info(f"""
    **Especificações Técnicas:**
    - Resolução: {tamanho_saida}x{tamanho_saida} pixels
    - Taxa de quadros: {velocidade_fps} FPS
    - Total de frames: {num_frames_total}
    - Duração por frame: {duracao_frame}ms
    - Tamanho do arquivo: {len(gif_bytes) / 1024:.2f} KB
    """)
    
    # Botão de download
    st.download_button(
        label="📥 Baixar GIF Ultra Premium",
        data=gif_bytes,  # Conteúdo do arquivo
        file_name="animacao_ultra_premium.gif",  # Nome sugerido para salvar
        mime="image/gif"  # Tipo MIME do arquivo
    )
    
    # Dicas para o usuário
    with st.expander("💡 Dicas Profissionais"):
        st.markdown("""
        **Como obter os melhores resultados:**
        
        1. **Texto curto é melhor**: 1-3 palavras ficam mais impactantes
        2. **Combine efeitos**: Ative Neon + Partículas + Arco-íris para efeito "rave"
        3. **Paletas temáticas**: Escolha paleta que combine com sua marca
        4. **Fundos gradientes**: Criam profundidade visual
        5. **Ajuste FPS**: 30 FPS = suave, 60 FPS = ultra-suave (arquivo maior)
        6. **Movimentos sutis**: Intensidade 0.5-0.8 fica mais elegante
        7. **Vinheta + Scanlines**: Efeito cinematográfico/retrô instantâneo
        
        **Combinações Recomendadas:**
        - **Cyberpunk**: Paleta Cyberpunk + Neon + Aberração + Scanlines
        - **Tropical**: Paleta Tropical + Partículas + Arco-íris + Gradiente
        - **Clássico Elegante**: Monochrome + Vinheta + Pulsar Suave
        - **Festa**: Neon Tokyo + Arco-íris + Partículas + Tornado Cósmico
        """)

else:
    # Mensagem quando não há conteúdo para animar
    st.info("💡 Digite um texto ou envie uma imagem acima para começar!")
    
    # Exemplos para inspirar o usuário
    with st.expander("📚 Ver Exemplos de Uso"):
        st.markdown("""
        **Exemplos de Textos Impactantes:**
        - SALE (para promoções)
        - NOVO (lançamentos)
        - VIP (eventos exclusivos)
        - WOW (destaque)
        - 50% OFF (descontos)
        
        **Tipos de Imagens Recomendadas:**
        - Logos de marcas
        - Ícones
        - Emojis grandes
        - Ilustrações vetoriais
        - Fotos com fundo removido (PNG transparente)
        """)

# ============================================================================
# RODAPÉ COM INFORMAÇÕES
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎨 <b>Gerador de GIFs Ultra Premium</b> | Versão 2.0 Continental Edition</p>
    <p>Desenvolvido com ❤️ usando Python, Streamlit e PIL</p>
</div>
""", unsafe_allow_html=True)
