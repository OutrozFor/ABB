SGBD com Árvore Binária de Busca (ABB)

Este projeto é um SGBD simples escrito em Python, que armazena registros de pessoas (CPF, nome e data de nascimento) em uma estrutura linear e utiliza uma Árvore Binária de Busca (ABB) para indexação, busca e remoção eficiente pelo CPF.

Funcionalidades:

- Inserção de registros: Adiciona novos registros e os indexa pelo CPF.
- Remoção lógica: Marca registros como deletados e remove o índice correspondente na ABB.
- Busca por CPF: Permite localizar rapidamente um registro usando o CPF como chave.
- Listagem ordenada: Gera uma lista dos registros válidos em ordem crescente de CPF.
- Percursos na ABB: Suporta percursos em ordem, pré-ordem, pós-ordem e em largura.
- Persistência em arquivo: Salva e carrega os dados dos registros em arquivo usando pickle.

Estruturas principais
Registro: Representa cada pessoa armazenada (CPF, nome, data de nascimento, flag de deletado).
ABB e NoABB: Implementam a árvore binária de busca para indexação dos registros pelo CPF.
SGBD: Gerencia a estrutura de dados linear (EDL), a árvore de índice e as operações de inserir, remover, buscar, listar e persistir registros.
