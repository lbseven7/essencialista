# import re
# import os
# import unicodedata
# from datetime import datetime

# def corrigir_nomes(texto):
#     # Dicionário de substituições: { "nome_errado": "nome_correto" }
#     substituicoes = {
#         r"Virgínia Enen": "Virgínia Essene",
#         r" Teard": "Teilhard de Chardin",
#         r"Teard de Shardan": "Teilhard de Chardin",
#         r"Tear de Shardan": "Teilhard de Chardin",
#         r"Shardan": "Teilhard de Chardin",
#         r"Chardã": "Teilhard de Chardin",
#         r"Teardan": "Teilhard de Chardin",
#         r"Brigamiang": "Brigham Young",
#         r"Brigamang": "Brigham Young",
#         r"Bill Schnosl": "Bill Schnoebelen",
#         r"South Lake": "Salt Lake City",
#         r"Joal Col de Tibé": "Djwal Khul",
#         fr"'[risadas]'": ""
#     }
    
#     for errado, correto in substituicoes.items():
#         texto = re.sub(errado, correto, texto, flags=re.IGNORECASE)
#     return texto

# def limpar_pontuacao_gramatical(texto):
#     padrao_erro = r',\s+(com|que|e|para|pelo|do|da|ao|de)\b'
#     texto = re.sub(padrao_erro, r' \1', texto, flags=re.IGNORECASE)
#     texto = re.sub(r',([a-zA-Zá-úÁ-Ú])', r', \1', texto)
#     texto = re.sub(r'\s+,', ',', texto)
#     return texto

# def limpar_texto(texto):
#     # 1. REMOÇÃO AGRESSIVA DE TEMPOS E RUÍDOS DE TRANSCRIÇÃO
    
#     # Remove formatos como "0:00O", "0:00", "0:"
#     texto = re.sub(r'\b\d+:\d{0,2}\w*', '', texto)
    
#     # Remove "minutos", "segundos" e variações grudadas
#     texto = re.sub(r'\d+\s*(minutos?|segundos?)\w*', '', texto, flags=re.IGNORECASE)
#     texto = re.sub(r'(minutos?|segundos?)\w*', '', texto, flags=re.IGNORECASE)
    
#     # Remove formatos "1 hora", "10 minutos", etc
#     texto = re.sub(r'\d+\s*(horas?|minutos?|segundos?)\w*', '', texto, flags=re.IGNORECASE)
    
#     # Remove colchetes de tempo [00:00:00]
#     texto = re.sub(r'\[\d{1,2}:\d{2}(:\d{2})?\]', '', texto)

#     # 2. LIMPEZA DE "VÍCIOS DE LINGUAGEM" E "E" PERDIDOS
#     # Remove "e" ou "né" isolados entre espaços que costumam ser pausas na fala
#     texto = re.sub(r'\s+[eE]\s+', ' ', texto)
#     texto = re.sub(r'\s+[nN]é\s+', ' ', texto)
    
#     # 3. Correção de nomes errados
#     texto = corrigir_nomes(texto)
    
#     # 4. Limpeza de pontuação e espaços excessivos
#     texto = re.sub(r'\s+', ' ', texto).strip()
#     texto = re.sub(r',+', ',', texto)
#     texto = re.sub(r'([.!?])\s*,+', r'\1', texto) # Remove vírgulas logo após . ! ou ?
#     texto = re.sub(r'\s+,', ',', texto)
    
#     # 5. Divisão em frases e Capitalização Automática
#     partes = re.split(r'([.!?])\s*', texto)
    
#     frases_corrigidas = []
#     for i in range(0, len(partes)-1, 2):
#         frase = partes[i].strip()
#         # Remove qualquer vírgula ou ponto sobrando no INÍCIO da frase
#         frase = re.sub(r'^[,\s.]+', '', frase)
#         pontuacao = partes[i+1]
        
#         if frase:
#             frase = frase[0].upper() + frase[1:]
#             frases_corrigidas.append(frase + pontuacao)
            
#     # Caso sobre uma última frase sem pontuação final
#     if len(partes) % 2 != 0 and partes[-1].strip():
#         frase_final = partes[-1].strip()
#         frase_final = re.sub(r'^[,\s.]+', '', frase_final)
#         if frase_final:
#             frase_final = frase_final[0].upper() + frase_final[1:]
#             frases_corrigidas.append(frase_final + ".")

#     # 6. Agrupamento em parágrafos (blocos de 5 frases)
#     paragrafos = []
#     bloco_atual = []
    
#     for i, frase in enumerate(frases_corrigidas):
#         bloco_atual.append(frase)
#         if len(bloco_atual) == 5 or (i + 1) == len(frases_corrigidas):
#             paragrafos.append(" ".join(bloco_atual))
#             bloco_atual = []
            
#     return "\n\n".join(paragrafos)

# def gerar_post_blog(titulo, categoria, assinatura, conteudo_sujo):
#     conteudo_limpo = limpar_texto(conteudo_sujo)
#     data_atual = datetime.now().strftime("%Y-%m-%d")
    
#     # Slug robusto (remove acentos e caracteres especiais)
#     slug = titulo.lower()
#     import unicodedata
#     slug = unicodedata.normalize('NFD', slug).encode('ascii', 'ignore').decode('utf-8')
#     slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    
#     nome_arquivo_md = f"{slug}.md"
#     # Salva na pasta 'artigos' para que o convert.js possa processar
#     caminho_arquivo = os.path.join("artigos", nome_arquivo_md)
#     nome_imagem = f"{slug}.webp"
    
#     template = f"""---
# title: "{titulo}"
# date: "{data_atual}"
# image: "{nome_imagem}"
# category: "{categoria}"
# signature: "{assinatura}"
# ---

# {conteudo_limpo}
# """
    
#     with open(caminho_arquivo, "w", encoding="utf-8") as f:
#         f.write(template)
    
#     print(f"🚀 Post '{caminho_arquivo}' gerado com sucesso!")


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
