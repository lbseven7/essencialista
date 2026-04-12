const fs = require('fs');
const path = require('path');
const MarkdownIt = require('markdown-it');
const matter = require('gray-matter');

const md = new MarkdownIt({
    html: true,
    linkify: true
});

const inputDir = path.join(__dirname, 'artigos');
const outputDir = path.join(__dirname, 'posts');

// URL do Backend (Google Apps Script) - Atualize aqui se mudar o script
const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbxVuAC4UeWvSORncW4rj5bqquF2ySxMRzP3uwB5CCMIlCKp7yHrNJj3ARv7nrywy2e9/exec';

// Função para criar nomes de arquivos limpos (slugs)
function slugify(text) {
    return text.toString().toLowerCase()
        .normalize('NFD').replace(/[\u0300-\u036f]/g, "") // Remove acentos
        .replace(/\s+/g, '-')           // Substitui espaços por hífen
        .replace(/[^\w\-]+/g, '')       // Remove caracteres não alfanuméricos
        .replace(/\-\-+/g, '-')         // Remove hífens duplos
        .replace(/^-+/, '')             // Remove hífen no início
        .replace(/-+$/, '');            // Remove hífen no fim
}

function resolveTitle(data, markdownBody, fallbackHtmlName) {
    const titleFromFrontMatter = data.title || data['Título'] || data['titulo'];
    if (titleFromFrontMatter) return String(titleFromFrontMatter).trim();
    const matchTitulo = markdownBody.match(/^\s*T[ií]tulo:\s*(.+)$/mi);
    if (matchTitulo) return matchTitulo[1].trim();
    const matchH1 = markdownBody.match(/^\s*#\s+(.+?)\s*$/m);
    if (matchH1) return matchH1[1].trim();
    return fallbackHtmlName.replace('.html', '').replace(/-/g, ' ');
}

function applyBoldToSubtitles(html) {
    // Agora inclui h3 e corrigiu o fechamento da tag no regex
    return html.replace(/<h([1-3])([^>]*)>([\s\S]*?)<\/h\1>/g, '<h$1$2><strong>$3</strong></h$1>');
}

// Seu Template HTML (Mantido igual)
const htmlTemplate = (data, content, prevHref, nextHref, slug, relacionados) => `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="category" content="${data.category || 'Geral'}">
    <title>${data.title} - Essencialista</title>
    <link rel="icon" type="image/webp" href="../images/sem-bg-black.webp">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
    <style type="text/css">
        @theme {
            --color-orange-500: #f97316;
            --color-orange-600: #ea580c;
        }
    </style>
    <style>
        html { scroll-behavior: smooth; }
        #progress-container { position: fixed; top: 0; left: 0; width: 100%; height: 4px; background: transparent; z-index: 9999; }
        #progress-bar { height: 100%; width: 0%; background: linear-gradient(90deg, #f97316, #ea580c); transition: width 0.1s; }
        .animate-fade-in { animation: fadeIn 0.6s ease forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .content-area img { max-width: 100%; height: auto; border-radius: 0.5rem; margin: 1.5rem 0; }

        /* --- ESTILOS DO MODO FOCO --- */
        body.focus-mode header, 
        body.focus-mode footer, 
        body.focus-mode section#comentarios-artigo,
        body.focus-mode section.mt-12,
        body.focus-mode .mt-10.flex,
        body.focus-mode .mt-8.pt-6.border-t { display: none !important; }
        
        body.focus-mode { background-color: #f4f1ea !important; color: #1a1a1a !important; }
        body.focus-mode main { max-width: 800px !important; margin-top: 2rem !important; }
        body.focus-mode article { box-shadow: none !important; background: transparent !important; padding: 0 !important; }
        body.focus-mode .content-area { font-size: 1.25rem !important; line-height: 1.8 !important; }
    </style>
</head>
<body class="bg-gray-100 text-gray-800 font-sans">
    <!-- Barra de Progresso -->
    <div id="progress-container"><div id="progress-bar"></div></div>

    <!-- Botão de Alternar Modo Foco -->
    <div id="focusToggle" class="fixed bottom-6 right-6 z-[100]">
        <button onclick="toggleFocusMode()" class="bg-black text-white p-4 rounded-full shadow-2xl hover:bg-orange-600 transition-all flex items-center justify-center group">
            <i class="fas fa-book-open text-xl"></i>
            <span class="max-w-0 overflow-hidden group-hover:max-w-xs group-hover:ml-2 transition-all duration-500 whitespace-nowrap text-sm font-bold uppercase">Modo Foco</span>
        </button>
    </div>
    <header class="bg-black text-white p-6 shadow-md sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center relative">
            <div class="flex items-center space-x-3">
                <a href="../index.html"><img src="../images/sem-bg-black.webp" alt="Logo" class="h-10"></a>
                <a href="../index.html"><h1 class="text-2xl font-bold">Essencialista</h1></a>
            </div>
            <div class="flex items-center gap-4">
                <button id="mobileMenuBtn" class="md:hidden p-2 rounded bg-white/10 hover:bg-white/20 min-w-[44px]"><i class="fas fa-bars"></i></button>
                <nav id="main-nav" class="hidden md:block absolute left-0 right-0 top-full w-full bg-black/95 backdrop-blur-sm border-t border-white/10 p-6 md:static md:bg-transparent md:border-none md:p-0">
                    <ul class="flex flex-col space-y-4 md:flex-row md:space-y-0 md:space-x-6 items-start md:items-center">
                        <li><a href="../index.html" class="hover:text-orange-500 font-bold block w-full py-2">Início</a></li>
                        <li><a href="../biblioteca.html" class="hover:text-orange-500 font-bold block w-full py-2">Biblioteca</a></li>
                        <li><a href="../index.html#featured-articles" class="hover:text-orange-500 font-bold block w-full py-2">Artigos</a></li>
                        <li><a href="../about.html" class="hover:text-orange-500 font-bold block w-full py-2">Sobre</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>
    <main class="container mx-auto mt-8 p-4 max-w-2xl">
        <article class="bg-white p-6 rounded-lg shadow-lg mb-10 animate-fade-in">
            ${data.image ? `<img src="../images/${data.image}" class="w-full h-64 object-cover mb-6 rounded-lg shadow" alt="${data.title} Preview">` : ''}
            <div class="mb-2"><span class="text-orange-600 font-black text-xs uppercase tracking-widest">${data.category}</span></div>
            <h2 class="text-3xl font-bold mb-6 leading-tight">${data.title}</h2>
            <div class="content-area space-y-4 leading-relaxed text-justify text-gray-700">${content}</div>
            
            <div class="mt-8 pt-6 border-t border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                 <a href="#comentarios-artigo" class="inline-block bg-gray-100 text-gray-600 px-4 py-2 rounded-lg hover:text-orange-600 transition">
                    <i class="far fa-comment-dots mr-2"></i>Deixar um comentário
                 </a>
                 <a href="https://api.whatsapp.com/send?text=Olha%20esse%20estudo%20interessante%20no%20Essencialista:%20${encodeURIComponent(data.title)}%20-%20https://essencialista.vercel.app/posts/${slug}.html" 
                    target="_blank" 
                    class="inline-block bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition font-bold flex items-center gap-2">
                    <i class="fab fa-whatsapp text-lg"></i> Compartilhar
                 </a>
            </div>

            <div class="mt-6 p-4 bg-gray-50 border-l-4 border-orange-500 rounded">
                <p class="italic text-gray-600">👉 ${data.signature || data.assinatura || 'O tempo está próximo. Prepare-se!.'}</p>
                <p class="text-right mt-2 font-bold text-sm">- Essencialista</p>
            </div>

            <div class="mt-10 flex flex-wrap justify-center gap-3">
                <a href="${prevHref}" class="bg-black text-white px-5 py-2 rounded-full text-sm hover:bg-orange-600 transition">← Anterior</a>
                <a href="../index.html" class="bg-black text-white px-5 py-2 rounded-full text-sm hover:bg-orange-600 transition font-bold">Home</a>
                <a href="${nextHref}" class="bg-black text-white px-5 py-2 rounded-full text-sm hover:bg-orange-600 transition">Próximo →</a>
            </div>
        </article>

        ${relacionados.length > 0 ? `
        <section class="mt-12">
            <h3 class="text-xl font-bold mb-6 border-b-4 border-orange-500 inline-block">Você também pode gostar</h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                ${relacionados.map(r => `
                    <a href="../${r.href}" class="group bg-white rounded-lg shadow hover:shadow-xl transition-all p-3 flex flex-col h-full">
                        <img src="../images/${r.image || 'default.webp'}" class="w-full h-24 object-cover rounded mb-2" alt="${r.title} Preview">
                        <span class="text-[9px] font-black text-orange-600 uppercase tracking-widest mb-1">${r.category}</span>
                        <h4 class="font-bold text-xs group-hover:text-orange-600 line-clamp-2 leading-tight">${r.title}</h4>
                    </a>
                `).join('')}
            </div>
        </section>
        ` : ''}

        <section id="comentarios-artigo" class="mt-20">
            <div class="bg-white p-6 rounded-xl shadow-lg border-t-4 border-black">
                <h3 class="text-2xl font-bold mb-6 text-center">Espaço do Leitor</h3>
                <form id="commentForm" class="space-y-4">
                    <input type="hidden" id="artigoId" value="${slug}">
                    <input type="text" id="nome" placeholder="Seu nome" required class="border border-gray-200 p-3 rounded-lg w-full focus:ring-2 focus:ring-orange-500 outline-none transition">
                    <input type="email" id="email" placeholder="Seu e-mail" required class="border border-gray-200 p-3 rounded-lg w-full focus:ring-2 focus:ring-orange-500 outline-none transition">
                    <textarea id="comentario" placeholder="O que você achou deste texto?" required rows="4" class="border border-gray-200 p-3 rounded-lg w-full focus:ring-2 focus:ring-orange-500 outline-none transition"></textarea>
                    <button type="submit" id="btnEnviar" class="bg-black text-white px-6 py-3 rounded-lg hover:bg-orange-600 transition duration-300 w-full font-bold uppercase">Enviar Comentário</button>
                </form>
                <p id="msgStatus" class="mt-3 text-center font-semibold"></p>
            </div>
            <div id="listaComentarios" class="mt-10 space-y-4 mb-20">
                <h3 class="text-xl font-bold border-b-2 border-orange-500 inline-block mb-4">Comentários</h3>
                <div id="loader" class="text-gray-500 italic text-sm">Buscando interações...</div>
            </div>
        </section>
    </main>

    <footer class="bg-black text-white p-10 mt-12">
        <div class="container mx-auto text-center">
            <img src="../images/sem-bg-black.webp" alt="Essencialista Logo" class="h-12 mx-auto mb-4">
            <p class="text-gray-400 text-sm">Essencialista &copy; 2026 - Fé e Ciência em Equilíbrio</p>
        </div>
    </footer>
    <script>
        const WEB_APP_URL = '${WEB_APP_URL}';

        async function carregarComentarios() {
            try {
                const res = await fetch(WEB_APP_URL + '?artigoId=${slug}');
                const dados = await res.json();
                document.getElementById('loader')?.remove();
                if (!Array.isArray(dados)) return;
                const container = document.getElementById('listaComentarios');
                dados.forEach(c => {
                    const div = document.createElement('div');
                    div.className = 'bg-gray-50 p-4 rounded-lg border-l-4 border-orange-500 mb-4 animate-fade-in';
                    const n = document.createElement('p'); n.className="font-bold text-gray-900"; n.textContent = c.nome;
                    const co = document.createElement('p'); co.className="text-sm text-gray-700 mt-1"; co.textContent = c.comentario;
                    div.append(n, co);
                    container.appendChild(div);
                });
            } catch (e) { console.error("Erro ao carregar comentários:", e); }
        }

        document.getElementById("commentForm").onsubmit = async function(e) {
            e.preventDefault();
            const btn = document.getElementById("btnEnviar");
            const status = document.getElementById("msgStatus");
            
            const nomeValue = document.getElementById("nome").value.trim();
            const emailValue = document.getElementById("email").value.trim();
            const comentarioValue = document.getElementById("comentario").value.trim();

            // 1. Validação de Nome (Mínimo 3 letras)
            if (!/^[a-zA-ZÀ-ÿ\s]{3,}$/.test(nomeValue)) {
                status.className = "mt-3 text-center font-bold text-red-600 dark:text-red-400 animate-bounce";
                status.innerText = "ERRO: Insira um nome válido (mínimo 3 letras).";
                document.getElementById("nome").focus();
                return false;
            }

            // 2. Validação de E-mail de Nível Corporativo + Lista Negra
            const emailRegex = /^[^\s@]+@[^\s@]+\.(com|net|org|edu|gov|br|io|me|info|site|online|xyz|app|tech|dev|blog)(\.[a-z]{2})?$/i;
            const dominiosBanidos = ['mailinator.com', 'yopmail.com', '10minutemail.com', 'tempmail.com', 'guerrillamail.com', 'sharklasers.com', 'dispostable.com', 'getnada.com'];
            const dominioEmail = emailValue.split('@')[1]?.toLowerCase();

            if (!emailRegex.test(emailValue) || dominiosBanidos.includes(dominioEmail)) {
                status.className = "mt-3 text-center font-bold text-red-600 dark:text-red-400 animate-bounce";
                status.innerText = dominiosBanidos.includes(dominioEmail) 
                    ? "ERRO: E-mails temporários não são permitidos." 
                    : "ERRO: Use um e-mail com extensão válida (ex: .com ou .com.br)";
                document.getElementById("email").focus();
                return false;
            }

            // 3. Validação de Comentário (Qualidade de Texto)
            const temLetras = /[a-zA-ZÀ-ÿ]/.test(comentarioValue);
            const muitasRepeticoes = /(.)\\1{4,}/.test(comentarioValue); 
            const excessoSimbolos = (comentarioValue.match(/[^a-zA-ZÀ-ÿ0-9\s]/g) || []).length > comentarioValue.length * 0.4;

            if (comentarioValue.length < 10 || !temLetras || muitasRepeticoes || excessoSimbolos) {
                status.className = "mt-3 text-center font-bold text-red-600 dark:text-red-400 animate-bounce";
                status.innerText = "ERRO: O comentário parece inválido ou contém muitos símbolos.";
                document.getElementById("comentario").focus();
                return false;
            }

            status.innerText = "";
            btn.disabled = true; btn.innerText = "Enviando...";
            
            try {
                const payload = {
                    artigoId: "${slug}",
                    nome: document.getElementById("nome").value,
                    email: document.getElementById("email").value,
                    comentario: document.getElementById("comentario").value
                };
                
                const res = await fetch(WEB_APP_URL, { 
                    method: 'POST', 
                    mode: 'no-cors',
                    body: JSON.stringify(payload) 
                });
                
                // Com no-cors, não conseguimos ler res.ok, então assumimos sucesso se não houver erro
                status.className = "mt-3 text-center font-semibold text-green-600";
                status.innerText = "Enviado com sucesso! Aparecerá após a moderação.";
                this.reset();
            } catch (err) { 
                status.className = "mt-3 text-center font-semibold text-red-600";
                status.innerText = "Erro ao enviar. Tente novamente."; 
            } finally { 
                btn.disabled = false; 
                btn.innerText = "Enviar Comentário"; 
            }
        };

        function toggleFocusMode() {
            const isFocus = document.body.classList.toggle('focus-mode');
            if (isFocus) window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Lógica da Barra de Progresso
        window.onscroll = () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById("progress-bar").style.width = scrolled + "%";
        };

        document.getElementById('mobileMenuBtn').onclick = () => {
            const nav = document.getElementById('main-nav');
            nav.classList.toggle('hidden');
        };

        window.onload = carregarComentarios;
    </script>
</body>
</html>
`;

function processMarkdownFiles() {
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    const manifest = [];
    const toGenerate = [];
    let countIgnored = 0;

    const files = fs.readdirSync(inputDir).filter(f => path.extname(f) === '.md');

    files.forEach(file => {
        try {
            const markdownPath = path.join(inputDir, file);
            const baseName = file.replace('.md', '');
            const outputFilename = slugify(baseName) + '.html';
            const outputPath = path.join(outputDir, outputFilename);

            const stat = fs.statSync(markdownPath);
            
            // --- LÓGICA DE CACHE (VERIFICAÇÃO DE MUDANÇA) ---
            let needsUpdate = true;
            if (fs.existsSync(outputPath)) {
                const outputStat = fs.statSync(outputPath);
                if (stat.mtime <= outputStat.mtime) {
                    needsUpdate = false;
                }
            }

            const markdownFile = fs.readFileSync(markdownPath, 'utf8');
            const { data, content } = matter(markdownFile);
            const title = resolveTitle(data, content, outputFilename);
            const category = data.category || data.categoria || "Fé";

            const contagemPalavras = content.split(/\s+/).length;
            const tempoLeitura = Math.max(1, Math.ceil(contagemPalavras / 200)); 

            const href = `posts/${outputFilename}`;

            manifest.push({
                title,
                category,
                image: data.image || null,
                href,
                tempoLeitura,
                date: data.date || stat.mtime.toISOString(),
                mtime: stat.mtime.toISOString()
            });

            const entry = {
                href,
                outputPath,
                data: { ...data, title, category, tempoLeitura },
                htmlContent: applyBoldToSubtitles(md.render(content)),
                slug: slugify(baseName)
            };

            if (needsUpdate) {
                toGenerate.push(entry);
                console.log(`🆕 Alteração detectada: ${file}`);
            } else {
                countIgnored++;
            }
        } catch (err) {
            console.error(`❌ Erro ao processar o arquivo ${file}:`, err.message);
        }
    });

    const sortedManifest = [...manifest].sort((a, b) => {
        const dateDiff = new Date(b.date).getTime() - new Date(a.date).getTime();
        if (dateDiff !== 0) return dateDiff;
        return a.href.localeCompare(b.href, 'pt-BR');
    });

    fs.writeFileSync(path.join(outputDir, 'index.json'), JSON.stringify(sortedManifest, null, 2), 'utf8');

    // Gerar apenas os arquivos modificados
    toGenerate.forEach(g => {
        const currentIndex = sortedManifest.findIndex(m => m.href === g.href);
        let nextHref = '../index.html', prevHref = '../index.html';

        if (currentIndex !== -1) {
            if (currentIndex > 0) nextHref = `../${sortedManifest[currentIndex - 1].href}`;
            if (currentIndex < sortedManifest.length - 1) prevHref = `../${sortedManifest[currentIndex + 1].href}`;
        }

        // Lógica de Relacionados
        const getPalavrasChave = (texto) => texto.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, "").split(/\W+/).filter(p => p.length > 3);
        const palavrasAtuais = getPalavrasChave(g.data.title);

        const relacionados = sortedManifest
            .filter(m => m.href !== g.href)
            .map(m => {
                let score = 0;
                if (m.category === g.data.category) score += 10;
                const palavrasComparar = getPalavrasChave(m.title);
                score += palavrasAtuais.filter(p => palavrasComparar.includes(p)).length * 2;
                return { ...m, score };
            })
            .filter(m => m.score > 0).sort((a, b) => b.score - a.score).slice(0, 3);

        const finalHtml = htmlTemplate(g.data, g.htmlContent, prevHref, nextHref, g.slug, relacionados);
        fs.writeFileSync(g.outputPath, finalHtml, 'utf8');
    });

    if (toGenerate.length > 0) {
        console.log(`\n🚀 Conversão finalizada! ${toGenerate.length} arquivos atualizados.`);
    } else {
        console.log(`\n✨ Nada para atualizar. (${countIgnored} arquivos permanecem iguais)`);
    }
}

processMarkdownFiles();