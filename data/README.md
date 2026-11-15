# Dados locais

O servidor cria `objetos.json` automaticamente na primeira execução, com **12.000 objetos fictícios, 1.000 por categoria**. A semente aleatória é fixa; os prazos são relativos à data de inicialização. A árvore contém 1.132 locais. A base nova tem 9.000 guardados e 3.000 devolvidos. As alterações persistem nesse arquivo.

Se já existe uma base antiga, rode `python iniciar.py --populate`: o comando completa as quantidades por categoria, preservando todos os registros e IDs existentes. Repetir o comando não adiciona registros quando as metas já foram atingidas. Novos IDs começam acima do maior existente. A complementação pode ter uma distribuição de situações diferente da base nova, conforme os registros preservados.

Para recriar a base do zero, encerre o servidor, faça uma cópia de segurança do JSON se necessário e remova somente `data/objetos.json`; a próxima execução recria a base. O arquivo gerado não é versionado: qualquer clone consegue reproduzir os dados a partir do código de geração.

Não execute duas instâncias sobre o mesmo arquivo. A gravação usa substituição atômica e o serviço serializa as operações em memória. O JSON é a fonte dos dados; os índices são construídos ao iniciar e atualizados incrementalmente após salvar as alterações.

Para apresentar com nove objetos novos sem modificar sua base, execute `python iniciar.py --demo`. Esse modo mantém o JSON em uma pasta temporária, descartada ao encerrar normalmente. Reiniciar o modo demonstrativo começa novamente com os nove exemplos.
