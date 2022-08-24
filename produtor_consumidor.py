import threading
import random
import time

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR


buffer = []
tam = 10 # tamanho máximo do buffer
semaforo = threading.Semaphore()

def inserir_no_buffer(vlr : int):
    if len(buffer) < tam:
        buffer.append(vlr)
    else:
        raise IndexError

def produzir_item():
    return random.randint(1,10)

def consumir_item():
    valor = buffer[0]
    buffer.remove(valor)
    return valor

def produtor():
    while True:
        if len(buffer) < tam:
            valor = produzir_item()
            semaforo.acquire()
            inserir_no_buffer(valor)
            print(f"{bcolors.OK}"+"Inserindo "+ str(valor)+ f"{bcolors.RESET}")
            semaforo.release()


def consumidor():
    while True:
        if len(buffer) != 0:
            semaforo.acquire()
            valor = consumir_item()
            print(f"{bcolors.FAIL}"+"Consumindo "+ str(valor)+ f"{bcolors.RESET}")
            semaforo.release()


thread_produtor = threading.Thread(target=produtor)
thread_consumidor = threading.Thread(target=consumidor)

thread_produtor.start()
thread_consumidor.start()