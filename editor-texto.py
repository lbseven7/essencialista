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
titulo = "A História Perdida"
categoria = "Profecia"
assinatura = ""

# 2. Cole aqui o texto bruto que você obteve da transcrição
texto_bruto = """
Então eu vou te contar uma boa história.
0:033 segundosAmém. Você está animado? Amém. Vamos orar. Pai celestial nos abençoe. Ao olharmos para a história da
0:1212 segundosBíblia, em nome de Jesus oramos. Amém. Amém. Então, mais uma vez,
0:1818 segundosquantos de vocês gostam de boas histórias? Louvado seja o Senhor. Você sabia que os discípulos perderam a história da Bíblia?
0:2727 segundosE ah, foi só quando Jesus, após sua ressurreição, estava neste caminho para Emaús, com esses dois discípulos, que
0:3636 segundosele começou a mostrar a eles algo que eles tinham perdido, porque o que eles tinham perdido era a história da Bíblia.
0:4545 segundosE quando eles entenderam a história da Bíblia, adivinha qual foi o resultado?
0:5050 segundosavivamento. J reforma o queima no coração. Queima no coração. E assim esta
0:5656 segundosnoite queremos ah entender a história da Bíblia. Eu amo uma boa história. Então
1:051 minuto e 5 segundosesta noite vamos olhar para a história da Bíblia e a mensagem se intitula o quarto decreto. Agora e vamos começar
1:131 minuto e 13 segundosnossa história no livro de Daniel. Então eu convido você a abrir comigo, se puder, Daniel capítulo 5. Daniel
1:201 minuto e 20 segundoscapítulo 5. E vamos olhar para a história de Belsazar e a escrita na
1:291 minuto e 29 segundosparede. Quantos de vocês estão familiarizados com essa história? Tudo bem. Então eu quero que você confira isso em Daniel 5, começando com o versículo 1.
1:391 minuto e 39 segundosBelsazar, o rei, fez um grande banquete. Agora, Belsazar é o rei de quê?
1:441 minuto e 44 segundosBabilônia. E Babilônia é um poder ante Deus. Amém. Então, aqui está Belsazá, o rei da Babilônia. A Bíblia diz aqui:
1:521 minuto e 52 segundos"Ele fez um grande banquete para mil de seus príncipes e bebeu vinho diante dos mil. E Belsazar, enquanto provava o
2:002 minutosvinho, ordenou que trouxessem os vasos de ouro e prata que seu pai, Nabuco Donozor, havia tirado do templo que estava em
2:082 minutos e 8 segundosJerusalém, para que o rei e seus príncipes, suas esposas e suas concubinas pudessem beber neles. Então,
2:152 minutos e 15 segundoso que está acontecendo aqui é que Belsazar, lembre-se, a Babilônia havia levado os judeus cativos e também havia levado os vasos sagrados de Deus.
2:262 minutos e 26 segundosE assim, Belçazar pega esses vasos sagrados de Deus fora do lugar onde ele os guarda e ele traz esses vasos
2:342 minutos e 34 segundossagrados para essas câmaras. Porque o que ele está prestes a fazer é, na verdade, zombar do Deus do
2:422 minutos e 42 segundoscéu. Certo? Agora vamos continuar lendo o versículo 3. Então trouxeram os vasos de ouro que haviam sido tirados do templo da casa de
2:502 minutos e 50 segundosDeus que estava em Jerusalém. E o rei e seus príncipes, suas esposas e suas concubinas beberam neles. Eles beberam vinho e louvaram os deuses de ouro, de
2:582 minutos e 58 segundosprata, de bronze, de ferro, de madeira e de pedra. Agora pause aqui porque Bazar está realmente
3:053 minutos e 5 segundossendo, quer dizer, ele está simplesmente desafiando Deus. Deixa que eu te contar o porquê.
3:113 minutos e 11 segundosPorque bem, nesta hora algo está acontecendo do lado de fora, das muralhas da Babilônia. Há um homem chamado
3:203 minutos e 20 segundosCiro. E Ciro e todo o seu exército estão cercando a cidade da Babilônia. Mas Bazar por dentro não se importa porque a
3:283 minutos e 28 segundosBabilônia tem muros que são impenetráveis. Ela está situada sobre o rio Eufrates e Belsazar está basicamente
3:363 minutos e 36 segundosnão apenas zombando de Deus, mas também zombando de Ciro. Você não vai conseguir entrar aqui. Esta cidade é muito bem fortificada.
3:443 minutos e 44 segundosEles estavam de fato tentando cercar a Babilônia, mas a Babilônia tinha suprimentos suficientes para suportar o
3:523 minutos e 52 segundoscerco. E assim Bazar, seguro em seu domínio, está zombando do Deus do
3:593 minutos e 59 segundoscéu. Mas ele não sabe de algo sobre Ciro. Deixa eu compartilhar com você. Vá comigo se puder. Mantenha seu lugar aqui em Daniel. Vamos abrir o livro de
4:074 minutos e 7 segundosIsaías, Net capítulo 44. Vamos ler algo sobre Ciro. Isaías. Com licença,
4:144 minutos e 14 segundoscapítulo 44. E vamos ver o que a Bíblia nos diz aqui.
4:224 minutos e 22 segundosIsaías 44, começando com o verso 27.
4:274 minutos e 27 segundosIsaías 44, verso 27. Vamos voltar ao verso 26.
4:314 minutos e 31 segundosE a Bíblia diz que confirma a palavra de seu servo, que realiza o conselho de seus mensageiros, que diz a Jerusalém:
4:394 minutos e 39 segundos"Serás habitada e as cidades de Judá serás edificada, e eu levantarei os lugares em ruínas dela, que diz ao
4:484 minutos e 48 segundosabismo: Seca-te, e eu secarei os teus rios, que diz de Ciro. Ele é meu pastor e realizará todo o meu prazer, até dizendo a Jerusalém:
4:594 minutos e 59 segundos"Serás edificada e ao templo teu fundamento será lançado". Capítulo 45.
5:065 minutos e 6 segundosAssim disse o Senhor ao seu ungido Assiro, cuja mão direita eu segurei para subjugar nações diante dele, eu solto os
5:135 minutos e 13 segundoslombos dos reis para abrir diante dele as portas de duas folhas e as portas não serão fechadas.
5:225 minutos e 22 segundosFoi profetizado sobre Ciro que ele abriria as portas que protegiam a cidade de Babilônia. Os dois saem dos portões.
5:295 minutos e 29 segundosA Bíblia diz que Ciro secará o abismo e o em essência entrará em Babilônia e permitirá que o
5:375 minutos e 37 segundospovo de Deus, os judeus sejam libertados.
5:435 minutos e 43 segundosBem, isso é exatamente o que acontece, porque como diz a história, um dos cavalos favoritos de Ciro, na
5:505 minutos e 50 segundosverdade, seu cavalo favorito, afogado no rio Eufrates, e ele estava tão bravo com
5:575 minutos e 57 segundoso rio que decidiu secar o abismo. E assim eles começaram a construir, sabe, colocando pedras nos
6:046 minutos e 4 segundosrios para desviar as águas. E quando eles fizeram isso, descobriram que os portões tinham sido deixados destrancados.
6:146 minutos e 14 segundosE assim Siro e seu exército marcharam pelo leito do rio. Eles em essência desceram ao fundo, foi o que acabamos de ler. E marcharam pelo leito do rio,
6:246 minutos e 24 segundosabriram os portões e entraram na cidade,
6:266 minutos e 26 segundosa cidade que o rei da Babilônia pensava que estava seguro. Então, volte comigo, porque bem na hora em que isso está acontecendo,
6:366 minutos e 36 segundosrepare comigo. Capítulo 5 de Daniel. Estamos voltando ao capítulo 5 de Daniel. E eu quero que você repare no que acontece
6:446 minutos e 44 segundosaqui. Verso 5. Na mesma hora apareceram dedos de uma mão de homem e escreveram em frente ao candelabro na parede
6:516 minutos e 51 segundosrebocada do palácio do rei. E o rei viu a parte da mão que escreveu. E você se lembra? A Bíblia diz que a expressão do
6:586 minutos e 58 segundosrei o mudou e os seus quadris estavam
7:067 minutos e 6 segundossoltos. Ah, cara, eu não sei se você sabe o que isso significa. Seus quadris estavam
7:137 minutos e 13 segundossoltos, mas não fique pensando muito nisso. Colocando de outra forma, ele estava realmente assustado e perdeu a
7:217 minutos e 21 segundosfunção de si mesmo e os seus quadris estavam soltos,
7:277 minutos e 27 segundosdiz a Bíblia, e os joelhos dele batiam um no outro.
7:327 minutos e 32 segundosÓ, cara, ele está com medo. Ele está com medo e então ele não entende o que está
7:397 minutos e 39 segundosacontecendo, o que essa escrita significa. Então ele chama Daniel,
7:437 minutos e 43 segundoscerto? E repare no que Daniel diz. Vá comigo. Daniel capítulo 5 verso 25.
7:507 minutos e 50 segundosDaniel vai dizer a ele o que foi escrito, porque ele não entende a escrita. E diz assim: "Esta é a escrita que foi escrita. Menem mene e eu
7:587 minutos e 58 segundosfararcina". Esta é a interpretação da coisa. Menny, Deus contou o teu reino. E o quê? E o quê? Terminei. Tequel, você foi pesado na balança e achado em falta.
8:108 minutos e 10 segundosPeres, né? Teu reino está dividido e dado aos medos e peças. Crio, naquela noite derruba Babilônia. Agora vire comigo em suas Bíblias para o livro de Donos Crônicas,
8:218 minutos e 21 segundoscapítulo 36. Que livro estamos indo? Dois Crônicas, capítulo 36.
8:298 minutos e 29 segundosQuando você chegar lá, diga amém. Dois Crônicas, capítulo 36. E nós vamos dar uma
8:378 minutos e 37 segundosolhada nos versos 22 e 23. Agora, no primeiro ano de Ciro, rei da Pérsia, a palavra do Senhor falada
8:448 minutos e 44 segundospela boca de Jeremias poderia ser cumprida. O Senhor despertou o espírito de Ciro, rei da Pérsia, para que ele fizesse uma proclamação. Agora, no quê,
8:528 minutos e 52 segundospessoal? proclamação em todo o seu reino e também a colocou por escrito, dizendo assim: "Assim diz Ciro, rei da Pérsia,
9:019 minutos e 1 segundotodos os reinos da terra, o Senhor Deus do céu me deu e me encarregou de construir em sua casa em Jerusalém, que
9:099 minutos e 9 segundosestá em Judá. Quem está entre vocês de todo o seu povo, que o Senhor, seu Deus, esteja com ele e deixe-o fazer o quê?
9:169 minutos e 16 segundosDeixe-o subir. Deixe-o subir. Há uma
9:249 minutos e 24 segundoshistória. Há uma história. Por onde eu
9:359 minutos e 35 segundoscomeço? Babilônia é um poder antius. E agora você pode estar se perguntando, pastor, eu sei o que você tem nos dito,
9:449 minutos e 44 segundosque Cristo está em todas as escrituras. Eu quero que você confira isso. Babilônia,
9:559 minutos e 55 segundosSatanás, você sabia que Babilônia é realmente controlada por
10:0210 minutos e 2 segundosSatanás? O rei da Babilônia não é ninguém menos que o próprio Satanás.
10:1010 minutos e 10 segundosSim. Então, eu quero que você leve essa história em consideração e eu quero que você se pergunte, houve alguma vez em
10:1710 minutos e 17 segundosque o verdadeiro rei da Babilônia pegou algo que pertencia ao Deus do céu e decidiu zombar disso?
10:2410 minutos e 24 segundosou ele diante do universo que observa, essa pessoa não seria ninguém
10:3210 minutos e 32 segundosmenos que Jesus Cristo. Agora eu quero que você se lembre disso, porque enquanto Belsazar está
10:4110 minutos e 41 segundoszombando, ele acredita que seu reino está
10:4810 minutos e 48 segundosseguro. Enquanto Satanás zomba de Jesus diante do universo que observa, ele
10:5410 minutos e 54 segundospensa que conseguiu vencer Jesus, mas ele mal percebe
11:0411 minutos e 4 segundosalgo. Você vê, Satanás está levando Jesus para fora das muralhas de Jerusalém. O que significa que
11:1211 minutos e 12 segundosJesus está saindo das muralhas da cidade? as muralhas da cidade.
11:2111 minutos e 21 segundosÓ, você não está me entendendo. Mal sabe Satanás que o homem quem ele está levando para fora das
11:2811 minutos e 28 segundosmuralhas da cidade não era ninguém menos que um tipo de Ciro.
11:3911 minutos e 39 segundosOk? Você se lembra quando estávamos lendo sobre Ciro agora h pouco? E a Bíblia diz o sobre Siro, que ele era o
11:4711 minutos e 47 segundosungido de Deus. Mas você percebe que essa palavra ungido significa Messias. Ciro não era o
11:5611 minutos e 56 segundosMessias. Ele foi chamado de ungido de Deus. Mas o que Ciro iria fazer seria um símbolo ou um tipo do que Jesus Cristo mesmo iria fazer. Então você diz:
12:0512 minutos e 5 segundos"Pastor, o que você quer dizer?" Lembre-se do que Ciro fez.
12:1012 minutos e 10 segundosSiron ia penetrar o domínio do inimigo. E a maneira como ele ia fazer isso era descendo ao profundo. Ah! Ah!
12:2312 minutos e 23 segundosAh!
12:2812 minutos e 28 segundosAssim como Ciro secou o profundo e desceu, por assim dizer, e abriu, ó,
12:3712 minutos e 37 segundosportões. Então Jesus Cristo, o homem que estava sendo crucificado fora das muralhas da cidade de Jerusalém, desceu ao domínio do inimigo,
12:5012 minutos e 50 segundosaquele chamado domínio impenetrável, secar o
12:5612 minutos e 56 segundosprofundo para libertar os cativos livres.
13:0613 minutos e 6 segundosMas espere, tem mais. Porque lembre-se, quando
13:1213 minutos e 12 segundosquando Belsazar vê essa escrita na parede, essa mão invisível, parte das
13:2013 minutos e 20 segundospalavras que foram escritas eram essas.
13:2513 minutos e 25 segundosestá consumado. Teu
13:3413 minutos e 34 segundosreino. Belsazar está consumado. Foi o sinal da morte. E uau! Uau! Você sabe no que que estou pensando agora? Quando
13:4213 minutos e 42 segundosCristo morreu na cruz, ele gritou:
13:4613 minutos e 46 segundos"Está consumado".
13:5213 minutos e 52 segundosVocê pode se lembrar que havia uma mão invisível. Você percebe que quando Jesus
14:0014 minutosmorreu, havia uma mão invisível que rasgou o véu do templo. Eu quero que você ouça essas palavras. Comentário bíblico, volume 5,
14:1214 minutos e 12 segundospágina 1 e 109. Ouça o que diz. Não foi a mão do sacerdote que rasgou de cima para baixo o magnífico véu que dividia o santo do santíssimo? Foi a mão de Deus.
14:2314 minutos e 23 segundosQuando Cristo gritou, está consumado o santo vigilante, que era um convidado invisível na festa de Belsazar.
14:3414 minutos e 34 segundosDeclarou a nação judaica como uma nação sem igreja, a mesma mão que traçou na parede os caracteres que registraram a
14:4214 minutos e 42 segundoscondenação de Belsazar e o fim do reino babilônico. Rasgou o vé do templo de cima para
14:4914 minutos e 49 segundosbaixo. Quais são as chances de que a ela comparasse aquele incidente na cruz com o que aconteceu?
15:0715 minutos e 7 segundosAh, havia um, você se lembra quando Jesus morreu,
15:1215 minutos e 12 segundoscerto? E e havia um selo romano colocado sobre seu túmulo para ter
15:2515 minutos e 25 segundoscerteza que a porta da morte não seria aberta.
15:3015 minutos e 30 segundosVeja, o selo de Roma era realmente um símbolo de um selo muito maior, o selo de Satanás. E um selo significa não toque,
15:3815 minutos e 38 segundosnão mova, não perturbe, não mude. Certifique-se de que Cristo permaneça no
15:4515 minutos e 45 segundostúmulo. Era como se Satanás estivesse dizendo, certifique-se de que ele permaneça no túmulo. Então, selar esse
15:5315 minutos e 53 segundosselo com um selo romano. Então, você sabe o que eu gosto? Eu gosto de como em Mateus 28 versículo 1. A Bíblia diz que um selo representa autoridade, certo?
16:0316 minutos e 3 segundosEntão, a autoridade de Satanás mantenha o no túmulo. Você se lembra? Roma é um símbolo de Satanás no livro do Apocalipse. Mantenha a no túmulo. Então,
16:1316 minutos e 13 segundoso anjo desce na manhã de domingo e olha para o selo de autoridade.
16:1716 minutos e 17 segundosÓ, este é o seu selo de autoridade. É. E ele o rola para fora do caminho. E para piorar a situação, ele
16:2516 minutos e 25 segundosse senta
16:2716 minutos e 27 segundos[Aplausos]
16:3116 minutos e 31 segundosem sinalizando o poder e a autoridade do céu sobre as portas da morte e do inferno. Então, Cristo, amados, abriu as
16:4016 minutos e 40 segundosportas para que seu povo pudesse ser libertado. Então, a pergunta que eu tenho para nós hoje é: por que ainda estamos vivendo na tumba?
16:5016 minutos e 50 segundoscomo se a pedra ainda estivesse lá. Amados, ouçam-me. Cristo não nos libertou apenas para que pudéssemos seguir com nossas vidas. Não, não, não,
17:0017 minutosnão, não. Veja, quando Ciro libertou os cativos, ele os libertou para fazer algo. E esse algo era voltar para Jerusalém para reconstruir a cidade de Deus.
17:1217 minutos e 12 segundosÓ, ó, ó, ó. Você, você.
17:1517 minutos e 15 segundosHavia uma missão, havia um propósito. Qual era essa missão? Ouça.
17:2017 minutos e 20 segundosLembra como lemos em Crônicas? Como ele fez esse fez esse decreto? Bem, o decreto está, na verdade, encontrado no próximo livro da Bíblia, que é o livro de Esdras. Você pode abrir lá comigo,
17:3117 minutos e 31 segundosfala comigo rapidamente, se puder. Livro de Esdras. Esdras. E vamos olhar para o
17:3817 minutos e 38 segundoscapítulo de Esdras, capítulo 1. E vamos dar uma olhada no versículo. Esdras,
17:4317 minutos e 43 segundoscapítulo 1. E vamos olhar vamos do versículo 1 ao tr. Esdras, capítulo 1.
17:4917 minutos e 49 segundosAgora, no primeiro ano de Ciro, rei da Pérsia, para que a palavra do Senhor pudesse ser cumprida, conforme falado pela boca de Neemias, o profeta. O
17:5817 minutos e 58 segundosSenhor despertou o espírito de Siro, rei da Pérsia. Ele faz esse decreto sob este decreto. Este decreto, ouça com atenção,
18:0618 minutos e 6 segundoseste decreto foi feito para permitir que os filhos de Israel retornassem a Jerusalém para construir o templo. Para construir o quê, pessoal? O templo.
18:1518 minutos e 15 segundosCertos. Esse era todo o foco. Desculpe, sim. Para construir o templo. Isso mesmo. Agora houve outro
18:2318 minutos e 23 segundosdecreto dado. Você sabia que esse decreto foi dado por Ciro? Mas houve um segundo decreto dado. E a propósito, sob
18:3018 minutos e 30 segundoseste decreto, 50.000 judeus deixaram a Babilônia para ir construir o templo. Havia outro decreto também
18:3718 minutos e 37 segundosencontrado no livro de Esdras. Esse decreto foi dado por Dário e esse decreto foi contra os inimigos do povo de Deus que estavam tentando impedi-los
18:4518 minutos e 45 segundosde reconstruir o templo. Mas houve um terceiro decreto que foi dado no mesmo livro, Esdras. E esse decreto foi dado por Artaxerches em 457 an.
18:5718 minutos e 57 segundosEsse decreto tratava não apenas do templo, mas também da cidade. E também deu a Israel autonomia como seu próprio
19:0519 minutos e 5 segundospaís independente, uma nação novamente. Você está comigo até aqui?
19:1019 minutos e 10 segundosIsso tudo está em qual livro, pessoal? O livro de Esdras. Agora havia mais um decreto. Você sabia disso? Esse decreto é encontrado no próximo livro da Bíblia,
19:2019 minutos e 20 segundosque é o livro de Neemias. Neemias recebeu um decreto final. E esse também foi dado por
19:2719 minutos e 27 segundosArtaxerches. Foi cerca de 13 anos depois. E a razão para isso é a seguinte, porque o trabalho que havia
19:3519 minutos e 35 segundossido feito sobre os primeiros três decretos estava incompleto. Então Neemias teve que aparecer e ele viu que o trabalho não estava terminado e ele recebe um decreto final de artaxerches.
19:4719 minutos e 47 segundosEle vai para Jerusalém.
19:4919 minutos e 49 segundosEle volta para Jerusalém para ajudar a reconstruir especificamente o muro e as
19:5619 minutos e 56 segundosruas. E esses são os quatro decretos. Na verdade, Neemias quando chegou a Jerusalém disse: "Escutem, ele disse aos
20:0420 minutos e 4 segundosjudeus: "Vocês não sabem disso? Enquanto esse trabalho permanecer desolado, somos uma reprovação para
20:1120 minutos e 11 segundosDeus. Vamos nos levantar e terminar o trabalho, igreja, organizar.
20:1920 minutos e 19 segundosE alguém diz, digamos, eu quero que você diga, vamos juntar tudo. Precisamos nos organizar. Quantos acreditam que precisamos nos organizar? Tudo bem, eu
20:2820 minutos e 28 segundosadoro uma boa história, mas sabe o que eu odeio em boas histórias? Eu odeio quando boas
20:3520 minutos e 35 segundoshistórias são interrompidas. E agora vamos colocar essa história em pausa. Então, apenas pause aí. Onde estamos pausando? Em que livro estamos?
20:4520 minutos e 45 segundosNemias. Vamos pausar bem aqui. Agora eu quero contar a história. É a história da
20:5420 minutos e 54 segundosBíblia. É uma história incrível, mas para contar a história da Bíblia, precisamos ir ao livro de Gênesis.
21:0121 minutos e 1 segundoEntão, você está pronto para ir ao livro de Gênesis? Não abram suas Bíblias,
21:0521 minutos e 5 segundosapenas foquem em mim. Tudo bem? Então, para onde estamos indo, pessoal? Gênesis. Tudo bem? Muito bom.
21:1321 minutos e 13 segundosAgora, o livro de Gênesis nos apresenta a um homem chamado Adão. Amém. O livro de Gênesis nos apresenta a criação do homem,
21:2321 minutos e 23 segundosAdão. Mas a Bíblia diz que Adão é, na verdade, o primeiro Adão. Você sabia que Jesus Cristo foi o segundo Adão? Amém.
21:3221 minutos e 32 segundosEntão você tem no livro de Gênesis, você tem a gênese do primeiro homem, mas na verdade a gênese do primeiro homem é meio que um símbolo ou tipo da gênese do
21:4121 minutos e 41 segundossegundo Adão. Amém. Alguém está animado? Não, realmente, né? É tipo,
21:4921 minutos e 49 segundostudo bem. Qual livro vem depois de Gênesis?
21:5421 minutos e 54 segundosÊxodo. Você sabia que o livro de Êxodo é sobre um homem que foi tirado das águas,
21:5921 minutos e 59 segundosfoi para o deserto por 40 anos e depois voltou para libertar seu povo? Isso é muito interessante, porque
22:0722 minutos e 7 segundoso segundo Adão, Jesus Cristo, também foi tirado das águas em seu batismo. Foi para o deserto por 40 dias e depois
22:1422 minutos e 14 segundosvoltou para libertar seu povo.
22:2022 minutos e 20 segundosObrigado. Qual livro vem depois de Êxodo?
22:2322 minutos e 23 segundosVocê sabe sobre o que é o livro de Levítico? O livro de Levítico fala sobre o trabalho do sacerdote em purificar seu
22:3122 minutos e 31 segundospovo de seus pecados. Isso é muito interessante porque Cristo, o segundo Adão, também foi tirado das águas, foi
22:3822 minutos e 38 segundospara o deserto por 40 dias, voltou para libertar seu povo e então começou o trabalho de purificar seu povo de seus pecados.
22:4922 minutos e 49 segundosQual livro vem depois de Levítico?
22:5322 minutos e 53 segundosMuito interessante. Você sabe sobre o que é o livro de Números? O livro de Números fala sobre Moisés liderando os 12, chamando
23:0723 minutos e 7 segundos70. Bem, isso é interessante porque Jesus, o segundo Adão, é tirado das águas, vai para o deserto por 40 dias,
23:1623 minutos e 16 segundosvolta para libertar seu povo, começa o trabalho de purificá-los de seus pecados.
23:2223 minutos e 22 segundosE também chama 12 e ordena 70.
23:3023 minutos e 30 segundosQual livro vem depois de Números? Bem, isso é interessante porque o livro de Deuteronômio é, na verdade, o último sermão de Moisés.
23:3823 minutos e 38 segundosNo final daquele livro, ele reúne as 12 tribos, ele repete a da aliança. Eles cantam uma canção e então ele sai
23:4623 minutos e 46 segundossozinho para morrer, mas ele morre, é sepultado e ressuscita.
23:5823 minutos e 58 segundosIsso é bem interessante, porque Jesus, o segundo Adão, que foi tirado das águas, que vai para o deserto por 40 dias,
24:0624 minutos e 6 segundosvolta para libertar seu povo, faz o trabalho de purificá-los de seus pecados, chama 12, ordena 70, também
24:1324 minutos e 13 segundosreúne os 12 no final de seu ministério, repete a aliança, eles
24:2024 minutos e 20 segundoscantam uma canção e ele sai sozinho para morrer, mas ele morre. é sepultado e ressuscita. É, quem
24:3024 minutos e 30 segundosdiria? Espera o que qual livro vem depois de Deuteronômio? Josué. Muito interessante.
24:3824 minutos e 38 segundosO livro de Josué fala sobre um homem que lidera, que derruba uma nação com um grito alto. Assim como Jesus Cristo, o segundo Adão, que é tirado das águas,
24:4824 minutos e 48 segundosvai para o deserto por 40 dias, volta para libertar seu povo, faz o trabalho de purificá-los de seus pecados, chama 12, ordena 70, os reúne, repete a
24:5624 minutos e 56 segundoscanção, repete a aliança, sai para morrer. Quando ele morre, ele derruba o
25:0325 minutos e 3 segundosreino de Satanás com um grito alto. está consumado. Isso é bem interessante. Mas tem mais,
25:1525 minutos e 15 segundosporque tem outro livro que vem depois do livro de Josué. Que livro é esse? Juízes. Muito interessante. Você sabe sobre o que é o livro de Juízes?
25:2525 minutos e 25 segundosO livro de Juízes fala sobre as 12 tribos avançando para conquistar, mesmo que elas não tenham mais um líder físico. Muito interessante, porque após
25:3325 minutos e 33 segundosa morte, sepultamento e ressurreição de Jesus, a igreja primitiva, que agora não tem mais um líder físico, como fizeram com Jesus,
25:4325 minutos e 43 segundosJosué, agora avança conquistando em nome de Cristo. Isso é bem interessante. Qual livro vem depois de
25:5225 minutos e 52 segundosJuízes? Bem interessante. Você sabe sobre o que é o livro de Rute? O livro de Rut fala
26:0126 minutos e 1 segundosobre o livro de Hebreus. É, desculpe, o livro de Rute fala sobre uma mulher
26:0926 minutos e 9 segundosgentia com uma sogra hebraica.
26:1826 minutos e 18 segundosEssa mulher gentia, você sabe o que ela está fazendo? Ela está trabalhando no campo, colhendo os feixes.
26:2826 minutos e 28 segundosE a propósito, Boaz, que era um tipo de Cristo, está olhando para aquela mulher, tipo, quem é aquela senhora no campo? Ohó, não, não, não,
26:3626 minutos e 36 segundosnão. Quem é aquela mulher no campo?
26:4026 minutos e 40 segundosÓ, cara, vamos tentar desse lado. Vamos ver quem é aquela mulher trabalhando no campo. Eu estou atraído por aquela
26:4826 minutos e 48 segundosmulher trabalhando no campo. Esse é o tipo de mulher que Jesus gosta. Uma mulher, uma igreja trabalhando no campo, colhendo os
26:5726 minutos e 57 segundosfeixes. E a propósito, ela diz de sua sogra hebraica: "Seu Deus será o meu Deus".
27:0627 minutos e 6 segundosMuito interessante. Muito interessante. Mas o que vem depois do livro de Rute, Primeiro Samuel, isso é
27:1327 minutos e 13 segundosinteressante. Você sabe sobre o que é o livro de B Samuel? O livro de Bor Samuel. E a propósito, estamos indo a algum lugar com isso, tá bom? Tem um
27:2027 minutos e 20 segundosponto aqui, o livro de Primeiro Samuel fala sobre uma nação, a nação israelita, que teve uma ideia realmente maluca.
27:2927 minutos e 29 segundosEles decidiram que iriam rejeitar seu sumo sacerdote Samuel para ter um rei governando sobre eles em vez
27:3627 minutos e 36 segundosdisso. E esse rei usurparia a autoridade do sacerdócio. Em outras palavras, esse rei reuniria, de certa forma a igreja e o
27:4527 minutos e 45 segundosestado. Muito interessante, porque depois que a igreja estava trabalhando por algum tempo no campo e fazendo suas coisas, eles
27:5327 minutos e 53 segundosfizeram algo muito interessante. Eles rejeitaram seu sumo sacerdote, Jesus Cristo, por um homem chamado
28:0328 minutos e 3 segundosConstantino. Quem decidiu se juntar à igreja? E uau, isso é muito interessante. É quase como se essa história estivesse paralelando o Antigo
28:1228 minutos e 12 segundosTestamento. Agora, amados, depois de Primeira Samuel, você tem dois Samuel,
28:1628 minutos e 16 segundosvocê tem um e dois reis, você tem um e dois crônicas que detalham toda a apostasia de Israel.
28:2628 minutos e 26 segundosque a propósito os levou a serem capturados de maneira inesperada por um reino chamado mistério.
28:3928 minutos e 39 segundosUau! Uau! Isso se paralela aos 1260 anos. Quem teria pensado que de Gênesis
28:4728 minutos e 47 segundosaté Sudinho Crônicas estaria em que forma de sombra?
28:5428 minutos e 54 segundosA grande controvérsia, como entendemos no livro, a grande controvérsia. Espera o
29:0229 minutos e 2 segundosquê? Mas espera, tem mais. Você vê depois de dois crônicas,
29:1029 minutos e 10 segundoslembre-se, dois crônicas nos traria simbolicamente até que ano?
29:1529 minutos e 15 segundos17 98. Fim dos 1260 anos. Certo? Então parte aqui, não se antecipe a mim,
29:2329 minutos e 23 segundosapenas pense agora. Qualquer livro que vier a seguir deve ter, se estamos seguindo a linha, alguma importância
29:3129 minutos e 31 segundospara alguns eventos principais que aconteceriam após 1798. Então, eu tenho uma pergunta para
29:3829 minutos e 38 segundosvocê. Que livro vem depois de dois crônicas? Você sabe o que aprendemos um pouco mais cedo?
29:4729 minutos e 47 segundosque houve três decretos,
29:4929 minutos e 49 segundosproclamações dados no livro de Esdras. Vocês não estão me entendendo. Não, não, não, não, não, não, não, não,
29:5729 minutos e 57 segundosnão, não. Três decretos.
30:1330 minutos e 13 segundosEntão,
30:1530 minutos e 15 segundosprimeiro decreto era para chamar a atenção para o santuário. Sob aquele primeiro decreto,
30:2730 minutos e 27 segundosnos é dito que 50.000 pessoas deixaram a Babilônia para fazer esse trabalho. Você quer saber quantas
30:3430 minutos e 34 segundospessoas saíram das igrejas caídas da Babilônia quando a mensagem começou a ser pregada?
30:4330 minutos e 43 segundos50,000. Você pode conferir no livro A Grande Controvérsia. Tudo bem, vou ficar em
30:5130 minutos e 51 segundossilêncio porque estamos tão animados agora.
31:0331 minutos e 3 segundosObrigado. Porque o silêncio é a nova empolgação. O segundo decreto foi contra
31:1131 minutos e 11 segundosos inimigos do povo de Deus, assim como a segunda mensagem do anjo é contra a Babilônia.
31:1731 minutos e 17 segundosFoi o terceiro decreto que disse: "Tudo bem, agora você pode se tornar seu próprio poder autônomo." E isso não se tratava apenas
31:2531 minutos e 25 segundosda construção do templo, mas também da construção da cidade e da reconstrução de tudo esse lançamento de Jerusalém, assim como a mensagem do terceiro anjo.
31:3431 minutos e 34 segundosSob a mensagem do terceiro anjo, a Igreja Adventista do Sétimo Dia foi formada.
31:4431 minutos e 44 segundosEsse é o livro de Esdras. Agora, qual livro vem depois de Esdras?
31:5431 minutos e 54 segundosO quarto decreto.
32:0232 minutos e 2 segundosNossa!
32:0332 minutos e 3 segundosUau! Você vê, amado Neemias, o deveria terminar o trabalho que havia começado sobre os primeiros três decretos. Mas
32:1132 minutos e 11 segundosouça com atenção, o povo de Deus, os judeus se tornaram tão eh um um desanimados no trabalho. Eles se
32:2032 minutos e 20 segundosdeixaram levar por construir suas próprias casas e fazer suas próprias coisas a ponto de deixarem o trabalho de
32:2832 minutos e 28 segundosDeus de lado. E levou Neemias quando Neemias o ouviu isso. Espere, 13 anos depois e o
32:3632 minutos e 36 segundostrabalho não está feito. Neemias foi movido pelo espírito de Deus a dizer:
32:4132 minutos e 41 segundos"Não, algo precisa ser feito. Precisamos terminar o trabalho. Precisamos nos
32:4932 minutos e 49 segundosorganizar." Amados, já se passaram 172 anos, eu acho, desde 1844. Louvado seja Deus pelo trabalho
32:5732 minutos e 57 segundosque foi feito sobre as mensagens dos três anjos. Mas, amado, eu acredito que um quarto anjo, um um quarto
33:0533 minutos e 5 segundosdecreto deve ser proclamado para que o trabalho seja
33:1333 minutos e 13 segundosconcluído. Mas, amado, a triste notícia é esta.
33:1933 minutos e 19 segundosNós pausamos um pouco o a história. Nós
33:2733 minutos e 27 segundospausamos a história. Estamos presos entre Esdras e
33:3633 minutos e 36 segundosNeemias. Nós pausamos a história porque temos vidas para viver. Você sabe, quero dizer, não dá para explicar que tudo se
33:4433 minutos e 44 segundosresume ao evangelho. Eu preciso alimentar meus filhos. E quero dizer,
33:4833 minutos e 48 segundosvocê sabe, nós temos que ah, meio que viver o no deserto. Você vê, amado, no no Antigo
33:5633 minutos e 56 segundosTestamento, as crianças de Israel, havia alguns que estavam ansiosos para sair do deserto, mas havia outros que estavam.
34:0334 minutos e 3 segundosNós precisamos fazer do nosso lar aqui porque o homem levou tanto tempo. Então,
34:0834 minutos e 8 segundosprecisamos proporcionar uma educação para nossos filhos e precisamos ganhar a vida no deserto. Amado, estamos buscando ganhar
34:1734 minutos e 17 segundosa vida no deserto ou ainda acreditamos que Jesus está voltando e quer nos levar à terra prometida?
34:2434 minutos e 24 segundosNão estou dizendo para não viver, estou apenas dizendo para lembrar que nossa prioridade deve ser que Jesus está voltando. E eu não acredito que essa
34:3234 minutos e 32 segundosseja nossa prioridade. Agora nós pausamos a história para satisfazer nossos próprios desejos.
34:4034 minutos e 40 segundosA história, amado, está em pausa. E uma coisa que eu realmente odeio em boas histórias é quando elas são muito
34:4934 minutos e 49 segundoscolocadas em pausa. É hora de despausar. É hora de despausar. Ouça,
35:0035 minutosamado, ao estudarmos o livro de Neemias,
35:0335 minutos e 3 segundosaprendemos que Neemias era um homem que foi tão tocado pelo espírito de Deus. Ele era, ouça, ele não era um pastor,
35:0935 minutos e 9 segundosele não era um pregador, ele era um copeiro. E Neemias disse: "Eu irei e terminarei o trabalho". O que precisamos neste momento são o mais Neemias. Oh, você vê.
35:2335 minutos e 23 segundosMas ouça-me, a mensagem do quarto anjo não é nada mais do que a efusão do Espírito Santo. Em Apocalipse 18, aquele
35:3135 minutos e 31 segundosanjo é descrito como descendo e iluminando a terra com sua glória. E então chama as pessoas para fora da Babilônia. Mas ouçam-me,
35:4235 minutos e 42 segundospessoal, a mensagem não é tanto sair da Babilônia para a Babilônia. A mensagem é a glória.
35:5035 minutos e 50 segundosÓ, sim.
35:5235 minutos e 52 segundosO é a o glória que leva as pessoas para fora da Babilônia. Não é sair da Babilônia. Eles vão ficar tipo, por quê? Tchau.
36:0536 minutos e 5 segundosAh, eu saí da Babilônia, não adianta nada. Precisamos ter a glória. E a glória é a glória de Cristo.
36:1436 minutos e 14 segundosEntão eu tenho uma pergunta para você. Onde está a glória de Cristo?
36:2436 minutos e 24 segundosÉ por isso que Isaías 55 diz: "Assim como a chuva cai do céu,
36:3236 minutos e 32 segundossim, diz: "A minha palavra sairá e não voltará para mim vazia". Perceba como a palavra é comparada à chuva. Em Deuteronômio, a Bíblia diz:
36:4536 minutos e 45 segundos"Minha doutrina cairá como a chuva sobre a grama".
36:4936 minutos e 49 segundosEm outras palavras, amados, a efusão do Espírito Santo é uma mensagem e uma missão. Qual é a mensagem? A mensagem é
36:5836 minutos e 58 segundosCristo e dele crucificado. Porque Cristo e dele crucificado é a glória de Deus. Quando olhamos para a cruz, toda a glória. O que fez as pessoas?
37:1237 minutos e 12 segundosLembre-se, foi Ciro de Secando o abismo que levou as pessoas para fora da Babilônia. Crio, secando o abismo,
37:2537 minutos e 25 segundosapontou para Cristo na cruz. Então, como levamos as pessoas para fora da Babilônia? Muito simples.
37:3337 minutos e 33 segundosMostre a eles Cristo crucificado. Mostre a eles Cristo. Mostre a eles os anjos sentados no túmulo, dizendo: "Olha, a
37:4037 minutos e 40 segundosmorte de Cristo permite que você fique livre quando fazemos de Cristo e dele crucificado o centro de nossas
37:4837 minutos e 48 segundosdoutrinas. Quando fazemos, veja, isso é o olha, você quer saber o que que vai
37:5537 minutos e 55 segundosacontecer quando o Espírito Santo for derramado?
38:0038 minutosVocê a grama, porque você é a grama. A chuva cai sobre a grama, você é a grama.
38:0938 minutos e 9 segundosE quando a chuva cai sobre a grama, o povo de Deus vai começar a abrir a Bíblia e eles vão começar a ver coisas que são tão poderosas e tão incríveis
38:1738 minutos e 17 segundosque quando eles forem e abrirem, vão sentir queimação no coração. E deixe-me te dizer uma coisa. Quantos são
38:2438 minutos e 24 segundostímidos? Quantos de vocês têm medo de falar em público? Você sabe qual é o meu maior
38:3138 minutos e 31 segundosmedo? Falar em público. Quando eu vim para cá da Jamaica, quando eu era criança com 5
38:3738 minutos e 37 segundosanos, todo mundo ria do meu sutaque. E como resultado, eu desenvolvi um medo intenso de falar em público. Eu não
38:4538 minutos e 45 segundosfalaria. Eu ficava em pé na frente das pessoas e você podia ver o papel tremendo na sala de aula. Eu era assim até a
38:5338 minutos e 53 segundosfaculdade. E então algo aconteceu comigo. Eu tive queimação no
39:0039 minutoscoração. E amados, deixe-me te dizer uma coisa. Quando você tem queimação no coração, quando você tem queimação no
39:0839 minutos e 8 segundoscoração, a queimação supera o medo. A queimação supera a timidez. É por isso que Deus está
39:1639 minutos e 16 segundostentando nos colocar em chamas. Ele está dizendo: "Olha, se eu conseguir que eles se concentrem em mim nas escrituras,
39:2239 minutos e 22 segundoseles vão sentir queimação no coração". E foi a queimação no coração que levou os discípulos ao cenáculo e que resultou na efusão do Espírito
39:3039 minutos e 30 segundosSanto. Então, Deus está tentando derramar seu espírito sobre seu povo. E é olhando e encontrando Cristo
39:3839 minutos e 38 segundosnas Escrituras que teremos uma mensagem tão poderosa que as pessoas na Babilônia a ouvirão e sairão. Não é apenas uma mensagem,
39:4739 minutos e 47 segundosamados, é uma missão. Você vê, a Bíblia nos diz que aqueles que se lembram do trabalho de Neemias para reparar a
39:5739 minutos e 57 segundosbrecha, Isaías 58 nos diz muito claramente que aqueles que honram o sábado serão chamados de reparadores da brecha.
40:0640 minutos e 6 segundosMas, amados, por favor, ouçam-me. Muitos adventistas do sétimo dia nunca guardaram o sábado. Porque se você olhar como o
40:1440 minutos e 14 segundossábado deve ser guardado, a Bíblia diz que o sábado deve ser um dia de misericórdia. Ou seja, não, não, não,
40:2240 minutos e 22 segundosnão, não, não quer dizer que no sábado você vai à igreja, hein? Ouve o sermão,
40:2740 minutos e 27 segundosdiz: "Louvado seja o Senhor". participa do almoço comunitário, vai para casa e dorme. Isso não é o
40:3440 minutos e 34 segundossábado. De acordo com Deus, o sábado é eu ir à igreja. Eu ouço o sermão. Depois do
40:4240 minutos e 42 segundossermão, eu me pergunto, tá? Quem precisa ser libertado? Quem precisa de roupas?
40:4840 minutos e 48 segundosQuem me precisa de comida? Quem precisa de ministério? Quem está preso pela maldade? Leia o texto. A Bíblia diz que
40:5740 minutos e 57 segundoseste dia foi feito para aliviar os oprimidos, para desfazer as amarras da maldade. E nos adventistas do sétimo
41:0541 minutos e 5 segundosdia, passamos tempo demais na igreja no sábado. Vocês não estão me entendendo. Vocês veem, amados, no
41:1241 minutos e 12 segundossábado estamos trancados longe do mundo. Espera o quê? E se, olha só, e se no sábado
41:2041 minutos e 20 segundosestivéssemos lá fora no mundo? E se no sábado estivéssemos lá fora? abençoando pessoas que precisam.
41:2741 minutos e 27 segundosNão estou falando sobre quebrar o sábado. Então não apenas, ó, pastor Mar,
41:3041 minutos e 30 segundosnão é disso que estou falando. Tô falando sobre ministrar as necessidades das pessoas no sábado. E se a sua comunidade soubesse, cara, eu
41:3941 minutos e 39 segundosadoro quando chega o sábado, porque aqueles adventistas, aqueles adventistas, eles
41:4641 minutos e 46 segundosestão ministrando para as pessoas, eles estão saindo para alcançar a comunidade,
41:5141 minutos e 51 segundospara ver quais são as suas necessidades e como podem ajudá-las e como podem assisti-las. E se a Igreja Adventista do
41:5841 minutos e 58 segundosSétimo Dia decidisse que todo sábado seria um dia de misericórdia, nós vamos maneiras de abençoar as pessoas. Nós
42:0642 minutos e 6 segundosvamos encontrar maneiras criativas de abençoar as pessoas para que elas possam saber disso. O sábado foi criado como um
42:1342 minutos e 13 segundospresente de amor do Deus do céu. Você percebe o que isso faria com o mundo? Você percebe o que isso faria conosco?
42:2342 minutos e 23 segundosSim. A você vê a mensagem e a missão mudam o caráter. A mensagem e a missão mudam o caráter.
42:3442 minutos e 34 segundosE amados, Deus está esperando que a gente entenda isso. Então, veja isso. Qual livro vem
42:4242 minutos e 42 segundosdepois de Neemias? Ester.
42:4842 minutos e 48 segundosInteressante. Você sabe sobre o que é o livro de Ester?
42:5342 minutos e 53 segundosO livro de Ester fala sobre um decreto de morte dado contra o povo de Deus que se
43:0243 minutos e 2 segundosrecusa a cumprir as leis do governo. Mas, amados, ouçam-me. Ester
43:1143 minutos e 11 segundosnão aparecerá até que Neemias tenha sido cumprido. Então, por que você está correndo para o deserto? Quem está te procurando?
43:2643 minutos e 26 segundosNinguém. Você sabe porque ninguém está te procurando? Porque você não está fazendo barulho. Você não está fazendo barulho.
43:3343 minutos e 33 segundosAmados, ouçam-me. Neemias, quando ele foi até seu povo, ele disse: "Vamos lá,
43:3843 minutos e 38 segundostemos que terminar essa parede e temos que terminar juntos. Temos uma missão.
43:4443 minutos e 44 segundosVamos cumprir essa missão. Vamos fazer isso, mas temos que fazer isso juntos.
43:5143 minutos e 51 segundosTemos que nos organizar, Mateus. Não, não, não. Temos
43:5743 minutos e 57 segundosque conseguir isso, mas juntos temos que nos organizar, temos que conseguir, amados,
44:0844 minutos e 8 segundosnão um aqui e outro ali. Temos que nos organizar. Deus está chamando o seu povo para cumprir a missão juntos.
44:1944 minutos e 19 segundosQual livro vem depois de Ester, ó? Sim. Não é o livro de Jó sobre
44:2744 minutos e 27 segundosum homem que passa por um tempo de dificuldades quando parece que Deus se afastou e o abandonou. Não é isso que vai acontecer
44:3444 minutos e 34 segundosno final dos tempos? A propósito, o livro de Ester,
44:3944 minutos e 39 segundoscara, estou ficando sem tempo. Você sabe que o livro de Ester é
44:4644 minutos e 46 segundossobre, lembra? Quem é o cara? Lembra do Amã? Como Hamã estava tipo, ei, você sabe o quê? Todo mundo se curva diante
44:5444 minutos e 54 segundosde mim, mas tinha um cara que não se curvava para ele. E esse era Mordecai,
44:5844 minutos e 58 segundosporque Mordeekai simplesmente não se curvava. E então Raman pensou: "Bem,
45:0245 minutos e 2 segundoscomo Mordecai não se curva, eu vou atrás do povo dele." Você percebe que Satanás tinha alguém que não se curvava
45:1045 minutos e 10 segundospara ele. Jesus. E por que Jesus não se curvava para ele? Ele diz, diz: "Vou atrás do povo
45:1845 minutos e 18 segundosdele. Eu vou atrás do povo dele." E assim, amados, Jó aponta para um povo que passará por um tempo de dificuldades. Qual livro quando você está passando por um tempo de
45:2645 minutos e 26 segundosdificuldades? É o livro que a maioria das pessoas lê. Os salmos falam sobre Davi em sua
45:3445 minutos e 34 segundosfuga de seu inimigo. E o salmo mostra o clamor de Davi. Senhor, livra-me dos meus inimigos.
45:4245 minutos e 42 segundosO que vem a seguir são os livros de Eclesiastes e Provérbios. E amados,
45:4545 minutos e 45 segundosesses livros nos dizem como o povo de Deus deve ter sabedoria. Você acha que vamos precisar de sabedoria no fim dos tempos? Há uma mulher estranha que o
45:5345 minutos e 53 segundospovo de Deus precisará evitar no fim dos tempos? Com certeza. Provérbios 31. Leia sobre isso. Essas mulheres que fizeram
46:0046 minutosos reis ficarem bêbados por causa do álcool. Que livro vem depois de Provérbios? Cântico dos
46:0946 minutos e 9 segundoscânticos. Sim. Jesus vai vir buscar sua noiva. O noivo virá buscar sua
46:1846 minutos e 18 segundosnoiva. Amados, quem teria pensado que essa é a história da Bíblia? Nós perdemos isso. Você sabe o que vem depois de
46:2746 minutos e 27 segundosSalomão? Cântico dos cânticos. Os profetas maiores. Você sabe, todos eles falaram sobre a segunda vinda de Cristo e o estabelecimento do reino milenar.
46:3846 minutos e 38 segundosEles falaram sobre a destruição dos inimigos do povo de Deus. E então os profetas menores falam todos sobre a justiça do julgamento de Deus. Porque
46:4546 minutos e 45 segundosdurante o milênio, adivinha só? A justiça de de Deus será vindicada. E curiosamente o livro do
46:5446 minutos e 54 segundosAntigo Testamento termina com o livro de Malaquias, que conclui: "Com os ímpios se tornando cinzas sob as solas dos
47:0247 minutos e 2 segundosnossos pés". Quem teria pensado que todo o Antigo Testamento é a grande controvérsia, como entendemos no
47:1147 minutos e 11 segundoslivro, a grande controvérsia. Quem teria pensado? Quem teria pensado? E então,
47:1847 minutos e 18 segundosamados, quando tudo isso estiver feito,
47:2047 minutos e 20 segundosCristo estará verdadeiramente conosco. Mateus 1:21, ele estará verdadeiramente conosco. É sobre isso que os evangelhos
47:2947 minutos e 29 segundosfalam. Então haverá uma só língua e todo o povo de Deus estará unido. O livro de Atos.
47:3747 minutos e 37 segundosEntão, judeus e gentios de todos os lugares, Roma,
47:4247 minutos e 42 segundosGalácia, Éfeso, Filipos, de todos os cantos, o povo de todas as diferentes nações e nacionalidades. E as línguas se unirão,
47:5347 minutos e 53 segundosamados, para contemplar a revelação sempre crescente de Jesus Cristo por toda a eternidade. Acabamos de de ouvir a
48:0148 minutos e 1 segundohistória de toda a Bíblia, do Gênesis até Apocalipse. Perdemos a
48:0948 minutos e 9 segundoshistória. Eu tenho mais uma coisa para compartilhar com vocês e 2 minutos e 48 segundos para fazer
48:1648 minutos e 16 segundosisso. Jesus, Jesus é um símbolo de sua igreja. A igreja dele deve segui-lo aonde quer que ele vá. Amém.
48:2648 minutos e 26 segundosJesus nasceu. Houve o nascimento da igreja do Novo Testamento. Sim, Jesus foi batizado. Houve um batismo da igreja do Novo Testamento no Pentecostes. Sim,
48:3748 minutos e 37 segundosJesus foi para o deserto. A igreja primitiva ia para o deserto por 1260 anos. Sim. Jesus, depois que ele sai do
48:4448 minutos e 44 segundosdeserto, uma das primeiras coisas que ele faz é limpar o templo. Assim como após
48:5248 minutos e 52 segundos1798, a nova igreja de Deus participaria desse processo de purificação do templo.
48:5848 minutos e 58 segundos1844. O deserto termina em 1798. A purificação do templo começa em
49:0449 minutos e 4 segundos1844. Você sabe disso? Quando Jesus estava purificando o templo pela primeira vez, depois que saiu do deserto, os judeus disseram: "4 anos
49:1349 minutos e 13 segundosestamos construindo este templo. Você vai levantá-lo novamente em três dias?
49:1849 minutos e 18 segundosVocê sabia que se você pegar 46 anos e adicionar a 1798, você
49:2849 minutos e 28 segundosobtém 1844?" Você está falando sério, mas tem mais uma coisa que o senhor fez.
49:3749 minutos e 37 segundosBem ali, ao mesmo tempo, ele transformou água em vinho, em uma festa de casamento, água em vinho. E os homens que estavam levando a água disseram:
49:4849 minutos e 48 segundos"Ah, você guardou o melhor vinho para o final." Amados, a Babilônia ali tá dando vinho ao mundo
49:5749 minutos e 57 segundosagora. O povo de Deus tem o melhor vinho. É hora de avançar.
50:0650 minutos e 6 segundoscom esse vinho. É hora de avançar com isso. É hora de
50:1450 minutos e 14 segundosdespausar. Eu quero fazer um apelo. Vou pedir que você fique em pé. Não vou pedir que você venha até aqui. Não fique em pé. Não fique em pé. Espere pelo meu
50:2150 minutos e 21 segundosapelo. Meu apelo é amém. Fique em pé diante do apelo. É isso que eu
50:2850 minutos e 28 segundosgosto. Precisamos do espírito de Neemias. Você precisa perceber que não se trata do pastor fazendo isso ou desse
50:3650 minutos e 36 segundoscara fazendo isso ou daquele cara fazendo isso. É sobre mim. É sobre mim. Deus precisa que eu
50:4350 minutos e 43 segundosseja como Neemias. E hoje você está dizendo: "Senhor, é isso. Eu despauso. Deus tem me chamado para ser batizado.
50:5050 minutos e 50 segundosEu tenho colocado isso em pausa. Eu estou despausando. Deus me chamou para pregar. Eu coloquei isso em pausa. Eu estou despausando esta noite. Deus,
50:5950 minutos e 59 segundosuse-me como você quiser. Como você quer que eu seja usado, use-me, Senhor. Eu oficialmente despauso. Se esse é o seu desejo, eu vou
51:0751 minutos e 7 segundospedir que você fique de pé. Pai celestial, ajude-nos a despausar.
51:1751 minutos e 17 segundosPerdoe-nos por colocar a sua história em pausa enquanto vivíamos nossas vidas e fazíamos a nossa
51:2451 minutos e 24 segundosvontade. Por favor, Senhor, encha-nos com o seu espírito. Reina sobre nós,
51:2951 minutos e 29 segundosSenhor. Abra nossos olhos para que possamos contemplar Cristo em todas as Escrituras. E, Pai, ajude-nos não apenas
51:3751 minutos e 37 segundosa pregar a mensagem, mas a viver a mensagem.
51:4151 minutos e 41 segundosPai, ajude-nos a começar a realmente guardar o sábado. E, Senhor, à medida que essas duas coisas se combinam, que as paredes
51:4851 minutos e 48 segundossejam reconstruídas para que você possa finalmente voltar. Obrigado, Senhor, por nos contar a história da Bíblia. Em nome de Jesus, nós oramos.
51:5851 minutos e 58 segundosAmém. Vocês podem se sentar.

"""

# 3. Chame a função para gerar o arquivo .md
gerar_post_blog(titulo, categoria, assinatura, texto_bruto)
