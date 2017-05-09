import os
import numpy as np
from imfractal import test_comparison
import matplotlib.pyplot as plt
import random
from math import floor


min_distance = 100000000
min_synth_spectrum = np.zeros(21)

max_iterations = 20000
min_it = max_iterations - 10000
max_it = max_iterations + 20000
step_it = 10000

max_particles = 16000
min_part = max_particles - 4000
max_part = max_particles + 4000
step_part = 1000

max_size = 400
min_size = max_size - 100
max_size = max_size + 500
step_size = 50

mid_rand = 0.435
min_rand = mid_rand - 0.02
max_rand = mid_rand + 0.05
step_rand = 0.01

mid_rand_z = 0.75
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

def compare(it, part, size, rand, rand_z, min_distance):
    min_call = ""
    min_spectrum = []
    args_call = str(it) + " " + str(part) + " " + str(size) + " " + str(rand) + " " + str(rand_z)
    generation_call = "./porous_generation/porous_generate " + args_call

    change=False

    print ""
    os.system(generation_call)
    distance, synth_spectrum, real_spec = test_comparison.compare([])
    print "Distance real - synthetic : ", distance

    if(distance < min_distance):
        min_distance = distance
        min_spectrum = synth_spectrum
        real_spectrum = real_spec
        min_call = "Args: " + args_call + ", " + str(min_distance)

        make_graphics(real_spectrum, min_spectrum, min_call)
        change=True

    print "CURRENT MINIMUM:"
    print min_distance
    print min_spectrum
    print min_call
    print ""

    return min_distance, min_spectrum, min_call, change

def go_direction(sign, min_distance_ret, varss, var_i, steps, current_minimum):
    min_spectrum = []
    min_call = ""
    min_distance = min_distance_ret
    change=True

    while(change):

            print min_distance_ret, current_minimum, min_distance

            print "New min distance: ", min_distance_ret
            print "chosen variable: ", var_i

            min_distance = min_distance_ret

            varss[var_i] += steps[var_i] * sign

            min_distance_ret, min_spectrum, min_call, change = compare(varss[0], varss[1], varss[2], varss[3], varss[4], min_distance)


    return min_distance_ret, min_spectrum, min_call

def go_variable(var_i, it, part, size, rand, rand_z, min_distance):
    # generate random direction: 1 or -1 (0)
    direction = random.randint(0,1)

    varss = [it, part, size, rand, rand_z]
    steps = [step_it, step_part, step_size, step_rand, step_rand_z]

    # first call
    args_call = "ARGS: " + str(it) + " " + str(part) + " " + str(size) + " " + str(rand) + " " + str(rand_z)
    print args_call
    min_distance_ret, min_spectrum, min_call, change = compare(it, part, size, rand, rand_z, min_distance)

    sign = 1
    if(direction <= 0):
        sign = -1

    min_distance, min_spectrum, min_call = go_direction(sign, min_distance_ret, varss, var_i, steps, min_distance_ret)
    # see if the other direction is better
    print "OTHER DIRECTION"
    print min_spectrum
    print "               "
    print "               "
    print "               "
    print "               "
    min_distance2, min_spectrum2, min_call2 = go_direction(-sign, min_distance, varss, var_i, steps, min_distance)

    if min_distance2 < min_distance:
        min_distance = min_distance2
        min_spectrum = min_spectrum2
        min_call = min_call2

    return min_distance, min_spectrum, min_call


print "Starting for..."

def brute_force():
    for it in range(min_it, max_it, step_it):
        for part in range(min_part, max_part, step_part):
            for size in range(min_size, max_size, step_size):
                for rand in np.arange(min_rand, max_rand, step_rand):
                    for rand_z in np.arange(min_rand_z, max_rand_z, step_rand_z):
                        min_distance, min_spectrum, min_call = compare(it, part, size, rand, rand_z, min_distance)

def follow_gradient_dumb():
    min_call = ""
    min_distance = 100000000
    # generate random position in hyperspace
    it = int(floor(random.uniform(min_it, max_it)))
    part = int(floor(random.uniform(min_part, max_part)))
    size = int(floor(random.uniform(min_size, max_size)))
    rand = random.uniform(min_rand, max_rand)
    rand_z = random.uniform(min_rand_z, max_rand_z)

    # randomly choose one variable
    var_i = random.randint(0,4)

    min_distance, min_spectrum, min_call = go_variable(var_i, it, part, size, rand, rand_z, min_distance)
    
    return min_distance, min_spectrum, min_call




min_distance, min_spectrum, min_call = follow_gradient_dumb()
print "..............Result............. "
print "MINIMUM:"
print min_distance
print "SYNTH:" , min_spectrum
print min_call
