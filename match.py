import os
import numpy as np
from imfractal import test_comparison
import matplotlib.pyplot as plt


min_distance = 100000000
min_call = ""
min_synth_spectrum = np.zeros(21)
real_spectrum = []

max_iterations = 20000
min_it = max_iterations - 10000
max_it = max_iterations + 20000
step_it = 10000

max_particles = 12000 
min_part = max_particles - 4000
max_part = max_particles + 4000
step_part = 1000

max_size = 400
min_size = max_size - 380
max_size = max_size + 400
step_size = 50

mid_rand = 0.035
min_rand = mid_rand - 0.02
max_rand = mid_rand + 0.05
step_rand = 0.01

mid_rand_z = 0.15
min_rand_z = mid_rand_z - 0.1
max_rand_z = mid_rand_z + 0.2
step_rand_z = 0.1

def make_graphics(fds_real, fds_synth, gen_call):
    fig = plt.figure()
    plt.plot(fds_real,'-', label = 'Real')
    plt.plot(fds_synth, 'x', label = 'Synth')
    plt.title(gen_call)

    plt.legend()
    plt.savefig('best_result.png')

print "Starting for..."

for it in range(min_it, max_it, step_it):
    for part in range(min_part, max_part, step_part):
        for size in range(min_size, max_size, step_size):
            for rand in np.arange(min_rand, max_rand, step_rand):
                for rand_z in np.arange(min_rand_z, max_rand_z, step_rand_z):
                    args_call = str(it) + " " + str(part) + " " + str(size) + " " + str(rand) + " " + str(rand_z)
                    generation_call = "./porous_generation/porous_generate " + args_call

                    print ""
                    os.system(generation_call)
                    distance, synth_spectrum, real_spec = test_comparison.compare(real_spectrum)
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

