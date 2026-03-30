# 🏛️ Projeto Essencialista

### 🚀 Essencialista
* **Acesse o Website:** https://essencialista.vercel.app/

O **Essencialista** é uma plataforma pessoal do artista **Leo Barbosa**, dedicada a artigos e reflexões sobre teologia, filosofia e vida espiritual. O projeto busca aprofundar o entendimento das Escrituras e a convivência com o contraditório, apresentando um design limpo, moderno e imersivo.

---

## ✨ Funcionalidades Principais

### 📖 Experiência de Leitura Imersiva
* **Modo Foco:** Leitura imersiva com fundo sépia e tipografia otimizada para estudos profundos.
* **Barra de Progresso:** Indicador visual no topo que acompanha o avanço da leitura.
* **Dark Mode:** Alternância inteligente com persistência via `localStorage`.
* **Tempo de Leitura:** Cálculo automático baseado na contagem de palavras de cada artigo.

### 🏷️ Organização e Automação
* **Geração Estática:** Script Node.js que converte Markdown em HTML com sistema de cache inteligente.
* **Filtros por Categoria:** Navegação rápida entre temas como **Fé, Ciência, Vida e Profecia**.
* **Artigos Relacionados:** Sugestões inteligentes ao final de cada post baseadas em tema e categoria.
* **Navegação Inteligente:** Botões "Anterior" e "Próximo" ordenados cronologicamente.

### 💬 Interação e Redes Sociais
* **Sistema de Comentários:** Integração com Google Sheets e painel de moderação exclusivo (`admin.html`).
* **Gerador de Cards:** Ferramenta interna (`generator.html`) para criar artes de divulgação profissionais para Status do WhatsApp.
* **Compartilhamento Direto:** Botão nativo para enviar estudos via WhatsApp com um clique.

---

## 💻 Tecnologias Utilizadas

| Tecnologia | Descrição |
| :--- | :--- |
| **Node.js** | Motor de geração de arquivos estáticos (`convert.js`). |
| **Python** | Inteligência para limpeza e correção ortográfica de transcrições (`editor-texto.py`). |
| **Tailwind CSS** | Estilização utilitária para layout 100% responsivo. |
| **JavaScript (ES6+)** | Lógica de filtragem, Modo Foco e integração com API. |
| **Google Apps Script** | Backend serverless para armazenamento de comentários. |

---

## ⚙️ Como Operar o Blog

### 1. Criar ou Tratar um Artigo
Para processar uma transcrição bruta ou organizar um texto existente, use o script Python:
```powershell
python editor-texto.py
```
*Isso corrigirá maiúsculas, removerá vícios de fala e salvará o arquivo na pasta `/artigos`.*

### 2. Gerar o Site
Sempre que criar ou editar um post, rode o conversor:
```powershell
node convert.js
```

### 3. Criar Artes para Redes Sociais
Abra o arquivo `generator.html` no seu navegador, cole o link do post e baixe o card PNG em alta resolução.

---

## 📂 Estrutura do Projeto
```text
├── artigos/            # Arquivos fonte em Markdown (.md)
├── posts/              # Arquivos finais em HTML e index.json
├── images/             # Imagens e thumbnails oficiais
├── cards/              # Local para salvar artes de divulgação
├── convert.js          # Script principal de conversão
├── editor-texto.py     # Script de tratamento de texto
├── generator.html      # Gerador de artes para WhatsApp
├── admin.html          # Painel de moderação de comentários
└── home.html           # Página principal do portal
```

---

## 📞 Contato
* **WhatsApp:** https://wa.me/73991182932
* **Email:** leob.com.br@gmail.com | essencialista7@gmail.com

---

## ⚖️ Licença
**© 2026 Essencialista - @lbseven7**
* **Conteúdo:** Propriedade intelectual do autor.
* **Código-Fonte:** Disponibilizado para estudo. É vedado o uso comercial, entre em contato.