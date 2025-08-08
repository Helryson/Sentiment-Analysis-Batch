CONTEUDO_INPUT = """
Esta é uma conversa entre vários participantes. Foque nas mensagens do usuário.
Identifique o sentimento geral das falas do usuário ao longo da conversa, levando em conta o contexto em que a conversa se encontra. Classifique como Positivo, Negativo ou Neutro, e dê uma breve explicação do motivo da classificação dada.

Conversa:
{linha_conversa}

Retorne a classificação geral da conversa, ou seja, qual foi o sentimento dominante nas mensagens do usuário, no modelo json com a seguinte estrutura:"Sentimento": "(Negativo, Positivo ou Neutro)"
"Explicação": "explicação do motivo da classificação com um trecho que demonstre isso".
"""