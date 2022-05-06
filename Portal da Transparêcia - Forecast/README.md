# Gastos públicos de senadores brasileiros  :eyes:  

Projeto realizado com o intuito de análisar os gastos dos senadores no Brasil visando obter uma maior compreensão o comportamento das despesas do parlamentares. :credit_card:.

Durante o projeto foi necesssário realizar  a extração, limpeza, manipulação e visualização dos dados. No final do projeto é criado uma série temporal para tentar prever os gastos futuros dos senadores.

# Os dados :mag:
Na seção "Transparência" no site do [Senado Federal](https://www12.senado.leg.br/transparencia/dados-abertos-transparencia/dados-abertos-ceaps) , é possível localizar os dados da CEAPS (Cota para o Exercício da Atividade Parlamentar dos Senadores),
que é um valor disponibilizado pelo Governo para cada senador poder usufruir no exercício de sua função. O valor da cota depende da unidade da federação que o deputado representa, a diferença entre os valores de cada estado se baseia no custo da passagem de avião entre o estado de eleição do senador e Brasília.

Foram utilizados os dados disponiveis entre 2017 e 2022 (no momento da elaboração do projeto este só estava disponível até o mes 04).

## Limpeza e união dos dados
Ao baixar o arquivos encontramos o primeiro erro: O arquivo estava com erro de codificação não permitindo sua abertura. A forma mais fácil de abrir o documento manualmente, abrindo-o em um bloco de notas e para salva-lo corretamente na formatação utf-8.

Os dados estão no formato
```
ANO | MES | SENADOR | TIPO_DESPESA | CNPJ_CPF | FORNECEDOR | DOCUMENTO | DATA | DETALHAMENTO | VALOR_REEMBOLSADO | COD_DOCUMENTO
```

Rápidamente podemos observar que a coluna DATA se encontra com com erro de preenchimento, O valor do ano na coluna DATA não corresponde ao valor encontrado n coluna ANO. Como não há uma espécie de manual sobre a descrição dos dados disponibilizados, e não sei se é possivel o senador declarar um gasto com uma em para um ano diferente do ano corrente, não era possivel determinar qualo campo estaria correto. Por isso, para evitar uma análise inflacionada, optei por remover os valores onde essas duas informações divergiam em todos esses datasets.

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

EDA :bar_chart:
A realizar uma descrição rápida dos dados
```python
df[["VALOR_REEMBOLSADO"]].describe().T
```
Obtemos os seguitnes resultados

| count 	| mean 	| std 	| min 	| 25% 	| 50% 	| 75% 	| max 	| 120000.0 	|
|---:	|---:	|---:	|---:	|---:	|---:	|---:	|---:	|---:	|
| VALOR_REEMBOLSADO 	| 106248.0 	| 1180.784423 	| 2714.858603 	| -243.4 	| 137.61 	| 350.915 	| 1271.475 	| 120000.0 	|

Podemos observar que:
- A quantia reembolsada em média custa R$ 1.180,78
- O valor que divide a distribuição dos dados na metade, mediana, é de R$ 350,91
- Grande parte dos valores reembolsados está abaixo de R$1.271 reais
- O maior valor reembolsado foi de R$ 102.000,00, vamos ver quem gastou isso

O estudo revelou que média dos gastos anuais entre 2017 e 2021 foi de R$ 23.910.440,98. Se o gasto fosse dividido igualmente entre todos os 81 senadores teriamos uma valor médio de R$ 295.190 por senador por ano ou R$ 24.599 reais por senador por mes.

## Distribuição anual entre 2017 e 2021
![](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Portal%20da%20Transpar%C3%AAcia%20-%20Forecast/images/Gastos_anuais.png)
## Distribuição mensal entre 2017 e 2021
![](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Portal%20da%20Transpar%C3%AAcia%20-%20Forecast/images/gastos_mensais.png)

Pode-se constatar na distribuição mensal que no primeiro mês do ano não há grandes gastos,sendo o menor gasto mensal em Janeiro, possívelmente devido ao período de recesso. Porém há uma crescente dos valores logo após. Os maiores gastos se concentram no último trimestre do ano, especialmente no último trimestres

## Gastos por senador por ano

```python
plt.figure(figsize=(14,7))
graph = sns.lineplot(y = "VALOR_REEMBOLSADO", x="ANO", hue = "SENADOR", data = df, ci = None, marker = "o")
graph.get_legend().remove() # remover legenda;
```
ao plotarmos o gráfico dos gastos dos senadores por ano, podemos notar que:

INSERIR IMAGEM

- há uma ruptura de determinados valores em 2019, isso porque foi ano de eleição para o senado alguns não se reelegeram.
- alguns senadores gastam valores bem acima dos demais.
- outra coisa é que parece haver uma crescente nos gastos no ano antes da eleição (2018).

Para confirmar se realmente há um aumento nos gastos no ano eleitoral(2018), realizamos uma comparação entre os gastos de 2018 com os gastos de 2017, por senador.
```python
f, ax = plt.subplots(figsize=(20, 7))

#gastos 2018
sns.set_color_codes("muted")
sns.barplot(x="Senador", y="gasto 2018", data=df17_18,
            label="2018", color="b")

#gastos 2017
sns.set_color_codes("pastel")
sns.barplot(x="Senador", y="gasto 2017", data=df17_18,
            label="2017", color="b", alpha=0.85)

#legenda
ax.legend(ncol=2, loc="upper right", frameon=True)
ax.set_xticklabels(labels=df17_18.Senador,rotation=90)
sns.despine(left=True, bottom=True)
```

![](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Portal%20da%20Transpar%C3%AAcia%20-%20Forecast/images/compara%C3%A7%C3%A3o_17_18.png)

Percebemos que 34.93% dos sendores aumentaram os gastos se compararmos os gastos de 2017 e 2018, o ano eleitoral.

## Quais foram os maiores gastos ao longo do tempo?
### Maiores Gastos em uma única nota
```python
df[["VALOR_REEMBOLSADO","SENADOR","TIPO_DESPESA"]].sort_values(by=['VALOR_REEMBOLSADO'], ascending=False).head(10)
```
| VALOR_REEMBOLSADO 	| TIPO_DESPESA 	| DATA 	|  	|
|---:	|---:	|---:	|---	|
| 120000.0 	| WELLINGTON FAGUNDES 	| Contratação de consultorias, assessorias, pesq... 	| 2020-12-21 	|
| 102000.0 	| SÉRGIO PETECÃO 	| Contratação de consultorias, assessorias, pesq... 	| 2018-11-29 	|
| 102000.0 	| SÉRGIO PETECÃO 	| Contratação de consultorias, assessorias, pesq... 	| 2018-12-17 	|
| 100000.0 	| VANESSA GRAZZIOTIN 	| Contratação de consultorias, assessorias, pesq... 	| 2018-12-17 	|
| 96250.0 	| SÉRGIO PETECÃO 	| Contratação de consultorias, assessorias, pesq... 	| 2020-12-29 	|
| 96250.0 	| SÉRGIO PETECÃO 	| Contratação de consultorias, assessorias, pesq... 	| 2020-12-21 	|
| 79200.0 	| ROSE DE FREITAS 	| Contratação de consultorias, assessorias, pesq... 	| 2019-06-11 	|
| 77012.0 	| SÉRGIO PETECÃO 	| Contratação de consultorias, assessorias, pesq... 	| 2022-02-28 	|
| 76200.0 	| HÉLIO JOSÉ 	| Divulgação da atividade parlamentar 	| 2017-12-21 	|
| 74100.0 	| SÉRGIO PETECÃO 	| Divulgação da atividade parlamentar 	| 2017-06-12 	|

Ao buscar pelos 10 maiores valores reembolsados na série temporal análisada foi constatado que:
- O serviço de consultoria é o que incorre em maior valor gasto de maneira unitária. Entre os 10 maiores valores, o top 8 composto por consultoria
- O senador SÉRGIO PETECÃO ocupa 6 das 10 posições do ranking
- O senador SÉRGIO PETECÃO é responsável pelo 2º e 3º lugar, com 102 mil reais. E estes gastos ocorreram com menos de 1 mês de diferença.
- Há um salto de mais de 45 mil reais entre o maior e o 10º maior gasto.

### Senadores que mais gastaram ao longo do tempo
```python
top_gasto = df[["SENADOR","VALOR_REEMBOLSADO"]].groupby("SENADOR").sum().sort_values(by="VALOR_REEMBOLSADO", ascending = False)[:10]
top_gasto.T
```
| SENADOR 	| PAULO ROCHA 	| EDUARDO BRAGA 	| TELMÁRIO MOTA 	| SÉRGIO PETECÃO 	| OMAR AZIZ 	| ROBERTO ROCHA 	| HUMBERTO COSTA 	| CIRO NOGUEIRA 	| WELLINGTON FAGUNDES 	| ACIR GURGACZ 	|
|---:	|---:	|---:	|---:	|---:	|---:	|---:	|---:	|---:	|---:	|---:	|
| VALOR_REEMBOLSADO 	| 2374917.23 	| 2349034.91 	| 2238641.32 	| 2212796.14 	| 2182435.66 	| 2136729.82 	| 2014268.74 	| 1959964.06 	| 1958326.86 	| 1923811.91 	|

![](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Portal%20da%20Transpar%C3%AAcia%20-%20Forecast/images/gastos_senadores_unica_nota.png)

## Analisando o gasto pelos CNPJ declarados
### Top 10 empresas com mais notas recebidas.
```python
empresas_mais_notas = df[["CNPJ_CPF"]].value_counts()
empresas_mais_notas[:10]
```
| CNPJ_CPF 	| QUANTIDADE DE CONTRATOS 	|
|---:	|---:	|
| 16.978.175/0001-08 	| 7661 	|
| 33.937.681/0001-78 	| 2858 	|
| 02.558.157/0001-62 	| 2302 	|
| 07.575.651/0001-59 	| 2213 	|
| 26.480.780/0001-08 	| 1342 	|
| 00.031.708/0001-00 	| 1183 	|
| 33.469.172/0022-92 	| 1146 	|
| 02.575.829/0001-48 	| 1021 	|
| 00.821.459/0001-56 	| 862 	|
| 09.296.295/0001-60 	| 800 	|

Podemos observar que algumas empresas respondem por um considerado numero de notas emitidas
O  1º CNPJ com mais notas emitidas é da empresa ADRIA VIAGENS E TURISMO LTDA.
Apontada como fornecedora dos mais diversos tipos de serviço, entre eles:
- Passagens aéreas, aquáticas e terrestres nacionais
- Locomoção, hospedagem, alimentação, combustíveis e lubrificantes
- Aquisição de material de consumo para uso no escritório político, inclusive aquisição ou locação de software, despesas postais, aquisição de publicações, locação de móveis e de equipamentos.

O  2º CNPJ com mais notas emitidas é da empresa LATAM. Que forneceu somente o serviço de passagens aéreas.
E o 3º CNPJ com mais notas emitidas é da empresa VIVO. Que forneceu somente o serviço de uso no escritório.
 
## E Qual empresa recebeu mais valores no acumulado do período?
```python
empresas_maiores_valores = df[["CNPJ_CPF","VALOR_REEMBOLSADO"]].groupby("CNPJ_CPF").sum().sort_values(by="VALOR_REEMBOLSADO", ascending=False)
```
![](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Portal%20da%20Transpar%C3%AAcia%20-%20Forecast/images/empresas_mais_valores.png)

De longe a empresa que mais recebeu valores dos senadores foi a empresa ADRIA VIAGENS E TURISMO LTDA, que também foi a mesma que teve o maior volume de notas.

Das 10 empresas com mais notas emitidas, 5 estão entre as top 10 empresas com maiores valores recebidos no período.

## Forecast

O ideia deste projeto foi obtida durante o evento 7daysofcode da alura.
O objetivo do evento era que durante 7 dias seriam enviados por email ideias de desafios para serem realizados por conta própria.
