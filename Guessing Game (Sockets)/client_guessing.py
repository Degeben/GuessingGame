import socket

def main():
    client()

def client():
    # Create a TCP stream socket local to this computer using port 7777
    ip_address = '127.0.0.1'
    port = 7777
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender:
        sender.connect((ip_address, port))
        # The server must initially send the client a 'hello' message upon connection
        buffer = sender.recv(1024)
        text_received = buffer.decode('ascii')
        # If the server does not respond with the 'hello' message, terminate the program
        if text_received != 'hello\r\n':
            print('Server is not ready yet')
            return
        # Loop forever to receive user input
        while True:
            # Allow the user to guess a number, or an empty string to quit
            input_string = input('Enter your guess (leave empty to disconnect): ')
            if not input_string:
                # If the user's input was empty, our message to the server will be a 'quit' message
                message = 'quit\r\n'
            elif input_string.isdigit():
                # If the user entered a valid integer, our message will be a 'guess' message
                message = f'guess\t{input_string}\r\n'
            else:
                # If the user entered anything else, make them to try again
                print('Invalid input')
                continue
            # Send the ASCII encoded message to the server
            sender.sendall(message.encode('ascii'))
            # If the user didn't enter anything, the client can safely disconnect and end the program
            if not input_string:
                break
            # Receive a response from the server and decode it using ASCII encoding
            buffer = sender.recv(1024)
            text_received = buffer.decode('ascii')
            # If the server responded with a 'correct' message, tell the user they won and stop the loop
            if text_received == 'correct\r\n':
                print('Congratulations! You won!')
                break
            # The server should have responded with either a 'too-high' or 'too-low' message as a hint
            else:
                print(f"Incorrect guess. Here's a hint: {text_received.strip()}")

if __name__ == '__main__':
    main()
