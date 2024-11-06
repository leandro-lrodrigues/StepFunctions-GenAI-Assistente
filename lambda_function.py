import boto3
import json

# Função que processa as interações com o assistente virtual
def lambda_handler(event, context):
    # Obter o prompt enviado pelo usuário
    user_input = event.get('prompt', 'Olá, como posso ajudá-lo hoje?')

    # Armazenar o histórico da conversa
    conversation_history = event.get('conversation_history', [])
    
    # Adicionar o novo input do usuário ao histórico
    conversation_history.append(f"Usuário: {user_input}")

    # Lógica para determinar qual prompt será usado
    if len(conversation_history) == 1:  # Primeira interação
        prompt = "Olá, como posso ajudá-lo hoje?"
    elif len(conversation_history) == 2:  # Após a primeira resposta
        prompt = "Entendido. Por favor, me diga qual produto você está interessado?"
    elif len(conversation_history) == 3:  # Após a segunda resposta
        prompt = "Ótimo! O que exatamente você gostaria de saber sobre o produto X?"
    elif len(conversation_history) == 4:  # Após a terceira resposta
        prompt = "O produto X possui as seguintes características principais: [listar características]. Posso ajudá-lo com mais alguma informação?"
    elif len(conversation_history) == 5:  # Conclusão
        prompt = "Obrigado por entrar em contato! Se precisar de mais ajuda, estarei aqui."
    else:
        prompt = "Desculpe, não entendi. Pode reformular a pergunta?"

    # Cria o cliente Bedrock
    bedrock_client = boto3.client('bedrock', region_name='sa-east-1')  # Verifique a região correta

    try:
        # Chama o modelo Bedrock com o método correto `invoke_model`
        response = bedrock_client.invoke_model(
            modelId='your-bedrock-model-id',  # Substitua pelo seu modelo real
            body=json.dumps({"prompt": prompt}),
            contentType='application/json'
        )

        # Processa a resposta do modelo
        response_body = json.loads(response['body'].read())  # Lê a resposta
        model_response = response_body.get('generatedText', 'Nenhuma resposta gerada.')

        # Adiciona a resposta do modelo ao histórico da conversa
        conversation_history.append(f"Assistente: {model_response}")

        # Retorna a resposta gerada pelo modelo e o histórico de conversas
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': model_response,
                'conversation_history': conversation_history  # Retorna o histórico completo
            })
        }

    except Exception as e:
        # Captura qualquer erro
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
