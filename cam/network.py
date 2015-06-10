import socket
import time

class Server(object):
  SERVER_HOST = ''
  SERVER_PORT = 1436
  
  def __init__(self, sock_type, get_msg, host_ip=None, host_port=None):
    self.host_ip = host_ip or self.SERVER_HOST
    self.host_port = int(host_port) or self.SERVER_PORT
    self.sock = socket.socket(socket.AF_INET, sock_type)
    self.get_msg = get_msg
    
  def serve(self):
    self.sock.bind((self.host_ip, self.host_port))
    print('connected @ %s:%s' % (self.host_ip, self.host_port))
    self.sock.listen(1)
    
    while True:
      (client, addr) = self.sock.accept()
      print('client: %s' % str(addr))
      total_sent_bytes = 0
      msg = self.get_msg(addr)
      
      while total_sent_bytes < len(msg):
        sent_bytes = client.send(msg[total_sent_bytes:])
        if sent_bytes == 0:
          print('socket connection broken (server)')  # TODO: raise/log?
        total_sent_bytes += sent_bytes
      client.shutdown(socket.SHUT_RDWR)
      client.close()
    self.sock.shutdown(socket.SHUT_RDWR)
    self.sock.close()
    
  def __del__(self):
    self.sock.shutdown(socket.SHUT_RDWR)
    self.sock.close()
    
class UdpSender(object):
  
  def __init__(self, get_msg, target_ip, target_port):
    self.send_addr = (target_ip, int(target_port))
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.get_msg = get_msg
    
  def send_forever(self):
    msgs_sent = 0
    start_time = time.clock()
    while True:
      if msgs_sent % 30 == 0:
        end_time = time.clock()
        print('30 msgs in %f sec' % (end_time - start_time))
        start_time = end_time
        msgs_sent = 0
      total_sent_bytes = 0
      msg = self.get_msg(self.send_addr)
      
      while total_sent_bytes < len(msg):
        # print('msg len: %s' % len(msg))
        msg_chunk = msg[total_sent_bytes:total_sent_bytes + 32768]
        sent_bytes = self.sock.sendto(msg_chunk, self.send_addr)
        # print('sent bytes: %s' % sent_bytes)
        if sent_bytes == 0:
          print('failed to send')  # TODO: raise/log?
        total_sent_bytes += sent_bytes
      
      # send blank message to signify being done
      self.sock.sendto('', self.send_addr)
      msgs_sent += 1
      
    self.sock.close()
    
  def __del__(self):
    self.sock.close()
    
class UdpReceiver(object):
  
  def __init__(self, listen_ip, listen_port, msg_fin_callback):
    self.listen_ip = listen_ip
    self.listen_port = int(listen_port)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.msg_fin_callback = msg_fin_callback
    
  def receive_forever(self):
    self.sock.bind((self.listen_ip, self.listen_port))
    
    msg_buffer = ''
    while True:
      data, addr = self.sock.recvfrom(32768)
      if data == '':
        self.msg_fin_callback(msg_buffer)
        msg_buffer = ''
      else: 
        msg_buffer += data
        
  def __del__(self):
    self.sock.close()
    
class Client(object):
  
  def __init__(self, sock_type):
    self.sock = socket.socket(socket.AF_INET, sock_type)
    
  def receive(self, ip, port):
    self.sock.connect((ip, int(port)))
    chunks = []
    bytes_recd = 0
    while True:
      chunk = self.sock.recv(2048)
      if chunk == '':
        break
      chunks.append(chunk)
      bytes_recd += len(chunk)
    self.sock.shutdown(socket.SHUT_RDWR)
    self.sock.close()
    return ''.join(chunks)
    
  
