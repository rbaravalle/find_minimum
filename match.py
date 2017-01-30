import os
import numpy as np
from imfractal import test_comparison
import matplotlib.pyplot as plt


min_distance = 100000000
min_call = ""
min_synth_spectrum = np.zeros(21)
real_spectrum = np.zeros(21)

max_iterations = 20000
min_it = max_iterations - 10000
max_it = max_iterations + 10000
step_it = 10000

def make_graphics(fds_real, fds_synth, gen_call):
    fig = plt.figure()
    plt.plot(fds_real,'-', label = 'Real')
    plt.plot(fds_synth, 'x', label = 'Synth')
    plt.title(gen_call)

    plt.legend()
    plt.savefig('best_result.png')

print "Starting for..."

for it in range(min_it, max_it, step_it):
    args_call = str(it) + " 12000 400 0.035 0.15"
    generation_call = "./porous_generation/porous_generate " + args_call

    print ""
    os.system(generation_call)
    distance, synth_spectrum, real_spec = test_comparison.compare()
    print "Distance real - synthetic : ", distance

    if(distance < min_distance):
        min_distance = distance
        min_spectrum = synth_spectrum
        real_spectrum = real_spec
        min_call = "Args: " + args_call + ", " + str(min_distance)

        make_graphics(real_spectrum, min_spectrum, min_call)

    print "CURRENT MINIMUM:"
    print min_distance
    print min_spectrum
    print min_call
    print ""




print "..............Result............. "
print "MINIMUM:"
print min_distance
print "SYNTH:" , min_spectrum
print "REAL:" , real_spectrum
print min_call

