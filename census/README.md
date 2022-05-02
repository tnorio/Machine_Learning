# Classificação  Census 1994 
Projeto criado com o objetivo de exercer os conceitos de machine learning.
O problema consiste em um dataset do censo de 1994 dos Estados Unidos, disponibilizado no UCI Machine Learning Repository.

O objetivo é classificar se, dado as carácteristicas da pessoa, prever se ela conseguirá ganhar mais de $ 50.000,00 por ano.

Este é um problema de classificação e, como sabemos a saída esperada (> 50k/ano ou < 50k/ano), temos um problema de aprendizado supervisionado.

Para solucionar o problema foi realizado:
1. uma breve análise exploratória dos dados
2. feature engeneering
3. Resampling
4. GridsearchCV
5. árvore de decisão (DecisionTreeClassifier).

O Resultado foi um modelo de ML com um F-1 score de 82% e um AUC de 89%.
