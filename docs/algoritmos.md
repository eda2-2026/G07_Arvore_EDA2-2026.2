# Árvores e decisões de implementação

## AVL: prazos de retirada

A chave é a tupla `(prazo ISO, id)`: dois objetos podem ter o mesmo prazo sem colidir. O índice contém somente objetos guardados. A altura de uma árvore vazia é zero; a de uma folha é um. O fator de balanceamento é `altura(esquerda) - altura(direita)` e deve permanecer em −1, 0 ou 1.

As inserções e remoções atualizam alturas e aplicam rotações LL, RR, LR e RL. Remover um nó com dois filhos usa o sucessor em ordem. Inserção, remoção e busca pontual custam O(log n); uma consulta de intervalo custa O(log n + k), com k resultados. O percurso em ordem produz prazos crescentes sem ordenar o resultado com um algoritmo externo.

O método `range` contabiliza nós efetivamente examinados e evita visitar ramos fora do intervalo. A interface mostra a árvore completa de objetos guardados, mesmo quando os demais filtros reduzem a lista. A altura e as rotações referem-se ao índice completo. Rotações contam rotações simples; uma rotação dupla soma duas.

## Trie: nomes de objetos

Os nomes são normalizados com `casefold` e decomposição Unicode, removendo acentos somente no índice. Cada nó tem filhos por caractere e um conjunto de IDs terminais. A pesquisa percorre o prefixo e faz DFS iterativo nos descendentes, reunindo IDs. Assim, `ócu` e `OCU` encontram o mesmo objeto. Nomes repetidos preservam todos os objetos.

A busca é por início do nome completo, não por palavras no meio da descrição. Para prefixo de tamanho p, subárvore com s nós e k referências terminais, o custo é O(p + s + k). Prefixo vazio percorre toda a Trie. Os nós visitados incluem os passos do prefixo e os nós da subárvore; não representam comparações equivalentes às da AVL. Inserir um nome com m caracteres custa O(m), em média para os dicionários de filhos.

## Árvore n-ária: mapa do campus

A hierarquia tem 1.132 locais: os 12 originais e 20 setores com cinco prédios e dez salas por prédio. Os nomes são únicos. Um índice por nome é construído em O(v) ao carregar o módulo; localizar a raiz da subárvore custa O(1) em média e coletar seus s descendentes por DFS custa O(s). Selecionar Bloco A continua incluindo o próprio bloco, Sala A101 e Laboratório. Os novos setores ficam recolhidos na interface.

## Integração e limitações

Um dicionário por ID conecta os resultados dos índices aos registros. Filtros por local e prefixo são interseções sobre os candidatos. A consulta padrão usa a AVL para obter os objetos guardados em ordem de prazo. Consultas por devolvidos ou todos usam ordenação nativa O(n log n), pois os devolvidos não pertencem à AVL.

Os índices são construídos ao iniciar. Durante o uso, cadastrar insere na Trie e na AVL; editar remove as chaves antigas e insere as novas; devolver remove da AVL; excluir remove de ambas. A remoção da Trie preserva prefixos compartilhados e poda apenas ramos vazios. As rotações da AVL acumulam desde o início do processo e podem ocorrer também nas remoções.

Cada alteração grava o JSON inteiro antes de atualizar os índices. Se a gravação falhar, os índices e os registros anteriores são preservados. A operação isolada da AVL é O(log n), mas a alteração completa custa O(B + n + m + log n), em que B é o tamanho do JSON gravado e m o tamanho dos nomes envolvidos. Ao iniciar, construir os índices custa O(n log n + L), sendo L a soma dos caracteres dos nomes.

O retorno da API inclui um snapshot da AVL limitado à profundidade solicitada (3 a 7 níveis na interface; padrão 5). Os nós da fronteira indicam o tamanho total da subárvore e se há descendentes recolhidos. A árvore de verdade não é truncada. A geração da imagem custa O(min(n, 2^d)), com d níveis. A consulta continua aplicando os filtros sobre os candidatos antes da paginação; a requisição completa não deve ser descrita como O(log n). Consultas por devolvidos/todos registram zero nós visitados na AVL, pois usam ordenação alternativa.

A exportação CSV reaplica os filtros do balcão, preserva acentos com UTF-8 e BOM, usa ponto e vírgula e escapa aspas/quebras de linha. Campos que poderiam ser interpretados como fórmulas por planilhas recebem um apóstrofo inicial.

O servidor atende somente em `127.0.0.1`, sem login ou dependências externas. A base padrão possui 12.000 objetos (1.000 por categoria), inicialmente 9.000 guardados e 3.000 devolvidos; o modo `--demo` usa nove. A paginação limita o retorno de objetos, mas a persistência ainda regrava o arquivo todo. Não há controle de acesso, múltiplos processos, recuperação automática de JSON corrompido ou promessa de durabilidade contra queda de energia. A gravação atômica evita arquivos parcialmente substituídos, e um bloqueio serializa consultas e alterações no processo.

## Estatísticas de ordem na AVL

Cada nó mantém `size = 1 + tamanho(esquerda) + tamanho(direita)`, atualizado junto com a altura após inserções, remoções e rotações. `select(k)` encontra a chave da posição k (base zero), descartando subárvores conforme seu tamanho. `rank(chave)` conta as chaves estritamente menores. Ambas custam O(log n) na AVL. A mediana mostrada é a inferior: para quantidade par, escolhemos a primeira das duas posições centrais. Prazos iguais continuam desempatados por ID.

## Laboratório e caminhos

Até 31 inserções e 31 remoções podem ser executadas por experimento. Remoções ocorrem após as inserções e usam a implementação real da AVL. Snapshots independentes preservam a árvore em cada passo; duplicatas e remoções ausentes aparecem como operações sem alteração. A busca calcula o caminho em cada snapshot: dourado indica valores examinados e verde indica o alvo encontrado. Os percursos apresentados são do resultado final; BFS utiliza uma fila `deque`.

## Comparação reproduzível

O benchmark recebe 100, 1.000 ou 5.000 inteiros distintos e um dos quatro cenários: aleatório, ordenado, inverso ou quase ordenado (1% de pares trocados). A semente é 42. AVL e BST recebem a mesma sequência; a busca sequencial usa uma cópia dela. Todas executam os mesmos 100 alvos presentes mais dois ausentes. As respostas são comparadas com uma referência antes do resultado ser exibido.

Uma comparação de construção corresponde a um nó não vazio examinado para inserir uma chave. Na busca, uma visita corresponde a um nó ou valor examinado; não contamos cada operador Python isoladamente. A BST é iterativa para suportar entradas que a transformem em uma cadeia sem exceder a recursão. A busca sequencial não tem altura ou rotações. Seu tempo de construção mede a cópia da lista. Tempos de relógio são observações de uma execução local, variam entre máquinas e não substituem os contadores nem uma análise assintótica.

## Experimentos sugeridos

1. Insira `30,20,10`: LL; raiz final 20.
2. Insira `10,20,30`: RR; raiz final 20.
3. Insira `30,10,20`: LR; duas rotações simples.
4. Insira `10,30,20`: RL; duas rotações simples.
5. Insira `1,2,3,4,5,6,7,8,9,10`: compare a AVL com a cadeia que uma BST sem balanceamento formaria.
6. No balcão, busque `gar`, selecione Bloco A e limite o prazo. Observe quais índices participam do filtro.
