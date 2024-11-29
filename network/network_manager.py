import socket
import json
import threading
from typing import Callable, Dict
from queue import Queue

class NetworkManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = Queue()
        self.handlers: Dict[str, Callable] = {}
        self.running = False
        
    def start_server(self):
        """Start server for hosting games"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.running = True
        
        # Start listener thread
        threading.Thread(target=self._accept_connections).start()
        
    def connect_to_server(self):
        """Connect to existing game server"""
        self.socket.connect((self.host, self.port))
        self.running = True
        
        # Start listener thread
        threading.Thread(target=self._receive_messages).start()
        
    def send_game_action(self, action_data: Dict):
        """Send game action to other player"""
        message = json.dumps(action_data)
        self.socket.send(message.encode())
        
    def register_handler(self, action_type: str, handler: Callable):
        """Register handler for specific action type"""
        self.handlers[action_type] = handler
        
    def _accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            client_socket, _ = self.socket.accept()
            threading.Thread(
                target=self._handle_client,
                args=(client_socket,)
            ).start()
            
    def _handle_client(self, client_socket: socket.socket):
        """Handle client connection"""
        while self.running:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                    
                message = json.loads(data.decode())
                self.message_queue.put(message)
                
            except Exception as e:
                print(f"Error handling client: {e}")
                break
                
        client_socket.close()
        
    def _receive_messages(self):
        """Receive and process messages"""
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                    
                message = json.loads(data.decode())
                self.message_queue.put(message)
                
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
                
    def process_messages(self):
        """Process queued messages"""
        while not self.message_queue.empty():
            message = self.message_queue.get()
            action_type = message.get("action")
            
            if action_type in self.handlers:
                self.handlers[action_type](message) 