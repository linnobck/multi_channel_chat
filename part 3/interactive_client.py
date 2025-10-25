import socket
import pickle
import sys
import threading
import zmq
from datetime import datetime


def listen_to_channel(ip, pub_port):
    # set up pub channel
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(f"tcp://{ip}:{pub_port}")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    print(f"Connected to pub channel at tcp://{ip}:{pub_port}")

    # print every incoming message
    while True:
        message = sub_socket.recv_string()
        print(f"\n{message}")


def send_messages(ip, post_port, username):
    # read user input and post messages to server
    while True:
        message = input()

        timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        msg_data = (username, timestamp, message)

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, post_port))
            client_socket.sendall(pickle.dumps(msg_data))

            # get server ack
            response = pickle.loads(client_socket.recv(1024))

            client_socket.close()

            if message.upper() == "EXIT":
                sys.exit(0)

        except Exception as e:
            print(f"Error sending message: {e}")


def main():
    if len(sys.argv) != 5:
        print("Usage: python interactive_client.py <ip> <post_port> <pub_port> <name>")
        sys.exit(1)

    ip = sys.argv[1]
    post_port = int(sys.argv[2])
    pub_port = int(sys.argv[3])
    username = sys.argv[4]

    # thread for listening to PUB channel
    listener_thread = threading.Thread(target=listen_to_channel, args=(ip, pub_port), daemon=True)
    listener_thread.start()

    send_messages(ip, post_port, username)


if __name__ == "__main__":
    main()