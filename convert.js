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

function resolveTitle(data, markdownBody, fallbackHtmlName) {
    const titleFromFrontMatter = data.title || data['Título'] || data['titulo'];
    if (titleFromFrontMatter) return String(titleFromFrontMatter).trim();
    const matchTitulo = markdownBody.match(/^\s*T[ií]tulo:\s*(.+)$/mi);
    if (matchTitulo) return matchTitulo[1].trim();
    const matchH1 = markdownBody.match(/^\s*#\s+(.+?)\s*$/m);
    if (matchH1) return matchH1[1].trim();
    return fallbackHtmlName.replace('.html', '');
}

function applyBoldToSubtitles(html) {
    return html.replace(/<h([12])([^>]*)>([\s\S]*?)<\/h\1>/g, '<h$1$2><strong>$3</strong></h$1>');
}

// Template ajustado para incluir a meta-tag de categoria no HTML
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
    </style>
</head>
<body class="bg-gray-100 text-gray-800 font-sans">
    <header class="bg-black text-white p-6 shadow-md">
        <div class="container mx-auto flex justify-between items-center relative">
            <div class="flex items-center space-x-3">
                <a href="../home.html"><img src="../images/sem-bg-black.webp" alt="Logo" class="h-10"></a>
                <a href="../home.html"><h1 class="text-2xl font-bold">Essencialista</h1></a>
            </div>
            <div class="ml-auto flex items-center gap-4">
                <button id="mobileMenuBtn" class="md:hidden p-2 rounded bg-white/10 hover:bg-white/20"><i class="fas fa-bars"></i></button>
                <nav id="main-nav" class="hidden md:block absolute left-0 right-0 top-full w-full z-50 bg-black text-white p-4 md:static md:bg-transparent md:p-0">
                    <ul class="flex flex-col space-y-3 md:flex-row md:space-y-0 md:space-x-6">
                        <li><a href="../home.html" class="hover:text-orange-500">Início</a></li>
                        <li><a href="../home.html#articles-section" class="hover:text-orange-500">Artigos</a></li>
                        <li><a href="../about.html" class="hover:text-orange-500">Sobre</a></li>
                        <li><a href="../contact.html" class="hover:text-orange-500">Contato</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>
    <main class="container mx-auto mt-8 p-4 max-w-2xl">
        <article class="bg-white p-6 rounded-lg shadow-lg mb-10">
            ${data.image ? `<img src="../images/${data.image}" class="w-full h-64 object-cover mb-6 rounded-lg">` : ''}
            <h2 class="text-3xl font-bold mb-4">${data.title}</h2>
            <div class="space-y-4 leading-relaxed text-justify">${content}</div>
            <!--Link para a section Comentar-->
            <a href="#comentarios-artigo" class="text-orange-600 hover:underline">Comentar</a>
            <div class="mt-6 p-4 bg-gray-50 border-l-4 border-black rounded">
                <p class="italic">👉 ${data.signature || data.assinatura || 'Reflexão do dia'}</p>
                <p class="text-right mt-2 font-semibold">- Essencialista</p>
            </div>
            <div class="mt-6 flex justify-center gap-3">
                <a href="${prevHref}" class="bg-black text-white px-6 py-1 rounded-full">Anterior</a>
                <a href="${nextHref}" class="bg-black text-white px-6 py-1 rounded-full">Próximo</a>
                <!--Botão Voltar ao Home-->
                <a href="../home.html"
                    class="bg-black text-white px-6 py-1 rounded-full hover:bg-orange-500 transition duration-300">
                    Voltar ao Home
                </a>
                <!-- Botão de Voltar pra Cima-->
                <a href="#" class="bg-black text-white px-6 py-1 rounded-full hover:bg-gray-800 transition duration-300">
                    <i class="fas fa-arrow-up"></i>
                </a>
            </div>
        </article>

        <!-- Artigos Relacionados -->
        ${relacionados.length > 0 ? `
        <section class="mt-12">
            <h3 class="text-xl font-bold mb-4 border-b-2 border-orange-500 inline-block">Artigos Relacionados</h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                ${relacionados.map(r => `
                    <a href="../${r.href}" class="group bg-white rounded-lg shadow hover:shadow-md transition p-3 flex flex-col h-full">
                        <img src="../images/${r.image || 'default.webp'}" class="w-full h-24 object-cover rounded mb-2">
                        <span class="text-[8px] font-black text-orange-600 uppercase tracking-widest mb-1">${r.category}</span>
                        <h4 class="font-bold text-xs group-hover:text-orange-600 line-clamp-2 leading-tight">${r.title}</h4>
                    </a>
                `).join('')}
            </div>
        </section>
        ` : ''}

        <!-- Seção de Comentários -->
        <section id="comentarios-artigo" class="mt-20">
            <div class="bg-white p-6 rounded-xl shadow-lg">
                <h3 class="text-2xl font-bold mb-6 text-center">Deixe um comentário</h3>
                <form id="commentForm" class="space-y-4">
                    <input type="hidden" id="artigoId" value="${slug}">
                    <input type="text" id="nome" placeholder="Seu nome" required class="border border-gray-300 p-3 rounded-lg w-full focus:ring-2 focus:ring-orange-500 outline-none">
                    <input type="email" id="email" placeholder="Seu e-mail (privado)" required class="border border-gray-300 p-3 rounded-lg w-full focus:ring-2 focus:ring-orange-500 outline-none">
                    <textarea id="comentario" placeholder="Escreva seu comentário aqui..." required rows="4" class="border border-gray-300 p-3 rounded-lg w-full focus:ring-2 focus:ring-orange-500 outline-none"></textarea>
                    <button type="submit" id="btnEnviar" class="bg-black text-white px-6 py-3 rounded-lg hover:bg-orange-500 transition duration-300 w-full font-bold uppercase tracking-wide">Enviar Comentário</button>
                </form>
                <p id="msgStatus" class="mt-3 text-center font-semibold"></p>
            </div>

            <div id="listaComentarios" class="mt-10 space-y-4 mb-20">
                <h3 class="text-xl font-bold border-b-2 border-black inline-block mb-4">Comentários</h3>
                <div id="loader" class="text-gray-500 italic text-sm">Carregando comentários...</div>
            </div>
        </section>
    </main>
    <footer class="bg-black text-white p-4 mt-12">
        <div class="container mx-auto text-center">
            <p><img src="../images/sem-bg-black.webp" alt="Essencialista Logo" class="h-10 inline-block">Essencialista.
                Todos os direitos reservados &copy; 2025</p>
        </div>
    </footer>

    <script>
        const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbzvsw1a929OYZMd1sT6jYByl0iRE3a7xXBIiRoP51VREkmq0h6emxajQxkz0QadgUo0/exec';
        const slug = document.getElementById('artigoId').value;

        // Script para abrir/fechar o menu mobile 
        document.getElementById('mobileMenuBtn').onclick = () => { 
            const nav = document.getElementById('main-nav'); 
            nav.classList.toggle('hidden'); 
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
                    container.innerHTML += '<p class="text-gray-500 italic text-sm">Nenhum comentário ainda. Seja o primeiro!</p>';
                    return;
                }

                dados.forEach(c => {
                    const div = document.createElement('div');
                    div.className = 'bg-white p-4 rounded-lg shadow border-l-4 border-orange-500 animate-fade-in';
                    div.innerHTML = \`
                        <p class="font-bold text-gray-900 text-sm">\${c.nome}</p>
                        <p class="text-gray-700 text-sm mt-1">\${c.comentario}</p>
                        <p class="text-[10px] text-gray-400 mt-2 uppercase">\${new Date(c.data).toLocaleDateString('pt-BR')}</p>\`;
                    container.appendChild(div);
                });
            } catch (e) { 
                if(document.getElementById('loader')) document.getElementById('loader').innerText = "Erro ao carregar comentários."; 
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
            btn.disabled = true; btn.innerText = "Enviando...";
            try {
                await fetch(WEB_APP_URL, { 
                    method: 'POST', 
                    mode: 'no-cors', 
                    headers: { 'Content-Type': 'text/plain' }, 
                    body: JSON.stringify(payload) 
                });
                status.className = "mt-3 text-center font-semibold text-green-600 text-sm";
                status.innerText = "Enviado! Aparecerá após a moderação.";
                this.reset();
            } catch (err) {
                status.className = "mt-3 text-center font-semibold text-red-600 text-sm";
                status.innerText = "Erro ao enviar.";
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
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

    const manifest = [];
    const toGenerate = [];

    fs.readdirSync(inputDir).forEach(file => {
        if (path.extname(file) === '.md') {
            const markdownPath = path.join(inputDir, file);
            const markdownFile = fs.readFileSync(markdownPath, 'utf8');
            const { data, content } = matter(markdownFile);

            const htmlContent = applyBoldToSubtitles(md.render(content));
            const outputFilename = file.replace('.md', '.html').normalize('NFD').replace(/[\u0300-\u036f]/g, "");
            const title = resolveTitle(data, content, outputFilename);
            const category = data.category || data.categoria || "Fé"; // Pega do Markdown ou define padrão

            const outputPath = path.join(outputDir, outputFilename);
            const stat = fs.statSync(markdownPath);
            const href = `posts/${outputFilename}`;

            toGenerate.push({
                href,
                outputPath,
                data: { ...data, title, category },
                htmlContent,
                mtime: stat.mtime.toISOString()
            });

            manifest.push({
                title,
                category, // ADICIONADO AO MANIFESTO
                image: data.image || null,
                href,
                date: data.date || null,
                mtime: stat.mtime.toISOString()
            });
            console.log(`✅ ${file} [${category}] preparado.`);
        }
    });

    const indexPath = path.join(outputDir, 'index.json');
    fs.writeFileSync(indexPath, JSON.stringify(manifest, null, 2), 'utf8');

    // --- LÓGICA DE NAVEGAÇÃO CORRIGIDA ---
    // Ordenar manifesto pelo tempo (mais recente primeiro) para definir a sequência
    const sortedManifest = [...manifest].sort((a, b) => {
        const tA = new Date(a.date || a.mtime).getTime();
        const tB = new Date(b.date || b.mtime).getTime();
        return tB - tA;
    });

    // Gerar os arquivos HTML físicos
    toGenerate.forEach(g => {
        const currentIndex = sortedManifest.findIndex(m => m.href === g.href);

        let nextHref = '../home.html';
        let prevHref = '../home.html';

        if (currentIndex !== -1) {
            // Próximo (mais recente que o atual, se houver)
            if (currentIndex > 0) {
                const nextItem = sortedManifest[currentIndex - 1];
                nextHref = `../${nextItem.href}`;
            }
            // Anterior (mais antigo que o atual, se houver)
            if (currentIndex < sortedManifest.length - 1) {
                const prevItem = sortedManifest[currentIndex + 1];
                prevHref = `../${prevItem.href}`;
            }
        }

        // --- LÓGICA DE ARTIGOS RELACIONADOS (SEMELHANÇA DE TEMAS) ---
        const getPalavrasChave = (texto) => {
            return texto.toLowerCase()
                .normalize('NFD').replace(/[\u0300-\u036f]/g, "") // Remove acentos
                .split(/\W+/)
                .filter(p => p.length > 3); // Apenas palavras significativas
        };

        const palavrasAtuais = getPalavrasChave(g.data.title);

        const relacionados = sortedManifest
            .filter(m => m.href !== g.href) // Exclui o próprio artigo
            .map(m => {
                let score = 0;
                // Pontuação por categoria idêntica
                if (m.category === g.data.category) score += 10;

                // Pontuação por palavras em comum no título
                const palavrasComparar = getPalavrasChave(m.title);
                const palavrasComum = palavrasAtuais.filter(p => palavrasComparar.includes(p));
                score += palavrasComum.length * 2;

                return { ...m, score };
            })
            .filter(m => m.score > 0) // Apenas os que têm alguma semelhança
            .sort((a, b) => b.score - a.score) // Ordena pela maior pontuação
            .slice(0, 3); // Pega os 3 mais relevantes

        const finalHtml = htmlTemplate(g.data, g.htmlContent, prevHref, nextHref, path.basename(g.outputPath, '.html'), relacionados);
        fs.writeFileSync(g.outputPath, finalHtml, 'utf8');
    });

    console.log(`📄 Manifesto atualizado com categorias e navegação corrigida!`);
}

processMarkdownFiles();