from flask import Flask, request, jsonify
import datetime


from threading import Lock

from langchain.memory import ConversationBufferMemory
from src import agent

app = Flask(__name__)

# Store conversations in memory
conversations = {}
conversations_lock = Lock()


@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the chatbot API!'


@app.route('/showConversations', methods=['GET'])
def showConversations():
    for k, v in conversations.items():
        print(k)
        print(v.buffer)
        print('\n')
    return str(conversations)


@app.route('/chat', methods=['POST'])
def chat():
    # Get the JSON payload from the request
    json_data = request.get_json()

    if not json_data:
        return jsonify({'error': 'Invalid JSON payload'})

    # Extract the user ID and query from the JSON payload
    user_id = json_data.get('id')
    user_query = json_data.get('query')

    with conversations_lock:
        if user_id in conversations:
            memory = conversations[user_id]
        else:
            memory = ConversationBufferMemory(
                memory_key="memory", return_messages=True)
            conversations[user_id] = memory

        # Make the API call to generate a response
        bot_response = agent.get_response(user_query, memory)

        # conversation.append({
        #     'user_query': user_query,
        #     'bot_response': bot_response,
        #     'timestamp': str(datetime.datetime.now())
        # })

    # Return the response as JSON
    return jsonify({
        'id': user_id,
        'response': bot_response,
        'timestamp': str(datetime.datetime.now())
    })


if __name__ == '__main__':

    app.run()
