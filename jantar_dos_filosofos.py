from threading import Thread, Semaphore
import random
import time


class DiningPhilosophers:
    # constructor
    def __init__(self, number_of_philosophers=5, meal_size=7):
        """
        meal_size: jobs
        philosophers: processos
        chopsticks: resources (como garfo e faca/hashi, o filósofo só pode comer se ele estiver com ambos)
        meal_size = 7 & number_of_philosophers = 5 -> [7, 7, 7, 7, 7], então, cada filósofo terá 7 trabalhos para executar
        """

        self.meals = [meal_size for _ in range(number_of_philosophers)]
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        self.status = ["  P  " for _ in range(number_of_philosophers)]
        self.chopstick_holders = ["     " for _ in range(number_of_philosophers)]

    def philosopher(self, i):
        j = (i + 1) % 5
        """
            j será usado para representar o último filósofo da lista, por exemplo,
            se tivermos cinco filósofos [0, 1, 2, 3, 4, 5], o último não terá um segundo
            talher, então, usando (i+1) % 5 a lista ficará assim: [0, 1, 2, 3, 4, 0] (lembre-se que estamos em uma mesa redonda,
            então o último elemento tem que ser relacionado ao primeiro elemento)
        """

        # esse loop irá finalizar quando cada fiósofo finalizar seus trabalhos(meals)
        while self.meals[i] > 0:
            self.status[i] = "  P  "  # todos irão ter estado inicial como pensando
            time.sleep(random.random())  # colocar o filósofo para esperar por um tempo entre 0 e 1
            self.status[i] = "  _  "
            if self.chopsticks[i].acquire(
                timeout=1
            ):  # checar se um dos talheres está sendo utilizado por alguém
                self.chopstick_holders[
                    i
                ] = " /   "  # se ele não estiver sendo usado, atribua-o para o filósofo
                time.sleep(
                    random.random()
                )  # depois de atribuir o talher, colocar o filósofo para esperar por um tempo entre 0 e 1
                if self.chopsticks[j].acquire(
                    timeout=1
                ):  # aqui checará se o próximo talher está sendo utilizado
                    self.chopstick_holders[
                        i
                    ] = " / \\ "  # se não estiver sendo utilizado, atribua-o para o filósofo
                    self.status[
                        i
                    ] = "  C  "  # defina o status do filósofo para: C (comendo)
                    time.sleep(random.random())  # colocar o filósofo para esperar por um tempo entre 0 e 1
                    self.meals[
                        i
                    ] -= 1  # subtrair um job(meal_size) do filósofo
                    self.chopsticks[
                        j
                    ].release()  # depois de comer, libera o segundo talher
                    self.chopstick_holders[
                        i
                    ] = " /   "  # atribui apenas um talher ao filóso
                self.chopsticks[i].release()  # libera o primeiro talher
                self.chopstick_holders[
                    i
                ] = "     "  # atribui nenhum talher ao filósofo
                self.status[i] = "  P  "  # o status será definido como P (pensando) novamente.


def main():
    n = 5  # defina o numero de filósofos
    m = 7  # defina o tamanho da refeição

    dining_philosophers = DiningPhilosophers(n, m)  # instanciando a classe
    philosophers = [
        Thread(target=dining_philosophers.philosopher, args=(i,)) for i in range(n)
    ]  # inicialização da thread
    for philosopher in philosophers:  # irá percorrer cada filósofo na lista
        philosopher.start()  # start na operação
    while ( sum(dining_philosophers.meals) > 0):  # estará checando se ainda há refeições para serem consumidas
        print("=" * (n * 5))  # print na quantidade de refeições
        print(
            "".join(map(str, dining_philosophers.status)),
            " : ",
            str(dining_philosophers.status.count("  C  ")),
        )  # print o status em que o filósofo se encontra
        print("".join(map(str, dining_philosophers.chopstick_holders)))
        print(
            "".join("{:3d}  ".format(m) for m in dining_philosophers.meals),
            " : ",
            str(sum(dining_philosophers.meals)),
        )  # print a quantidade restante da refeição de cada filósofo
        time.sleep(0.1)  # sleep de 0.1 para poder passar para a execução do próximo step

    for philosopher in philosophers:
        philosopher.join()  # garantir que não há paralelismo


if __name__ == "__main__":
    main()  # executando a função
