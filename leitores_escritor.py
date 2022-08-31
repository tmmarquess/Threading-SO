import threading
import time
import random

class bcolors: #Classe para imprimir texto colorido no terminal
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


contador_de_leitores = 0 #Armazena a quantidade de leitores atual
sem_leitores = threading.Semaphore() # Semáforo que controla o contador de leitores

sem_escrita = threading.Semaphore() # Semáforo que controla a escrita de dados
escritor_quer_escrever = False # booleano que impede mais leitores de entrar, caso há novos dados a escrever

def leitor(number : int):
    global contador_de_leitores, escritor_quer_escrever
    while True:
        if not escritor_quer_escrever: #Se o escritor não quiser escrever, 
            sem_leitores.acquire() # Reserva o semáforo de leitores
            contador_de_leitores += 1 # Incrementa +1 leitor no contador
            if contador_de_leitores == 1: # Se for o primeiro leitor, 
                sem_escrita.acquire() # reserva o semáforo de escita
            sem_leitores.release() # solta o semáforo de leitores

            print(f'{bcolors.OK}{number} - Lendo dados{bcolors.RESET}') # Lê os dados

            sem_leitores.acquire() # Reserva o semáforo de leitores
            contador_de_leitores -= 1 # Decrementa -1 leitor no contador
            if contador_de_leitores == 0: # Se for o ultimo leitor,
                sem_escrita.release() # Libera o semáforo de escrita
            sem_leitores.release() # solta o semáforo de leitores




def escritor():
    global escritor_quer_escrever, contador_de_leitores
    while True:
        escritor_quer_escrever = random.choice([False, True, False]) # escolhe aleatóriamente se o escritos quer escrever dados
        if escritor_quer_escrever: # se o escritor quer escrever
            sem_escrita.acquire() # Reserva o semáforo de escrita
            print(f'{bcolors.FAIL}Escrevendo dados{bcolors.RESET}') # Escreve dados
            time.sleep(3) # Tempo de escrita de dados
            sem_escrita.release() # Libera o semáforo de escrita
        time.sleep(2) # Countdown de inserção de dados


leitor1 = threading.Thread(target=leitor,args=(1, ))
leitor2 = threading.Thread(target=leitor,args=(2, ))
leitor3 = threading.Thread(target=leitor,args=(3, ))
escritor1 = threading.Thread(target=escritor)

escritor1.start()
leitor1.start()
leitor2.start()
leitor3.start()