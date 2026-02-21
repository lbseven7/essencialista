# 🏛️ Projeto Essencialista

### 🚀 Essencialista
* **Acesse o Website:** [https://essencialista.vercel.app/](https://essencialista.vercel.app/)

O **Essencialista** é uma plataforma pessoal do artista **Leo Barbosa**, dedicada a artigos e reflexões sobre teologia, filosofia e vida espiritual. O projeto busca aprofundar o entendimento das Escrituras e a convivência com o contraditório, apresentando um design limpo, moderno e imersivo.

---

## ✨ Funcionalidades Principais

### 📖 Experiência de Leitura Imersiva
* **Barra de Progresso:** Indicador visual no topo que acompanha o avanço da leitura.
* **Dark Mode (Modo Noturno):** Alternância inteligente com persistência via `localStorage`.
* **Header Dinâmico:** Efeito de *Glassmorphism* (transparência e desfoque) que se ajusta ao rolar a página.
* **Scroll Reveal:** Animações de entrada que revelam os artigos suavemente conforme o scroll.

### 🏷️ Organização e Navegação
* **Filtros por Categoria:** Navegação rápida entre temas como **Fé, Ciência, Vida e Profecia**.
* **Grid Responsivo:** Exibição dinâmica de artigos baseada em um banco de dados JSON (`posts/index.json`).
* **Skeleton Loading:** Carregamento elegante de imagens para evitar saltos de layout.
* **Navegação Clara:** Links estruturados para Início, Artigos, Sobre e Contato.

### 💬 Interação e Feedback
* **Sistema de Comentários:** Integração com Google Sheets (via Google Apps Script) para processamento de comentários em tempo real.
* **Feedback de Ações:** Botão de copiar e-mail com tooltip de confirmação e validação de formulários.

---

## 💻 Tecnologias Utilizadas

Este projeto é uma **Single Page Application (SPA)** focada em performance e simplicidade técnica.

| Tecnologia | Descrição |
| :--- | :--- |
| **HTML5** | Estrutura semântica do conteúdo. |
| **Tailwind CSS** | Estilização utilitária para um layout moderno e 100% responsivo. |
| **JavaScript (ES6+)** | Lógica de filtragem, Modo Escuro, manipulação de DOM e integração com API. |
| **Font Awesome** | Biblioteca de ícones para interface e botões de ação. |
| **Google Apps Script** | Backend serverless para armazenamento de comentários em planilhas. |

---

## 📂 Estrutura do Projeto

```text
├── posts/
│   ├── index.json          # Banco de dados dos artigos (JSON)
│   ├── artigo-exemplo.html # Páginas de conteúdo individual
├── images/
│   ├── sem-bg-black.png    # Logo oficial
│   ├── cruz.jpg            # Hero images
│   └── ...
├── home.html               # Página principal do portal
├── about.html              # Sobre o autor e o projeto
└── contact.html            # Informações de contato

Excelente! Unifiquei as informações técnicas anteriores (Dark Mode, Filtros, Barra de Progresso) com a sua descrição institucional e artística. O README agora reflete tanto a **essência filosófica** do projeto quanto a **robustez técnica** que implementamos.

Aqui está o `README.md` completo e atualizado:

---

```markdown
# 🏛️ Projeto Essencialista

### 🚀 Essencialista
* **Acesse o Website:** [https://essencialista.vercel.app/](https://essencialista.vercel.app/)

O **Essencialista** é uma plataforma pessoal do artista **Leo Barbosa**, dedicada a artigos e reflexões sobre teologia, filosofia e vida espiritual. O projeto busca aprofundar o entendimento das Escrituras e a convivência com o contraditório, apresentando um design limpo, moderno e imersivo.

---

## ✨ Funcionalidades Principais

### 📖 Experiência de Leitura Imersiva
* **Barra de Progresso:** Indicador visual no topo que acompanha o avanço da leitura.
* **Dark Mode (Modo Noturno):** Alternância inteligente com persistência via `localStorage`.
* **Header Dinâmico:** Efeito de *Glassmorphism* (transparência e desfoque) que se ajusta ao rolar a página.
* **Scroll Reveal:** Animações de entrada que revelam os artigos suavemente conforme o scroll.

### 🏷️ Organização e Navegação
* **Filtros por Categoria:** Navegação rápida entre temas como **Fé, Ciência, Vida e Profecia**.
* **Grid Responsivo:** Exibição dinâmica de artigos baseada em um banco de dados JSON (`posts/index.json`).
* **Skeleton Loading:** Carregamento elegante de imagens para evitar saltos de layout.
* **Navegação Clara:** Links estruturados para Início, Artigos, Sobre e Contato.

### 💬 Interação e Feedback
* **Sistema de Comentários:** Integração com Google Sheets (via Google Apps Script) para processamento de comentários em tempo real.
* **Feedback de Ações:** Botão de copiar e-mail com tooltip de confirmação e validação de formulários.

---

## 💻 Tecnologias Utilizadas

Este projeto é uma **Single Page Application (SPA)** focada em performance e simplicidade técnica.

| Tecnologia | Descrição |
| :--- | :--- |
| **HTML5** | Estrutura semântica do conteúdo. |
| **Tailwind CSS** | Estilização utilitária para um layout moderno e 100% responsivo. |
| **JavaScript (ES6+)** | Lógica de filtragem, Modo Escuro, manipulação de DOM e integração com API. |
| **Font Awesome** | Biblioteca de ícones para interface e botões de ação. |
| **Google Apps Script** | Backend serverless para armazenamento de comentários em planilhas. |

---

## 📂 Estrutura do Projeto

```text
├── posts/
│   ├── index.json          # Banco de dados dos artigos (JSON)
│   ├── artigo-exemplo.html # Páginas de conteúdo individual
├── images/
│   ├── sem-bg-black.png    # Logo oficial
│   ├── cruz.jpg            # Hero images
│   └── ...
├── home.html               # Página principal do portal
├── about.html              # Sobre o autor e o projeto
└── contact.html            # Informações de contato

```

---

## ⚙️ Como Executar Localmente

O projeto é estático e de fácil execução:

1. **Clone o repositório:**
```bash
git clone [https://github.com/lbseven7/essencialista.git](https://github.com/lbseven7/essencialista.git)
cd essencialista

```


2. **Abra o projeto:**
Basta abrir o arquivo `home.html` em qualquer navegador moderno.
> *Nota: É necessária conexão com a internet para carregar o Tailwind CSS e o Font Awesome via CDN.*



---

## 📝 Conteúdo e Temática

Os artigos abordam a profundidade da experiência humana sob a ótica cristã:

* A centralidade do sacrifício de Cristo (Romanos 15:4).
* A justiça pela fé e a diferença entre legalismo e Evangelho.
* Reflexões sobre ciência da mente, cultura e educação espiritual.
* Análises proféticas e os desafios do mundo contemporâneo.

---

## 📞 Contato

* **WhatsApp:** [Enviar Mensagem](https://wa.me/73991182932)
* **Email:** `leob.com.br@gmail.com` | `essencialista7@gmail.com`
---

## ⚖️ Licença

**Todos os direitos reservados.**
© 2026 Essencialista - @lbseven7

* **Conteúdo (Textos e Artigos):** Propriedade intelectual do autor, não podendo ser reproduzidos sem permissão expressa.
* **Código-Fonte:** Disponibilizado para estudo e fins não comerciais. Para replicação ou uso comercial, entre em contato com o proprietário.



```