# Validação do projeto

Execute, na raiz:

```sh
python -m unittest discover -s tests -v
```

Os testes usam diretórios temporários e um servidor HTTP em porta escolhida pelo sistema. Não alteram os dados pessoais da demonstração nem acessam serviços externos.

| Área | Verificação |
| --- | --- |
| AVL | Quatro rotações, duplicatas, remoções, altura, ordenação e chaves compostas |
| Propriedades | 2.500 operações determinísticas, comparadas com um conjunto, verificando invariantes após cada operação |
| Poda | Intervalo de seis valores em 1.000 chaves ordenadas visita menos de 30 nós |
| Trie | Prefixos, acentos, maiúsculas, nomes repetidos, remoção com poda e preservação de prefixos compartilhados |
| Locais | Subárvores, folhas, raiz e local inexistente |
| Serviço | Cadastro, edição, 72 combinações de filtros, devolução, exclusão e recarga do JSON |
| Índices incrementais | 150 alterações aleatórias comparadas com índices reconstruídos do arquivo |
| Concorrência | 24 cadastros com oito threads sem IDs repetidos |
| Persistência | Falha de gravação mantém memória e arquivo anterior; dados inválidos não são sobrescritos |
| HTTP | Recursos estáticos, CRUD, laboratório, JSON inválido, limites, parâmetros e bloqueio de caminhos externos |
| Laboratório | Snapshots independentes, ordenação, duplicatas e limites de entrada |
| CSV | Filtros, BOM UTF-8, acentos, aspas, quebras de linha e neutralização de fórmulas |

## Conferência manual da interface

- Buscar `gar` e `OCU`; testar um prefixo sem resultados.
- Selecionar um bloco e confirmar que seus descendentes participam do filtro.
- Limitar prazo e alternar Guardados, Devolvidos e Todos.
- Cadastrar, editar, devolver e excluir um objeto, conferindo confirmações e mensagens.
- Exportar uma busca por `gar` e conferir que o CSV contém somente as duas garrafas.
- Recarregar a página e reiniciar o processo para conferir a persistência.
- No laboratório, avançar e voltar nos quatro tipos de rotação.
- Reduzir a janela para 390 px e verificar a navegação e o formulário.
- Tentar um nome contendo marcação HTML e conferir que ele aparece como texto.

Testes aprovados cobrem os cenários descritos; não constituem garantia de ausência de defeitos em qualquer ambiente.
