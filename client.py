import socket
import threading
import pyaudio

# Client configuration
SERVER_HOST = "127.0.0.1"  # Replace with server IP
SERVER_PORT = 5000
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (Hz)

# Audio setup
audio = pyaudio.PyAudio()
input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
output_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

def receive_audio(client_socket):
    """Receive audio from the server and play it."""
    while True:
        try:
            data = client_socket.recv(CHUNK)
            output_stream.write(data)
        except:
            break

# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Start receiving audio in a separate thread
threading.Thread(target=receive_audio, args=(client_socket,)).start()

# Send audio to the server
try:
    while True:
        data = input_stream.read(CHUNK)
        client_socket.sendall(data)
except KeyboardInterrupt:
    print("Exiting...")
    client_socket.close()
    input_stream.close()
    output_stream.close()
    audio.terminate()
