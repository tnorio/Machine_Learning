# Detecção de Perfis Automatizados - Twibot20
Este projeto foi realizado como projeto de conclusão do curso de Data Science da Digital House.
Com exceção da obtenção dos dados, todo o processo de manipulação e modelagem dos dados foi realizado por mim.

O projeto possui como objetivo a criação de um modelo de classificação capaz de identificar características que possam levar a identificação de um perfil automatizado (bot) na rede social Twitter.

## Dados

Os dados utilizados no projeto foram obtidos pela equipe do paper [TwiBot-20: A Comprehensive Twitter Bot Detection Benchmark](https://www.researchgate.net/publication/355785254_TwiBot-20_A_Comprehensive_Twitter_Bot_Detection_Benchmark). O paper foi elaborado com o objetivo de criar um dataset que seja representativo da realidade observada no twitter.

Após entrar em contato por email com um dos  autores do paper, explicar a idéia do projeto e que se tratava de um projeto com fins academicos os dados foram gentilmente cedidos.
Como os dados não estão disponíveis de forma pública na internet, este repositório contará apenas com uma amostra de 15 elementos do treino e do teste para ilustrar os processos desenvolvidos.

Os dados recebidos estavam em formato .json e já estavam divididos em treino e teste, e assim foi mantido para preservar comparações futuras.

### Documentação dos dados

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
![treino]
![teste]


## Manipulação dos dados
1. Desdobramento da coluna profile.
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

2.Desdobramento da coluna tweet
Dentre os tweets das observações foram extraidas:
- número de urls postados
- número de urls repetidas postadas
- número de # postadas
- número de # repetidas postadas
- número de @ mencionados
- número de @ repetidos mencionados

