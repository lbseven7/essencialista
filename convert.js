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
const htmlTemplate = (data, content, prevHref, nextHref) => `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="category" content="${data.category || 'Geral'}">
    <title>${data.title} - Essencialista</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html { scroll-behavior: smooth; }
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
                <nav id="main-nav" class="hidden md:block absolute left-0 right-0 top-full w-full z-[100] bg-black text-white p-4 md:static md:bg-transparent md:p-0">
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
            <div class="mt-6 p-4 bg-gray-50 border-l-4 border-black rounded">
                <p class="italic">👉 ${data.signature || data.assinatura || 'Reflexão do dia'}</p>
                <p class="text-right mt-2 font-semibold">- Essencialista</p>
            </div>
        </article>
        <div class="mt-6 flex justify-center gap-3">
            <a href="${prevHref}" class="bg-black text-white px-6 py-1 rounded-full">Anterior</a>
            <a href="${nextHref}" class="bg-black text-white px-6 py-1 rounded-full">Próximo</a>
        </div>
    </main>
    <footer class="bg-black text-white p-4 mt-12">
        <div class="container mx-auto text-center">
            <p><img src="../images/sem-bg-black.webp" alt="Essencialista Logo" class="h-10 inline-block">Essencialista.
                Todos os direitos reservados &copy; 2025</p>
        </div>
    </footer>

    <script>
        // Script para abrir/fechar o menu mobile 
        document.getElementById('mobileMenuBtn').onclick = () => { 
            const nav = document.getElementById('main-nav'); 
            nav.classList.toggle('hidden'); 
        };
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

        const finalHtml = htmlTemplate(g.data, g.htmlContent, prevHref, nextHref);
        fs.writeFileSync(g.outputPath, finalHtml, 'utf8');
    });

    console.log(`📄 Manifesto atualizado com categorias e navegação corrigida!`);
}

processMarkdownFiles();