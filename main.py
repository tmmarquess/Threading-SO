from threading import Thread, Semaphore
import random
import time


class DiningPhilosophers:
    # constructor
    def __init__(self, number_of_philosophers=5, meal_size=7):
        '''
            meal_size: jobs
            philosophers: processes
            chopsticks: resources (like garf and fork, a philosopher only can eat if he has both oh then)
            meal_size = 7 & number_of_philosophers = 5 -> [7, 7, 7, 7, 7], thus, each philosopher will have 7 jobs to do
        '''

        self.meals = [meal_size for _ in range(number_of_philosophers)]
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        self.status = ['  P  ' for _ in range(number_of_philosophers)]
        self.chopstick_holders = ['     ' for _ in range(number_of_philosophers)]

    def philosopher(self, i):
        j = (i + 1) % 5
        '''
            j will be used to represent the last philosopher of the list, for example,
            if we have five philosophers [0, 1, 2, 3, 4, 5], the last one will not have a second
            chopstick, so, using (i+1) % 5 the list will be like: [0, 1, 2, 3, 4, 0] (remember that we're in a rounded table,
            so the last element have to be relationed to the first element)
        '''

        # this loop only will finish when each philosopher finish their meal
        while self.meals[i] > 0:
            self.status[i] = '  P  ' # they all will start thinkinkg (pensando)
            time.sleep(random.random()) # put the philosopher to sleep
            self.status[i] = '  _  '
            if self.chopsticks[i].acquire(timeout=1): # check if the chopstick is been used for someone
                self.chopstick_holders[i] = ' /   ' # if chopstick is not been used, set that to the philosopher
                time.sleep(random.random()) # after get a chopstick, put the philosopher to sleep
                if self.chopsticks[j].acquire(timeout=1): # here we will check if the next chopstick is been used
                    self.chopstick_holders[i] = ' / \\ ' # if chopstick is not been used, set that to the philosopher
                    self.status[i] = '  C  ' # set de status to: C (comendo) for the philosopher
                    time.sleep(random.random()) # put the philosopher to sleep
                    self.meals[i] -= 1 # subtract one meal of the philosopher that are eating
                    self.chopsticks[j].release() # after eat, release the second chopstick
                    self.chopstick_holders[i] = ' /   ' # set just one chopstick to the philosopher
                self.chopsticks[i].release() # release the first chopstick
                self.chopstick_holders[i] = '     ' # set none chopstick to the philosopher
                self.status[i] = '  P  ' # the status will be setted as thinking again


def main():
    n = 5 # set the number of philosophers
    m = 7 # set the quantity of meals to each philosopher

    dining_philosophers = DiningPhilosophers(n, m) # creating the instance
    philosophers = [Thread(target=dining_philosophers.philosopher, args=(i,)) for i in range(n)] # thread initialization
    for philosopher in philosophers: # will go through any philosopher of the list
        philosopher.start() # start the operation
    while sum(dining_philosophers.meals) > 0: # will be checking if still have meals to be eaten
        print("=" * (n*5)) # print the quantity of meals
        print("".join(map(str, dining_philosophers.status)), " : ",
              str(dining_philosophers.status.count('  C  '))) # print the status that the philosopher is
        print("".join(map(str, dining_philosophers.chopstick_holders)))
        print("".join("{:3d}  ".format(m) for m in dining_philosophers.meals), " : ",
              str(sum(dining_philosophers.meals))) # print the quantity of meals of each philosopher
        time.sleep(0.1) # sleep a little after go to the next step

    for philosopher in philosophers:
        philosopher.join() # ensure there is no parallel processing going on

if __name__ == "__main__":
    main() # execute the function