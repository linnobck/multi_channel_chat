import zmq
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python pub_client.py <ip> <pub_port>")
        sys.exit(1)

    ip = sys.argv[1]
    pub_port = int(sys.argv[2])

    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(f"tcp://{ip}:{pub_port}")

    # subscribe to all messages
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    print(f"Subscribed to tcp://{ip}:{pub_port}")

    while True:
        message = sub_socket.recv_string()
        print(message)

if __name__ == "__main__":
    main()