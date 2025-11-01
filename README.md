
## 📄Projeto Essencialista

### 🚀 Essencialista

O projeto **Essencialista** é um website focado em artigos e reflexões sobre a essência da fé, teologia, filosofia e vida espiritual, buscando aprofundar o entendimento das Escrituras e a convivência com o contraditório. O design é limpo e moderno, desenvolvido com **Tailwind CSS**.

### ✨ Funcionalidades Principais

  * **Página Inicial (Home):** Banner de destaque, citação bíblica central (Romanos 15:4) e chamada para ação.
  * **Artigos em Destaque:** Exibição em *grid* responsivo dos artigos mais recentes, como "Ensinados por Deus", "A Justiça pela Fé" e "O Poder da Palavra".
  * **Navegação Clara:** Menu de cabeçalho com links para **Início**, **Artigos**, **Sobre** e **Contato**.
  * **Responsividade:** Layout adaptável a diferentes tamanhos de tela (desktop, tablet e mobile).
  * **Scroll Suave:** Configuração de `scroll-behavior: smooth` para uma melhor experiência de navegação entre seções.

### 💻 Tecnologias Utilizadas

Este projeto é uma Single Page Application (SPA) baseada em HTML puro, estilizada por um framework utilitário.

| Tecnologia | Descrição |
| :--- | :--- |
| **HTML5** | Estrutura básica do conteúdo. |
| **Tailwind CSS** | Framework CSS utilitário para estilização rápida e responsiva. |
| **Font Awesome** | Biblioteca de ícones (utilizada no footer e no botão "subir ao topo"). |
| **JavaScript** | Utilizado apenas para o link de *scroll* suave (embutido via CSS `scroll-behavior`). |

### 📁 Estrutura do Projeto

A estrutura de arquivos esperada é a seguinte:

```
├── articles/
│   ├── article1.html
│   ├── article2.html
│   └── ...
├── images/
│   ├── sem-bg-black.png
│   ├── cruz.jpg
│   └── loading.png
├── home.html (Página principal)
├── about.html
└── contact.html
```

### ⚙️ Como Executar Localmente

Siga estas etapas simples para colocar o projeto em funcionamento na sua máquina:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/lbseven7/essencialista.git
    cd essencialista
    ```

2.  **Abra o arquivo:**
    O projeto é estático. Simplesmente abra o arquivo `home.html` no seu navegador de preferência.

    > Nota: Como o Tailwind CSS está sendo carregado via CDN (`<script src="https://cdn.tailwindcss.com"></script>`), não há necessidade de um *build* local para a estilização funcionar.

### 📝 Conteúdo e Artigos

Os artigos apresentados na seção de destaque (`featured-articles`) abordam temas como:

  * A centralidade do sacrifício de Cristo.
  * A necessidade da revelação divina para o entendimento das Escrituras.
  * A diferença entre legalismo e o Evangelho da Graça.
  * Reflexões sobre a vida espiritual, conhecimento e cultura mental.

### 📞 Contato

O rodapé do projeto inclui links para contato:

  * **WhatsApp:** `https://wa.me/73991182932`
  * **Email:** `mailto:contato@essencialista.com`
  * **Website Relacionado:** `https://www.reflorbrasil.com.br`

-----

### ⚖️ Licença

O conteúdo e o código deste projeto estão protegidos por direitos autorais (`&copy; 2024 Essencialista`).

  * **Conteúdo (Textos e Artigos):** Todos os artigos e textos são de propriedade da Essencialista e não podem ser reproduzidos sem permissão expressa.
  * **Código-Fonte (HTML/CSS):** O código-fonte deste website, incluindo a estrutura HTML e a estilização baseada em Tailwind CSS, é fornecido "no estado em que se encontra". Para usos não comerciais e de aprendizado, é permitido o estudo. Para uso comercial ou replicação, é necessária a autorização do proprietário.

**Todos os direitos reservados.**

-----