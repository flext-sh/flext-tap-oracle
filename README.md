# FLEXT Tap Oracle

Singer Tap para extracao de dados de bancos Oracle para pipelines ELT.

Descricao oficial atual: "FLEXT Tap Oracle - Modern Singer Tap for Oracle Database".

## O que este projeto entrega

- Extrai dados tabulares Oracle para formato Singer.
- Padroniza captura para carga incremental/recorrente.
- Alimenta targets e transformacoes dbt com dados de origem.

## Contexto operacional

- Entrada: conexao Oracle e catalogo de extracao.
- Saida: stream Singer de dados Oracle.
- Dependencias: flext-db-oracle e orquestracao Singer/Meltano.

## Estado atual e risco de adocao

- Qualidade: **Alpha**
- Uso recomendado: **Nao produtivo**
- Nivel de estabilidade: em maturacao funcional e tecnica, sujeito a mudancas de contrato sem garantia de retrocompatibilidade.

## Diretriz para uso nesta fase

Aplicar este projeto somente em desenvolvimento, prova de conceito e homologacao controlada, com expectativa de ajustes frequentes ate maturidade de release.
