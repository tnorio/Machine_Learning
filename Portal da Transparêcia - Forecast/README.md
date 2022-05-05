Projeto realizado com o intuito de análisar os gastos dos senadores no Brasil visando obter uma maior compreensão o comportamento das despesas do parlamentares.
Durante o projeto foi necesssário realizar  a extração, limpeza, manipulação e visualização dos dados. No final do projeto é criado uma série temporal para tentar prever os gastos futuros dos senadores.
O dataset foi obtido pela lei da transparencia no site SITE.

Os dados
Na seção "Transparência" no site do Senado Federal, é possível localizar os dados da CEAPS (Cota para o Exercício da Atividade Parlamentar dos Senadores),
que é um valor disponibilizado pelo Governo para cada senador poder usufruir no exercício de sua função. O valor da cota depende da unidade da federação que o deputado representa e a diferença entre os valores de cada estado se baseia no custo da passagem de avião entre o estado de eleição do senador e Brasília.

Neste projeto optamos por utilizar os dados disponiveis entre 2017 e 2022.

Limpeza e união dos dados
Ao baixar o arquivos encontramos o primeiro erro: O arquivo estava com erro de codificação não permitindo sua abertura. A forma mais fácil de abrir o documento manualmente, abrindo-o em um bloco de notas e para salva-lo corretamente na formatação utf-8.

Os dados estão no formato
```
ANO | MES | SENADOR | TIPO_DESPESA | CNPJ_CPF | FORNECEDOR | DOCUMENTO | DATA | DETALHAMENTO | VALOR_REEMBOLSADO | COD_DOCUMENTO
```

Rápidamente podemos observar que a coluna DATA se encontra com com erro de preenchimento, O valor do ano na coluna DATA não corresponde ao valor encontrado n coluna ANO. Como não há uma espécie de manual sobre a descrição dos arquivos disponibilizados, não sabia em qual valor confiar. Por isso optei por remover os valores onde essas duas informações divergiam em todos esses datasets.

```python
def drop_linhas_ano_errado(df,ano_certo):
  count=0
  for i,row in enumerate(df['DATA']):
    split_row = str(row).split("/")
    if split_row[2] != str(ano_certo):
      #print(i, " = ", split_row)
      df.drop(index=i, axis ="rows", inplace= True)
      count += 1
  return(f"Foram deletadas {count} linhas ")
```
Foram deletadas 86 linhas  em 2022(até o mês 04)
Foram deletadas 247 linhas em 2021
Foram deletadas 293 linhas em 2020
Foram deletadas 196 linhas em 2019
Foram deletadas 312 linhas em 2018
Foram deletadas 246 linhas em 2017

Após isso todos os dados foram salvos em um único dataframe, que foi utilizado durante os próximas etapas do projeto

EDA

O objetivo deste projeto foi realizado durante o  evento 7daysofcode da alura.
O objetivo do evento era que durante 7 dias seriam enviados por email ideias de desafios para serem realizados por conta própria.
