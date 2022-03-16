import ast,socket
chat_list = []

def handle_client(client_socket):
    """
    Handle a client connection.
    """
    # Receive the message
    request = client_socket.recv(1024)
    print(request)
    request = ast.literal_eval(request.decode())
    if request[0] == 'send':
        chat_list.append(request[1])
    if request[0] == 'get_chats':
        chat_log = 'Chat:'
        for item in chat_list:
            chat_log = chat_log + '\n' + item
        client_socket.send(chat_log.encode())
    print(request)
    # Send the message back

    # Close the connection
    client_socket.close()