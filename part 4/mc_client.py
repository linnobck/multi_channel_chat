import socket
import pickle
import sys
import threading
import zmq
from datetime import datetime
import time


def listen_to_channel(ip, pub_port, channel):
    # receive messages for specific channel
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(f"tcp://{ip}:{pub_port}")

    # only sub to chosen channel
    # or all if 'ALL'
    if channel.upper() == "ALL":
        sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        print("Subscribed to all channels (read-only)")
    else:
        sub_socket.setsockopt_string(zmq.SUBSCRIBE, channel)
        print(f"Subscribed to channel '{channel}'")

    while True:
        message = sub_socket.recv_string()
        print(f"\n{message}")


def send_messages(ip, post_port, channel, username):
    # send messages to server unless channel is ALL
    if channel.upper() == "ALL":
        print("You cannot write into this channel (read-only)")

    while True:
        message = input()
        if not message.strip():
            continue

        timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        msg_data = (channel, username, timestamp, message)

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, post_port))
            client_socket.sendall(pickle.dumps(msg_data))

            ack = pickle.loads(client_socket.recv(1024))
            client_socket.close()

            if message.upper() == "EXIT":
                sys.exit(0)

        except Exception as e:
            print(f"Error sending message: {e}")
            time.sleep(1)


def main():
    if len(sys.argv) != 6:
        print("Usage: python mc_client.py <ip> <post_port> <pub_port> <channel> <name>")
        sys.exit(1)

    ip = sys.argv[1]
    post_port = int(sys.argv[2])
    pub_port = int(sys.argv[3])
    channel = sys.argv[4]
    username = sys.argv[5]

    # background listener thread
    listener_thread = threading.Thread(target=listen_to_channel, args=(ip, pub_port, channel), daemon=True)
    listener_thread.start()

    send_messages(ip, post_port, channel, username)


if __name__ == "__main__":
    main()