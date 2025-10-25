import pickle
import socket
import sys

def main():
    # check for correct number of cl arguments
    if len(sys.argv) != 3:
        print("Usage: python post_server.py <ip> <port>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2]) # set port to input
    messages = []

    # set up socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind((ip, port))
    
    # listen for incoming connections
    # allowing unlimited connection
    server_socket.listen()
    print(f"Listening on {ip}:{port}")

    while True:
        # returns new connection socket for communication and client's address
        connection, address = server_socket.accept()
        print(f"Connected with {address}")

        try:
            # receive client data with buffer bytes
            data = connection.recv(1024)
            if not data:
                continue # skip if no data was received
            
            message_tuple = pickle.loads(data)
            messages.append(message_tuple)

            username, timestamp, message = message_tuple
            print(f"[{timestamp}] {username}: {message}")

            # Acknowledge to client
            ack = f"Message from {username} received at {timestamp}"
            connection.sendall(pickle.dumps(ack))
            
        except pickle.PickleError as pe:
            # invalid pickle
            print(f"Error unpickling data: {pe}")
        except Exception as e:
            # general error
            print(f"Error occurred: {e}")
        
        if message_tuple[2].upper() == "EXIT":
            print(f"{username} disconnected")
            connection.close()
            continue


if __name__ == "__main__":
    main()  
