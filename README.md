# 🎯 ValorScript

> Uma Linguagem Específica de Domínio (DSL) para descrição de estratégias e táticas do jogo Valorant.

## 📌 Sobre o projeto

A **ValorScript** é uma Linguagem Específica de Domínio (DSL) desenvolvida para representar, de forma estruturada, estratégias e táticas utilizadas em partidas de **Valorant**.

A linguagem permite descrever informações como:

* estratégia utilizada;
* rodada;
* mapa;
* objetivo;
* composição da equipe;
* jogadores e agentes;
* habilidades utilizadas;
* posições;
* tempo de espera;
* local de plantio da Spike.

O projeto foi desenvolvido como atividade acadêmica envolvendo **linguagens específicas de domínio, análise léxica, análise sintática e gramáticas EBNF**.

---

## 🎯 Objetivo

O objetivo da ValorScript é criar uma linguagem simples e específica para representar estratégias de Valorant de maneira estruturada e fácil de interpretar.

Em vez de descrever uma estratégia utilizando texto livre, a linguagem utiliza uma sintaxe padronizada.

Por exemplo:

```text
STRATEGY ataqueA {
    ROUND 5
    MAP Ascent
    OBJECTIVE A

    TEAM ATTACK {

        PLAYERS {
            PLAYER Nathan Jett
            PLAYER Joao Sova
        }

        ACTIONS {
            USE Jett Dash AT A_Main
            USE Sova Reveal AT A
            POSITION A_Main
            WAIT 5
            PLANT A
        }
    }
}
```

---

## 🎮 Domínio

O domínio escolhido para a DSL é o jogo **Valorant**, especificamente a descrição de estratégias de uma equipe durante uma rodada.

A escolha desse domínio permite trabalhar com conceitos naturalmente estruturados, como:

```text
Strategy
 ├── Round
 ├── Map
 ├── Objective
 └── Team
      ├── Players
      └── Actions
```

Isso torna o domínio adequado para uma DSL porque possui um conjunto específico de conceitos, regras e operações que podem ser representados por uma linguagem própria.

---

## ✨ Principais características

A ValorScript possui suporte para:

### Estratégias

```text
STRATEGY ataqueA {
    ...
}
```

### Rodadas

```text
ROUND 5
```

### Mapas

```text
MAP Ascent
```

### Objetivos

```text
OBJECTIVE A
```

### Equipes

```text
TEAM ATTACK {
    ...
}
```

ou:

```text
TEAM DEFENSE {
    ...
}
```

### Jogadores e agentes

```text
PLAYERS {
    PLAYER Nathan Jett
    PLAYER Joao Sova
}
```

### Utilização de habilidades

```text
USE Jett Dash AT A_Main
```

### Posicionamento

```text
POSITION BSite
```

### Espera

```text
WAIT 5
```

### Plantio

```text
PLANT A
```

---

# 🔤 Tokens

A linguagem possui diferentes categorias de tokens.

| Categoria       | Exemplos                           |
| --------------- | ---------------------------------- |
| Palavras-chave  | `STRATEGY`, `ROUND`, `MAP`, `TEAM` |
| Tipos de equipe | `ATTACK`, `DEFENSE`                |
| Ações           | `USE`, `POSITION`, `WAIT`, `PLANT` |
| Identificadores | `ataqueA`, `Nathan`, `Jett`        |
| Números         | `1`, `5`, `10`                     |
| Símbolos        | `{`, `}`                           |
| Operador        | `AT`                               |

Os identificadores seguem o formato:

```text
/[a-zA-Z_][a-zA-Z0-9_]*/
```

Os números seguem:

```text
/[0-9]+/
```

---

# 📐 Gramática

A gramática da ValorScript foi implementada utilizando a sintaxe do **Lark**, baseada nas regras definidas em EBNF.

A regra inicial da linguagem é:

```text
start
```

A partir dela, a estrutura principal é:

```text
start
    → strategy
```

Uma estratégia possui a seguinte estrutura:

```text
strategy
    → STRATEGY ID {
        ROUND NUMBER
        MAP ID
        OBJECTIVE ID
        TEAM team_type {
            PLAYERS {
                player+
            }
            ACTIONS {
                action+
            }
        }
    }
```

As ações disponíveis incluem:

```text
USE ID ID AT ID
POSITION ID
WAIT NUMBER
PLANT ID
```

A gramática completa pode ser encontrada no arquivo:

```text
grammar.lark
```

---

# 🌳 Análise sintática

A análise sintática é realizada utilizando o **Lark Parser** com o algoritmo **LALR**.

A partir de um programa escrito em ValorScript, o parser verifica se a sequência de tokens segue as regras definidas na gramática.

Quando o programa é válido, é construída uma árvore sintática.

Exemplo simplificado:

```text
start
└── strategy
    ├── ataqueA
    ├── round 5
    ├── map Ascent
    ├── objective A
    └── team
        ├── attack
        ├── players
        │   ├── Nathan → Jett
        │   └── Joao → Sova
        └── actions
            ├── USE Jett → Dash @ A_Main
            ├── USE Sova → Reveal @ A
            ├── POSITION A_Main
            ├── WAIT 5
            └── PLANT A
```

A árvore também pode ser visualizada utilizando o método `pretty()` do Lark.

---

# 🧠 Análise semântica

Além da análise sintática, o projeto possui verificações semânticas básicas implementadas em `checker.py`.

Essas verificações analisam se determinados elementos fazem sentido dentro do domínio da linguagem.

Por exemplo:

```text
USE Jett Dash AT A
```

é uma utilização válida porque `Dash` pertence à Jett.

Enquanto:

```text
USE Jett Turret AT A
```

pode ser identificada como semanticamente inválida, pois `Turret` pertence a outro agente.

Também são verificadas as localizações utilizadas por:

```text
POSITION
PLANT
```

Dessa forma, o projeto diferencia:

```text
Análise sintática
```

de:

```text
Análise semântica
```

---

# 📁 Estrutura do projeto

```text
valorant-dsl/
│
├── examples/
│   ├── valido_01.vsl
│   ├── valido_02.vsl
│   ├── valido_03.vsl
│   ├── valido_04.vsl
│   ├── valido_05.vsl
│   ├── invalido_01.vsl
│   ├── invalido_02.vsl
│   └── invalido_03.vsl
│
├── tests/
│   └── test_dsl.py
│
├── checker.py
├── grammar.lark
├── main.py
├── parser.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Responsabilidade dos arquivos

| Arquivo            | Responsabilidade                      |
| ------------------ | ------------------------------------- |
| `grammar.lark`     | Define a gramática da ValorScript     |
| `parser.py`        | Cria e executa o parser Lark          |
| `checker.py`       | Realiza verificações semânticas       |
| `main.py`          | Executa e apresenta os resultados     |
| `examples/`        | Armazena exemplos válidos e inválidos |
| `tests/`           | Contém os testes automatizados        |
| `requirements.txt` | Lista as dependências                 |
| `README.md`        | Documentação do projeto               |

---

# ⚙️ Tecnologias utilizadas

* **Python**
* **Lark**
* **Rich**
* **unittest**
* **EBNF**
* **LALR Parser**

---

# 🚀 Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/valorant-dsl.git
cd valorant-dsl
```

## 2. Criar o ambiente virtual

### Windows

```powershell
python -m venv .venv
```

Ativar:

```powershell
.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

# ▶️ Executando a DSL

Para executar os exemplos:

```bash
python main.py
```

O programa analisa os arquivos `.vsl` presentes na pasta:

```text
examples/
```

Para cada arquivo, são apresentados:

* resultado da análise sintática;
* tokens reconhecidos;
* árvore sintática;
* árvore visual;
* resultado da análise semântica.

---

# 🧪 Testes

Os testes automatizados podem ser executados com:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam situações como:

* estratégia válida;
* `WAIT` recebendo um valor inválido;
* ausência da estrutura obrigatória de `TEAM`.

---

# 📝 Exemplo completo

```text
STRATEGY defesaB {
    ROUND 8
    MAP Bind
    OBJECTIVE B

    TEAM DEFENSE {

        PLAYERS {
            PLAYER Nathan Killjoy
            PLAYER Joao Omen
        }

        ACTIONS {
            POSITION BSite
            USE Omen Smoke AT BSite
            WAIT 10
        }
    }
}
```

Esse exemplo representa uma estratégia defensiva no mapa Bind, com jogadores utilizando Killjoy e Omen, posicionamento no bombsite B, utilização de Smoke e espera de 10 segundos.

---

# 🎓 Contexto acadêmico

Projeto desenvolvido como atividade acadêmica relacionada ao estudo de:

* Linguagens Específicas de Domínio;
* Gramáticas;
* EBNF;
* Tokens;
* Análise léxica;
* Análise sintática;
* Árvores de análise;
* Análise semântica.

---

# 👥 Autores

**Nathan Maniçoba**,
**Eduardo Oliveira**

