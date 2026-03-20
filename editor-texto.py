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
titulo = "Medalha de Honra ao Papa Leão"
categoria = "Profecia"
assinatura = "E toda a terra se maravilhou seguindo a besta..."

# 2. Cole aqui o texto bruto que você obteve da transcrição
texto_bruto = """

0:00Queridos irmãos, recebemos a notícia agora que os Estados Unidos preparam uma medalha de honra ao Papa Leão. Essa
0:1010 segundosmedalha de honra que será entregue ao Papa Leão, inclusive ele fará um discurso e designado especialmente para as
0:1919 segundoscelebrações dos 250 anos de liberdade, né, de independência da América. Não somente
0:2727 segundosisso, os Estados Unidos também prestarão uma homenagem, vão dedicar os Estados Unidos a Maria. Meus amados,
0:3737 segundoseu estou sorrindo porque nós estamos vendo os cumprimentos proféticos à nossa cara, estampados.
0:4747 segundosO que mais precisa acontecer para que eu ponha em ordem a minha casa, para que eu ponha em ordem a minha vida?
0:5757 segundospara que eu não somente decida, mas realmente morra, para que o meu eu morra completamente, porque esse ano promete,
1:071 minuto e 7 segundosmuitas coisas vão acontecer esse ano. Apertem os cintos, meus queridos.
1:141 minuto e 14 segundosSentimos o cheiro da volta de Jesus no ar.
1:191 minuto e 19 segundosMas eu não me refiro esse ano à volta de Jesus. Eu me refiro esse ano a acontecimentos proféticos contundentes.
1:281 minuto e 28 segundosAquele acontecimento profético que será o último chamado para as pessoas do mundo. E, infelizmente a porta estará se
1:371 minuto e 37 segundosfechando para os adventistas do sétimo dia para sempre. a porta da misericórdia, esse evento chamado o descanso dominical obrigatório.
1:481 minuto e 48 segundosTudo está planejado, as pessoas estão nos seus cargos,
1:531 minuto e 53 segundosos projetos já estão no na presidência dos Estados Unidos, bastando apenas
2:002 minutosapenas serem assinados ou por uma decisão de Congresso ou por uma assinatura do presidente.
2:082 minutos e 8 segundosPois a Heritage Foundation está trabalhando com isso. Uma instituição que já conseguiu que mais de 50% de suas
2:172 minutos e 17 segundospetições fossem aprovadas no governo federal e agora tem essa petição do descanso dominical apresentada ao
2:262 minutos e 26 segundosgoverno federal. Você acha que vai ser negado? Você tem acompanhado as notícias? Você está vendo as grandes
2:332 minutos e 33 segundosmovimentações? Você tá vendo a imprensa pedindo descanso dominical? Você tem observado os religiosos pedindo o
2:402 minutos e 40 segundosdescanso dominical? Você tem observado os políticos, senadores, deputados eh de
2:472 minutos e 47 segundosestados e também federais, todos unidos nesse grande movimento de descanso dominical, meus queridos, por que que é
2:552 minutos e 55 segundostão falado a questão do descanso dominical?
2:592 minutos e 59 segundosPorque o descanso dominical obrigatório será um marco profético, histórico,
3:053 minutos e 5 segundosprofético, aonde irá desencadear todas as coisas. A ruína dos Estados Unidos, financeira e econômica, a e
3:143 minutos e 14 segundosmoral, a ruína junto o mundo também, um efeito dominó. E não somente isso, além
3:203 minutos e 20 segundosdessas ruínas, virá então o decreto de morte no futuro para aqueles que se negarem a guardar os mandamentos de
3:283 minutos e 28 segundoshomens, as tradições de homens e quiserem seguir somente a Bíblia,
3:333 minutos e 33 segundosseremos acusados de tradicionalistas, de extremistas,
3:403 minutos e 40 segundoseh, toda sorte de coisa. E assim como acusaram na época medieval, na Santa
3:463 minutos e 46 segundosInquisição, entre aspas, né, acusavam pessoas inocentes de bruxaria, de canibalismo e outras coisas. Não fique
3:553 minutos e 55 segundoscom esse pensamento poético de que você será acusado, preso, levado para os
4:044 minutos e 4 segundostribunais, paraas prisões, campos de trabalhos forçados, simplesmente porque adventista não tem esse pensamento tão
4:124 minutos e 12 segundosromântico ou simplesmente porque descansa no dia do sábado, mas seremos acusados de todas as coisas, coisas que
4:214 minutos e 21 segundospodemos imaginar e coisas que não podemos nem imaginar seremos acusados. É chegado o tempo, meu querido. É chegado
4:294 minutos e 29 segundoso tempo. E eu tô vendo que muitas famílias não estão preparadas. Eu estou vendo que muitos pais não estão preparados ou filhos não estão
4:384 minutos e 38 segundospreparados. E muito a gente investe, a gente investe em educação, a gente investe em orientação, a gente investe em aconselhamento.
4:484 minutos e 48 segundosMas os corações hoje em dia estão obstinados.
4:514 minutos e 51 segundosOs corações hoje em dia não querem se submeter à palavra de Deus. Não. Existem casos que jovens, por exemplo,
5:005 minutostem aprendido que quando você eh adultera em pensamento, para Deus é pecado como se fosse o pecado de uma
5:105 minutos e 10 segundosrelação sexual e corpo a corpo real. E eu escutei uma jovem dizer que não tem
5:175 minutos e 17 segundosnada a ver, que Deus não olha assim, que é diferente o pecado do contato sexual de adultério com ah o olhar de adúltero.
5:285 minutos e 28 segundosTambém temos encontrado jovens que defendem o sexo anal. Nós temos encontrado pessoas que defendem todo
5:365 minutos e 36 segundostipo de esporte, inclusive um dos mais violentos, o esporte de futebol e o esporte de lutas, aonde o sangue jorra.
5:485 minutos e 48 segundosMeus queridos, não há mais Bíblia para essa geração. Para muitos dos nossos filhos e filhas, já não existe mais Bíblia, não existe mais nada.
5:575 minutos e 57 segundosA Bíblia agora é a mente deles e o Deus é o Deus do ventre deles. É o ventre que decide.
6:056 minutos e 5 segundosExiste pessoas que dizem que não vão de mesmo com doenças terríveis,
6:116 minutos e 11 segundosnão vão mudar de alimentação. Não toque nesse assunto, porque você só, se você tocar nesse assunto, você perderá o a
6:196 minutos e 19 segundosamizade dessa pessoa ao defender que a palavra de Deus nos diz que o corpo é o templo do Espírito Santo. É uma geração
6:286 minutos e 28 segundosrebelde, obstinada, uma geração decidida a pecar e a seguir os seus próprios caminhos.
6:356 minutos e 35 segundosa desprezar a Bíblia. Mas em breve, meus queridos, em breve a porta estará fechando. Em breve a porta da graça, a
6:436 minutos e 43 segundosporta da misericórdia vai se fechar pela e vai ser definitivo. E eu quero dizer a vocês que será tarde demais para esses
6:516 minutos e 51 segundoscrentes que têm toda sorte de luz, mas continuam nos seus caminhos rebeldes. E
6:586 minutos e 58 segundosa nós, os pais, que só nos resta interceder pelos filhos.
7:047 minutos e 4 segundosE os filhos que têm pais rebeldes, só resta aos filhos muita intercessão,
7:107 minutos e 10 segundosclamor e lágrimas. Eu tenho derramado lágrimas pela minha família e por mim mesmo. E você tem feito isso? Escreva
7:197 minutos e 19 segundosaqui nos comentários. Meus queridos, nós estamos no fim do tempo do fim. Esse ano ainda vai acontecer muita coisa. Se prepare.
7:307 minutos e 30 segundosE eu quero dizer para você que nós estamos indo paraa África.
7:347 minutos e 34 segundosDepois de passar em Cuba, lá em Cuba nós ajudamos uma família que estava com necessidade de alimentação. Nós ajudamos uma paraplégica com a cadeira de rodas.
7:447 minutos e 44 segundosNós compramos 40 lâmpadas para igrejas que estariam na escuridão por causa do embargo econômico dos Estados Unidos, o
7:537 minutos e 53 segundosembargo e de petróleo, onde eles não têm energia elétrica. Então nós compramos 40 lâmpadas para ajudar a 40 pontos de
8:018 minutos e 1 segundoevangelismo que estará acontecendo agora nas próximas semanas. Também ajudamos a 40 obreiros bíblicos a avançarem o
8:098 minutos e 9 segundosevangelho junto com a ajuda de outras de outra televisão adventista.
8:148 minutos e 14 segundosE também, queridos, ajudamos um lar de crianças a poder ter alimentação para
8:218 minutos e 21 segundosmais três, 4, 5 meses. Tudo isso fizemos com a sua ajuda, porque você entende que o tempo acabou, que chegou o momento de
8:308 minutos e 30 segundosse desprender e agora nós vamos paraa África, mas nós queremos levar Bíblias,
8:368 minutos e 36 segundosmas as bíblias são caras, tem que pagar o frete das Bíblias e nós queremos avançar. Vamos lá numa média de dezenas
8:438 minutos e 43 segundose dezenas de pastores e obreiros bíblicos e precisamos comprar essas bíblias. Se você quiser nos ajudar,
8:508 minutos e 50 segundosenvia sua doação de amor. Vamos avançar,
8:538 minutos e 53 segundosigreja. Vamos avançar em doações de amor. Vamos avançar no crescimento do caráter cristão. Vamos avançar na morte
9:039 minutos e 3 segundosdo eu. Vamos avançar na presença gloriosa de Jesus, do Espírito Santo e do Pai Celestial que habita em nós. A
9:129 minutos e 12 segundospalavra diz: "Se alguém me ama, guardará a minha palavra e eu e o meu pai viremos e nele faremos morada". O Espírito Santo
9:219 minutos e 21 segundosestará está conosco também, porque Jesus falou: "Não vos deixarei órfãos, eis que o consolador virá e ele estará e eu
9:299 minutos e 29 segundosestarei com vocês até o fim dos séculos." Meus queridos, esse é o momento não de desanimar, esse é o
9:369 minutos e 36 segundosmomento de avançar com toda a força que existe em nosso organismo.
9:439 minutos e 43 segundosE ainda o Senhor, quando essa força se acabar, o Senhor enviará ainda mais força do seu depósito celestial. Vamos
9:529 minutos e 52 segundosavançar, igreja. Existe uma igrejinha que nós estamos tentando terminar a construção lá na Tailândia. Existe
10:0010 minutostambém uma escola num país comunista que estamos tentando construir lá num país
10:0610 minutos e 6 segundosde laus, mas nós precisamos avançar e só você pode nos ajudar. Então, esteja atentos, olhos bem abertos, coração
10:1510 minutos e 15 segundosvigilante, sabendo que o tempo tá se acabando. Vamos avançar, igreja, vamos avançar.
10:2210 minutos e 22 segundosOremos como nunca oramos. Eh, leiamos a palavra de Deus como nós nunca lemos em nossa vida.
10:2910 minutos e 29 segundose morramos para o eu como nunca aconteceu em nossa vida. Ou os olhos
10:3610 minutos e 36 segundospregados no céu e os pés na terra. Que o Senhor te abençoe e te guarde. Nos vemos
10:4310 minutos e 43 segundosem nosso próximo vídeo, em nome de Jesus. Amém. E amém."""

# 3. Chame a função para gerar o arquivo .md
gerar_post_blog(titulo, categoria, assinatura, texto_bruto)
