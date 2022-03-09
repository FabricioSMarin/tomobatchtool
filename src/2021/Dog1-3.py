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
        [2.840, 1.548, -18.500, 0.89, 0.14, 0.002, 0.002, 50],
        [2.838, 1.548, -16.000, 0.9, 0.14, 0.002, 0.002, 50],
        [2.836, 1.548, -13.500, 0.908, 0.14, 0.002, 0.002, 50],
        [2.834, 1.548, -11.000, 0.918, 0.14, 0.002, 0.002, 50],
        [2.831, 1.548, -8.500, 0.928, 0.14, 0.002, 0.002, 50],
        [2.828, 1.548, -6.000, 0.886, 0.14, 0.002, 0.002, 50],
        [2.825, 1.548, -3.500, 0.876, 0.14, 0.002, 0.002, 50],
        [2.823, 1.548, -1.000, 0.878, 0.14, 0.002, 0.002, 50],
        [2.820, 1.548, 1.500, 0.878, 0.14, 0.002, 0.002, 50],
        [2.818, 1.548, 4.000, 0.88, 0.14, 0.002, 0.002, 50],
        [2.813, 1.548, 6.500, 0.842, 0.14, 0.002, 0.002, 50],
        [2.809, 1.548, 9.000, 0.812, 0.14, 0.002, 0.002, 50],
        [2.806, 1.548, 11.500, 0.804, 0.14, 0.002, 0.002, 50],
        [2.803, 1.548, 14.000, 0.796, 0.14, 0.002, 0.002, 50],
        [2.800, 1.548, 16.500, 0.79, 0.14, 0.002, 0.002, 50],
        [2.800, 1.548, 19.000, 0.764, 0.14, 0.002, 0.002, 50],
        [2.802, 1.548, 21.500, 0.728, 0.14, 0.002, 0.002, 50],
        [2.800, 1.548, 24.000, 0.714, 0.14, 0.002, 0.002, 50],
        [2.798, 1.548, 26.500, 0.7, 0.14, 0.002, 0.002, 50],
        [2.797, 1.548, 29.000, 0.686, 0.14, 0.002, 0.002, 50],
        [2.795, 1.548, 31.500, 0.666, 0.14, 0.002, 0.002, 50],
        [2.796, 1.548, 34.000, 0.616, 0.14, 0.002, 0.002, 50],
        [2.795, 1.548, 36.500, 0.596, 0.14, 0.002, 0.002, 50],
        [2.794, 1.548, 39.000, 0.576, 0.14, 0.002, 0.002, 50],
        [2.792, 1.548, 41.500, 0.558, 0.14, 0.002, 0.002, 50],
        [2.791, 1.548, 44.000, 0.54, 0.14, 0.002, 0.002, 50],
        [2.798, 1.548, 46.500, 0.472, 0.14, 0.002, 0.002, 50],
        [2.798, 1.548, 49.000, 0.448, 0.14, 0.002, 0.002, 50],
        [2.798, 1.548, 51.500, 0.422, 0.14, 0.002, 0.002, 50],
        [2.797, 1.548, 54.000, 0.396, 0.14, 0.002, 0.002, 50],
        [2.797, 1.548, 56.500, 0.37, 0.14, 0.002, 0.002, 50],
        [2.813, 1.548, 59.000, 0.32, 0.14, 0.002, 0.002, 50],
        [2.819, 1.548, 61.500, 0.284, 0.14, 0.002, 0.002, 50],
        [2.821, 1.548, 64.000, 0.254, 0.14, 0.002, 0.002, 50],
        [2.824, 1.548, 66.500, 0.224, 0.14, 0.002, 0.002, 50],
        [2.826, 1.548, 69.000, 0.196, 0.14, 0.002, 0.002, 50],
        [2.693, 1.548, 71.500, 1.842, 0.14, 0.002, 0.002, 50],

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
