# Detecção de Perfis Automatizados - Twibot20 :bird: :space_invader:
Este projeto foi realizado como projeto de conclusão do curso de Data Science da Digital House.

## Objetivos :pushpin: :grey_exclamation:
O projeto possui como objetivo a criação de um modelo de classificação capaz de identificar características que possam levar a identificação de um perfil automatizado (bot) na rede social Twitter. O modelo deve ser capaz de identificar o maior número de bots possiveis ao mesmo tempo que evita a ocorrência de falso positivo,a identificação de usuários reais como bots.

Não é difícil encontrar artigos científicos que proponham a criação de modelos com esse objetivo, porém muitos deles não utilizam dados realmente representativos do mundo real, devido a complexidade de identificar se um perfil realmente é um bot ou não, ou não performam bem em um teste verdadeiro. De qualquer maneira, alguns artigos foram consultados com o intuito de obter uma maior compreensão sobre o problema e identificar possíveis features e modelos relevantes para o problema.

## :book: Dados 

Os dados utilizados no projeto foram obtidos pela equipe do paper [TwiBot-20: A Comprehensive Twitter Bot Detection Benchmark](https://www.researchgate.net/publication/355785254_TwiBot-20_A_Comprehensive_Twitter_Bot_Detection_Benchmark). O paper foi elaborado com o objetivo de criar um dataset que seja representativo da realidade observada no twitter.

Após entrar em contato por email com um dos  autores do paper, explicar a idéia do projeto e que se tratava de um projeto com fins acadêmicos,  os dados foram gentilmente compartilhados.
Como os dados não estão disponíveis de forma pública na internet, este repositório contará apenas com uma amostra de 15 elementos do treino e do teste para ilustrar os processos desenvolvidos.

Os dados recebidos estavam em formato .json e já estavam divididos em treino e teste, e assim foi mantido para preservar comparações futuras.

### Documentação dos dados  :eyes: :clipboard:

|                  ID |                                           profile |                                             tweet |                                          neighbor |                              domain | label |
|--------------------:|--------------------------------------------------:|--------------------------------------------------:|--------------------------------------------------:|------------------------------------:|------:|
|            17461978 | {'id': '17461978 ', 'id_str': '17461978 ', 'na... | [RT @CarnivalCruise: 🎉 Are you ready to see wh... |                                              None | [Politics, Business, Entertainment] |     0 |
| 1297437077403885568 | {'id': '1297437077403885568 ', 'id_str': '1297... |                                              None | {'following': ['170861207', '23970102', '47293... |                          [Politics] |     1 |
|            17685258 | {'id': '17685258 ', 'id_str': '17685258 ', 'na... | [RT @realDonaldTrump: THANK YOU #RNC2020! http... | {'following': ['46464108', '21536398', '186434... |   [Politics, Entertainment, Sports] |     0 |

- 'ID': ID de identificação utilizado pelo twitter
- 'profile':  Dicionário com informações do perfil obtidas pela API do Twtiter
- 'tweet': Os últimso 200 tweets do usuário
- 'neighbor': 20 seguidores e seguidos aleatórios do usuário
- 'domain': Assunto discutido pelo usuário, podendo ser: politics, business, entertainment e sports
- 'label': target. '1'= bot | '0'= humano

A quantidade de bots e humanos nos dados estava um pouco desbalanceada, porém está é uma característica esperada da população no mundo real. Estando da seguinte forma:

![treino](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Detec%C3%A7%C3%A3o%20de%20Perfis%20Automatizados%20-%20Twibot20/images/bot-humano%20treino.jpg)
![teste](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Detec%C3%A7%C3%A3o%20de%20Perfis%20Automatizados%20-%20Twibot20/images/bot-humano%20teste.jpg)


# Manipulação dos dados  :pencil:
## 1. Desdobramento da coluna profile.
Dentre as diversas informaçoes [disponiveis](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user) na coluna profile
foram extraidas as seguintes informações:
- location -> se possui uma localização descrita no perfil.
- followers_count -> Número de seguidores
- friends_count -> Número de perfis seguidos pelo usuário  (AKA  “followings”)
- geo_enabled -> se o perfil já ativou o GPS em alguma postagem
- verified -> Se o perfil é verificado
- statuses_counts -> número de posts
- default_profile -> Se o ousuário já alterou o tema ou o plano de fundo do perfil
- default_profile_image -> Se o usuário já alterou a  foto padrão inicial
- created_at -> a idade do perfil
- name -> nome do perfil
- screen_name -> nome / pseudonimo do prefil (pode ser alterado)
- description -> descrição do perfil
- statuses_count -> quantidade de posts realizados
- listed_count -> quantidade de listas públicas que o usuário é membro
- favourites_count -> quantidade de likes que o usuário já deu em posts 

### 1.1 Algumas dessas features foram utilizadas para a criação de novas:

- profile_m_age -> idade do perfil em meses, baseada no created_at. Usada para Criação de features nas etapas seguintes.
- frequencia de tweets -> statuses_count / profile_m_age
- name_lenght -> quantidade de caracteres do do name
- screen_name_length -> quantidade de caracteres do screen_name
- description_length -> quantidade de caracteres do da descrição
- ff ratio -> friends_count /  followers_count. Razão entre as pessoas que você segue (friends) dividido pelas pessoas que seguem você (followers).
- followers_growth_rate -> followers_count / profile_m_age. Taxa de crescimento dos followers
- friends_growth_rate ->  friends_count / profile_m_age. Taxa de crescimento dos friends
- favourites_growth_rate -> favourites_count / profile_m_age. Taxa de crescimento dos favourites
- listed_growth_rate -> listed_count / profile_m_age. Taxa de crescimento do listed


## 2.Desdobramento da coluna tweet
Dentre os 200 tweets de cada observação foram extraidas:
- número de urls postados
- número de urls repetidas postadas
- número de # postadas
- número de # repetidas postadas
- número de @ mencionados
- número de @ repetidos mencionados

Estas informações foram extraidas com base na premisssa de que perfis automatizados são comumente utilizados para a propagação massiva (spam) de mensagens.

### 2.1 TFIDF - NLP
Com o intuito de extrair informações que possam ser relevantes para a análise com base nos textos dos posts, foi realizado um processamento de linguagem natural (NLP) simples. Foi utilizado o TFIDF para extrair as palavras 200 mais relevantes entre todos os posts.

A idéia por trás do TFIDF é que se uma palavra aparece com frequência em um documento, então ela deve ser importante e por isso deve receber um score alto. Mas se a palavra aparece em muitos outros documentos, provavelmente não é um identificador sobre o tema do documento ( pode ser um conectivo, preposição, etc.), então deve receber um valor baixo.

TFIDF é a junção de 2 transformações:
**TF** -> Term Frquency ( frequência do termo)
**TF(w)** = (Nº de vezes que a palavra w aparece no documento) / (Nº total de termos no documento)

**IDF** -> Inverse Term Frequency ( Inverso da frequência do termo )
**IDF(w)** = log_e( Nº total de documentos) / (Nº dedocumentos que contemnham o termo w)

**TFIDF(w) = TF(w) * IDF(w)**

Para não adicionarmos mais 200 colunas aos nosso dados, uma para cada uma das palavras selecionadas, foram selecionadas apenas as colunas que possuiam a maior variância entre os scores. Pois uma coluna com baixa variância significa que os valores entre todas as observações não são muito diferentes, e por isso, no geral, não proporcionariam informações relevantes, para distinção dos usuários, ao modelo.

Assim somente as palavras que possuiam uma variância maior que o 3º quartil, o top 25%, foram mantidas.
Ainda assim algumas palavras sem sentido, passaram pelos filtros. Como emojis (amp) e conectivos em espanhol (en, la, los....) que foram removidas.
As seguintes palavras foram aplicadas ao modelos, com seus respectivos TFIDF score.

` ['biden', 'covid19', 'day', 'del', 'don', 'dont', 'follow', 'game',
'god', 'good', 'great', 'gt', 'happy', 'im', 'just', 'know', 'like',
'lol', 'love', 'music', 'new', 'news', 'people', 'president',
'realdonaldtrump', 'rt', 'season', 'team', 'thank', 'thanks', 'think',
'time', 'today', 'tonight', 'trump', 'video', 'win', 'youtube'] `
 
## Boruta_py - Feature Selection :mag:

Antes de aplicar o modelo nos dados, foi realizado uma seleção de features utilizando a biblioteca [Boruta](https://github.com/scikit-learn-contrib/boruta_py).
Boruta é um algorítmo bastante interessante, que checa a importância de uma determianda feature de acordo com sua performance contra uma versão com valores aleatorios da mesma (chamada de shadow feature), além de utilziar conceitos da distribuição binomial para checar se uma feature realmente é importante ou não. Entre outras coisas, vale dar uma olhada na documentação para saber mais.

O resultado do modelo com o Boruta aplicado, teve uma diferença bem pequena na casa de 0.00Algumacoisa nas métricas de avaliação. Porém, ao reduzir a quantidade de colunas necessárias para o modelo, removendo 14 colunas, reduziu a carga de processamento utilizada. Além de que essa alteração foi positiva em todas as métricas.

As colunas removidas pelo Boruta foram:

`['default_profile', 'use_background_img',
   'location', 'geo_enable', 'verified',
   'profile_image', 'covid19',
   'god', 'gt', 'music','season',
   'video', 'win','youtube']`

# O MODELO :milky_way:  :octocat:

Diversos modelos e combinações entre modelos/features/transformações foram testados na busca pelo modelo que obtivesse a maior performance possível.
Dentre os artigos científicos pesquisados, muitos se utilizavam ou ao menos mencionavam o Random Forest como o modelo que melhor se ajusta-se ao problema em questão.
Antes e durante o processo de transformação dos dados, alguns outros modelos foram capazes de performar melhor que o Random Forest. Como o SVM e até mesmo a regressão logística. Porém, ainda com uma performance bem a baixo do esperado. 

Antes de abordar o modelo, vamos falar sobreas métricas de avaliação que foram utilizadas para selecionar o modelo com maior performance.

## Métricas de Avaliação :chart_with_upwards_trend:

O objetivo do projeto é criar um modelo que maximize a identificação de perfis automatizados, e, ao mesmo tempo, minimize a ocorrência de falsos positivos. Pois a identificação errada de um usuário verdadeiro pode causar sérios problemas, tanto para o usuário quanto para a empresa. Para isso foram priorizadas as seguintes métricas:

- **Recall**: Porcentagem de observações corretamente identificada como 1(bot), dentre todas as observações 1(bot). Penaliza Falso Negativo.
- **Precision**: Porcentagem de observações corretamente identificada como 1(bot), dentre todas as classificadas como 1(bots). Penaliza falso Positivo
- **F1**:Representa média entre Precision e Recall, dando um peso igual às duas métricas.

Normalmente ocorre um trade-off entre Precision e Recall, para aumentar uma devemos reduzir outra, por isso também foi utilizado o F1-score, sendo a métrica de maior relevância para a avaliação de performance do modelo.

![precision e recall](https://upload.wikimedia.org/wikipedia/commons/2/26/Precisionrecall.svg)

Agora que já entendemos as métricas,vamos para o modelo

## Random Forest :deciduous_tree:

Após todas as transformações realizadas, constatou-se que realmente os modelos baseados em arvore (como o XGBoost, ADA e Random Forest) foram os que mais performaram. Após a otimização dos hiper-parâmetros dos modelos mencionados, o Random Forest foi modelo que melhor se ajustou ao problema e obteve as melhores métricas.

Random Forest é um modelo de Ensamble do tipo Baggin (Bootstrap Aggregating). Ensambles do tipo Baggin realizam diversos modelos em paralelo e combinam seus resultados para uma previsão final. O Random Forest, além de criar várias arvores em paralelo para estimar o resultado final, ainda utiliza subgrupos aleatórios das features em cada árvore para criar uma floresta não correlacionada de arvores de decisão.

As métricas obtidas com nosso modelo foram

|    Modelo |           | RF_HPgrid1000_boruta |
|----------:|-----------|---------------------:|
| --------- | --------- | -------------------- |
|           | Treino    | Teste                |
| Accurácia | 0.865     | 0.806                |
| Precision | 0.87      |                0.811 |
|    Recall | 0.856     |                0.799 |
|        F1 | 0.885     |                0.831 |


### Avaliação do modelo

#### Matriz de Confusão
O modelo construído obteve a seguinte matriz de confusão para o teste, considerando um treshhold padrão de 0.5

![ConfusionMatrixDisplay](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Detec%C3%A7%C3%A3o%20de%20Perfis%20Automatizados%20-%20Twibot20/images/Matriz%20%20de%20confus%C3%A3o%20teste.jpg)

Através da matriz de confusão conseguimos observar a quantidade de:
- Falsos Postivos -> humanos identificados como bot de forma errada
- Verdadeiros Positivos -> bots corretamente identificados como bots
- Falsos Negativos -> bots que não foram identificados como bots
- Verdadiero Negativo -> humanos corretamente identificados como humanos

A Matriz de confusão nos mostra a quantidade de observações corretamente identificadas na diagonal esquerda (\) e as observações identificadas de maneira errada na diagonal direita (/). E é apartir dela que são computadas as métricas de avaliação mencionadas anteriormente.

#### Curva ROC

Podemos alterar o comportamento da Matriz de confusão de de acordo com o treshold escolhido para rotulação das observações. Em outras palavras, ao rodar o modelo para *N* observações ele retorna a probabilidade de que determinada observação seja um bot, e de acordo com o limiar de classificação escolhido para rotular determinada observação como bot a matriz de confusão é alterada, e por consequencia os resultados das métricas de avaliação.

Assim se quisermos ser mais conservadores, rotulando como bot somente as observações com alta probabilidade, devemos AUMENTAR o limiar de classificação (treshold). Ao fazer isso por consequência, deixaremos de identificar alguns bots porém reduziremos a quantidade de usuários verdadeiros identificados como bot. Em outras palavras, assim  diminuimos os Verdadeiros Positivos e também diminuimos os Falso Positivos.

Se diminuirmos nosso limiar de classificação, o oposto irá ocorrer.

E através da Curva ROC, conseguimos plotar esse trade-off entre Verdadeiro positivo e Falso negativos de acordo com a variação do limiar escolhido (treshold)

![ROC](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Detec%C3%A7%C3%A3o%20de%20Perfis%20Automatizados%20-%20Twibot20/images/ROC.jpg)

AUC se refere a Area Under de Curve, ou área abaixo da curva, evai de 0 até 1. Quanto maior seu valor, melhor o modelo será capaz de identificar os Verdadeiros Positivos sem ocorrer em Falsos Positivos.

### Feature Importance -SHAP

Para analisármos quais foram as features mais importantes para a avaliação proposta pelo do modelo e como a variação de seus valores impacta no resultado final, foi utilizado o [SHAP](https://shap.readthedocs.io/en/latest/index.html) (SHapley Additive exPlanations). O SHAP utiliza conceitos da teoria dos jogos e é capaz de demonstrar o quanto a alteração de uma variável é capaz de influenciar o resultado do modelo, nos ajudando a compreeender o funcionamento do modelo.

Ele ordena as features de acordo com o chamado Shapley Values, que, basicamente, mede o impacto de cada feature no modelo.

No gráfico abaixo, as features estão rankeadas, do maior para o menor, de acordo com o Shapley value geral de cada feature. Valores em vermelho, são mais importante em avaliar se um perfil é um bot ou não.

![SHAP](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Detec%C3%A7%C3%A3o%20de%20Perfis%20Automatizados%20-%20Twibot20/images/SHAP.jpg)

Podemos observar que erificou-se que as 5 features mais significativas para o modelo foram:
- friends_followers_ratio
- Listed_count
- Followers_count
- Listed_growth_rate
- followers_growth_rate

Isso nos mostra que a quantidade de conexões, sejam seguidos ou seguidores, que um perfil possui e a taxa decrescimento que essas conexões são realizadas são fatores preponderantes para determinar se determinar se um perfil será um bot ou um humano. Oque confirma um conhecimento heurístico das redes sociais, humanos querem se conectar com outros humanos, não querendo se associar com perfis falsos/bots.

## Conclusão  :confetti_ball:

Caso você tenha dado uma olhada no artigo científico utilizado como fonte de dados do modelo, pode observar que a proposta do artigo, como falado anteriormente, é a de criação de um dataset que seja representativo do mundo real. E não a criação de um modelo de machine learning capaz de identificar bots e humanos.

No final do artigo os autores testam alguns modelos propostos por outros artigos científicos utilizando o dataset gerado, e apresentam os resultados de cada modelo. Vale ressaltar que os modelos testados foram propostos por artigos recentes, o mais antigo é de 2011 sendo qua agrande maioria se concentra entre os anos de 2018 e 2020. 

Se compararmos nosso modelo com os modelos testados, nosso modelo ocupa a 2ª colocação no ranking! Estando apenas cerca de 2% abaixo do modelo que melhor performou, observando o F1 score. É oque podemos observar na reprodução da tabela observada no artigo, com o resultado do nosso modelo.

![Comparação de resultados](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Detec%C3%A7%C3%A3o%20de%20Perfis%20Automatizados%20-%20Twibot20/images/resultados.jpg)

Ao análisar o artigo do melhor modelo avaliado, pude perceber que uma das features mais importantes em seu modelo, foi uma métrica de comparação do nome e da descrição de cada perfil. Que só foi capaz de ser criada após a extração de dados de centenas de milhares de usuários. Claramente este tipo de feature não seria possível ser craido por este projeto, visto que demandaria um esforço computacional/técnico que não esteve disponível na elaboração deste projeto.

De qualquer forma estou muito satisfeito com o resultado, apenas 2% de diferença no F1 score sem a necessidade de minearar dados de centenas de milhares de usuários na plataforma.

### Considerações finais

A complexidade e das redes sociais e comportamento humano, torna este um problema altamente dinâmico. Praticamente todos os dias novas formas de enganar as medidas de prevenção a perfis automatizados são criadas e adotadas pelos bots das redes sociais. E ao mesmo tempo novas formas de evitar o surgimento e propagação de perfis fake são implementadas pelas plataformas. Oque torna a busca por uma solução um trabalho constante.

As features dos  utilizadas no modelo, com excessão das features baseadas em texto, pois os assuntos nas redes são altamente dinâmicos e variam de acordo com a região / acontecimentos mais recentes, foram features que podem continuar a ser aplicadas em modelos futuros e que não possuem vieses preconceituosos contra determinados grupos de usuários.  Sendo assim, este modelo se torna mais um passo na constante busca por um ambiente de interações sociais livre de manipulações de fake news / spams.

## Bibliografia :book:

- [TwiBot-20: A Comprehensive Twitter Bot Detection Benchmark](https://www.researchgate.net/publication/355785254_TwiBot-20_A_Comprehensive_Twitter_Bot_Detection_Benchmark)
- [A one-class classification approach for bot detection on Twitter](https://www.sciencedirect.com/science/article/pii/S0167404820300031)
- [Online Human-Bot Interactions: Detection, Estimation, and Characterization](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3324593)
- [Detecting Twitter Fake Accounts using Machine Learning and Data Reduction Techniques](https://www.semanticscholar.org/paper/Detecting-Twitter-Fake-Accounts-using-Machine-and-Homsi-Nemri/a745f5458c992b83a0fb8da3fe1b0a240d155d60)
- [Fake Account Detection in Twitter Based on Minimum Weighted Feature](https://www.researchgate.net/publication/304569053_Fake_Account_Detection_in_Twitter_Based_on_Minimum_Weighted_Feature_set)
