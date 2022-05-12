# Previsão de variação do Nível do Mar - Regressão Linear
Nossos dados contém o valor médio da variação do nivel do mar ```CSIRO Adjusted Sea Level ``` (Y)  e o ano da medição ``` Year``` (X) 1880 até 2013.

Vamos utilizar os dados para:
1. Ajustar um modelo de regressão linear
2. Análisar como o modelo ficou
3. Com base no modelo, prever a qual será a variação do nivel do mar até 2050.

Nosso modelo de regressão linear irá tentar prever a alteração do nível do mar $y$ de acordo com a alteração do ano.

Vamos começar plotando a distribuição dos nossos dados

![scatter data]("https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Previsao%20Nivel%20do%20Mar%20-%20Reg.%20Linear/img/scatter_data.png")

Podemos observar que a alteração do nível do mar vem ocorrendo de forma quase linear. Por isso vamos utilizar um modelo linear para tentar prever alterações futuras.

## Regressão Linear
A regressão linear é um modelo relativamente simples, oque pode ser ruim por não conseguir uma boa performance em problemas mais complexos, por outro lado sua vantagem é ser de fácil explicação.

Com um modelo de regressão linear é um metodo estatístico usado para prever a relação entre duas variáveis. Queremos prever o quanto de alteração da variável dependente ou preditora ```X``` influencia no valor da variável independente ou de resposta```Y```

###Equação
Um modelo de regressão linear é composto pela seguinte equação:

<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;\bg_white&space;\hat{y}_i=\beta_0+\beta_1*x_i" width="150"/>

* <img src="https://latex.codecogs.com/png.image?\dpi{110}&space;\bg_white&space;\hat{y}_i" width="25"/>: Valor que vamos prever. A variável dependente
*<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;\bg_white&space;x_i" width="25"/>: váriavel de entrada / independente
* <img src="https://latex.codecogs.com/png.image?\dpi{110}&space;\bg_white&space;\beta_0" width="25"/>: *intercept*, é ponto que corta o eixo y quando x=0.
* <img src="https://latex.codecogs.com/png.image?\dpi{110}&space;\bg_white&space;\beta_1" width="25"/>: coeficiente angular, define a angulação da reta. Quanto mais inclinada maior a influencia que a alteração de $x_i$  provoca em <img src="https://latex.codecogs.com/png.image?\dpi{110}&space;\bg_white&space;\hat{y}_i" width="25"/>:

Usando a regressão linear nos buscamos encontrar a linha que melhor se "ajusta" aos nossos dados. Essa linha é conhecida como regressão dos minimos quadrados, pois ela se propõe a reduzir ao máximo o quadrado dos erros, que são a diferença entre o valor predito e o valor real.

A linha é calculada com o objetivo de reduzir ao máximo o quadrado dos erros.

## Criando o modelo
Vamos usar a biblioteca [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) do Scikitlearn realiza os passos descritos anteriormente para chegar aos valores do coeficiente angular e do intercept que minimizam os erros.
Sabendo que:
- Com o metodo `coef_ `a biblioteca nos retornar o coeficiente angular.
- Com o metodo `intercept` a biblioteca nos retornar o intercept.

Podemos definir uma função que calcule a reta:
`python
#criando uma funcao para calcular a reta
def Regression(intercept,slope,X):
  """
  Retorna a reta de uma regressão linear de acordo com os valores da função
  """

  return intercept + ( slope * X ).values

`

Lembrando a equação da reta:
<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;\bg_white&space;\hat{y}_i = \beta_0 + \beta_1*x_i" width="25"/>:

Que no nosso problema se traduz em
Variação prevista do nível do Mar = intercept+ (slope* Ano)

Com isso podemos plotar nosso gráfico.

**imagem ate3**

## Métricas de acertividade do modelo
Para saber o quão bom o nosso modelo foi ajustado existem algumas métricas que nos permitem uma maior precisão para avaliação do desempenho do modelo e comparação com outros modelos. Vamos utilizar para avaliar nosso modelo o R² e do *MSE*

### R-squared (R²) / Coeficiente de Determinação

É uma métrica de correlação que tem duas vantagens: é fácil de calcular e fácil de interpretar. 

Demonstra proporcionalmente o quanto da variação na variável resposta $y$ pode ser explicada pelas  variações das variáveis de entrada $x$ no modelo. Sempre será um valor entre 0 e 1, quanto mais próximo de 1 melhor. E pode ser interpretado como uma porcentagem.

É definido com a equação:

$R^2 = \frac{var(média) - var(modelo)}{var(média)} = 1 - \frac{var(modelo)}{var(média)}$

* var = Variância

No Scikitlearn podemos obter o valor do R² utilizando a classe ![r2_score]("https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html")
`python
from sklearn.metrics import r2_score
r2_score(y_true=df["CSIRO Adjusted Sea Level"],y_pred=Regression(linr.intercept_,linr.coef_,df[["Year"]]))`
`0.9697466074149554`

O modelo foi capaz de explicar 96% da variância em torno da  alteração do nível do mar.

### Erro Médio Quadrático / mean Squared Error (*MSE*)
As medidas de erro são usadas para fins comparativos com outros modelos e para ter uma ideia de o quão aceitável está a saída do nosso modelo.

O *MSE* nos diz média do quadrado da diferença entre os valores preditos pela reta e o valor real. bQuanto MENOR o valor da métrica de erro, melhor ajustado está o nosso modelo.

Equação
<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;\bg_white&space;MSE = \frac{1}{n} \sum(y - \hat{y})^2" width="25"/>:
 Nosso modelo obteve 0.18% no valor do MSE.
 
 ## Vamos esticar essa série até 2050
 
 No gráfico acima percebe-se que ocorre um crescimento mais acentuado dos valores por volta do ano 2000.
 
 Vamos criar um novo modelo somente com os dados de 200 até 2013 para podermos observar melhor o impacto que esta alteração pode causar até 2050.
 
 `python
 #dataset e modelo
df2k = df[df["Year"]>=2000]

linr2k = LinearRegression()
linr2k.fit(X=df2k[["Year"]],y=df2k[["CSIRO Adjusted Sea Level"]])

#extend ano
X_extendido2k = np.arange(df2k.Year.min(), 2051 )
`
Podemos observar que o valor encontrado no nosso modelo de 2000 até 2013 possui um valor para o coeficiente angular ```coef_``` de ```0.16```, bem maior que o valor do modelo anterior de ```0.6```.
Oque já era esperado, pois foi observado um aumento da inclinação dos pontos observados. Uma menor variação no eixo X Ano, causou uma maior variação no eixo Y Variação do nível do mar.



É o gráfico comparativo dos dois modelos ficou


**PLOT FINAL**

#Conclusão
Levando em consideração as previsões finais do modelo. O primeiro modelo, que levou em o comportamento de toda a série temporal, de 1880 até 2013, previu uma variação máxima no nível do mar em 2050 de VALOR.
E o seungo modelo, que levou em considerção somente os dados de 2000 até 2013,  previu uma variação máxima no nível do mar em 2050 de VALOR.
Uma diferença de 

 
