# Previsão de variação do Nível do Mar - Regressão Linear
Nossos dados contém o valor médio da variação do nivel do mar ```CSIRO Adjusted Sea Level ``` (Y)  e o ano da medição ``` Year``` (X) 1880 até 2013.

Vamos utilizar os dados para:
1. Ajustar um modelo de regressão linear
2. Análisar como o modelo ficou
3. Com base no modelo, prever a qual será a variação do nivel do mar até 2050.

Nosso modelo de regressão linear irá tentar prever a alteração do nível do mar $y$ de acordo com a alteração do ano.

Vamos começar plotando a distribuição dos nossos dados

IMAGEM

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
Para criar este modelo vamos usar a biblioteca
