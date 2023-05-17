import socket
import random

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 7777))
server_socket.listen()

print('Server listening on port 7777...')

# Game loop
while True:
    # Accept incoming connection and create client socket
    client_socket, client_address = server_socket.accept()
    print(f'Client {client_address} connected.')

    # Generate random number from 1 to 99 (inclusive)
    answer = random.randint(1, 99)
    print(f'Answer is {answer}.')

    # Send hello message to client
    client_socket.sendall(b'hello\r\n')

    # Game loop for individual client
    while True:
        # Receive incoming message from client
        message = client_socket.recv(1024).decode('ascii').strip()

        if not message:
            # Client disconnected
            print(f'Client {client_address} disconnected.')
            break

        if message == 'quit':
            # Client wants to quit
            print(f'Client {client_address} quit.')
            break

        if message.startswith('guess\t'):
            # Client made a guess
            guess = int(message[6:])
            if guess == answer:
                # Client guessed correctly
                client_socket.sendall(b'correct\r\n')
                print(f'Client {client_address} guessed correctly!')
                break
            elif guess > answer:
                # Client guessed too high
                client_socket.sendall(b'too-high\r\n')
                print(f'Client {client_address} guessed too high.')
            else:
                # Client guessed too low
                client_socket.sendall(b'too-low\r\n')
                print(f'Client {client_address} guessed too low.')
        else:
            # Client sent an invalid message
            client_socket.sendall(b'invalid\r\n')
            print(f'Client {client_address} sent an invalid message.')
    
    # Close client socket
    client_socket.close()
