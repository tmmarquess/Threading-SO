import threading
import random


class bcolors: #Classe para imprimir texto colorido no terminal
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


buffer = [] # Buffer compartilhado
tam = 10  # tamanho máximo do buffer
semaforo = threading.Semaphore() # Semáforo que controla o acesso ao buffer


def inserir_no_buffer(vlr: int): # Simulando um buffer limitado através do tamanho dele
    if len(buffer) < tam: # Verificando se o tamanho do buffer estrapola o máximo
        buffer.append(vlr) 
    else: # Caso estrapole, gera uma excessão
        raise IndexError


def produzir_item(): # gera um valor aleatório de 0 até 10
    return random.randint(1, 10)


def consumir_item(): #consome o primeiro item da lista
    valor = buffer[0]
    buffer.remove(valor)
    return valor


def produtor():
    while True:
        if len(buffer) < tam: # se o buffer ainda não estiver cheio, enche ele
            valor = produzir_item() # produz um valor
            semaforo.acquire() # reserva o semáforo do buffer
            inserir_no_buffer(valor) # insere o valor no buffer
            print(f"{bcolors.OK}Inserindo {str(valor)} {bcolors.RESET}") # imprime o valor inserido
            semaforo.release() # solta o semáforo do buffer


def consumidor():
    while True:
        if len(buffer) != 0: # se a quantidade de itens armazenada no buffer for diferente de zero
            semaforo.acquire() # reserva o semáforo do buffer
            valor = consumir_item() # Consome um item
            print(f"{bcolors.FAIL}Consumindo {str(valor)} {bcolors.RESET}") #imprime o valor consumido
            semaforo.release() # solta o semáforo do buffer


thread_produtor = threading.Thread(target=produtor)
thread_consumidor = threading.Thread(target=consumidor)

thread_produtor.start()
thread_consumidor.start()
