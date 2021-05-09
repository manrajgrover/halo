from halo import Halo
from time import sleep


@Halo(text='Loading {task}', spinner='line')
def run_task(halo_iter=[], stop_text='', stop_symbol=' '):
    sleep(1)

@Halo(text='Loading {task} at {task2}', spinner='line')
def run_task2(halo_iter=[], stop_text='', stop_symbol=' '):
    sleep(1)

tasks1 = ['breakfest', 'launch', 'dinner']
tasks2 = ['morning', 'noon', 'night']

#with symbol
run_task(halo_iter=tasks1, stop_symbol='🦄'.encode(
    'utf-8'), stop_text='Task1 Finished')

#without symbol
run_task2(halo_iter=list(zip(tasks1, tasks2)), stop_text='Finished Time')
run_task2.spinner.symbol = ''