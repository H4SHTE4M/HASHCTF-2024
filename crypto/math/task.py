# !/usr/bin/env python3
import socketserver
import os, sys, signal, string
from random import randint
from secret import flag

BANNER = br"""
 __ __   ____  _____ __ __    __ ______  _____ 
|  |  | /    |/ ___/|  |  |  /  ]      ||     |
|  |  ||  o  (   \_ |  |  | /  /|      ||   __|
|  _  ||     |\__  ||  _  |/  / |_|  |_||  |_  
|  |  ||  _  |/  \ ||  |  /   \_  |  |  |   _] 
|  |  ||  |  |\    ||  |  \     | |  |  |  |   
|__|__||__|__| \___||__|__|\____| |__|  |__|                                                        
"""
N = 56135841374488684373258694423292882709478511628224823806418810596720294684253418942704418179091997825551647866062286502441190115027708222460662070779175994701788428003909010382045613207284532791741873673703066633119446610400693458529100429608337219231960657953091738271259191554117313396642763210860060639141073846574854063639566514714132858435468712515314075072939175199679898398182825994936320483610198366472677612791756619011108922142762239138617449089169337289850195216113264566855267751924532728815955224322883877527042705441652709430700299472818705784229370198468215837020914928178388248878021890768324401897370624585349884198333555859109919450686780542004499282760223378846810870449633398616669951505955844529109916358388422428604135236531474213891506793466625402941248015834590154103947822771207939622459156386080305634677080506350249632630514863938445888806223951124355094468682539815309458151531117637927820629042605402188751144912274644498695897277
g = 986762276114520220801525811758560961667498483061127810099097

MENU = br"""
What are you going to do?
1. getbit
2. exit
"""

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()


    def close(self):
        self.send(b"Bye~")
        self.request.close()

    def pow(self,a,k,n):
        if k==0:
            return 1
        elif k%2==0:
            temp=self.pow(a,k//2,n)
            return temp*temp%N
        else:
            return a*self.pow(a,k-1,n)%N

    def get_bit(self,a,i,b):
        return self.pow(g, a*2**(b^(flag[i // 8] & (1 << (i % 8)))), N)*randint(1,N)%N


    def handle(self):
        signal.alarm(1200)

        self.send(BANNER)
        self.send(b"Welcome to HASHCTF!")
        self.send(b"To be, or not to be, that is the question~")
	
        while True:
            self.send(MENU, newline=False)
            choice = self.recv()

            if choice == b"1":
                msg1 = self.recv(prompt=b"Tell me which bit do you want to check\n")
                if not msg1 or not msg1.isdigit():
                    self.send(b'Invalid input.')
                    continue
                if not 0 <= int(msg1) < 8*len(flag):
                    self.send(b'The index is out of range.')
                    continue
		
		
		
                bit = self.recv(prompt=b"What do you think this bit is\n")
                if not (bit==b"0" or bit==b"1") :
                    self.send(b'Invalid input.')
                    continue

                msg2 = self.recv(prompt=b"This number may not be easy to get\n")
                if not msg2 or not msg2.isdigit():
                    self.send(b'Invalid input.')
                    continue
                if int(msg2)<0:
                    self.send(b'It is out of range.')
                    continue
                try:
                    self.send(hex(self.get_bit(int(msg2),int(msg1),int(bit))).encode())
                    continue
                except:
                    self.send(b'Something Wrong?')
                    continue

            else:
                self.send("Bye~")
                self.close()
                exit()
                break

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10000
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

