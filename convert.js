const fs = require('fs');
const path = require('path');
const MarkdownIt = require('markdown-it');
const matter = require('gray-matter'); // Para ler metadados
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

// Função para gerar o HTML completo com os dados variáveis
const htmlTemplate = (data, content) => `
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
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <a href="../home.html">
                    <img src="../images/sem-bg-black.png" alt="Essencialista Logo" class="h-10">
                </a>
                <a href="../home.html">
                    <h1 class="text-2xl font-bold">Essencialista</h1>
                </a>
            </div>
            <nav>
                <ul class="flex space-x-6">
                    <li><a href="../home.html" class="hover:text-orange-500">Início</a></li>
                    <li><a href="../home.html#articles-section" class="hover:text-orange-500">Artigos</a></li>
                    <li><a href="../about.html" class="hover:text-orange-500">Sobre</a></li>
                    <li><a href="../contact.html" class="hover:text-orange-500">Contato</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container mx-auto mt-8 p-4 max-w-2xl">
        <article class="bg-white p-6 rounded-lg shadow-lg mb-10">
            ${data.image ? `<img src="../images/${data.image}" alt="${data.title}" class="w-full h-64 object-cover mb-6 rounded-lg">` : ''}
            
            <h2 class="text-3xl font-bold mb-4">${data.title}</h2>
            
            <div class="space-y-4 leading-relaxed text-justify">
                ${content}
            </div>

            ${data.reflection ? `
                <div class="mt-6 p-4 bg-gray-50 border-l-4 border-black rounded">
                    <p class="italic">👉 Reflexão final: ${data.reflection}</p>
                    <p class="text-right mt-2 font-semibold">- Essencialista</p>
                </div>
            ` : ''}
        </article>

        <div class="mt-6 text-center">
            <a href="#" class="bg-black text-white px-6 py-1 rounded-full hover:bg-gray-800 transition duration-300">
                <i class="fas fa-arrow-up"></i>
            </a>
        </div>
        <div class="mt-6 text-center">
            <a href="${data.nextArticle || '../home.html'}" class="bg-black text-white px-6 py-1 rounded-full hover:bg-gray-800 transition duration-300">
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

</body>
</html>
`;

// Função principal de processamento
function processMarkdownFiles() {
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    const manifest = []; // manifesto dos posts

    fs.readdirSync(inputDir).forEach(file => {
        if (path.extname(file) === '.md') {
            const markdownPath = path.join(inputDir, file);
            const markdownFile = fs.readFileSync(markdownPath, 'utf8');

            const contentMatter = matter(markdownFile);
            const data = contentMatter.data;
            const markdownBody = contentMatter.content;

            const htmlContent = md.render(markdownBody);

            const outputFilename = file.replace('.md', '.html');
            const title = resolveTitle(data, markdownBody, outputFilename);

            const finalHtml = htmlTemplate({ ...data, title }, htmlContent);

            const outputPath = path.join(outputDir, outputFilename);
            fs.writeFileSync(outputPath, finalHtml, 'utf8');

            const stat = fs.statSync(markdownPath);
            manifest.push({
                title,
                image: data.image || null,
                href: `posts/${outputFilename}`,
                date: data.date || null,
                mtime: stat.mtime.toISOString()
            });

            console.log(`✅ ${file} convertido para ${outputFilename}`);
        }
    });

    // Salva manifesto JSON
    const indexPath = path.join(outputDir, 'index.json');
    fs.writeFileSync(indexPath, JSON.stringify(manifest, null, 2), 'utf8');
    console.log(`📄 Manifesto atualizado: posts/index.json (${manifest.length} itens)`);
}

processMarkdownFiles();