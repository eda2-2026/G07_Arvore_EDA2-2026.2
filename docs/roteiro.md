# Roteiro de apresentação

1. **Problema (30 s):** objetos se acumulam no campus; o balcão precisa localizar itens e priorizar os prazos mais próximos.
2. **Executar (30 s):** na raiz, rode `python iniciar.py` e abra `http://localhost:8000`. A primeira execução cria nove registros fictícios.
3. **Trie (1 min):** digite `gar`; aparecem duas garrafas. Busque `OCU` para demonstrar a normalização de acentos. Limpe os filtros.
4. **Árvore n-ária (1 min):** selecione Bloco A e mostre que Sala A101 e Laboratório são incluídos. Volte para Campus.
5. **AVL aplicada (1 min):** limite o prazo pelo calendário. Abra o índice AVL e explique a chave composta `(prazo, id)`, a altura e o BF.
6. **Cadastro e devolução (1 min):** registre um objeto; confirme a devolução e mude a situação para Devolvidos. Reinicie o servidor para verificar a persistência.
7. **Laboratório (2 min):** use os quatro exemplos de rotação; avance uma inserção de cada vez. Compare com a sequência ordenada e explique por que a altura não vira uma cadeia.
8. **Código e testes (1 min):** mostre `app/structures/avl.py` e rode `python -m unittest discover -s tests -v`. Explique que há operações aleatórias comparadas com um conjunto de referência.

Os dados são fictícios. Antes de repetir a demonstração, encerre o servidor e remova apenas `data/objetos.json` para recriar os exemplos. O vídeo pode ser adicionado ao badge de apresentação do README posteriormente.
