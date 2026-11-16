<div align="center">
  <h2>🌳 Reencontra — Achados e Perdidos do Campus</h2>
</div>

<div align="center">
  <h3>Estruturas de Dados 2 — Árvores</h3>
</div>

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/eda2-2026/G07_Arvore_EDA2-2026.2?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/eda2-2026/G07_Arvore_EDA2-2026.2?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-Conclu%C3%ADdo-success?style=for-the-badge)
![Disciplina](https://img.shields.io/badge/DISCIPLINA-EDA2-4f46e5?style=for-the-badge)
![Dados](https://img.shields.io/badge/DADOS-Fict%C3%ADcios-0ea5e9?style=for-the-badge)

</div>

<div align="center">
  <h2>📑 Índice</h2>
</div>

- [🎯 Objetivos](#-objetivos)
- [📖 Sobre o projeto](#-sobre-o-projeto)
- [👩🏾‍💻 Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias](#️-tecnologias)
- [🤞 Como executar o projeto](#-como-executar-o-projeto)
- [⚙️ Configurações do projeto](#️-configurações-do-projeto)
- [🔐 Login demonstrativo](#-login-demonstrativo)
- [📊 Algoritmos](#-algoritmos)
- [🎥 Apresentação](#-apresentação)
- [👩‍💻 Contribuidores](#-contribuidores)
- [🧑‍💻 Estrutura do projeto](#-estrutura-do-projeto)
- [🧪 Testes](#-testes)

<div align="center">
  <h2>🎯 Objetivos</h2>
</div>

Demonstrar o uso prático de **árvores** na disciplina **Estruturas de Dados 2 (EDA2)** por meio de um balcão de achados e perdidos de campus.

- 🧠 **Objetivo acadêmico:** implementar e observar AVL, Trie e árvore n-ária.
- 🗂️ **Aplicação prática:** localizar objetos, consultar prazos e registrar devoluções.
- ⚙️ **Algoritmos:** rotações AVL, percurso em ordem, busca por intervalo e DFS.
- 📈 **Demonstração:** árvores visuais, altura, fatores de balanceamento e nós visitados.
- 🎓 **Simplicidade:** execução local sem instalação de pacotes ou banco de dados.


<div align="center">
  <h2>📖 Sobre o projeto</h2>
</div>

O **Reencontra** ajuda um balcão de achados e perdidos a organizar objetos encontrados no campus. A **Trie** pesquisa o início do nome, a **árvore n-ária** agrupa locais e a **AVL** mantém os prazos dos objetos guardados em ordem.

A base inicial tem **12.000 objetos fictícios — 1.000 em cada uma das 12 categorias — e 1.132 locais** em uma hierarquia de setores, prédios e salas. Nomes, descrições, situações e prazos simulam registros de um balcão de campus. Os dados são gerados localmente com semente fixa e prazos relativos à primeira execução.

O laboratório permite acompanhar inserções e remoções, observar o caminho de busca e comparar AVL, BST sem balanceamento e busca sequencial em até 5.000 elementos. O modo `--demo` mantém nove objetos pequenos para uma apresentação passo a passo.


<div align="center">
  <h2>👩🏾‍💻 Funcionalidades</h2>
</div>

- 🔎 Busca por prefixo, sem diferenciar acentos ou maiúsculas.
- 🌳 Filtro por local incluindo todos os seus descendentes.
- 🗂️ Filtro por categoria, hierarquia recolhível e paginação de 24 objetos.
- 📅 Consulta por limite de prazo, em ordem crescente de retirada.
- 📦 Cadastro e edição com validação de nome, descrição, local e prazo.
- ✅ Registro de devolução e exclusão com confirmação.
- 💾 Persistência local com gravação atômica do JSON.
- 📄 Exportação CSV dos resultados filtrados, com acentos e proteção contra fórmulas.
- 🎬 Modo de apresentação com dados temporários, sem alterar a base salva.
- 📊 Métricas da consulta e visualização do índice AVL real.
- 🔬 AVL aumentada com tamanho de subárvore, mediana, rank e seleção do k-ésimo menor.
- 🧪 Laboratório com snapshots, inserções, remoções e exemplos LL, RR, LR e RL.
- 🧭 Busca destacada, pré-ordem, em ordem, pós-ordem e percurso em largura com fila.
- 🔍 Zoom e profundidade ajustável no índice real, com tamanho das subárvores recolhidas.
- ⚖️ Comparação AVL × BST × sequencial com entradas aleatórias, ordenadas, inversas e quase ordenadas; tabelas, gráficos e contagem de visitas.
- ✨ Layout responsivo, mensagens de erro e estados vazios.


<div align="center">
  <h2>🛠️ Tecnologias</h2>
</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)
![unittest](https://img.shields.io/badge/Testes-unittest-508740?style=for-the-badge&logo=python&logoColor=white)

</div>

Servidor HTTP, persistência e testes usam somente a biblioteca padrão do Python. A interface usa módulos JavaScript nativos, sem build ou dependências externas.


<div align="center">
  <h2>🤞 Como executar o projeto</h2>
</div>

### 1. Pré-requisito

Instale **Python 3.10 ou superior**: https://www.python.org/downloads/. No Windows, habilite a opção de adicionar o Python ao PATH. Confira com `python --version`.

### 2. Executar com um comando

Na pasta que contém este README:

```sh
python iniciar.py
```

👉 Abra **http://localhost:8000**. Para encerrar, use `Ctrl + C`.

Não é necessário instalar pacotes. Em sistemas em que o executável se chama `python3`, substitua `python` por `python3`.

### Porta alternativa

```sh
python iniciar.py --port 8080
```

Nesse caso, abra `http://localhost:8080`.


<div align="center">
  <h2>⚙️ Configurações do projeto</h2>
</div>

| Item | Detalhe |
| --- | --- |
| Servidor | Python, endereço local `127.0.0.1`, porta padrão `8000` |
| Interface | HTML, CSS e JavaScript servidos pelo mesmo processo |
| Dados | `data/objetos.json`, criado automaticamente |
| Persistência | JSON substituído atomicamente a cada alteração |
| Índices | Construídos ao iniciar e atualizados incrementalmente após salvar alterações |
| Dependências | Nenhuma além do Python |

| Comando | O que faz |
| --- | --- |
| `python iniciar.py` | Inicia a aplicação completa |
| `python iniciar.py --port 8080` | Usa outra porta |
| `python iniciar.py --demo` | Inicia uma demonstração nova com dados temporários |
| `python iniciar.py --populate` | Completa mil objetos por categoria na base existente e inicia o servidor |
| `python -m unittest discover -s tests -v` | Executa os testes automatizados |

**Restaurar a demonstração:** encerre o servidor, remova apenas `data/objetos.json` e inicie novamente. Não execute duas instâncias usando o mesmo arquivo.

**Já usava a versão com poucos dados?** Execute `python iniciar.py --populate`. A complementação preserva os cadastros existentes, não duplica a base ao repetir o comando e não exige apagar o JSON. Em um clone novo, os 12.000 registros já são criados automaticamente com `python iniciar.py`.

<div align="center">
  <h2>📊 Algoritmos</h2>
</div>

| Estrutura / algoritmo | Uso | Complexidade |
| --- | --- | --- |
| AVL | Inserir/remover chaves `(prazo, id)` | O(log n) por operação isolada |
| Busca por intervalo + em ordem | Objetos guardados até uma data | O(log n + k) |
| Rotações LL, RR, LR e RL | Manter a AVL balanceada | O(1) por rotação |
| AVL com tamanho de subárvore | Rank, mediana inferior e k-ésimo menor | O(log n) |
| Trie + DFS | Buscar nomes por prefixo | O(p + s + k) |
| Árvore n-ária + DFS | Coletar descendentes de um local indexado | O(s), após indexação O(v) |
| Percursos DFS / BFS | Pré-ordem, em ordem, pós-ordem e largura | O(n) |
| BST sem balanceamento | Busca/inserção para comparação | O(n) no pior caso |
| Busca sequencial | Referência para comparação | O(n) no pior caso |
| Dicionário por ID | Acessar o registro encontrado | O(1) em média |

`n`: objetos indexados; `k`: resultados/referências; `p`: caracteres do prefixo; `s`: nós da subárvore percorrida; `v`: locais.

As estruturas são implementadas manualmente. Cadastrar, editar, devolver e excluir atualizam os índices diretamente, inclusive com remoções na AVL e poda na Trie. A persistência regrava o JSON inteiro; o custo total de uma alteração é **O(B + n + m + log n)**, sendo `B` o tamanho do arquivo e `m` o tamanho dos nomes envolvidos. A consulta de devolvidos/todos usa ordenação nativa, pois esses resultados não estão integralmente na AVL. As complexidades da tabela descrevem os algoritmos isolados; a requisição também aplica filtros, pagina os resultados e produz um snapshot limitado a até sete níveis.

Detalhes, métricas e limitações: [`docs/algoritmos.md`](docs/algoritmos.md).

<div align="center">
  <h2>🧑‍💻 Estrutura do projeto</h2>
</div>

```text
.
├── iniciar.py                # Comando único de execução
├── README.md
├── .gitignore
├── app/                      # Servidor, serviço, validação e persistência
│   └── structures/           # AVL, Trie e árvore de locais
├── web/                      # Interface e visualização das árvores
├── data/                     # Orientação e JSON gerado localmente
├── docs/                     # Algoritmos, roteiro e testes
└── tests/                    # Testes de estruturas, serviço e HTTP
```


<div align="center">
  <h2>🧪 Testes</h2>
</div>

```sh
python -m unittest discover -s tests -v
```

A suíte verifica rotações, remoções, balanceamento, consultas por intervalo, estatísticas de ordem, acentos, prefixos, hierarquia, paginação, população da base, validação, persistência, concorrência, benchmark e rotas HTTP. Um teste executa **2.500 operações aleatórias determinísticas** e verifica os invariantes da AVL após cada operação. Outros comparam rank/seleção com um conjunto ordenado e conferem todos os 12.000 registros por categoria.

Os testes usam arquivos temporários e não modificam a base da aplicação. Escopo completo: [`docs/testes.md`](docs/testes.md). Sugestão de demonstração: [`docs/roteiro.md`](docs/roteiro.md).

## 🎥 Apresentação

<div align="center">
  <a href="https://youtu.be/3Qh7XT6HRRE" target="_blank">
    <img src="https://img.shields.io/badge/YouTube-Apresenta%C3%A7%C3%A3o-red?style=for-the-badge&logo=youtube&logoColor=white" alt="Apresentação no YouTube">
  </a>
</div>



<div align="center">
  <h2>👩‍💻 Contribuidores</h2>
</div>

<div align="center">
  <table align="center">
    <tr>
      <td align="center">
        <a href="https://github.com/xGabrielCv">
          <img src="https://github.com/xGabrielCv.png" width="80"/><br/>
          <sub><b>Jésus Gabriel Carvalho Ventura</b></sub>
        </a><br/>
        <sub>jgabrielcv1903@gmail.com</sub>
      </td>
      <td align="center">
        <a href="https://github.com/ArturDCR">
          <img src="https://github.com/ArturDCR.png" width="80"/><br/>
          <sub><b>Artur de Camargos</b></sub>
        </a><br/>
        <sub>arturdecamargos@gmail.com</sub>
      </td>
    </tr>
  </table>
</div>

