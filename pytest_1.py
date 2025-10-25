import subprocess
import time
import os
import signal
import pytest

@pytest.fixture(scope="module")
def start_server():
    port = 5555
    server = subprocess.Popen(
        ["python3", "part1/post_server.py", "127.0.0.1", str(port)],
        stdout=subprocess.DEVNULL,  # or subprocess.PIPE if you need logs
        stderr=subprocess.STDOUT
    )
    time.sleep(1)  # Let the server start
    yield port
    os.kill(server.pid, signal.SIGTERM)
    server.wait(timeout=3)

def test_post_messages_to_server(start_server):
    port = start_server

    messages = [
        ("alice", "hello"),
        ("bob", "hi there"),
        ("carol", "how are you?"),
    ]

    for user, msg in messages:
        result = subprocess.run(
            ["python3", "part1/post_client.py", "127.0.0.1", str(port), user, msg],
            check=True,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0