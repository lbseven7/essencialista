const fs = require('fs');
const path = require('path');
const MarkdownIt = require('markdown-it');
const matter = require('gray-matter'); // Para ler metadados

// Após a inicialização do MarkdownIt
const md = new MarkdownIt();

// 1. Defina os caminhos (Mantenha como definimos antes)
const inputDir = path.join(__dirname, 'artigos'); 
const outputDir = path.join(__dirname, 'posts');  

// Função para resolver o título a partir de várias fontes
function resolveTitle(data, markdownBody, fallbackHtmlName) {
    const titleFromFrontMatter = data.title || data['Título'] || data['titulo'];
    if (titleFromFrontMatter) return String(titleFromFrontMatter).trim();

    // Procura por linha "Título: ..."
    const matchTitulo = markdownBody.match(/^\s*T[ií]tulo:\s*(.+)$/mi);
    if (matchTitulo) return matchTitulo[1].trim();

    // Procura primeiro heading H1 "# ..."
    const matchH1 = markdownBody.match(/^\s*#\s+(.+?)\s*$/m);
    if (matchH1) return matchH1[1].trim();

    // Fallback para nome do arquivo (sem .html)
    return fallbackHtmlName.replace('.html', '');
}

// Helper para aplicar negrito aos subtítulos (h1 e h2) do conteúdo gerado
function applyBoldToSubtitles(html) {
    return html.replace(/<h([12])([^>]*)>([\s\S]*?)<\/h\1>/g, '<h$1$2><strong>$3</strong></h$1>');
}

// Função para gerar o HTML completo com os dados variáveis
const htmlTemplate = (data, content, prevHref, nextHref) => `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${data.title} - Essencialista</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html {
            scroll-behavior: smooth;
        }
    </style>
</head>

<body class="bg-gray-100 text-gray-800 font-sans">

    <header class="bg-black text-white p-6 shadow-md">
        <div class="container mx-auto flex justify-between items-center relative">
            <div class="flex items-center space-x-3">
                <a href="../home.html">
                    <img src="../images/sem-bg-black.png" alt="Essencialista Logo" class="h-10">
                </a>
                <a href="../home.html">
                    <h1 class="text-2xl font-bold">Essencialista</h1>
                </a>
            </div>

            <div class="ml-auto flex items-center gap-4">
                <button id="mobileMenuBtn" class="md:hidden p-2 rounded bg-white/10 hover:bg-white/20"
                        aria-label="Abrir menu" aria-expanded="false">
                    <i class="fas fa-bars"></i>
                </button>

                <nav id="main-nav"
                     class="hidden md:block absolute left-0 right-0 top-full w-full z-50 bg-black text-white p-4 shadow-lg max-h-[60vh] overflow-y-auto
                            md:static md:bg-transparent md:p-0 md:shadow-none md:max-h-none md:overflow-visible">
                    <ul class="flex flex-col space-y-3 md:flex md:flex-row md:space-y-0 md:space-x-6">
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
            ${data.image ? `<img src="../images/${data.image}" alt="${data.title}" class="w-full h-64 object-cover mb-6 rounded-lg">` : ''}
            
            <h2 class="text-3xl font-bold mb-4">${data.title}</h2>
            
            <div class="space-y-4 leading-relaxed text-justify">
                ${content}
            </div>

            ${(() => {
                const signature = data.signature || data.assinatura || data.reflection;
                return `
                <div class="mt-6 p-4 bg-gray-50 border-l-4 border-black rounded">
                    ${signature ? `<p class="italic">👉 ${signature}</p>` : ``}
                    <p class="text-right mt-2 font-semibold">- Essencialista</p>
                </div>
                `;
            })()}
        </article>

        <div class="mt-6 text-center">
            <a href="#" class="bg-black text-white px-6 py-1 rounded-full hover:bg-gray-800 transition duration-300">
                <i class="fas fa-arrow-up"></i>
            </a>
        </div>

        <div class="mt-6 flex justify-center gap-3 flex-wrap">
            <a href="${prevHref || '../home.html'}" class="bg-black text-white px-6 py-1 rounded-full hover:bg-gray-800 transition duration-300">
                Artigo Anterior
            </a>
            <a href="${nextHref || '../home.html'}" class="bg-black text-white px-6 py-1 rounded-full hover:bg-gray-800 transition duration-300">
                Próximo Artigo
            </a>
        </div>

        <div class="mt-6 text-center">
            <a href="../home.html"
                class="bg-black text-white px-6 py-1 rounded-full hover:bg-orange-500 transition duration-300">
                Voltar ao Home
            </a>
        </div>
    </main>

    <footer class="bg-black text-white p-4 mt-12">
        <div class="container mx-auto text-center">
            <p><img src="../images/sem-bg-black.png" alt="Essencialista Logo" class="h-10 inline-block">Essencialista.
                Todos os direitos reservados &copy; 2025</p>
        </div>
    </footer>

    <script>
        (function () {
            const btn = document.getElementById('mobileMenuBtn');
            const nav = document.getElementById('main-nav');
            btn?.addEventListener('click', () => {
                const isHidden = nav.classList.contains('hidden');
                if (isHidden) {
                    nav.classList.remove('hidden');
                    nav.classList.add('block');
                    btn.setAttribute('aria-expanded', 'true');
                } else {
                    nav.classList.add('hidden');
                    nav.classList.remove('block');
                    btn.setAttribute('aria-expanded', 'false');
                }
            });
        })();
    </script>
</body>
</html>
`;

// Função principal de processamento
function processMarkdownFiles() {
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    const manifest = []; // manifesto dos posts
    const toGenerate = []; // posts a gerar com dados completos

    // Converte markdowns -> HTML e popula manifest (sem escrever ainda)
    fs.readdirSync(inputDir).forEach(file => {
        if (path.extname(file) === '.md') {
            const markdownPath = path.join(inputDir, file);
            const markdownFile = fs.readFileSync(markdownPath, 'utf8');

            const contentMatter = matter(markdownFile);
            const data = contentMatter.data;
            const markdownBody = contentMatter.content;

            // 1) Render Markdown -> HTML
            const rawHtmlContent = md.render(markdownBody);
            // 2) Aplicar negrito nos subtítulos h1/h2
            const htmlContent = applyBoldToSubtitles(rawHtmlContent);

            const outputFilename = file.replace('.md', '.html');
            const title = resolveTitle(data, markdownBody, outputFilename);

            const outputPath = path.join(outputDir, outputFilename);

            const stat = fs.statSync(markdownPath);
            const href = `posts/${outputFilename}`;

            // Adia a escrita para depois
            toGenerate.push({
                href,
                outputPath,
                data: { ...data, title },
                htmlContent,
                mtime: stat.mtime.toISOString()
            });

            manifest.push({
                title,
                image: data.image || null,
                href,
                date: data.date || null,
                mtime: stat.mtime.toISOString()
            });

            console.log(`✅ ${file} preparado para ${outputFilename}`);
        }
    });

    // Lê manifesto anterior para preservar itens existentes
    const indexPath = path.join(outputDir, 'index.json');
    let prevIndex = [];
    if (fs.existsSync(indexPath)) {
        try {
            prevIndex = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
        } catch {
            prevIndex = [];
        }
    }

    // Se não houver manifesto anterior, fallback: varre posts/ e inclui .html já existentes
    if (prevIndex.length === 0) {
        const existingHtml = fs.readdirSync(outputDir)
            .filter(name => path.extname(name) === '.html');
        for (const name of existingHtml) {
            const href = `posts/${name}`;
            // Evita duplicar o que foi gerado neste ciclo
            const already = manifest.find(p => p.href === href);
            if (already) continue;

            let title = name.replace('.html', '');
            try {
                const html = fs.readFileSync(path.join(outputDir, name), 'utf8');
                const m = html.match(/<title>([^<]+)<\/title>/i);
                if (m && m[1]) title = m[1].trim();
            } catch {}

            const stat = fs.statSync(path.join(outputDir, name));
            manifest.push({
                title,
                image: null,
                href,
                date: null,
                mtime: stat.mtime.toISOString()
            });
        }
    }

    // Merge: mantém anteriores que não foram substituídos
    const newHrefs = new Set(manifest.map(p => p.href));
    const merged = [
        ...manifest,
        ...prevIndex.filter(p => !newHrefs.has(p.href))
    ];

    // Calcula ordem igual ao carrossel (mais recente primeiro)
    const ts = p => {
        const tDate = p.date ? new Date(p.date).getTime() : 0;
        const tMtime = p.mtime ? new Date(p.mtime).getTime() : 0;
        return Math.max(tDate, tMtime);
    };
    const sorted = merged.slice().sort((a, b) => ts(b) - ts(a));

    // Mapa para achar índice rápido
    const indexByHref = new Map(sorted.map((p, i) => [p.href, i]));

    // Escreve HTMLs com "Anterior" e "Próximo" corretos
    for (const g of toGenerate) {
        const i = indexByHref.get(g.href);
        let nextHref = '../home.html';
        let prevHref = '../home.html';
        if (typeof i === 'number' && sorted.length > 1) {
            const nextItem = sorted[(i + 1) % sorted.length];
            const prevItem = sorted[(i - 1 + sorted.length) % sorted.length];
            nextHref = `../${nextItem.href}`; // ex.: ../posts/autodidata.html
            prevHref = `../${prevItem.href}`; // ex.: ../posts/o-artista-visível.html
        }
        const finalHtml = htmlTemplate(g.data, g.htmlContent, prevHref, nextHref);
        fs.writeFileSync(g.outputPath, finalHtml, 'utf8');
        console.log(`🧭 Navegação para ${path.basename(g.outputPath)} -> prev: ${prevHref} | next: ${nextHref}`);
    }

    // Salva manifesto JSON
    fs.writeFileSync(indexPath, JSON.stringify(merged, null, 2), 'utf8');
    console.log(`📄 Manifesto atualizado: posts/index.json (${merged.length} itens)`);
}

processMarkdownFiles();