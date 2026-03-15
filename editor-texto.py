import re
from datetime import datetime

def corrigir_nomes(texto):
    # Dicionário de substituições: { "nome_errado": "nome_correto" }
    substituicoes = {
        r"Virgínia Enen": "Virgínia Essene",
        r" Teard": "Teilhard de Chardin",
        r"Teard de Shardan": "Teilhard de Chardin",
        r"Tear de Shardan": "Teilhard de Chardin",
        r"Shardan": "Teilhard de Chardin",
        r"Chardã": "Teilhard de Chardin",
        r"Teardan": "Teilhard de Chardin",
        r"Brigamiang": "Brigham Young",
        r"Brigamang": "Brigham Young",
        r"Bill Schnosl": "Bill Schnoebelen",
        r"South Lake": "Salt Lake City",
        r"Joal Col de Tibé": "Djwal Khul"
    }
    
    for errado, correto in substituicoes.items():
        texto = re.sub(errado, correto, texto, flags=re.IGNORECASE)
    return texto

def limpar_pontuacao_gramatical(texto):
    padrao_erro = r',\s+(com|que|e|para|pelo|do|da|ao|de)\b'
    texto = re.sub(padrao_erro, r' \1', texto, flags=re.IGNORECASE)
    texto = re.sub(r',([a-zA-Zá-úÁ-Ú])', r', \1', texto)
    texto = re.sub(r'\s+,', ',', texto)
    return texto

def limpar_texto(texto):
    # 1. REMOÇÃO AGRESSIVA DE TEMPOS
    
    # Remove formatos como "0:00O", "0:00", "0:"
    # O \b garante que pegamos apenas o início da palavra/tempo
    texto = re.sub(r'\b\d+:\d{0,2}\w*', '', texto)
    
    # O ajuste principal:
    # \d+\s*(minutos?|segundos?): captura o tempo
    # (\w*): captura o resto da palavra grudada (como "Uma", "detectores", etc)
    texto = re.sub(r'\d+\s*(minutos?|segundos?)\w*', '', texto, flags=re.IGNORECASE)
    
    # Se ainda sobrar apenas a palavra "segundos" ou "minutos" grudada sem número antes (ex: "segundosUma")
    # Este padrão apaga a palavra "segundos" e tudo o que vier grudado até o próximo espaço
    texto = re.sub(r'(minutos?|segundos?)\w*', '', texto, flags=re.IGNORECASE)
    
    # Remove formatos "1 hora", "10 minutos", etc
    texto = re.sub(r'\d+\s*(horas?|minutos?|segundos?)\w*', '', texto, flags=re.IGNORECASE)
    
    # Remove colchetes de tempo [00:00:00]
    texto = re.sub(r'\[\d{1,2}:\d{2}(:\d{2})?\]', '', texto)
    
    # 2. Correção de nomes errados (mantendo sua função original)
    texto = corrigir_nomes(texto)
    
    # 3. Limpeza de vírgulas, espaços excessivos
    texto = re.sub(r'\s+', ' ', texto).strip()
    texto = re.sub(r',+', ',', texto)
    texto = re.sub(r'\s+,', ',', texto)
    
    # 4. Divisão em frases e blocos (mantendo sua estrutura)
    frases = re.split(r'(?<=\.)\s+', texto)
    paragrafos = []
    bloco_atual = []
    
    for i, frase in enumerate(frases):
        frase = re.sub(r'^[\s,.]+', '', frase)
        frase = limpar_pontuacao_gramatical(frase)
        
        if frase.strip():
            bloco_atual.append(frase.strip())
            
        if len(bloco_atual) == 5 or (i + 1) == len(frases):
            paragrafos.append(" ".join(bloco_atual))
            bloco_atual = []
            
    return "\n\n".join(paragrafos)

def gerar_post_blog(titulo, categoria, assinatura, conteudo_sujo):
    conteudo_limpo = limpar_texto(conteudo_sujo)
    data_atual = datetime.now().strftime("%Y-%m-%d")
    
    # Slug simplificado
    slug = titulo.lower().replace(' ', '-').replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('á', 'a').replace(',', '').replace('.', '')
    nome_arquivo_md = f"{slug}.md"
    nome_imagem = f"{slug}.webp"
    
    template = f"""---
title: "{titulo}"
date: "{data_atual}"
image: "{nome_imagem}"
category: "{categoria}"
signature: "{assinatura}"
---

{conteudo_limpo}
"""
    
    with open(nome_arquivo_md, "w", encoding="utf-8") as f:
        f.write(template)
    
    print(f"🚀 Post '{nome_arquivo_md}' gerado com sucesso!")

    # --- EXECUÇÃO DO SCRIPT ---

# 1. Título do Post
titulo = "Um Reino Dividido Não Subsiste"
categoria = "Profecia"
assinatura = "..."

# 2. Cole aqui o texto bruto que você obteve da transcrição
texto_bruto = """0:00O que eu vou falar hoje não é confortável, não é um vídeo fácil de gravar, mas é necessário. Se você está
0:077 segundosorando pouco, comece a orar mais, porque o que eu vou dizer agora não é nem um
0:1313 segundospouco leve. Algo está acontecendo dentro da nossa igreja e nem todos estão percebendo, não porque seja invisível,
0:2424 segundosmas porque é algo sutil.
0:2727 segundosestá acontecendo diante dos nossos olhos, enquanto muitos ainda estamos,
0:3232 segundosmuitos de nós ainda estão olhando para fora, esperando perseguição do mundo,
0:3838 segundosenquanto o verdadeiro movimento está acontecendo por dentro, dentro da igreja. Existe uma dinâmica silenciosa se formando, uma atmosfera diferente,
0:5252 segundospequenas divisões, críticas disfarçadas de zelo, desconfianças,
0:5959 segundosdesconfianças plantadas quase imperceptivelmente,
1:051 minuto e 5 segundosmas nada é explosivo, nada é escandaloso, porém constante e estratégico.
1:131 minuto e 13 segundosE talvez você pense que isso é exagero,
1:171 minuto e 17 segundosmas não é a primeira vez que isso acontece dentro do povo de Deus. Não é a primeira vez. Quando Israel foi derrotado
1:251 minuto e 25 segundospor uma cidade eh pequena chamada Ai, o problema não estava nos muros, não
1:331 minuto e 33 segundosestava no exército inimigo, estava dentro do acampamento. Havia um homem lá chamado Acan. Havia um Acan entre eles.
1:431 minuto e 43 segundosOutro exemplo, quando Jesus foi entregue, não foi por um romano infiltrado entre os discípulos, foi
1:511 minuto e 51 segundosalguém que caminhava com ele, que sentava à mesa com ele, ou seja, um dos 12. Haviam Judas ali, Judas Iscariotes.
2:022 minutos e 2 segundosO padrão bíblico, queridos, mostra que muitas vezes o ataque mais perigoso não vem de fora, vem de dentro.
2:122 minutos e 12 segundosE eu vou contar algumas histórias aqui para vocês bem rápido. Eu vivi isso. Eu vivi situações que me fizeram entender
2:202 minutos e 20 segundosisso com muita clareza e ainda novo na igreja.
2:242 minutos e 24 segundosAlguns anos atrás, em uma igreja que eu frequentava, houve uma iniciativa muito bonita.
2:322 minutos e 32 segundosO diretor da Escola Sabatina, junto com outros irmãos, decidiu que aos sábados à tarde nós nos reuniríamos para visitar pessoas afastadas,
2:432 minutos e 43 segundoseh famílias que tinham parado de de frequentar, pessoas que estavam desanimadas, pessoas afastadas da igreja.
2:522 minutos e 52 segundosE a ideia era simples. A ideia era simples e bíblica.
2:572 minutos e 57 segundosNão agir como o irmão mais velho da parábola do filho pródigo. Não julgar, mas ir atrás, fazer como Jesus fazia.
3:073 minutos e 7 segundosJesus que deixou as 99 ovelhas e foi buscar a que tinha se perdido. Mas havia haviam duas pessoas ali que sempre
3:163 minutos e 16 segundosestavam nessas reuniões e toda vez que a gente falava que iria visitar alguém,
3:233 minutos e 23 segundoselas diziam assim: "Ah, esse aí já era, esse aí tá perdido, esse aí aprontou,
3:293 minutos e 29 segundosfaz anos que não vem na igreja". E elas ficavam de roda em roda perguntando quem as pessoas iriam visitar para poder desanimar as pessoas. E eu ficava
3:373 minutos e 37 segundospensando, né, é justamente porque a pessoa não está vindo que nós precisamos ir visitar, ir atrás. Não é para julgar.
3:453 minutos e 45 segundosA visita não era para condenar, era para restaurar. Restauração.
3:513 minutos e 51 segundosE ali eu comecei a perceber algo. Não era uma oposição frontal. Ninguém dizia:
3:573 minutos e 57 segundos"Não faça isso ou não faça aquilo". Era um desânimo que ia sendo plantado, era descrédito lançado, era esfriar o
4:064 minutos e 6 segundosespírito missionário. Presta atenção. E quando você convence o povo de Deus de que não vale a pena buscar os perdidos,
4:164 minutos e 16 segundosvocê paralisa a obra sem precisar fechar a igreja. Olha a estratégia do inimigo.
4:234 minutos e 23 segundosDepois disso, eu vivi uma outra experiência.
4:274 minutos e 27 segundosEh, eu e minha esposa éramos batizados em uma igreja adventista um pouco mais longe de casa. Era uma igreja missionária, uma igreja envolvida,
4:384 minutos e 38 segundosjovens ativos. E a gente saía para espalhar livros, entregar folhetos. E foi ali que começamos a nossa caminhada
4:484 minutos e 48 segundosno adventismo. E ali aprendemos a ser missionários. Mas por que que a gente ia nessa igreja longe de casa? Porque o pessoal que deu estudo para nós, eles
4:574 minutos e 57 segundoseram dali. Mas um certo tempo nós decidimos mudar para uma igreja mais próxima por causa da logística também,
5:045 minutos e 4 segundosné? Nós não tínhamos carro, minha filha era pequena e dias de chuva assim eram bem difíceis. A igreja mais perto também
5:135 minutos e 13 segundosestava precisando de gente para trabalhar. A gente sentiu isso e algumas pessoas também comentaram, chamaram a gente para ir lá, tudo mais. E a gente
5:215 minutos e 21 segundosfoi logo nos primeiros meses, com apenas um ano de batismo e já estando nessa igreja, eu fui colocado como diretor
5:295 minutos e 29 segundosassociado dos jovens. Eu tinha 26 anos na época. O diretor era mais velho, mas eu sempre expus para ele ali as minhas
5:375 minutos e 37 segundosideias, sempre pedia opinião, ele sempre dizia assim, ó, vai, faz. E era dessa forma que acontecia. Mas quando as coisas começaram de fato a acontecer,
5:485 minutos e 48 segundosquando a gente começava de fato a fazer aquilo que tinha a ideia junto com outros irmãos, eu percebi que ele ficava incomodado e aí vieram críticas. Ele
5:575 minutos e 57 segundosdizia que eu estava passando por cima dele, mesmo com a autorização dele e tudo mais.
6:026 minutos e 2 segundosrolou um certo estress ali. Outra coisa me chamou atenção naquela época, os jovens eles faziam a a recapitulação da
6:106 minutos e 10 segundoslição fora da igreja, fora da nave da igreja, no lugar externo e no frio de Curitiba, né? Quem mora em Curitiba sabe
6:186 minutos e 18 segundoscomo é o inverno lá. Então era uma reclamação que tinha, não era uma reclamação minha, os próprios jovens falavam desse desconforto. Então fui,
6:266 minutos e 26 segundosconversei com a diretora da Escola Sabatina, ela disse que não havia sala disponível. Mas eu percebi que havia ali
6:336 minutos e 33 segundosa sala do desbravadores e eu percebi que ela estava tomada ali para uma montanha de lixo. Ou seja, para você conseguir pegar alguma coisa lá,
6:426 minutos e 42 segundosvocê tinha que passar por cima de um monte de coisa arada assim, lixo mesmo,
6:496 minutos e 49 segundosque estavam ali descartado no chão mesmo, no meio da sala.
6:536 minutos e 53 segundosEu percebi que havia um depósito debaixo da escada ali que poderia ser usado para guardar as coisas que os desbravadores iriam realmente usar. Então, conversei
7:017 minutos e 1 segundocom o pessoal do clube, eles separaram o que eles usariam, eles foram lá lá e autorizaram a descartar o resto. Eh,
7:107 minutos e 10 segundosdecidimos reformular aquela sala. Foi difícil, eu e alguns jovens ali limpando tudo, né? Era um sonho se realizando e
7:207 minutos e 20 segundosfinalmente teríamos uma sala para estudar a Bíblia. Mas algo curioso aconteceu enquanto as coisas estavam lá,
7:297 minutos e 29 segundosas os lixos estavam lá largados, ninguém se importava com eles. Mas quando decidimos descartar, mesmo com a
7:367 minutos e 36 segundosautorização e com o acompanhamento dos desbravadores, os donos daquelas tralhas apareceram. Até uma lona furada virou
7:447 minutos e 44 segundosmotivo de conflito. Quando viram as coisas lá na lixeira, passaram lá e viram jogados lá fora, começou uma perseguição.
7:537 minutos e 53 segundosMesmo assim, conseguimos organizar a sala. A sala ficou bonita, começamos a estudar ali, projetos missionários
8:018 minutos e 1 segundoestavam nascendo e nós queríamos envolver toda a igreja nesses projetos.
8:078 minutos e 7 segundosA gente tava fazendo ali um movimento missionário.
8:118 minutos e 11 segundosAté que um sábado, durante o estudo da lição ali nessa salinha nova, a diretora que havia permitido o uso da sala entrou lá e disse a um amigo meu que estava lá.
8:218 minutos e 21 segundosEle tava lá para ajudar no impulso ali no início da classe. Ele já tinha lá seus 40 anos, mas estava ali nos ajudando. Ela disse que ele não poderia permanecer ali no meio da lição mesmo.
8:328 minutos e 32 segundosEla chegou e falou assim: "Olha, você não pode ficar aí". E ele argumentou.
8:368 minutos e 36 segundosEle falou assim: "Não, eu posso visitar a classe, eu posso, como itinerante,
8:398 minutos e 39 segundosestar aqui". Mas ela solicitou que ele saísse, ele falou: "Não vou sair". Então ela falou assim: "Então espera um pouquinho". Ela desceu, chamou o primeiro ancião, houve discussão ali,
8:518 minutos e 51 segundosfoi constrangedor. Nós tínhamos visitas na classe, foi constrangedor. Eh, e aí por causa desses conflitos,
8:598 minutos e 59 segundosvieram algumas reuniões para tentar acertar. Eu lembro que nessa época eu tava desempregado, né? passando dificuldades financeiras.
9:079 minutos e 7 segundosEh, minha vida estava difícil dentro de casa, dentro da igreja também. Eu comecei até a adoecer, mas a minha fé
9:169 minutos e 16 segundospermanecia firme, assim, abalada, mas firme, né? Eh, eu comecei a, foi ali que eu comecei a gravar os primeiros vídeos
9:249 minutos e 24 segundosali falando de Jesus. Eu criei um grupo de estudo bíblico pelo WhatsApp. cheguei a ter mais de 200 pessoas estudando a
9:329 minutos e 32 segundosBíblia ali comigo e com as pessoas que me ajudavam, claro, não fazia nada sozinho. Eh, quando eu relatava isso na
9:389 minutos e 38 segundosEscola Sabatina, uma vez eu relatei e e houve uma surpresa ali da diretora,
9:479 minutos e 47 segundosmas eu também percebia expressões assim de desconforto com ela, né? Como assim,
9:519 minutos e 51 segundos200 estudos? Mas enfim, tudo bem, né? Em uma conversa depois de uma reunião, eu ouvi uma frase que revelou muito.
10:0110 minutos e 1 segundoEh, provavelmente o pastor deve ter falado alguma coisa para ela ali, porque a reunião era para tratar sobre esses
10:0810 minutos e 8 segundosconflitos e tava eu e esse meu amigo que ela expulsou da classe ali do lado de fora, ela passou e falou assim: "Vocês
10:1510 minutos e 15 segundosquerem o meu cargo para vocês? Pode pegar." E saiu revoltada batendo porta de carro. Enfim, uma situação
10:2310 minutos e 23 segundosconstrangedora. Ali eu percebi mais ou menos qual era a dela, né? O que que ela pensava, né? Eu acho que ela se sentia
10:3110 minutos e 31 segundosrealmente ameaçada, mas nós não queríamos cargo, a gente queria trabalhar. E ali eu entendi que muitas vezes o problema não é a obra, é o medo,
10:4010 minutos e 40 segundosé a insegurança, é quando o cargo se torna identidade. Irmãos, não foi só isso que aconteceu.
10:4810 minutos e 48 segundosHouve muitos conflitos naquele período,
10:5110 minutos e 51 segundosmas também houve muitas bênçãos. Eu conheci pessoas maravilhosas, pessoas de
10:5710 minutos e 57 segundosDeus. E essa igreja foi instrumento de crescimento na minha vida. Eu cresci ali. Eu não estou falando mal da igreja adventista. Eu quero deixar bem claro.
11:0811 minutos e 8 segundosEu não estou aqui dizendo que a igreja adventista não presta. Não, porque eu amo essa igreja. Eu sou adventista do sétimo dia. Muito pelo contrário,
11:1611 minutos e 16 segundosqueridos, a igreja é o povo de Deus.
11:2011 minutos e 20 segundosA igreja adventista é a igreja que ensina a verdade e eu amo estar nessa igreja. O que eu estou dizendo é que certas atitudes podem revelar quando o
11:2911 minutos e 29 segundosinimigo tenta agir por dentro. Assim como houve um Judas entre os 12, assim como houve um Acan em Israel,
11:4011 minutos e 40 segundosassim como ao longo da história bíblica sempre houve oposição interna, acontece hoje também. Há uma perseguição interna.
11:5111 minutos e 51 segundosHá pessoas que entram para dividir,
11:5511 minutos e 55 segundosinfiltrados, pessoas que são infiltradas pelo inimigo. Outros saem da igreja e passam a atacar. Como esses canais aí eles criam perfis, páginas para
12:0412 minutos e 4 segundosperseguir a igreja, muitas vezes sendo ex-membros que já estiveram dentro da igreja, que agora a a o ramo deles é perseguir a igreja. Isso não é novidade,
12:1612 minutos e 16 segundosé um padrão espiritual.
12:1812 minutos e 18 segundosNós adventistas do sétimo dia, cremos no dom profético e reconhecemos o ministério de White como a profetisa de
12:2812 minutos e 28 segundosDeus. E profetas nunca são amados, nunca são unanimidade, porque eles falam a verdade e a verdade confronta. E quando
12:3612 minutos e 36 segundosconfronta incomoda. Mas existe esperança, queridos. Existe esperança. A igreja continua sendo instrumento de
12:4412 minutos e 44 segundossalvação, continua sendo lugar de milagres. Não podemos, olha aqui para
12:5112 minutos e 51 segundosmim, presta atenção, não podemos nos e desanimar por causa de conflitos internos. Não podemos abandonar a fé por
13:0013 minutoscausa de pessoas, porque nós sabemos em quem temos crido. E queridos, se há
13:0913 minutos e 9 segundosinfiltração, há também vigilância. Se há ataque, há também proteção divina.
13:1713 minutos e 17 segundosEntão, quero falar para você o seguinte:
13:1913 minutos e 19 segundosore mais, vigie mais. E como a lição, as lições da escola sabatina que passaram
13:2613 minutos e 26 segundosagora, eh, ensinaram, permaneçam firmes na fé. Permaneça firmes. O por eu fiz esse vídeo para que você não desanime.
13:3713 minutos e 37 segundosCoisas vão acontecer dentro da igreja,
13:4013 minutos e 40 segundosmas você precisa estar ali firme nos braços de Jesus. Se você ficou até aqui nesse vídeo, um forte abraço."""

# 3. Chame a função para gerar o arquivo .md
gerar_post_blog(titulo, categoria, assinatura, texto_bruto)


# gerar_post_blog("A Sucessão e a Maçonaria", "História", "Leo Barbosa", texto_original)