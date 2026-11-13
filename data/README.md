# Dados locais

O servidor cria `objetos.json` automaticamente na primeira execução, com nove objetos fictícios e prazos relativos à data de inicialização. As alterações persistem nesse arquivo. Para restaurar a demonstração, encerre o servidor e remova somente `data/objetos.json`; a próxima execução recria a base.

Não execute duas instâncias sobre o mesmo arquivo. A gravação usa substituição atômica e o serviço serializa as operações em memória. O JSON é a fonte dos dados; os índices são construídos ao iniciar e atualizados incrementalmente após salvar as alterações.

Para apresentar com nove objetos novos sem modificar sua base, execute `python iniciar.py --demo`. Esse modo mantém o JSON em uma pasta temporária, descartada ao encerrar normalmente. Reiniciar o modo demonstrativo começa novamente com os nove exemplos.
