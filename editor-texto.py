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
titulo = "Os Sete Selos"
categoria = "Profecia"
assinatura = "Estudo feito pelo Dr. Walter Veith na série Ataque Total"

# 2. Cole aqui o texto bruto que você obteve da transcrição
texto_bruto = """
Os Sete Selos e a Sala do Trono
Hoje vamos falar a respeito dos sete selos e depois vamos abordar um outro tema sobre as trombetas. Estes são assuntos importantes e pouco a pouco vamos avançar até chegar a um assunto ainda mais importante. Vamos então falar sobre alguns assuntos que têm que ver com o nosso tempo e, de modo especial, só posso dizer as coisas assim como são. Eu oro enquanto eu explico essas coisas porque há coisas estranhas, difíceis de compreender, e quem sabe as pessoas não queiram compreender; eu oro para que as pessoas não usem isso como desculpa para não assistir mais, mas que continuem a assistir até que todo o quadro fique claro.
É como um grande mosaico e tudo o que podemos fazer em uma conferência é colocar um pequeno bloco de informação na tela; parece um trabalho de retalhos. Primeiramente não entendemos todos os assuntos, mas se conseguirmos ordenar as informações até que o quadro fique mais claro, então a importância do livro de Apocalipse será perceptível e apreciada. Por isso, tenham paciência com vocês e comigo; se há assuntos que pareçam estranhos ou, quem sabe, fora do equilíbrio ou do alcance, é porque não temos toda a informação disponível.
Agora, os sete selos são tratados momentaneamente no capítulo 6, mas para preparar o terreno e o cenário para os sete selos há outros dois capítulos: o capítulo 4 e o 5. E é importante recordar que os capítulos eles mesmos não dizem nada porque os números da Bíblia foram acrescentados depois; a Bíblia não foi escrita com capítulos, ela foi escrita com blocos, assim ela não pode ser dividida em capítulos. Os números de capítulos são apenas uma forma conveniente para nós nos situarmos quando precisamos encontrar um texto.
Havendo o Cordeiro aberto um dos selos — agora, antes que ele abra um dos selos para nos dizer o que vai se passar na terra, primeiramente ele nos dá uma visão da grande sala do trono do céu, uma das visões mais ilustrativas da sala do trono do universo. Agora imaginem: estamos olhando para a sede do Poder Universal. Apocalipse 4:1 diz: "Depois dessas coisas olhei, eis que havia uma porta aberta no céu e a primeira voz como de trombeta que ouvira falar comigo disse: sobe para aqui e te mostrarei as coisas que depois destas devem acontecer". Assim que temos aqui uma visão profética e logo fui arrebatado no espírito, e eis que um trono estava posto no céu e havia alguém assentado sobre o trono.
"Mas, segundo a tua dureza e teu coração impenitente, entesouras para ti mesmo ira para o dia da ira e da manifestação do juízo de Deus" (Romanos 2:5). E o que esse texto tem que ver com o grande trono? Bem, a sala do grande trono é a sede do Rei do Universo e esse Rei do Universo é também o Juiz do universo. Então, antes que Deus nos permita olhar para o que vai acontecer nesta terra e olhar para as apostasias que virão e para as coisas terríveis que os homens vão fazer, Ele nos dá uma visão da Sua Majestade e do seu poder. Dá-nos a visão de que, apesar de parecer que o outro lado vai ganhar, é Deus quem está no controle e, finalmente, Ele será o juiz e chegará o tempo do juízo.
Então haverá um juízo, uma investigação e um pronunciamento da sentença. E quando vier esse juízo executivo, será melhor que estejamos do lado certo, porque todos devemos comparecer diante do tribunal de Cristo para que cada um receba segundo o que tiver feito por meio do corpo (Segunda Coríntios 5:10). Não se enganem, Jesus está no comando, está tudo sob o controle de Deus (Atos 17:31); um dia em que com justiça há de julgar o mundo por meio do homem que destinou e disso deu certeza a todos, ressuscitando-o dentre os mortos. Não se engane, não tenha dúvidas, Jesus um dia vai pôr fim ao pecado.
Apocalipse 4:3 diz que o que estava sentado era, na aparência, semelhante à pedra de jaspe e sardônio, e o arco celeste estava ao redor do trono e parecia semelhante à esmeralda. É inexplicável a glória que João viu ali na sala do trono de Deus. Ao redor do trono havia 24 tronos, e viu assentados sobre os tronos 24 anciãos com vestes brancas e tinham sobre suas cabeças coroas de ouro. Então aqui há 24 indivíduos assentados ao redor do trono de Deus, e do trono saíam relâmpagos, trovões e vozes; ele nem sequer consegue explicar a glória que vê, ele só vê luz e relâmpagos e a voz de Deus como um trovão. Diante do trono ardiam sete lâmpadas de fogo que são os sete espíritos de Deus.
Agora, já explicamos isso antes: há apenas um Espírito, mas o número sete representa os períodos de tempo. Deus está no controle em todas as eras, inclusive na era que vivemos agora. Mas quem são esses 24 anciãos? No Santuário Terrestre também havia 24 anciãos; nós lemos isso no livro de Primeira Crônicas 24:7. Lançaram sortes e caiu a primeira sorte sobre Joiaribe e a segunda sobre Jedaías, e são mencionados os demais; a lista dos anciãos escolhidos segue até o versículo 19: 24 anciãos. O ofício desses em seu ministério era entrar na casa do Senhor segundo lhes fora ordenado por Arão, seu pai, como o Senhor Deus de Israel lhe tinha mandado.
No Santuário Terrestre havia 24 anciãos que oficiavam com o sumo sacerdote que era Arão. Agora, se o terrestre era um tipo do celestial, então também no celestial há 24 anciãos oficiando com o Sumo Sacerdote que é Jesus. Seria interessante saber quem são, mas não nos é dito quem são, então só podemos especular algo.
Apocalipse 4:6 diz que via diante do trono como que um mar de vidro e sob essa luz magnificente em que se pode caminhar semelhante a cristal. No meio do trono e ao redor do trono havia quatro animais cheios de olhos por diante e por detrás. Quem são eles? O primeiro animal era semelhante a um leão, o segundo animal semelhante a um bezerro, o terceiro animal tinha o rosto como que de homem e o quarto animal era semelhante a uma águia que voava. Cada animal tinha para si seis asas ao redor, por dentro estavam cheios de olhos e não descansavam nem de noite nem de dia dizendo: "Santo, Santo, Santo é o Senhor Deus Todo-Poderoso, que era, e que é, e que há de vir".
Em Isaías, capítulo 6, versículo 2, temos uma outra afirmação: serafins estavam por cima dele; cada um tinha seis asas, com duas cobriam seus rostos, com duas cobriam os pés e com as outras duas voavam. Então estamos falando de querubins; esta é uma ordem de seres angélicos, são seres tão magnificentes e imponentes que João os descreve como bestas e lhes dá os atributos de um leão, de um bezerro, de um homem e de uma águia que voa. Você percebe a reverência com que estão diante de Deus; isso nos dá uma ideia da santidade de Deus.
O que eles representam? A interpretação tradicional é que o leão representa a força, o bezerro representa a resistência, o homem a inteligência e a águia que voa a rapidez. Outra interpretação é que eles refletem os atributos de Cristo: o leão é o símbolo da realeza, Jesus é o rei; o bezerro representa o que serve, é um símbolo do Cristo como servo; o homem representa a humanidade de Cristo; e a águia que voa é usada como um símbolo da divindade. Vemos na sala do trono de Deus o Cordeiro de Deus: ele é o rei, ele é o servo, ele é humano e ele é divino.
E quando os animais davam glória e ação de graças àquele que estava sentado sobre o trono para todo o sempre, os 24 anciãos se prostravam e o adoravam, lançando as suas coroas diante dele dizendo: "Digno és, Senhor, de receber glória, honra e poder porque tu criaste todas as coisas". A Bíblia é muito clara em nos dizer quem é o Criador: todas as coisas foram criadas pela palavra de Jesus Cristo.
E vi na destra do que estava sentado sobre o trono um livro escrito por dentro e por fora, selado com sete selos (Apocalipse 5:1). Vi um anjo forte bradando: "Quem é digno de abrir o livro e desatar os seus selos?". Ninguém no céu, nem na terra, nem debaixo da terra — nem uma pessoa morta pode abrir, mesmo que tenham sido pessoas boas como Abraão, o rei Davi ou Adão. Ninguém está à altura de abrir o livro nem sequer de olhar para dentro dele.
Quanto aos 24 anciãos, a Bíblia diz que quando Jesus ressuscitou dos mortos as tumbas foram abertas e as primícias se levantaram. Quando ele ascendeu aos céus, ele levou cativo o cativeiro; portanto, as pessoas que foram redimidas ao longo dos séculos ressurgiram naquele momento e foram com Jesus para o céu. A Bíblia nos diz que há alguns indivíduos no céu: Enoque foi transladado sem ver a morte; Elias foi levado em um redemoinho; e Moisés também teve uma ressurreição especial. Há várias pessoas no céu e entre eles obviamente há 24 que servem no santuário celestial.
Nenhum homem era digno de abrir os selos, mas felizmente há uma solução. Apocalipse 5:4 diz que João chorava muito porque ninguém havia sido achado digno. Se o testamento não fosse aberto, não haveria herança e estaríamos perdidos para sempre. Mas um dos anciãos disse: "Não chore, o Leão da tribo de Judá, a Raiz de Davi, venceu para abrir o livro". No meio do trono estava um Cordeiro como havendo sido morto; ele tinha sete chifres (representando poder e reinado) e sete olhos (vê através dos séculos).
Ele veio e tomou o livro da destra do que está assentado sobre o trono. Os quatro seres viventes e os 24 anciãos se prostraram diante do Cordeiro tendo harpas e salvas de ouro cheias de incenso, que são as orações dos santos. Cantavam um novo hino dizendo: "Digno és de tomar o livro porque foste morto e com o teu sangue nos compraste para Deus homens de toda tribo, língua, nação e povo". Isso desfaz todo tipo de exclusividade; você não é salvo pelo seu nascimento, nem pelo seu grupo étnico ou roupas, mas por meio da sua relação com Jesus Cristo.
O número dos que olhavam para o Cordeiro eram milhões de milhões e milhares de milhares. Temos essa visão inacreditável da cena do céu que nos mostra que vai haver uma vitória final de Jesus Cristo, por isso não temos nada a temer. Depois ele muda sua ênfase para nos dizer o que vai acontecer na terra, e os dois estão num contraste tão grande que até faz medo. Aparentemente a maior vitória de Satanás foi a sua maior derrota, quando viu Jesus pregado na cruz. Derrota aparentemente será convertida na maior vitória que o universo já viu.
Mudando da grande cena do trono para os cavalos do apocalipse: abrem-se os selos. Apocalipse 6:1 diz que ele viu alguém que cavalgava um cavalo branco e saiu como vencedor. Os períodos de tempo recapitulam as sete igrejas, mas os cavalos representam a mensagem e o anúncio do evangelho. O branco representa justiça, e ele tem um arco na mão. A primeira mensagem que saiu quando Jesus começou a sua igreja era a mensagem da salvação com poder e pureza; uma fé que conquista.
Então o segundo selo é aberto e vem um cavalo vermelho. O vermelho é a cor do sacrifício e do sangue; é o tempo de grande perseguição onde o sangue foi derramado porque Satanás está contra-atacando a mensagem do evangelho. Foi-lhe dada uma grande espada, que é a palavra de Deus; ela sai e diz uma coisa e isso causa guerra. É o tempo da perseguição romana com Nero até os tempos de Constantino, quando a perseguição era o método para se livrar do porta-voz do evangelho.
Havendo aberto o terceiro selo, olhei e eis um cavalo preto e o que estava sentado tinha uma balança na mão. Ouvi uma voz que dizia: "Uma medida de trigo por um denário e três medidas de cevada por um denário, mas não danifique o azeite e o vinho". A cor preta é oposta à branca; o trigo e a cevada tornam-se escassos, significando que a mensagem evangélica da salvação em Cristo está sob opressão. O azeite é o símbolo do Espírito Santo e o vinho é o símbolo da doutrina. O cavalo negro representa um tempo em que a palavra de Deus se torna escassa por causa do comprometimento; é o tempo em que Constantino casou o paganismo com o cristianismo.
Entraram lobos vorazes na igreja e a corrupção entrou logo no princípio. A salvação só por meio de Cristo foi substituída pela própria igreja que se pôs como mediadora; mudaram a lei de Deus para satisfazer as suas necessidades. Maria converteu-se em uma mediadora e desenvolveram muitos santos, o que vem do paganismo. Mas com Jesus Cristo não pode haver nenhum tipo de concessão; ou ele é o Senhor dos senhores ou ele não é.
Chegamos a um cavalo pálido que representa a morte; o evangelho morreu. Constantino foi o primeiro que destacadamente começou a emitir leis que restringiam a consciência do homem e o dia do sol do paganismo substituiu o sábado bíblico durante esse século de negociação. Constantino integrou ao cristianismo os enfeites exteriores dos pagãos para recomendar a nova religião. As moedas de Constantino levavam de um lado o nome de Cristo e do outro a figura do deus sol. O domingo foi recomendado por Constantino aos seus súditos tanto pagãos quanto cristãos.
Ao final, quando for aberto o último selo, então o testamento de Deus será aberto e o reino será dado ao Senhor. Isso significa que Jesus tem o controle do planeta e ele virá outra vez. Passamos pela história, somos os últimos nesta grande mensagem. Os reis da terra, os grandes, os ricos, os tribunos e todos os poderosos se esconderão nas cavernas das rochas e das montanhas, dizendo aos montes e aos rochedos: "caí sobre nós e escondei-nos". Haverá uma grande alegria entre as multidões quando o juízo vier. Você terá que estar de pé. Não seremos todos salvos; você precisa tomar uma decisão agora. Só os selados são capazes de ficar em pé. E havendo aberto o sétimo selo, houve silêncio no céu quase por meia hora. Se você considerar que isso é um tempo profético, é mais ou menos uma semana. Creio que o céu está vazio porque Cristo e seus anjos estão aqui embaixo para buscar os redimidos. Esta é uma escolha que temos que fazer. Jesus está no comando e podemos fazer parte do Seu reino. A minha oração é que todos aceitemos a salvação no único nome dado entre os homens pelo qual podemos ser salvos. 
Amém.

"""

# 3. Chame a função para gerar o arquivo .md
gerar_post_blog(titulo, categoria, assinatura, texto_bruto)
