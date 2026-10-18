# 🧙 The Tidy Witch

**Protótipo de jogo 3D desenvolvido com Python e OpenGL moderno**

## 📖 Sobre o projeto

**The Tidy Witch** é um projeto acadêmico de Computação Gráfica que propõe um jogo em primeira pessoa ambientado no quarto de uma bruxa.

A proposta é criar uma experiência aconchegante de exploração e organização, na qual o jogador deverá futuramente recolher e organizar livros, poções, cristais, vassouras e outros objetos mágicos.

Nesta etapa, o projeto corresponde à **Sprint 2 — Protótipo**, destinada à entrega das primeiras implementações do jogo.

O foco atual está na construção do ambiente tridimensional, no carregamento de modelos, nas transformações geométricas, na navegação em primeira pessoa e na implementação de colisões básicas.

## 🎯 Objetivos da Sprint 2

- Desenvolver uma aplicação 3D funcional utilizando OpenGL moderno.
- Criar o cenário inicial com base nas referências visuais do planejamento.
- Implementar movimentação e controle de câmera em primeira pessoa.
- Carregar e renderizar modelos tridimensionais externos.
- Aplicar transformações de translação, rotação e escala.
- Utilizar materiais para definir as cores dos objetos.
- Implementar colisões básicas com o cenário e os móveis.
- Organizar o código para facilitar as próximas etapas de desenvolvimento.

## ✅ Funcionalidades implementadas

### Ambiente tridimensional

Foi desenvolvido um quarto de bruxa com piso, paredes, teto, vigas de madeira, janela decorativa, móveis e diversos objetos mágicos.

A cena utiliza modelos tridimensionais carregados a partir de arquivos `.obj`, com materiais definidos em arquivos `.mtl`.

Entre os elementos presentes no cenário estão:

- Cama, estante, escrivaninha e mesas.
- Bancada de alquimia e bancada de trabalho.
- Caldeirão, tapete mágico e janela gótica decorativa.
- Livros, poções, velas, cristais e pergaminhos.
- Vassouras, cestos e outros elementos decorativos.
- Vigas, prateleiras e detalhes arquitetônicos.

### Câmera em primeira pessoa

Foi implementada uma câmera controlada pelo teclado e mouse, permitindo explorar o ambiente tridimensional.

**Controles:**

| Tecla/controle | Função                        |
| -------------- | ----------------------------- |
| W              | Movimentar para frente        |
| S              | Movimentar para trás          |
| A              | Movimentar para a esquerda    |
| D              | Movimentar para a direita     |
| Mouse          | Controlar a direção da câmera |
| Esc            | Capturar ou liberar o cursor  |

A movimentação utiliza `deltaTime` para reduzir a dependência da velocidade de deslocamento em relação à taxa de quadros.

### Transformações geométricas

As transformações são realizadas utilizando PyGLM, com matrizes Model, View e Projection.

A matriz Model permite posicionar, rotacionar e redimensionar os objetos do cenário de maneira independente.

A matriz View representa a câmera, enquanto a matriz Projection utiliza projeção em perspectiva.

No Vertex Shader, as transformações são aplicadas por meio da expressão:

```glsl
gl_Position = projection * view * model * vec4(a_pos, 1.0);
```

### Renderização com OpenGL moderno

A aplicação utiliza recursos do pipeline gráfico programável:

- **VAO:** configuração dos atributos dos vértices.
- **VBO:** armazenamento dos dados geométricos na GPU.
- **Vertex Shader:** processamento das posições dos vértices.
- **Fragment Shader:** definição das cores dos fragmentos.
- **Depth Test:** controle de profundidade para a renderização correta das superfícies.

### Carregamento de modelos e materiais

O sistema de carregamento interpreta informações básicas dos arquivos OBJ, incluindo vértices, faces e materiais.

Os materiais MTL fornecem as cores difusas `Kd`, utilizadas para colorir os modelos sem depender de texturas.

Essa abordagem permite adicionar novos objetos ao cenário sem modificar a lógica principal de renderização, desde que sejam compatíveis com o carregador implementado.

### Colisões básicas

Foi implementado um sistema de colisões no plano XZ, utilizando limites do quarto e caixas de colisão para móveis.

A câmera possui um raio de colisão, e a movimentação é verificada separadamente nos eixos X e Z, permitindo deslizar ao longo de obstáculos.

O sistema é uma implementação inicial, utilizando colisões simplificadas.

## 🎨 Escolhas estéticas

O projeto mantém a temática de fantasia e o ambiente aconchegante apresentados no planejamento inicial.

Para o protótipo, foi adotada uma estética **low-poly inspirada em jogos da era PlayStation 1 (PS1)**, caracterizada por:

- Modelos tridimensionais com geometria simplificada.
- Cores definidas diretamente pelos materiais.
- Pouca dependência de texturas.
- Móveis e objetos com formas estilizadas.
- Paleta com tons de madeira, roxo, azul e cores associadas a elementos mágicos.

O cenário foi organizado em áreas de descanso, estudo, alquimia e trabalho, buscando reproduzir a composição geral das referências visuais.

## 🔄 Modificações em relação ao planejamento

Durante o desenvolvimento do protótipo, foram realizados alguns ajustes em relação à proposta visual inicial.

**Simplificação dos modelos:** os objetos foram construídos com menos detalhes geométricos, priorizando a estética low-poly e a implementação com OpenGL.

**Materiais:** as cores são aplicadas a partir dos valores RGB dos arquivos MTL, sem utilização de texturas nesta etapa.

**Iluminação:** a iluminação Phong ainda não foi implementada. O protótipo utiliza diretamente as cores dos materiais.

**Organização do cenário:** alguns móveis e elementos decorativos foram reposicionados ou redimensionados para melhorar a circulação e a visualização do ambiente.

**Janela:** a janela gótica foi representada como um elemento decorativo, sem necessidade de criar uma abertura real na parede nesta versão.

Essas modificações preservam o tema e os objetivos centrais do projeto.

## 🛠️ Tecnologias utilizadas

| Tecnologia                | Utilização                             |
| ------------------------- | -------------------------------------- |
| Python                    | Linguagem principal                    |
| OpenGL moderno / PyOpenGL | Renderização 3D                        |
| GLFW                      | Janela, contexto gráfico e entradas    |
| PyGLM                     | Operações vetoriais e matriciais       |
| NumPy                     | Preparação dos arrays de vértices      |
| GLSL                      | Programação dos shaders                |
| OBJ / MTL                 | Armazenamento de geometria e materiais |

## 📁 Estrutura do projeto

```text
The-Tidy-Witch/
│
├── main.py
├── scene.py
├── camera.py
├── model.py
├── model_loader.py
├── requirements.txt
├── README.md
│
├── shaders/
│   ├── vertexShader.glsl
│   └── fragmentShader.glsl
│
└── models/
    ├── room_shell.obj
    ├── bed.obj
    ├── bookshelf.obj
    ├── book.obj
    ├── desk.obj
    ├── workbench.obj
    ├── alchemy_table.obj
    ├── round_rug.obj
    ├── gothic_window.obj
    ├── wooden_beams.obj
    ├── ...
    ├── palette.mtl
    ├── witch_lote1.mtl
    ├── witch_lote2.mtl
    └── witch_lote3.mtl
```

### Responsabilidades dos arquivos

- `main.py`: inicialização do OpenGL, entrada do usuário e laço principal.
- `scene.py`: criação, posicionamento e organização dos modelos do cenário.
- `camera.py`: câmera em primeira pessoa, movimentação e colisões.
- `model.py`: gerenciamento de VAO, VBO, transformações e renderização dos objetos.
- `model_loader.py`: leitura dos arquivos OBJ e MTL e preparação dos vértices.
- `shaders/`: shaders GLSL utilizados pela aplicação.
- `models/`: modelos e materiais tridimensionais.

## 🚀 Como executar

### Pré-requisitos

- Python compatível com as bibliotecas utilizadas.
- Placa gráfica e driver com suporte a OpenGL 4.6.
- Git, caso deseje clonar o repositório.

### 1. Obter o projeto

Clone o repositório:

```bash
git clone https://github.com/AtlasM30/The-Tidy-Witch.git
cd The-Tidy-Witch
```

Ou baixe os arquivos do repositório e extraia-os em uma pasta.

### 2. Instalar as dependências

No terminal, execute:

```bash
py -m pip install -r requirements.txt
```

Caso ainda não exista um `requirements.txt`, as principais dependências são:

```bash
py -m pip install glfw PyOpenGL PyOpenGL-accelerate PyGLM numpy
```

### 3. Executar a aplicação

Na pasta principal do projeto:

```bash
py main.py
```

Uma janela será aberta com o cenário tridimensional do quarto da bruxa.

Utilize WASD e o mouse para explorar o ambiente.

## 📌 Estado atual do desenvolvimento

O protótipo apresenta uma base gráfica e estrutural funcional, incluindo ambiente tridimensional, modelos, materiais, câmera, transformações e colisões básicas.

As mecânicas centrais de organização ainda não estão disponíveis, pois pertencem às próximas etapas do desenvolvimento.

### Funcionalidades planejadas para versões futuras

- Identificação de objetos interativos.
- Coleta, transporte e posicionamento de itens.
- Verificação de organização dos objetos nos locais corretos.
- Objetivos e progresso do jogador.
- Recompensas e personalização de vassouras.
- Iluminação pelo modelo de reflexão de Phong.
- Aperfeiçoamento de colisões, materiais e elementos visuais.

## 📚 Contexto acadêmico

Projeto desenvolvido para a disciplina de Computação Gráfica, com foco na aplicação prática de conceitos de renderização tridimensional, pipeline gráfico, transformações geométricas, câmera, shaders e organização de cenas.

**Projeto:** The Tidy Witch.
