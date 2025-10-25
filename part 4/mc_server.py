import socket
import pickle
import sys
import threading
import zmq


def handle_client(conn, pub_socket):
    # handle one client connection
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                continue

            channel, username, timestamp, message = pickle.loads(data)

            print(f"[{channel}] [{timestamp}] {username}: {message}")

            # acknowledge messages
            ack = f"[{channel}] Message from {username} received at {timestamp}"
            conn.sendall(pickle.dumps(ack))

            # publish message with channel prefix
            pub_socket.send_string(f"{channel} {username}: {message} ({timestamp})")

            if message.upper() == "EXIT":
                pub_socket.send_string(f"{channel} {username} has left the chat.")
                break

        except Exception as e:
            print(f"Error handling client: {e}")
            break
    conn.close()


def main():
    if len(sys.argv) != 4:
        print("Usage: python mc_server.py <ip> <post_port> <pub_port>")
        sys.exit(1)

    ip = sys.argv[1]
    post_port = int(sys.argv[2])
    pub_port = int(sys.argv[3])

    # PUB socket for broadcasting
    context = zmq.Context()
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind(f"tcp://{ip}:{pub_port}")

    # TCP socket for post connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, post_port))
    server_socket.listen()
    print("Listening for connections")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected with {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, pub_socket), daemon=True)
        thread.start()


if __name__ == "__main__":
    main()