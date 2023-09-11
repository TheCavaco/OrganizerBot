# Como correr

## Setup

1. É importante criar um python virtual environment e instalar a discord package:
```shell
pip install discord
```

2. O ficheiro ```keys.txt``` contêm o invite link para dar setup em novos servidores. Copiar o link para o browser e autorizar o uso do bot.

3. No discord, ativar o developer mode (Settings->Advanced)

4. Copiar o channel ID do canal de texto para usar como check-in.


## Correr o bot

### Apagando mensagens antigas
No modo default, o bot apaga as mensagens que já processou.

```shell
python3 main.py <channel_id> <filename>
```

```<channel_id>``` - Id do canal obtido no passo 4.

```<filename>``` - Nome do ficheiro único para a cadeira/servidor (O bot mantém um estado de que alunos já estão inscritos e em que grupos)


### Mantendo as mensagens
Para manter as mensagens enviadas pelos alunos no canal de check-in basta:
```shell
python3 main.py <channel_id> <filename> nod
```

***É IMPORTANTE NÃO CORRER O BOT COM DIFERENTES FILENAMES PARA A MESMA CADEIRA***


## Adicionalmente
O bot, se deixado a correr, vai automaticamente analisar todas as novas mensagens que forem enviadas para o canal de texto pretendido.
