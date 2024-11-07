import socket
import json
from game.settings import *
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

HOST = config['server_config']['host']
PORT = int(config['server_config']['port'])
LOCAL = int(config['server_config']['local'])


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        self.client.settimeout(20)
        if LOCAL == 1:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)        
            self.server = local_ip
        else:
            self.server = HOST
        self.port = PORT 
        
        self.addr = (self.server, self.port)
        self.local_data = {}
        self.server_data = {}

    def change_team_request(self, team):
        data = {
            'flag' : 4,
            'team' : team,
        }
        self.client.sendto(json.dumps(data).encode(), self.addr)
        
    
    def get_servers_list(self):
        req = {
            'flag' : 1,
        }
        self.client.sendto(json.dumps(req).encode(), (self.server, self.port))
        data, _ = self.client.recvfrom(MAX_DATA_SIZE)
        return json.loads(data.decode())
        
    def create_new_server(self, name):
        req = {
            'flag' : 2,
            'name' : name
        }
        self.client.sendto(json.dumps(req).encode(), (self.server, self.port))
        data, _ = self.client.recvfrom(MAX_DATA_SIZE)
        return json.loads(data.decode())
    
    def join_server(self, host, port):
        req = {
            'flag' : 3,
            'port' : port
        }
        self.client.sendto(json.dumps(req).encode(), (self.server, self.port))
        self.addr = (host, port)
        print(self.addr)
    
    def player_init(self, player_id, team):
        init_data = {
            'flag' : 1,
            'id' : player_id,
            'team' : team
        }
        self.client.sendto(json.dumps(init_data).encode(), self.addr)
        data, _ = self.client.recvfrom(MAX_DATA_SIZE)
        return json.loads(data.decode())
    
    def fetch_data(self):
        try:
            self.client.sendto(json.dumps(self.local_data).encode(), self.addr)
            data, _ = self.client.recvfrom(MAX_DATA_SIZE)
            self.server_data = json.loads(data.decode())
        except socket.timeout:
            print("Send/receive operation timed out.")
        except socket.error as e:
            print(f"Socket error: {e}")
    
    def disconect_to_current_server(self):
        disconnected_message = {
                'flag' : -1,
            }
        self.client.sendto(json.dumps(disconnected_message).encode(), self.addr)
        self.addr = (self.server, self.port) ## 
    
    def shut_down(self, id):
        try:
            disconnected_message = {
                'flag' : -1,
            }
            self.client.sendto(json.dumps(disconnected_message).encode(), self.addr)
            self.client.close()  
        except Exception as e:
            # print(f"Error during shutdown: {e}")
            pass