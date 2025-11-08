const fs = require('fs');
const path = require('path');
const MarkdownIt = require('markdown-it');
const md = new MarkdownIt();

// 1. Defina os caminhos
const inputDir = path.join(__dirname, 'artigos'); // Onde estão seus arquivos .md
const outputDir = path.join(__dirname, 'posts');  // Onde os arquivos .html serão salvos

// 2. Defina o seu template HTML (A parte que envolve o conteúdo)
// Substitua o que está dentro das crases (``) pelo seu HTML real.
// O placeholder '{{CONTENT}}' será substituído pelo HTML gerado do Markdown.
const htmlTemplate = (title, content) => `
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} - Seu Blog Essencialista</title>
    <link rel="stylesheet" href="../css/style.css"> 
</head>
<body>
    <header>
        <nav>...</nav>
    </header>

    <main class="container-de-artigo">
        ${content}
    </main>

    <footer>
        <p>&copy; ${new Date().getFullYear()} Essencialista.</p>
    </footer>
</body>
</html>
`;

// Função para processar todos os arquivos Markdown
function processMarkdownFiles() {
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    fs.readdirSync(inputDir).forEach(file => {
        if (path.extname(file) === '.md') {
            const markdownPath = path.join(inputDir, file);
            const markdownContent = fs.readFileSync(markdownPath, 'utf8');
            
            // Simplesmente usa a primeira linha (assumindo que seja o título)
            const lines = markdownContent.split('\n');
            const titleLine = lines.find(line => line.startsWith('# '));
            const title = titleLine ? titleLine.substring(2).trim() : 'Novo Artigo';

            // Converte o Markdown para HTML
            const htmlContent = md.render(markdownContent);
            
            // Envolve o conteúdo no template
            const finalHtml = htmlTemplate(title, htmlContent);

            // Salva o arquivo HTML
            const outputFilename = file.replace('.md', '.html');
            const outputPath = path.join(outputDir, outputFilename);
            fs.writeFileSync(outputPath, finalHtml, 'utf8');

            console.log(`✅ ${file} convertido para ${outputFilename}`);
        }
    });
}

processMarkdownFiles();