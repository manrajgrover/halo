from halo import Halo
from time import sleep


@Halo(text='Loading {task}', spinner='line')
def run_task(halo_iter=[], stop_text='', stop_symbol=' '):
    sleep(.5)


tasks1 = ['breakfest', 'launch', 'dinner']
tasks2 = ['morning', 'noon', 'night']

run_task(halo_iter=tasks1, stop_symbol='🦄'.encode(
    'utf-8'), stop_text='Task1 Finished')
run_task(halo_iter=tasks2, stop_text='Finished Time')
