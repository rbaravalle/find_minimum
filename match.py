import os
import numpy as np
from imfractal import test_comparison
import matplotlib.pyplot as plt
import random
from math import floor


min_distance = 100000000
min_synth_spectrum = np.zeros(21)
real_spectrum = []

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
    global real_spectrum
    distance, synth_spectrum, real_spectrum = test_comparison.compare(real_spectrum)
    print "Distance real - synthetic : ", distance

    if(distance < min_distance):
        min_distance = distance
        min_spectrum = synth_spectrum
        min_call = "Args: " + args_call + ", " + str(min_distance)

        make_graphics(real_spectrum, min_spectrum, min_call)
        change=True

    return min_distance, min_spectrum, min_call, change

def go_direction(sign, varss, var_i, current_minimum):
    min_spectrum = []
    min_call = ""
    change=True
    min_distance = current_minimum

    steps = [step_it, step_part, step_size, step_rand, step_rand_z]

    while(change):

            print "chosen variable: ", var_i

            varss[var_i] += steps[var_i] * sign

            min_distance, min_spectrum, min_call, change = compare(varss[0], varss[1], varss[2], varss[3], varss[4], min_distance)

    # varss contains the best variables' value where the distance is minimum
    return min_distance, min_spectrum, min_call, varss

def go_variable(var_i, it, part, size, rand, rand_z, min_distance):
    # generate random direction: 1 or -1 (0)
    direction = random.randint(0,1)

    varss = [it, part, size, rand, rand_z]
    best_vars = varss


    # first call
    args_call = "ARGS: " + str(it) + " " + str(part) + " " + str(size) + " " + str(rand) + " " + str(rand_z)
    print args_call
    min_distance_ret, min_spectrum, min_call, change = compare(it, part, size, rand, rand_z, min_distance)

    sign = 1
    if(direction <= 0):
        sign = -1

    min_distance, min_spectrum, min_call, best_vars = go_direction(sign, varss, var_i, min_distance_ret)
    # see if the other direction is better
    print "OTHER DIRECTION"
    print min_spectrum
    print "               "
    print "               "
    print "               "
    print "               "

    print "CURRENT MINIMUM:"
    print min_distance
    print min_spectrum
    print min_call
    print ""

    min_distance2, min_spectrum2, min_call2, best_vars2 = go_direction(-sign, varss, var_i, min_distance)

    if min_distance2 < min_distance:
        min_distance = min_distance2
        min_spectrum = min_spectrum2
        min_call = min_call2
        best_vars = best_vars2

    print "CURRENT MINIMUM:"
    print min_distance
    print min_spectrum
    print min_call
    print ""

    return min_distance, min_spectrum, min_call, best_vars


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
    best_vars=[]

    # generate random position in hyperspace
    it = int(floor(random.uniform(min_it, max_it)))
    part = int(floor(random.uniform(min_part, max_part)))
    size = int(floor(random.uniform(min_size, max_size)))
    rand = random.uniform(min_rand, max_rand)
    rand_z = random.uniform(min_rand_z, max_rand_z)


    already_visited = np.zeros((5))
    num_vars = 0
    # randomly choose one variable
    var_i = random.randint(0,4)
    already_visited[var_i] = 1

    min_distance, min_spectrum, min_call, best_vars = go_variable(var_i, it, part, size, rand, rand_z, min_distance)
 

    while(num_vars <= 5):

        # randomly choose another variable
        var_j = random.randint(0,4)

        while already_visited[var_j] > 0:
            var_j = random.randint(0,4)

        already_visited[var_j] = 1

        print "Trying another variable...   ", var_j
        print " --  "
        print " --  "
        print " --  "

        min_distance2, min_spectrum2, min_call2, best_vars2 = go_variable(var_j, best_vars[0], best_vars[1], best_vars[2], best_vars[3], best_vars[4], min_distance)

        if min_distance2 < min_distance:
            min_distance = min_distance2
            min_spectrum = min_spectrum2
            min_call = min_call2
            best_vars = best_vars2

            # start over
            num_vars = 0
            already_visited = np.zeros((5))
        else:
            num_vars +=1

        var_i = var_j


    
    return min_distance, min_spectrum, min_call, best_vars




min_distance, min_spectrum, min_call, best_vars = follow_gradient_dumb()
print "..............Result............. "
print "MINIMUM:"
print min_distance
print "SYNTH:" , min_spectrum
print min_call
print best_vars
