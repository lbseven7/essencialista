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
titulo = "Trindade: Nova Luz?"
categoria = "Profecia"
assinatura = "Estudo feito pelo Pr. Dennis Priebe"

# 2. Cole aqui o texto bruto que você obteve da transcrição
texto_bruto = """
0:00A segunda nova luz é a questão da trindade. Temos um movimento antitrinitariano contemporâneo que
0:099 segundosensina que não existe terceira pessoa da divindade, que o Espírito Santo é uma força ou uma energia ou uma influência
0:1616 segundosvinda do Pai ou do Filho. Citado de alguém, a Bíblia ensina que existe apenas dois dignos de adoração.
0:2424 segundosAgora, um colorário deste ensino diz que Jesus é literalmente o filho do pai,
0:3030 segundostendo um início no tempo, quando o pai o trouxe à existência. E mais uma citação,
0:3636 segundoso Pai e o Filho são ambos divinos, mas não absolutamente iguais.
0:4242 segundosSó por aí você vê que Cristo poderia morrer, ao passo que o Pai é imortal e não pode morrer.
0:4949 segundosEm apoio a este ensino, eles apontam para nossos pioneiros de que eles ensinaram isso claramente desde a década
0:5656 segundosde 1840 até aproximadamente a década de 1890.
1:011 minuto e 1 segundoComo em todos os erros, há uma verdade na base desses ensinamentos. Após o concílio de Niceia em 325, o Partido
1:091 minuto e 9 segundosPapal assumiu o título de trinitarianos e disseram que a divindade consiste em três personalidades e uma essência ou
1:171 minuto e 17 segundossubstância e que se tornou muito filosófico e metafísico.
1:231 minuto e 23 segundosEu vou ler um trechinho do manual de instruções da Igreja Católica para confirmação. Escute cuidadosamente.
1:331 minuto e 33 segundosO filho procede do pai. por um ato do intelecto, e isso é denominado geração eterna. Pelo que não apenas queremos
1:421 minuto e 42 segundosdizer que nunca houve um tempo em que o Pai existiu sem gerar o filho, mas também que o ato de geração é um ato contínuo.
1:511 minuto e 51 segundosPortanto, este é o ensino de que não poderia haver separação entre o Pai e o Filho na terra, uma vez que isso
1:581 minuto e 58 segundosinterromperia o ato de geração. Então, o filho não existiria, o que significa que o pai não existiria,
2:052 minutos e 5 segundosuma vez que, em essência nem o pai, nem o filho poderiam existir separados um do outro.
2:152 minutos e 15 segundosDe novo, de um dos textos dos livros didáticos,
2:202 minutos e 20 segundosna formação da doutrina da trindade, o conceito da geração eterna do filho era um dos fatores essenciais e principais.
2:292 minutos e 29 segundosA doutrina da trindade foi discutida,
2:312 minutos e 31 segundosmoldada e confessada em torno do conceito da geração eterna. E isso significa que o filho procede do pai por
2:392 minutos e 39 segundosgeração, o que significa começar uma próle ou dar a luz. Ouçam novamente com atenção.
2:492 minutos e 49 segundosDeus é um espírito. Isso está citado dos livros textos novamente. Deus é um espírito e o primeiro ato de um espírito
2:572 minutos e 57 segundostraz o conhecimento de si mesmo, sua própria imagem. Esta era uma pessoa viva da mesma substância e um com o Pai, isto
3:053 minutos e 5 segundosé, Deus, o Filho. Assim o Pai gera o Filho, a palavra divina, a sabedoria do
3:113 minutos e 11 segundospai de seu amor mútuo é soprado como se fosse uma pessoa viva, um com eles e de
3:193 minutos e 19 segundossua própria substância. Isto é Deus, o Espírito Santo. Assim, o Espírito Santo,
3:243 minutos e 24 segundoso Espírito de amor procede do Pai e do Filho. Deus, o Pai, conhece eternamente a si mesmo e assim continua a gerar o
3:333 minutos e 33 segundosfilho. Três pessoas não são pessoas de verdade, mas manifestações de um Deus. O
3:403 minutos e 40 segundosFilho e o Espírito Santo não são autoexistentes. Estão me ouvindo com atenção?
3:493 minutos e 49 segundosHá alguma maravilha que nossos pioneiros rejeitaram a doutrina da trindade?
3:573 minutos e 57 segundosJN Andrew disse: "Esta doutrina destrói a personalidade de Deus e de seu filho Jesus Cristo, nosso Senhor.
4:054 minutos e 5 segundosÉ um ensino muito confuso e quase impossível de entender sobre o Pai, o Filho e o Espírito Santo.
4:174 minutos e 17 segundosE vamos defender a verdade de que existem três pessoas com o nome familiar de Deus, seria melhor usarmos o nome
4:264 minutos e 26 segundosdivindade, o nome bíblico, como Allen White sempre fez. Pois o nome Trindade carrega uma bagagem que talvez não queiramos seguir.
4:384 minutos e 38 segundosEntão, vamos dar uma olhada nos textos bíblicos. Agora existem três seres na divindade. E como podemos ter certeza?
4:464 minutos e 46 segundosEntão vamos começar no livro de Mateus.
4:494 minutos e 49 segundosMateus capítulo 28 verso 19.
4:554 minutos e 55 segundosA conclusão muito famosa do Evangelho de Mateus.
5:015 minutos e 1 segundoMateus 28 19.
5:065 minutos e 6 segundosPortanto, ide. Fazei discípulos de todas as nações, batizando-os em nome,
5:125 minutos e 12 segundosperceba, do Pai, do Filho e do Espírito Santo. O nome, a palavra nome está no
5:195 minutos e 19 segundossingular e todos os três que se seguem estão no mesmo nível.
5:255 minutos e 25 segundosUm nome com um artigo definido usado para todos os três seres.
5:315 minutos e 31 segundosOs três são Deus e ainda assim eles são um Deus. Então, esta é uma simples declaração do que isso significa e como devemos entendê-la.
5:425 minutos e 42 segundosUm,
5:435 minutos e 43 segundosah, um sujeito um sujeito plural no Antigo Testamento é usado consistentemente com um verbo no
5:515 minutos e 51 segundossingular, no primeiro capítulo de Gênesis, quando fala sobre Deus criando
5:585 minutos e 58 segundosa sua imagem, o sujeito, o verbo e os pronomes estão no plural. Há um Deus,
6:066 minutos e 6 segundosmas é usado a palavra Elohim, que é um nome plural para Deus. Então, mesmo aí
6:136 minutos e 13 segundoshá uma indicação de pluralidade, mais de um. Continuemos no Novo Testamento. João capítulo 14 verso 16.
6:256 minutos e 25 segundosJesus está dizendo a seus discípulos que alguém virá depois que ele não estiver mais com eles. E observe esta frase: "Eu
6:356 minutos e 35 segundosrogarei ao Pai e ele vos dará outro consolador para que eu fique convosco para sempre".
6:426 minutos e 42 segundosA palavra outro significa que é do mesmo tipo que Cristo. Um do mesmo tipo que
6:496 minutos e 49 segundosCristo, de igual posição e igual personalidade. Vamos a Segundo Coríntios, capítulo 13,
6:586 minutos e 58 segundosverso 14, em que Paulo conclui sua carta.
7:067 minutos e 6 segundosSegundo Coríntios, capítulo 13 e verso 14.
7:137 minutos e 13 segundosA graça do Senhor Jesus Cristo e o amor de Deus e a comunhão do Espírito Santo
7:207 minutos e 20 segundossejam com todos vós. Observem cuidadosamente três dons de três seres diferentes, cada um com um dom separado
7:297 minutos e 29 segundospara nos dar. E o mesmo pensamento é transmitido por Pedro também em Primeira Pedro,
7:367 minutos e 36 segundosprimeiro Pedro capítulo 1, verso 2, em que ele introduz sua carta com essas palavras:
7:447 minutos e 44 segundosEleitos segundo a preciência de Deus Pai em santificação do Espírito para a
7:517 minutos e 51 segundosobediência e a aspersão do sangue de Jesus Cristo, graça e paz vos sejam multiplicadas.
8:008 minutosPerceba aqui três funções de três seres de testemunhos, volume 8, página 254.
8:098 minutos e 9 segundosHá três grandes poderes no céu.
8:138 minutos e 13 segundosEm evangelismo, página 615, há três seres vivos no trio celestial.
8:218 minutos e 21 segundosPágina 616. os eternos dignitários celestiais, Deus e Cristo e o Espírito Santo. Página 617.
8:318 minutos e 31 segundosOs três maiores poderes do céu, o Pai, o Filho e o Espírito Santo. Portanto,
8:388 minutos e 38 segundosconsistentemente três seres que se relacionam conosco como Deus.
8:468 minutos e 46 segundosAgora vamos olhar para o Espírito Santo,
8:508 minutos e 50 segundosuma vez que essencialmente é dito que o Espírito Santo não é uma pessoa, mas é apenas uma essência ou um poder ou uma força ou um representante dessa força.
9:059 minutos e 5 segundosEfésios capítulo 4 verso 30. Efésios capítulo 4 verso 30.
9:139 minutos e 13 segundosE não entristeçais o Espírito Santo de Deus, no qual estais selados para o dia da redenção. Vocês notaram a expressão
9:219 minutos e 21 segundosentristecer? Você pode entristecer uma influência? Você pode entristecer algo que é intangível? Tristeza, tristeza é uma emoção.
9:319 minutos e 31 segundosVejamos Primeiro Coríntios, capítulo 12,
9:359 minutos e 35 segundosverso 11. Primeiro Coríntios, capítulo 12 verso 11.
9:429 minutos e 42 segundosAqui está falando sobre os dons que são dados, mas um só e o mesmo espírito
9:509 minutos e 50 segundosopera em todas as coisas, repartindo particularmente cada um como quer. Em outras palavras, o Espírito Santo está
9:589 minutos e 58 segundosfazendo escolhas. Não o Pai, nem o Filho, mas o Espírito Santo está escolhendo quem recebe quais dons.
10:0710 minutos e 7 segundosRomanos, capítulo 8, versos 26. Romanos 8:26.
10:1610 minutos e 16 segundosE da mesma maneira também o espírito ajuda as nossas fraquezas, porque não sabemos o que havemos de pedir como
10:2310 minutos e 23 segundosconvém. Mas o mesmo Espírito intercede por nós com gemidos inexprimíveis. O
10:3010 minutos e 30 segundosEspírito intercede aqui, não o Pai, nem o Filho. O espírito implora por nós.
10:3710 minutos e 37 segundosVoltando a Atos. Atos capítulo 16 versos 6 e 7.
10:4610 minutos e 46 segundosAtos 16 versos 6 e 7.
10:5010 minutos e 50 segundosE passando pela Fríja e pela província da Galácia, foram impedidos pelo Espírito Santo de anunciar a palavra na Ásia. E quando chegaram à Mísia,
11:0011 minutosintentavam ir para Britínia, mas o espírito não lhe permitiu.
11:0511 minutos e 5 segundosEntão aqui temos uma ordem, uma ordem do Espírito Santo para não entrarem em um certo lugar.
11:1411 minutos e 14 segundosEm Atos 15 verso 28 nos diz: "Na verdade, pareceu bem ao Espírito Santo e a nós não vos impor mais em cargo algum,
11:2611 minutos e 26 segundossenão estas coisas necessárias."
11:2911 minutos e 29 segundosEm outras palavras, aqui o Espírito Santo é referido como o mesmo tipo de personalidade que os apóstolos. O Espírito Santo diz isso e nós também.
11:3911 minutos e 39 segundosmesmo tipo de personalidade.
11:4211 minutos e 42 segundosE agora é claro a famosa história em Atos capítulo 6 verso 3 e 4. Ananias e Safira.
11:5311 minutos e 53 segundosDisse então Pedro Ananias: "Por que encheu Satanás o teu coração para que mentisses ao Espírito Santo e retivesses parte do preço da herdade? Guardando-a
12:0112 minutos e 1 segundonão ficava para ti e vendida não estava em teu poder? E por que formaste este desígno em teu coração? Não mentiste aos homens, mas para Deus. [roncando] Então,
12:1312 minutos e 13 segundosantes de tudo, Ananias e Safira mentiram para uma pessoa. Não se mente para uma influência, não se mente para um poder,
12:2212 minutos e 22 segundosmas eles mentiram para o Espírito Santo. E este Espírito Santo se chama Deus.
12:2812 minutos e 28 segundosDeus é aquele para quem eles mentiram.
12:3312 minutos e 33 segundosAlgumas frases dos escritos de Allen White. Mensagens escolhidas, volume 1,
12:3812 minutos e 38 segundospágina 344. Cristo, nosso mediador, e o Espírito Santo estão constantemente intercedendo em favor do homem. Mas o
12:4712 minutos e 47 segundosEspírito não pleiteia por nós como faz Cristo, que apresenta o seu sangue. O espírito opera em nosso coração. Perceba
12:5612 minutos e 56 segundosessas duas coisas diferentes por duas pessoas diferentes. Cristo apresenta o seu sangue e o Espírito Santo opera em nosso coração.
13:0413 minutos e 4 segundosEvangelismo 616 e 617. O Espírito Santo,
13:0913 minutos e 9 segundosque é tanto uma pessoa quanto o próprio Deus, está por esses terrenos. O Espírito Santo é uma pessoa. O Espírito Santo tem personalidade.
13:2113 minutos e 21 segundosEssas são declarações que para mim parecem muito claras tanto das Escrituras como de Ellen White, de que o
13:2913 minutos e 29 segundosEspírito Santo é um indivíduo, da mesma forma que o Pai é um indivíduo e o Filho é um indivíduo. Agora, tem uma advertência aqui.
13:4013 minutos e 40 segundosO propósito do Espírito Santo não foi o de falar de si mesmo, mas falar sobre o Pai e o Filho.
13:4813 minutos e 48 segundosEntão, nós sabemos muito pouco sobre a natureza do Espírito Santo nas Escrituras. Ellen White faz uma
13:5713 minutos e 57 segundosadvertência aqui que eu acho que precisamos ouvir claramente. Então, eu vou ler exatamente como ela retratou.
14:0414 minutos e 4 segundosIsto está em Manuscript Releases, volume 14, página 175 até 180. E aqui está o que ela disse.
14:1414 minutos e 14 segundosOs irmãos não devem sentir ser uma virtude, ficar separados, porque não vem todos os pontos de menor importância
14:2214 minutos e 22 segundosexatamente sob a mesma luz. Se nas verdades fundamentais eles estão em um acordo, não devem diferir e disputar sobre assuntos de pouca importância,
14:3314 minutos e 33 segundosdeter-se em questões confusas, que afinal não são de grande importância,
14:3814 minutos e 38 segundostem a tendência direta de afastar a mente das verdades vitais para a salvação da alma. [roncando] Devem os
14:4514 minutos e 45 segundosirmãos ser muito moderados no insistir sobre esses pontos secundários que muitas vezes eles próprios não compreendem. pontos que não sabem ser a
14:5414 minutos e 54 segundosverdade e que o conhecer não é essencial para a salvação.
14:5914 minutos e 59 segundosOnde existirem essas diferenças entre nós, os que estão de fora dirão: "Haverá tempo suficiente para crermos como vocês quando vocês puderem concordar entre si quanto ao que constitui a verdade?"
15:0915 minutos e 9 segundosAssim, os ímpios tiram vantagem das divisões e controvérsias entre os cristãos.
15:1415 minutos e 14 segundosAlguns estão sempre buscando ser originais, trazer à tona algo novo e surpreendente e não percebem a importância de preservar a unidade da fé nos laços de amor como deveriam.
15:2615 minutos e 26 segundosDevemos orar por iluminação divina e ao mesmo tempo, ser cuidadosos quanto a receber qualquer coisa denominada nova
15:3315 minutos e 33 segundosluz. Devemos ter cuidado para que, sob a capa da busca de uma nova verdade,
15:3815 minutos e 38 segundosSatanás não desvie nossa mente de Cristo e das verdades especiais para este tempo. Foi me mostrado que este é o instrumento do inimigo para levar as
15:4615 minutos e 46 segundosmentes a se debruçarem sobre algum ponto obscuro ou sem importância, algo que não é totalmente revelado ou que não é essencial para nossa salvação. Isto é
15:5415 minutos e 54 segundostransformado em tema absorvente a verdade presente quando todas as investigações e suposições só servem para tornar os assuntos mais obscuros e
16:0216 minutos e 2 segundosconfundir a mente de alguns que deveriam estar buscando a união pela santificação da verdade. Então, qual é esta questão
16:1116 minutos e 11 segundosparalela de que ela está falando e que não é essencial para a salvação? Ela nos responde: "A natureza do Espírito Santo
16:2016 minutos e 20 segundosé um mistério não claramente revelado e você nunca será capaz de explicá-lo aos outros, pois o Senhor não o revelou a
16:2716 minutos e 27 segundosvocê. Você pode agrupar as escrituras e colocar sua construção sobre elas, mas a aplicação não está correta. Não é
16:3516 minutos e 35 segundosessencial que você saiba e seja capaz de definir exatamente o que é o Espírito Santo. Há muitos mistérios que eu não procuro entender ou explicar.
16:4616 minutos e 46 segundosEles são altos demais para mim e altos demais para você. Em alguns desses pontos, o silêncio é ouro. Sua mente
16:5516 minutos e 55 segundosestá inquieta. Você cometeria o erro que muitos outros cometeram de pensar que você tem uma nova luz quando se trata apenas de uma nova fase de erro. Você
17:0317 minutos e 3 segundospode pegar certos pontos de vista da escritura e, pesquisando-a à luz de suas próprias ideias, reunir um grande número de textos e afirmar que eles significam
17:1217 minutos e 12 segundostudo isso e aquilo e pedir a qualquer um que lhe prove que seus pontos de vistas estão incorretos. Aqui está seu perigo de desviar as mentes das questões essenciais para este tempo. Ora, irmão,
17:2417 minutos e 24 segundosé a verdade que queremos e devemos ter,
17:2717 minutos e 27 segundosmas não introduza o erro como nova verdade.
17:3217 minutos e 32 segundosE este conselho se aplica a todas as novas questões de luz que estamos considerando hoje.
17:3817 minutos e 38 segundosAgora, consideremos a questão de Jesus Cristo.
17:4317 minutos e 43 segundosE vamos começar com a famosa declaração em João capítulo 1, quando João introduz seu evangelho com essas clássicas
17:5117 minutos e 51 segundospalavras sobre Jesus Cristo. João 1 verso 1. No princípio era o verbo e o
18:0018 minutosverbo estava com Deus e o verbo era Deus. Ele estava no princípio com Deus.
18:0618 minutos e 6 segundosTodas as coisas foram feitas por ele e sem ele nada do que foi feito se fez.
18:1218 minutos e 12 segundosNele estava a vida, e a vida era à luz dos homens. Aqui ele claramente diz que Jesus não estava apenas com o Pai, ele
18:2018 minutos e 20 segundosera Deus. E é errado traduzir como um Deus. Ele foi o criador de tudo. O
18:2718 minutos e 27 segundosprincípio da vida estava nele. Ele não recebeu vida de ninguém.
18:3418 minutos e 34 segundosVoltemos a João, capítulo 8, verso 58. E esta é uma declaração muito importante
18:4118 minutos e 41 segundosdo que Jesus está fazendo aqui enquanto ele é desafiado pelos líderes judeus.
18:4818 minutos e 48 segundosDisse-lhe Jesus: "Em verdade, em verdade vos digo que antes que Abraão existisse,
18:5418 minutos e 54 segundoseu sou". Bem, o que isso significa? Voltemos ao livro de Êxodo, capítulo 3,
19:0219 minutos e 2 segundosverso 14. E teremos a mesma frase que Jesus está usando aqui. Êxodo capítulo 3, verso 14.
19:1319 minutos e 13 segundosE disse Deus a Moisés: "Eu sou o que sou." disse mais assim dirás aos filhos de Israel: Eu sou me enviou a vós. Logo,
19:2619 minutos e 26 segundoso Eu sou do Antigo Testamento, Jesus está reivindicando o mesmo nome para si mesmo. Ellen White dizem o desejado,
19:3719 minutos e 37 segundospágina 469 e 470,
19:4019 minutos e 40 segundoso nome de Deus dado a Moisés para exprimir a ideia da presença eterna fora reclamado como seu. Declarara-se aquele
19:4919 minutos e 49 segundosque tem existência própria, cujas saídas são desde os tempos antigos, desde os dias da eternidade. Maravilhosa graça de
19:5819 minutos e 58 segundosDeus, página 43. Através de todas as páginas da história sagrada, nas quais o trato de Deus com seu povo escolhido se
20:0620 minutos e 6 segundosacha registrado, a indícios frisantes do grande Eu Sou.
20:1120 minutos e 11 segundosToda a comunhão entre o céu e a raça decaída tem sido por meio de Cristo.
20:1520 minutos e 15 segundosCristo é o alfa e o ômega, o primeiro e o derradeiro.
20:2120 minutos e 21 segundosEntão, sempre que lemos sobre Yahé ou Jeová no Antigo Testamento, estamos lendo sobre Cristo. Vamos só dar uma
20:2920 minutos e 29 segundosolhada em um verso no Antigo Testamento que é muito claro. Isaías capítulo 40 verso 28.
20:4320 minutos e 43 segundosIsaías 40 verso 28.
20:5320 minutos e 53 segundosNão sabes, não ouviste que o eterno Deus, o Senhor, que é Javé, o criador
21:0121 minutos e 1 segundodos fins da terra, nem se cansa e nem se fatiga? É inescrutável o seu entendimento, o Deus eterno,
21:1021 minutos e 10 segundosque é Cristo, o primeiro e o derradeiro. Do desejado,
21:1621 minutos e 16 segundospágina 530, temos esta clássica declaração: Em Cristo, a vida original, não emprestada, não derivada.
21:2521 minutos e 25 segundosEvangelismo 615. Cristo é o filho de Deus pré-existente,
21:3121 minutos e 31 segundosexistente por si mesmo. Afirma-nos que nunca houve tempo em que ele não estivesse em íntima comunhão com o
21:3821 minutos e 38 segundoseterno Deus. Ele é o existente por si mesmo, filho de Deus. Do comentário bíblico 1115.
21:4621 minutos e 46 segundosDesde toda a eternidade Cristo foi unido com o Pai. Review Herold 5 de abril de
21:5221 minutos e 52 segundos1906. Cristo era essencialmente e no mais alto sentido Deus. Estava ele com Deus desde toda a eternidade. Agora,
22:0222 minutos e 2 segundospatriarcas e profetas, página 63 e 64 nos diz que unicamente um ser igual a Deus poderia fazer expiação. Apenas o
22:1122 minutos e 11 segundoscriador poderia redimir o homem. Se em algum momento da eternidade Jesus tivesse recebido vida do Pai, se sua
22:2122 minutos e 21 segundosvida tivesse sido emprestada ou derivada do Pai, se ele fosse dependente do Pai para a sua existência? Se Deus o tivesse
22:3022 minutos e 30 segundosapontado para compor a divindade, então Jesus não seria autoexistente. Ele não seria Deus no amplo sentido. Não seria
22:3822 minutos e 38 segundoseterno, nem poderia fazer expiação pela raça caída, nem redimir a humanidade.
22:4422 minutos e 44 segundosEsta se tornaria a questão crucial ao afirmar que Cristo não possui a mesma
22:5022 minutos e 50 segundosexistência que o Pai. Se Cristo, só mais uma reflexão a respeito,
22:5722 minutos e 57 segundosse Cristo não era plenamente Deus, então Deus estaria punindo uma terça parte inocente na cruz.
23:0623 minutos e 6 segundosApenas alguém que é imortal pode oferecer vida eterna ao homem.
23:1323 minutos e 13 segundosEntão, temos a expressão o unigênito,
23:1723 minutos e 17 segundosque na verdade é uma tradução defeituosa. Ah, vamos dar uma olhada no que realmente significa. Hebreus capítulo 11,
23:2623 minutos e 26 segundosa expressão que é usada do grego e que foi traduzida como o unigênito.
23:3523 minutos e 35 segundosHebreus, capítulo 11 verso 17.
23:4323 minutos e 43 segundosPela fé, Abraão, quando foi provado,
23:4623 minutos e 46 segundosofereceu a Isaque. Sim, aquele que recebera as promessas ofereceu o seu unigênito,
23:5623 minutos e 56 segundosseu filho unigênito. Ele não era o seu unigênito.
24:0424 minutos e 4 segundosEntão, deve haver algo diferente sobre essa expressão unigênito. O que quer dizer, na verdade é exclusivo.
24:1224 minutos e 12 segundosE é isso que Isaque era. Ele não era sequer o primogênito, excepcionalmente, particularmente,
24:2024 minutos e 20 segundosalguém de um tipo único, especial. Há uma frase interessante em Atos capítulo
24:2724 minutos e 27 segundos13 verso 33, usando a mesma frase, mas falando sobre outra coisa aqui. Atos 13:33.
24:3724 minutos e 37 segundosestá está descrevendo algo muito especial sobre Jesus.
24:4624 minutos e 46 segundosAqui diz: "Deus a cumpriu a nós, seus filhos, ressuscitando a Jesus, como também está escrito no segundo salmo,
24:5624 minutos e 56 segundosmeu filho és tu. Hoje te gerei. Hoje eu te gerei. Ele foi gerado dentre os
25:0325 minutos e 3 segundosmortos. Esta é uma forma particular de dizer que Jesus é unigênito.
25:1025 minutos e 10 segundosEntão, temos duas maneiras em que a expressão unigênito é usada, não se referindo necessariamente a um começo no tempo.
25:2125 minutos e 21 segundosÉ interessante que uma mulher chamada Maria de Agreda, uma freira católica visionária em 1600, disse que a palavra foi concebida por geração eterna do Pai.
25:3425 minutos e 34 segundosque Cristo nasceu antes de existir o tempo.
25:3825 minutos e 38 segundosIsso soa um pouco com o que vimos hoje em dia daqueles que acreditam que Jesus Cristo teve um começo.
25:4625 minutos e 46 segundosAqui temos uma sugestão para manter esse assunto em algum equilíbrio e resolver o que parece ser uma contradição. A
25:5325 minutos e 53 segundosnatureza da divindade não é o tema central das escrituras, onde é discutido
26:0026 minutosrevela três seres iguais. Todos existentes desde a eternidade, sendo um em propósito, mente de maneiras
26:0826 minutos e 8 segundosimpossíveis para os seres criados. O caráter de Deus é o foco, não a natureza da divindade.
26:1826 minutos e 18 segundosA questão central nas escrituras é a função da divindade, como a divindade opera e está sempre em posição
26:2626 minutos e 26 segundosdescendente do Pai para o Filho, para o Espírito Santo. E é por isso que a divindade quer que todos os seres criados se aproximem deles dessa forma.
26:3526 minutos e 35 segundosO Pai é a autoridade suprema. O filho é o representante visível para os seres criados e o espírito é a presença invisível com todos os seres criados.
26:4926 minutos e 49 segundosMesmo entre os anjos, o Pai teve que explicar a diferença entre Cristo e Lúcifer, já que ambos tinham funções
26:5726 minutos e 57 segundossemelhantes. Eles realizavam a vontade do Pai. Então, se este assunto foi mal compreendido no céu, talvez seja fácil ver porque temos alguns problemas.
27:0827 minutos e 8 segundosCristo sempre dirige a atenção ao Pai.
27:1127 minutos e 11 segundosEle assume um papel secundário e o Espírito Santo sempre dirige a atenção ao Pai e ao Filho. E ele é quase invisível maior parte do tempo. Então,
27:2227 minutos e 22 segundosminha conclusão é que eles são iguais em natureza e atributos, mas diferentes em função e classificação no que se refere aos seres criados.
27:3527 minutos e 35 segundosA divindade escolheu-se revelar gradualmente a raça humana
27:4227 minutos e 42 segundose aparentemente essa não é uma das questões cruciais para a redenção da humanidade. No Antigo Testamento, Yahé
27:5127 minutos e 51 segundosera o nome pessoal de Deus e o nome é intercambiável para o Pai e o Filho. O espírito era virtualmente desconhecido.
27:5927 minutos e 59 segundosHá indicações de pluralidade na divindade no livro de Gênesis.
28:0428 minutos e 4 segundosMas a ênfase é sempre em um Deus com o nome de Yahé.
28:0928 minutos e 9 segundosNo testamento, Cristo é revelado como a palavra de Deus ou o filho de Deus. E o Espírito Santo é revelado como
28:1728 minutos e 17 segundosconsolador ou advogado, com ênfase em três seres, em uma divindade,
28:2328 minutos e 23 segundosdescendendo em posição e função do Pai para o Filho e para o Espírito Santo.
28:3228 minutos e 32 segundosOs pioneiros adventistas estavam preocupados com o santuário e os 2300 dias, com a Bíblia acima da tradição, o
28:4028 minutos e 40 segundossétimo dia, o sábado, não havia muito estudo ou revelação sobre a trindade, três seres na divindade.
28:4928 minutos e 49 segundosE a trindade, no início de 1800, era uma mistura de Bíblia, filosofia medieval e os concílios da Igreja Primitiva. Havia
28:5728 minutos e 57 segundosum grupo chamado Conexão Cristã, que a trindade era católica e não bíblica. É interessante que José Beites e Thiago White foram membros da conexão cristã,
29:0929 minutos e 9 segundosporque a trindade aparentemente tornava o pai e o filho idênticos. Ela foi rejeitada por nossos pioneiros,
29:1729 minutos e 17 segundoslembrando novamente aquela falsa visão de Trindade. Eis o que José Beates disse a respeito da Trindade. Concluí que era
29:2629 minutos e 26 segundosuma impossibilidade para mim acreditar que o Senhor Jesus Cristo, filho do Pai, era também o Deus todo-pereroso, o Pai,
29:3329 minutos e 33 segundosum e o mesmo ser. Eu disse ao meu pai,
29:3629 minutos e 36 segundosse você pode me convencer de que nós somos um em essência, que você é o meu pai e eu sou o seu filho e que também eu sou o seu pai e você meu filho, então eu
29:4529 minutos e 45 segundosposso acreditar na trindade. Começamos a ver um pouco porque este era um assunto tão desconfortável para nossos pioneiros.
29:5529 minutos e 55 segundosE Deus aparentemente ficou satisfeito em deixar as coisas assim até a década de 1890. Lembre-se de que essa foi a época
30:0330 minutos e 3 segundosem que a última geração estava para ser formada. Ben White estava na Austrália.
30:0830 minutos e 8 segundosWW Prescott a visitou lá. Ele desenvolveu um novo estilo de evangelismo baseado na justificação pela fé e no caráter de Deus. Essencialmente
30:1630 minutos e 16 segundosa mensagem de 1888. Ele passou um tempo trabalhando com Ellen White e começou a questionar alguns dos ensinos dos pioneiros sobre a deidade de Cristo e a
30:2530 minutos e 25 segundosdivindade. E Eid Daniels, então presidente ali apoiou esta nova direção,
30:3130 minutos e 31 segundosao mesmo tempo em que Ellen White organizou o desejado de todas as nações,
30:3530 minutos e 35 segundosem que ela discordava fortemente dos nossos pioneiros sobre a pré-existência de Cristo. Emel Andresson tinha acabado
30:4330 minutos e 43 segundosde se tornar adventista 4 anos antes e ele disse que alguns líderes duvidavam que Allen White tivesse realmente escrito não emprestada, não derivada a respeito de Cristo no original.
30:5530 minutos e 55 segundosEm 1902, ele fez uma viagem especial à Califórnia, onde ela estava aposentada,
31:0131 minutos e 1 segundopara investigar o que ela de fato havia escrito. E ele encontrou estas declarações em sua própria caligrafia. E assim para ele que resolveu a questão.
31:1131 minutos e 11 segundosDevido à sua influência e o novo estudo sobre a divindade, a teologia adventista sobre a divindade tomou uma direção
31:1731 minutos e 17 segundosdiferente de nossos pioneiros nesse assunto.
31:2331 minutos e 23 segundosPor que tão tarde? Por que esperar até a década de 1890? Eu acredito que Deus tinha uma ordem de prioridade para
31:3031 minutos e 30 segundosintroduzir a verdade em nossa nova igreja. E ele fez isso gradualmente. Na década de 1840, o assunto era publicar,
31:3831 minutos e 38 segundosdivulgar e publicar. Era divulgar a palavra. Em 1850, o foco foi a organização da igreja. Na década de
31:4731 minutos e 47 segundos1860, foi a reforma da saúde. Na década de 1880, foi a justificação pela fé.
31:5431 minutos e 54 segundosDeus acompanhou a introdução de uma nova verdade para preservar a unidade em sua igreja. E o caráter de Deus tinha uma
32:0332 minutos e 3 segundosprioridade muito maior do que a natureza de Deus.
32:0832 minutos e 8 segundosAgora, alguns estão defendendo um retorno à posição antitrinitariana dos pioneiros.
32:1532 minutos e 15 segundosA parte mais perigosa é a questão levantada por um de seus principais defensores. Se Ellen White realmente
32:2232 minutos e 22 segundosescreveu tudo o que foi publicado, tudo que leva a sua assinatura. Veja, sempre que encontramos algo em seus escritos que contradizem nossas crenças,
32:3132 minutos e 31 segundosencontramos alguma razão aceitável para colocá-la de lado, que é o coração da alta crítica.
32:3932 minutos e 39 segundosIsso torna seus escritos sem efeito.
32:4232 minutos e 42 segundosNossas crenças têm prioridade sobre a inspiração.
32:4632 minutos e 46 segundosO que é a essência das igrejas de Babilônia? Aqui está uma declaração de alguém.
32:5332 minutos e 53 segundosEllen White foi inspirada em quase todos os seus escritos, mas ela ou alguém mexeu nos seus escritos.
33:0333 minutos e 3 segundosEntão todos vão escolher o que estiver de acordo com suas opiniões.
33:1033 minutos e 10 segundosTalvez até os adventistas conservadores terão que escolher entre a autoridade de Deus e a autoridade dos homens. M.

"""

# 3. Chame a função para gerar o arquivo .md
gerar_post_blog(titulo, categoria, assinatura, texto_bruto)
