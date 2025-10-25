import pickle
import socket
import sys
import threading
import zmq

def post_connection(connection, pub_socket):
    # handle one client connection
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                continue

            message_tuple = pickle.loads(data)
            username, timestamp, message = message_tuple
            print(f"[{timestamp}] {username}: {message}")

            # acknowledge to post client
            ack = f"Message from {username} received at {timestamp}"
            connection.sendall(pickle.dumps(ack))

            # pub message to zmq subs
            pub_socket.send_string(f"{username}: {message} ({timestamp})")

            if message.upper() == "EXIT":
                print(f"{username} disconnected")
                sys.exit(0)
                break

        except Exception as e:
            print(f"Error: {e}")
            break
    connection.close()


def main():
    if len(sys.argv) != 4:
        print("Usage: python pub_server.py <ip> <post_port> <pub_port>")
        sys.exit(1)

    ip = sys.argv[1]
    post_port = int(sys.argv[2])
    pub_port = int(sys.argv[3])

    # zmq context, pub socket
    context = zmq.Context()
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind(f"tcp://{ip}:{pub_port}")

    # TCP post socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, post_port))
    server_socket.listen()
    print(f"Listening on {ip}:{post_port}")

    # keeps server running forever so it can accept incoming connections
    while True:
        connection, addr = server_socket.accept()
        print(f"Connected with {addr}")
        threading.Thread(target=post_connection, args=(connection, pub_socket), daemon=True).start()


if __name__ == "__main__":
    main()

