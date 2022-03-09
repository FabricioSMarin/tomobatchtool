#!/APSshare/anaconda/x86_64/bin/python

import epics
from epics import caput, caget
from epics import PV
import time
import numpy as np

'''
please enter the scan prameters below:
scans [x-center(um), y-center.(um), x-width.(um), y-width.(um), x-stepsize.(um), Y-stepsize.(um), dwell.(ms)]
'''

scans = [
        [2.856, 1.548, -26.000, 0.82, 0.14, 0.002, 0.002, 50],
        [2.854, 1.548, -23.500, 0.83, 0.14, 0.002, 0.002, 50],
        [2.852, 1.548, -21.000, 0.84, 0.14, 0.002, 0.002, 50],
        [2.850, 1.548, -18.500, 0.848, 0.14, 0.002, 0.002, 50],
        [2.848, 1.548, -16.000, 0.858, 0.14, 0.002, 0.002, 50],
        [2.845, 1.548, -13.500, 0.866, 0.14, 0.002, 0.002, 50],
        [2.843, 1.548, -11.000, 0.87, 0.14, 0.002, 0.002, 50],
        [2.841, 1.548, -8.500, 0.87, 0.14, 0.002, 0.002, 50],
        [2.838, 1.548, -6.000, 0.872, 0.14, 0.002, 0.002, 50],
        [2.836, 1.548, -3.500, 0.872, 0.14, 0.002, 0.002, 50],
        [2.833, 1.548, -1.000, 0.874, 0.14, 0.002, 0.002, 50],
        [2.831, 1.548, 1.500, 0.868, 0.14, 0.002, 0.002, 50],
        [2.828, 1.548, 4.000, 0.862, 0.14, 0.002, 0.002, 50],
        [2.825, 1.548, 6.500, 0.854, 0.14, 0.002, 0.002, 50],
        [2.822, 1.548, 9.000, 0.846, 0.14, 0.002, 0.002, 50],
        [2.819, 1.548, 11.500, 0.838, 0.14, 0.002, 0.002, 50],
        [2.817, 1.548, 14.000, 0.828, 0.14, 0.002, 0.002, 50],
        [2.815, 1.548, 16.500, 0.814, 0.14, 0.002, 0.002, 50],
        [2.813, 1.548, 19.000, 0.802, 0.14, 0.002, 0.002, 50],
        [2.811, 1.548, 21.500, 0.788, 0.14, 0.002, 0.002, 50],
        [2.809, 1.548, 24.000, 0.776, 0.14, 0.002, 0.002, 50],
        [2.807, 1.548, 26.500, 0.76, 0.14, 0.002, 0.002, 50],
        [2.806, 1.548, 29.000, 0.74, 0.14, 0.002, 0.002, 50],
        [2.804, 1.548, 31.500, 0.722, 0.14, 0.002, 0.002, 50],
        [2.803, 1.548, 34.000, 0.702, 0.14, 0.002, 0.002, 50],
        [2.801, 1.548, 36.500, 0.684, 0.14, 0.002, 0.002, 50],
        [2.800, 1.548, 39.000, 0.664, 0.14, 0.002, 0.002, 50],
        [2.800, 1.548, 41.500, 0.64, 0.14, 0.002, 0.002, 50],
        [2.800, 1.548, 44.000, 0.612, 0.14, 0.002, 0.002, 50],
        [2.799, 1.548, 46.500, 0.588, 0.14, 0.002, 0.002, 50],
        [2.799, 1.548, 49.000, 0.562, 0.14, 0.002, 0.002, 50],
        [2.799, 1.548, 51.500, 0.538, 0.14, 0.002, 0.002, 50],
        [2.801, 1.548, 54.000, 0.508, 0.14, 0.002, 0.002, 50],
        [2.803, 1.548, 56.500, 0.478, 0.14, 0.002, 0.002, 50],
        [2.805, 1.548, 59.000, 0.448, 0.14, 0.002, 0.002, 50],
        [2.808, 1.548, 61.500, 0.418, 0.14, 0.002, 0.002, 50],
        [2.810, 1.548, 64.000, 0.388, 0.14, 0.002, 0.002, 50],

]

pvs = ['2xfm:m200.VAL', '2xfm:m13.VAL', '2xfm:m58.VAL', '2xfm:FscanH.P1WD',
       '2xfm:Fscan1.P1WD', '2xfm:FscanH.P1SI', '2xfm:Fscan1.P1SI', '2xfm:Flyscans:Setup:DwellTime.VAL']

sample_x = PV('2xfm:m200.VAL')
sample_x_rbv = PV('2xfm:m200.RBV')
sample_y = PV('2xfm:m13.VAL')
sample_y_rbv = PV('2xfm:m13.RBV')

def calc_ETA(scan):
    dwell = scan[0][7]
    y_step = scan[0][6]
    x_step = scan[0][5]

    eta = 0
    for i in range(len(scan)):
        pixels_wide = scan[i][3]/x_step
        pixels_tall = scan[i][4]/y_step
        eta += dwell*pixels_wide*pixels_tall*1.1
        total_time = eta/1000
    return total_time

eta = calc_ETA(scans)

print('Batchscan starts')

for batch_num, scan in enumerate(scans):

    print('entering scan parameters for scan #{0:d}'.format(batch_num + 1))
    for i, pvs1 in enumerate(pvs):
        print ('Setting %s' % pvs1)
        caput(pvs1, scans[batch_num][i])
        time.sleep(1.)

    # check whether the motors have moved to the requested position
    print('checking whether motors are in position')
    ready = abs(sample_x_rbv.get() - sample_x.get()) < 0.1 and abs(sample_y_rbv.get() - sample_y.get()) < 0.1
    while not ready:
        print('\t Motors are not ready')
        sample_x.put(sample_x.get())
        sample_y.put(sample_y.get())
        time.sleep(3.)
        ready = abs(sample_x_rbv.get() - sample_x.get()) < 0.1 and abs(
            sample_y_rbv.get() - sample_y.get()) < 0.1
    print('\t Motors are ready now!')

    caput('2xfm:Fscan1.EXSC', 1)
    time.sleep(1)
    done = False
    print('Checking every 10 sec for scan to complete')

    while not done:
        done = caget('2xfm:Fscan1.EXSC') == 0
        print('\t Batch {0:d}/{1:d} scan is ongoing'.format(batch_num + 1, len(scans)))
        hours = np.floor(eta / 60 / 60)
        minutes = np.floor((eta / 60 / 60 - hours) * 60)
        seconds = np.floor(eta - minutes * 60 - hours * 60 * 60)
        print('ETA = Hours: {}  Min: {}  Seconds: {}'.format(hours, minutes, seconds))
        eta -= 10
        time.sleep(10.)

print('Completeted. Congratulations!')
