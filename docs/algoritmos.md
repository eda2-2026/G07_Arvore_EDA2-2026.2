# Árvores e decisões de implementação

## AVL: prazos de retirada

A chave é a tupla `(prazo ISO, id)`: dois objetos podem ter o mesmo prazo sem colidir. O índice contém somente objetos guardados. A altura de uma árvore vazia é zero; a de uma folha é um. O fator de balanceamento é `altura(esquerda) - altura(direita)` e deve permanecer em −1, 0 ou 1.

As inserções e remoções atualizam alturas e aplicam rotações LL, RR, LR e RL. Remover um nó com dois filhos usa o sucessor em ordem. Inserção, remoção e busca pontual custam O(log n); uma consulta de intervalo custa O(log n + k), com k resultados. O percurso em ordem produz prazos crescentes sem ordenar o resultado com um algoritmo externo.

O método `range` contabiliza nós efetivamente examinados e evita visitar ramos fora do intervalo. A interface mostra a árvore completa de objetos guardados, mesmo quando os demais filtros reduzem a lista. A altura e as rotações referem-se ao índice completo. Rotações contam rotações simples; uma rotação dupla soma duas.

## Trie: nomes de objetos

Os nomes são normalizados com `casefold` e decomposição Unicode, removendo acentos somente no índice. Cada nó tem filhos por caractere e um conjunto de IDs terminais. A pesquisa percorre o prefixo e faz DFS iterativo nos descendentes, reunindo IDs. Assim, `ócu` e `OCU` encontram o mesmo objeto. Nomes repetidos preservam todos os objetos.

A busca é por início do nome completo, não por palavras no meio da descrição. Para prefixo de tamanho p, subárvore com s nós e k referências terminais, o custo é O(p + s + k). Prefixo vazio percorre toda a Trie. Os nós visitados incluem os passos do prefixo e os nós da subárvore; não representam comparações equivalentes às da AVL. Inserir um nome com m caracteres custa O(m), em média para os dicionários de filhos.

## Árvore n-ária: mapa do campus

A hierarquia tem 12 locais, contando a raiz Campus. Cada local pode ter vários filhos. DFS encontra o local e reúne os descendentes. Selecionar Bloco A inclui registros no próprio bloco, na Sala A101 e no Laboratório. Custo O(v), sendo v o número de locais; memória auxiliar O(v) no pior caso.

## Integração e limitações

Um dicionário por ID conecta os resultados dos índices aos registros. Filtros por local e prefixo são interseções sobre os candidatos. A consulta padrão usa a AVL para obter os objetos guardados em ordem de prazo. Consultas por devolvidos ou todos usam ordenação nativa O(n log n), pois os devolvidos não pertencem à AVL.

Os índices são construídos ao iniciar. Durante o uso, cadastrar insere na Trie e na AVL; editar remove as chaves antigas e insere as novas; devolver remove da AVL; excluir remove de ambas. A remoção da Trie preserva prefixos compartilhados e poda apenas ramos vazios. As rotações da AVL acumulam desde o início do processo e podem ocorrer também nas remoções.

Cada alteração grava o JSON inteiro antes de atualizar os índices. Se a gravação falhar, os índices e os registros anteriores são preservados. A operação isolada da AVL é O(log n), mas a alteração completa custa O(B + n + m + log n), em que B é o tamanho do JSON gravado e m o tamanho dos nomes envolvidos. Ao iniciar, construir os índices custa O(n log n + L), sendo L a soma dos caracteres dos nomes.

O retorno da API inclui um snapshot da AVL completa, com custo O(n), para a visualização didática. Portanto, a requisição HTTP completa não tem custo O(log n + k), mesmo quando a busca isolada por intervalo tem essa complexidade. Consultas por devolvidos/todos registram zero nós visitados na AVL, pois usam a ordenação alternativa.

A exportação CSV reaplica os filtros do balcão, preserva acentos com UTF-8 e BOM, usa ponto e vírgula e escapa aspas/quebras de linha. Campos que poderiam ser interpretados como fórmulas por planilhas recebem um apóstrofo inicial.

O servidor atende somente em `127.0.0.1`, sem login ou dependências externas. É uma demonstração local para pequenos conjuntos de dados. Não há controle de acesso, múltiplos processos, recuperação automática de JSON corrompido ou promessa de durabilidade contra queda de energia. A gravação atômica evita arquivos parcialmente substituídos, e um bloqueio serializa consultas e alterações no processo.

## Experimentos sugeridos

1. Insira `30,20,10`: LL; raiz final 20.
2. Insira `10,20,30`: RR; raiz final 20.
3. Insira `30,10,20`: LR; duas rotações simples.
4. Insira `10,30,20`: RL; duas rotações simples.
5. Insira `1,2,3,4,5,6,7,8,9,10`: compare a AVL com a cadeia que uma BST sem balanceamento formaria.
6. No balcão, busque `gar`, selecione Bloco A e limite o prazo. Observe quais índices participam do filtro.
