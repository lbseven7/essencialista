import re
import os
import unicodedata
from datetime import datetime

def corrigir_nomes(texto):
    substituicoes = {
        r"Virgínia Enen": "Virgínia Essene",
        r"Teard de Shardan|Tear de Shardan|Shardan|Chardã|Teardan| Teard": "Teilhard de Chardin",
        r"Brigamiang|Brigamang": "Brigham Young",
        r"Bill Schnosl": "Bill Schnoebelen",
        r"South Lake": "Salt Lake City",
        r"Joal Col de Tibé": "Djwal Khul",
        r"Lemaitre": "Georges Lemaître",
        r"Clavius": "Christopher Clavius",
        r"Antônio Vieira": "Padre Antônio Vieira",
        r"\[risadas\]|\[música\]|'\[risadas\]'": ""
    }
    for errado, correto in substituicoes.items():
        texto = re.sub(errado, correto, texto, flags=re.IGNORECASE)
    return texto

def limpar_texto(texto):
    if not texto:
        return ""

    # 1. REMOÇÃO DE TIMESTAMPS SUJOS DO YOUTUBE (ex: 0:2525, 1:281, 1:031)
    # Remove qualquer padrão de "número : número_com_3_ou_mais_digitos"
    texto = re.sub(r'\b\d+:\d{3,}\b', '', texto)
    
    # Remove padrões de tempo curtos que NÃO sejam referências bíblicas conhecidas
    # (Geralmente timestamps de início de linha ou isolados)
    texto = re.sub(r'\b\d+:\d{2,}\b', '', texto)

    # 2. REMOÇÃO DE "SEGUNDOS/MINUTOS" E NÚMEROS ISOLADOS
    texto = re.sub(r'(Segundos|Minutos|Horas|Segundo|Minuto)\s*', '', texto, flags=re.IGNORECASE)
    
    # Remove números isolados (timestamps que sobraram sem os dois pontos)
    # Mas protege se houver um ":" por perto (referência bíblica legítima tipo 24:8)
    texto = re.sub(r'(?<!:)\b\d{1,3}\b(?!:)', '', texto)

    # 3. LIMPEZA DE VÍCIOS DE FALA
    texto = re.sub(r'\s+[eE]\s+', ' ', texto)
    texto = re.sub(r'\s+[nN]é\s+', ' ', texto)
    
    # 4. CORREÇÕES DE NOMES
    texto = corrigir_nomes(texto)
    
    # 5. FORMATAÇÃO DE PONTUAÇÃO E ESPAÇOS
    # Remove pontos e vírgulas que ficaram "soltos" após a remoção dos números
    texto = re.sub(r'\s+', ' ', texto).strip()
    texto = re.sub(r'\s+\.', '.', texto)
    texto = re.sub(r'\.+', '.', texto)
    texto = re.sub(r',+', ',', texto)

    # 6. DIVISÃO EM FRASES E CAPITALIZAÇÃO
    if not re.search(r'[.!?]', texto):
        texto += "."

    partes = re.split(r'([.!?])\s*', texto)
    frases_corrigidas = []
    
    for i in range(0, len(partes)-1, 2):
        frase = partes[i].strip()
        # Limpa resíduos de pontuação e números que sobraram no início da frase
        frase = re.sub(r'^[,\s.?!0-9]+', '', frase)
        pontuacao = partes[i+1]
        
        if frase:
            frase = frase[0].upper() + frase[1:]
            frases_corrigidas.append(frase + pontuacao)

    # 7. AGRUPAMENTO EM PARÁGRAFOS
    paragrafos = []
    bloco_atual = []
    transicoes = ["Vejam", "Agora", "No entanto", "De fato", "Mas", "Então", "Quando", "Vejo", "Portanto"]
    
    for frase in frases_corrigidas:
        comeca_transicao = any(frase.startswith(t) for t in transicoes)
        if (comeca_transicao or len(bloco_atual) >= 4) and bloco_atual:
            paragrafos.append(" ".join(bloco_atual))
            bloco_atual = [frase]
        else:
            bloco_atual.append(frase)
            
    if bloco_atual:
        paragrafos.append(" ".join(bloco_atual))
            
    return "\n\n".join(paragrafos)

def gerar_post_blog(titulo, categoria, assinatura, conteudo_sujo):
    if not os.path.exists("artigos"):
        os.makedirs("artigos")
        
    conteudo_limpo = limpar_texto(conteudo_sujo)
    data_atual = datetime.now().strftime("%Y-%m-%d")
    
    slug = titulo.lower()
    slug = unicodedata.normalize('NFD', slug).encode('ascii', 'ignore').decode('utf-8')
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    
    caminho_arquivo = os.path.join("artigos", f"{slug}.md")
    
    template = f"""---
title: "{titulo}"
date: "{data_atual}"
image: "{slug}.webp"
category: "{categoria}"
signature: "{assinatura}"
---

{conteudo_limpo}
"""
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(template)
    
    print(f"🚀 Post '{caminho_arquivo}' gerado com sucesso!")

    # --- EXECUÇÃO DO SCRIPT ---

# 1. Título do Post
titulo = ""
categoria = "Profecia"
assinatura = ""

# 2. Cole aqui o texto bruto que você obteve da transcrição
texto_bruto = """

"""

# 3. Chame a função para gerar o arquivo .md
gerar_post_blog(titulo, categoria, assinatura, texto_bruto)
