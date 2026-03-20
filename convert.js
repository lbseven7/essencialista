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
    return html.replace(/<h([12])([^>]*)>([\s\S]*?)<\/h\1>/g, '<h$1$2><strong>$3</strong></h$1>');
}

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
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html { scroll-behavior: smooth; }
        .animate-fade-in { animation: fadeIn 0.6s ease forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        /* Garante que imagens dentro do conteúdo não estourem o layout */
        .content-area img { max-width: 100%; height: auto; border-radius: 0.5rem; margin: 1.5rem 0; }
    </style>
</head>
<body class="bg-gray-100 text-gray-800 font-sans">
    <header class="bg-black text-white p-6 shadow-md sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center relative">
            <div class="flex items-center space-x-3">
                <a href="../home.html"><img src="../images/sem-bg-black.webp" alt="Logo" class="h-10"></a>
                <a href="../home.html"><h1 class="text-2xl font-bold">Essencialista</h1></a>
            </div>
            <div class="flex items-center gap-4">
                <button id="mobileMenuBtn" class="md:hidden p-2 rounded bg-white/10 hover:bg-white/20 min-w-[44px]"><i class="fas fa-bars"></i></button>
                <nav id="main-nav" class="hidden md:block absolute left-0 right-0 top-full w-full z-50 bg-black text-white p-4 md:static md:bg-transparent md:p-0">
                    <ul class="flex flex-col space-y-3 md:flex-row md:space-y-0 md:space-x-6">
                        <li><a href="../home.html" class="hover:text-orange-500 font-bold">Início</a></li>
                        <li><a href="../home.html#featured-articles" class="hover:text-orange-500 font-bold">Artigos</a></li>
                        <li><a href="../about.html" class="hover:text-orange-500 font-bold">Sobre</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>
    <main class="container mx-auto mt-8 p-4 max-w-2xl">
        <article class="bg-white p-6 rounded-lg shadow-lg mb-10 animate-fade-in">
            ${data.image ? `<img src="../images/${data.image}" class="w-full h-64 object-cover mb-6 rounded-lg shadow">` : ''}
            <div class="mb-2"><span class="text-orange-600 font-black text-xs uppercase tracking-widest">${data.category}</span></div>
            <h2 class="text-3xl font-bold mb-6 leading-tight">${data.title}</h2>
            <div class="content-area space-y-4 leading-relaxed text-justify text-gray-700">${content}</div>
            
            <div class="mt-8 pt-6 border-t border-gray-100">
                 <a href="#comentarios-artigo" class="inline-block bg-gray-100 text-gray-600 px-4 py-2 rounded-lg hover:text-orange-600 transition">
                    <i class="far fa-comment-dots mr-2"></i>Deixar um comentário
                 </a>
            </div>

            <div class="mt-6 p-4 bg-gray-50 border-l-4 border-orange-500 rounded">
                <p class="italic text-gray-600">👉 ${data.signature || data.assinatura || 'Reflexão para uma vida com propósito.'}</p>
                <p class="text-right mt-2 font-bold text-sm">- Essencialista</p>
            </div>

            <div class="mt-10 flex flex-wrap justify-center gap-3">
                <a href="${prevHref}" class="bg-black text-white px-5 py-2 rounded-full text-sm hover:bg-orange-600 transition">← Anterior</a>
                <a href="../home.html" class="bg-black text-white px-5 py-2 rounded-full text-sm hover:bg-orange-600 transition font-bold">Home</a>
                <a href="${nextHref}" class="bg-black text-white px-5 py-2 rounded-full text-sm hover:bg-orange-600 transition">Próximo →</a>
            </div>
        </article>

        ${relacionados.length > 0 ? `
        <section class="mt-12">
            <h3 class="text-xl font-bold mb-6 border-b-4 border-orange-500 inline-block">Você também pode gostar</h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                ${relacionados.map(r => `
                    <a href="../${r.href}" class="group bg-white rounded-lg shadow hover:shadow-xl transition-all p-3 flex flex-col h-full">
                        <img src="../images/${r.image || 'default.webp'}" class="w-full h-24 object-cover rounded mb-2">
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
        const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbzvsw1a929OYZMd1sT6jYByl0iRE3a7xXBIiRoP51VREkmq0h6emxajQxkz0QadgUo0/exec';
        const slug = document.getElementById('artigoId').value;

        document.getElementById('mobileMenuBtn').onclick = () => { 
            document.getElementById('main-nav').classList.toggle('hidden'); 
        };

        async function carregarComentarios() {
            const container = document.getElementById('listaComentarios');
            try {
                const res = await fetch(WEB_APP_URL + '?artigoId=' + slug);
                const dados = await res.json();
                const loader = document.getElementById('loader');
                if(loader) loader.remove();

                const titulo = container.querySelector('h3');
                container.innerHTML = '';
                container.appendChild(titulo);

                if (!dados || dados.length === 0) {
                    container.insertAdjacentHTML('beforeend', '<p class="text-gray-500 italic text-sm">Nenhum comentário ainda. Seja o primeiro a participar!</p>');
                    return;
                }

                dados.forEach(c => {
                    const div = document.createElement('div');
                    div.className = 'bg-white p-4 rounded-lg shadow border-l-4 border-orange-500 animate-fade-in';
                    div.innerHTML = \`
                        <div class="flex justify-between items-start mb-1">
                            <p class="font-bold text-gray-900 text-sm">\${c.nome}</p>
                            <p class="text-[9px] text-gray-400 uppercase">\${new Date(c.data).toLocaleDateString('pt-BR')}</p>
                        </div>
                        <p class="text-gray-700 text-sm mt-1 leading-relaxed">\${c.comentario}</p>\`;
                    container.appendChild(div);
                });
            } catch (e) { 
                if(document.getElementById('loader')) document.getElementById('loader').innerText = "Não foi possível carregar os comentários."; 
            }
        }

        document.getElementById("commentForm").onsubmit = async function (e) {
            e.preventDefault();
            const btn = document.getElementById("btnEnviar");
            const status = document.getElementById("msgStatus");
            const payload = {
                artigoId: slug,
                nome: document.getElementById("nome").value,
                email: document.getElementById("email").value,
                comentario: document.getElementById("comentario").value
            };
            btn.disabled = true; btn.innerText = "Processando...";
            try {
                await fetch(WEB_APP_URL, { 
                    method: 'POST', 
                    mode: 'no-cors', 
                    headers: { 'Content-Type': 'text/plain' }, 
                    body: JSON.stringify(payload) 
                });
                status.className = "mt-3 text-center font-semibold text-green-600 text-sm";
                status.innerText = "Obrigado! Seu comentário foi enviado para aprovação.";
                this.reset();
            } catch (err) {
                status.className = "mt-3 text-center font-semibold text-red-600 text-sm";
                status.innerText = "Falha na conexão. Tente novamente mais tarde.";
            } finally { 
                btn.disabled = false; btn.innerText = "Enviar Comentário"; 
            }
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

    const files = fs.readdirSync(inputDir).filter(f => path.extname(f) === '.md');

    files.forEach(file => {
        const markdownPath = path.join(inputDir, file);
        const markdownFile = fs.readFileSync(markdownPath, 'utf8');
        const { data, content } = matter(markdownFile);

        const htmlContent = applyBoldToSubtitles(md.render(content));
        
        // Slugificação melhorada para o nome do arquivo de saída
        const baseName = file.replace('.md', '');
        const outputFilename = slugify(baseName) + '.html';
        
        const title = resolveTitle(data, content, outputFilename);
        const category = data.category || data.categoria || "Fé";

        const outputPath = path.join(outputDir, outputFilename);
        const stat = fs.statSync(markdownPath);
        const href = `posts/${outputFilename}`;

        toGenerate.push({
            href,
            outputPath,
            data: { ...data, title, category },
            htmlContent,
            mtime: stat.mtime.toISOString(),
            date: data.date || stat.mtime.toISOString() // Prioriza data do front-matter
        });

        manifest.push({
            title,
            category,
            image: data.image || null,
            href,
            date: data.date || stat.mtime.toISOString(),
            mtime: stat.mtime.toISOString()
        });
        
        console.log(`✅ ${file} [${category}] processado.`);
    });

    // Salva o index.json
    fs.writeFileSync(path.join(outputDir, 'index.json'), JSON.stringify(manifest, null, 2), 'utf8');

    // Ordenação do manifesto para navegação (Mais novos primeiro)
    const sortedManifest = [...manifest].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

    // Gerar os arquivos HTML físicos
    toGenerate.forEach(g => {
        const currentIndex = sortedManifest.findIndex(m => m.href === g.href);

        let nextHref = '../home.html';
        let prevHref = '../home.html';

        if (currentIndex !== -1) {
            // "Próximo" no blog geralmente é o post mais RECENTE (index menor no array ordenado DESC)
            if (currentIndex > 0) {
                const newerPost = sortedManifest[currentIndex - 1];
                nextHref = `../${newerPost.href}`;
            }
            // "Anterior" no blog geralmente é o post mais ANTIGO (index maior no array ordenado DESC)
            if (currentIndex < sortedManifest.length - 1) {
                const olderPost = sortedManifest[currentIndex + 1];
                prevHref = `../${olderPost.href}`;
            }
        }

        // Lógica de Relacionados
        const getPalavrasChave = (texto) => {
            return texto.toLowerCase()
                .normalize('NFD').replace(/[\u0300-\u036f]/g, "")
                .split(/\W+/)
                .filter(p => p.length > 3);
        };

        const palavrasAtuais = getPalavrasChave(g.data.title);

        const relacionados = sortedManifest
            .filter(m => m.href !== g.href)
            .map(m => {
                let score = 0;
                if (m.category === g.data.category) score += 10;
                const palavrasComparar = getPalavrasChave(m.title);
                const palavrasComum = palavrasAtuais.filter(p => palavrasComparar.includes(p));
                score += palavrasComum.length * 2;
                return { ...m, score };
            })
            .filter(m => m.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, 3);

        const finalHtml = htmlTemplate(
            g.data, 
            g.htmlContent, 
            prevHref, 
            nextHref, 
            path.basename(g.outputPath, '.html'), 
            relacionados
        );
        
        fs.writeFileSync(g.outputPath, finalHtml, 'utf8');
    });

    console.log(`\n🚀 Conversão finalizada! ${toGenerate.length} artigos gerados.`);
}

processMarkdownFiles();