# Detecção de Perfis Automatizados - Twibot20 :bird: :space_invader:
Este projeto foi realizado como projeto de conclusão do curso de Data Science da Digital House.
Com exceção da obtenção dos dados, todo o processo de manipulação e modelagem dos dados foi realizado por mim.

O projeto possui como objetivo a criação de um modelo de classificação capaz de identificar características que possam levar a identificação de um perfil automatizado (bot) na rede social Twitter.

## :book: Dados 

Os dados utilizados no projeto foram obtidos pela equipe do paper [TwiBot-20: A Comprehensive Twitter Bot Detection Benchmark](https://www.researchgate.net/publication/355785254_TwiBot-20_A_Comprehensive_Twitter_Bot_Detection_Benchmark). O paper foi elaborado com o objetivo de criar um dataset que seja representativo da realidade observada no twitter.

Após entrar em contato por email com um dos  autores do paper, explicar a idéia do projeto e que se tratava de um projeto com fins academicos os dados foram gentilmente cedidos.
Como os dados não estão disponíveis de forma pública na internet, este repositório contará apenas com uma amostra de 15 elementos do treino e do teste para ilustrar os processos desenvolvidos.

Os dados recebidos estavam em formato .json e já estavam divididos em treino e teste, e assim foi mantido para preservar comparações futuras.

### Documentação dos dados  :eyes: :clipboard:

|                  ID |                                           profile |                                             tweet |                                          neighbor |                              domain | label |
|--------------------:|--------------------------------------------------:|--------------------------------------------------:|--------------------------------------------------:|------------------------------------:|------:|
|            17461978 | {'id': '17461978 ', 'id_str': '17461978 ', 'na... | [RT @CarnivalCruise: 🎉 Are you ready to see wh... |                                              None | [Politics, Business, Entertainment] |     0 |
| 1297437077403885568 | {'id': '1297437077403885568 ', 'id_str': '1297... |                                              None | {'following': ['170861207', '23970102', '47293... |                          [Politics] |     1 |
|            17685258 | {'id': '17685258 ', 'id_str': '17685258 ', 'na... | [RT @realDonaldTrump: THANK YOU #RNC2020! http... | {'following': ['46464108', '21536398', '186434... |   [Politics, Entertainment, Sports] |     0 |

- 'ID': ID de identificação utilizado pelo twitter
- 'profile':  informações do perfil obtidas pela API do Twtiter
- 'tweet': Os últimso 200 tweets do usuário
- 'neighbor': 20 seguidores e seguidos aleatórios do usuário
- 'domain': Assunto discutido pelo usuário, podendo ser: politics, business, entertainment e sports
- 'label': target. '1'= bot | '0'= humano

A quantidade de bots e humanos nos dados estava um pouco desbalanceada, porém está é uma característica esperada da população no mundo real. Estando da seguinte forma:

![treino](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Detec%C3%A7%C3%A3o%20de%20Perfis%20Automatizados%20-%20Twibot20/images/bot-humano%20treino.jpg)
![teste](https://raw.githubusercontent.com/tnorio/Machine_Learning/main/Detec%C3%A7%C3%A3o%20de%20Perfis%20Automatizados%20-%20Twibot20/images/bot-humano%20teste.jpg)


## Manipulação dos dados  :pencil:
### 1. Desdobramento da coluna profile.
Dentre as diversas informaçoes [disponiveis](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user) na coluna profile
foram extraidas as seguintes informações:
- location (se tem ou não)
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

#### 1.1 Algumas dessas features foram utilizadas para a criação de novas:

- profile_m_age -> idade do perfil em meses, baseada no created_at 
- frequencia de tweets -> statuses_count / profile_m_age
- name_lenght -> quantidade de caracteres do do name
- screen_name_length -> quantidade de caracteres do screen_name
- description_length -> quantidade de caracteres do da descrição
- ff ratio -> friends_count /  followers_count. Razão entre as pessoas que você segue (friends) dividido pelas pessoas que seguem você (followers).
- followers_growth_rate -> followers_count / profile_m_age. Taxa de crescimento dos followers
- friends_growth_rate ->  friends_count / profile_m_age. Taxa de crescimento dos friends
- favourites_growth_rate -> favourites_count / profile_m_age. Taxa de crescimento dos favourites
- listed_growth_rate -> listed_count / profile_m_age. Taxa de crescimento do listed


### 2.Desdobramento da coluna tweet
Dentre os 200 tweets de cada observação foram extraidas:
- número de urls postados
- número de urls repetidas postadas
- número de # postadas
- número de # repetidas postadas
- número de @ mencionados
- número de @ repetidos mencionados

Estas informações foram extraidas com base na premisssa de que perfis automatizados são comumente utilizados para a propagação massiva (spam) de mensagens.

#### 2.1 TFIDF - NLP
Com o intuito de extrair informações que possam ser relevantes para a análise com base nos textos dos posts, foi realizado um processamento de linguagem natural (NLP) simples. Foi utilizado o TFIDF para extrair as palavras 200 mais relevantes entre todos os posts.

A idéia por trás do TFIDF é que se uma palavra aparece com frequencia em um documento, então ela deve ser importante e por isso deve receber um score alto. Mas se a palavra aparece em muitos outros documentos, provavelmente não é um identificador único ( pode ser um conectivo, preposição, etc.), então deve receber um valor baixo.

TFIDF é a junção de 2 transformações:
- TF -> Term Frquency ( frequência do termo)
TF(w) = (Nº de vezes que a palavra w aparece no documento) / (Nº total de termos no documento)

IDF -> Inverse Term Frequency ( Inverso da frequência do termo )
IDF(w) = log_e( Nº total de documentos) / (Nº dedocumentos que contemnham o termo w)

**TFIDF(w) = TF(w) * IDF(w)**

Para não adicionarmos mais 200 colunas aos nosso dados, uma para cada uma das palavras selecionadas, foram selecionadas apenas as colunas que possuiam a maior variância entre os scores. Pois uma coluna com baixa variância significa que os valores entre todas as observações não são muito diferentes, e por isso não proporcionariam informações relevantes ao modelo.

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
Boruta é um algorítmo bastante interessante, que checa a importancia de uma determianda coluna de acordo com sua performance contra uma versão com valores aleatorios da mesma (chamada de shadow feature), além de conceitos dad dsitribuição binomial para checar se uma feature realmente é importante ou não.

O resultado do modelo com o boruta aplicado, teve uma diferença bem pequena na casa de 0.00Algumacoisa nas métricas de avaliação. Porém, ao reduzir a quantidade de colunas necessárias para o modelo, reduziu a carga de processamento utilizada. Além de que essa alteração foi positiva em todas as métricas.

As colunas removidas pelo Boruta foram:

`['default_profile', 'use_background_img',
   'location', 'geo_enable', 'verified',
   'default_profile_image', 'covid19',
   'god', 'gt', 'music','season',
   'video', 'win','youtube']`

## O MODELO :milky_way:  :octocat:
