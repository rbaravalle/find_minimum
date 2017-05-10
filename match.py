import os
import numpy as np
from imfractal import test_comparison
import matplotlib.pyplot as plt
import random
from math import floor


min_synth_spectrum = np.zeros(21)
real_spectrum = []

max_iterations = 20000
min_it = max_iterations - 20000
max_it = max_iterations + 30000
step_it = 10000

max_particles = 16000
min_part = max_particles - 16000
max_part = max_particles + 16000
step_part = 1000

max_size = 400
min_size = max_size - 400
max_size = max_size + 500
step_size = 50

mid_rand = 0.435
min_rand = mid_rand - 0.1
max_rand = mid_rand + 0.1
step_rand = 0.01

mid_rand_z = 0.75
min_rand_z = mid_rand_z - 0.5
max_rand_z = mid_rand_z + 0.5
step_rand_z = 0.1

BIG_NUMBER = 100000000
min_distance_global = BIG_NUMBER
min_spectrum_global = []
min_call_global = []
best_vars_global = []

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

    #print ""
    os.system(generation_call)
    global real_spectrum
    distance, min_spectrum, real_spectrum = test_comparison.compare(real_spectrum)
    print "Distance real - synthetic : ", distance

    if(distance < min_distance):
        min_distance = distance
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

            varss[var_i] += ((0.5 + random.uniform(0,1)) * steps[var_i]) * sign

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
    #print args_call
    min_distance_ret, min_spectrum1, min_call1, change = compare(it, part, size, rand, rand_z, min_distance)

    sign = 1
    if(direction <= 0):
        sign = -1

    min_distance, min_spectrum, min_call, best_vars = go_direction(sign, varss, var_i, min_distance_ret)
    # see if the other direction is better

    if min_distance_ret < min_distance:
        min_distance = min_distance_ret
        min_spectrum = min_spectrum1
        min_call = min_call1
        best_vars = varss


    min_distance2, min_spectrum2, min_call2, best_vars2 = go_direction(-sign, varss, var_i, min_distance)

    if min_distance2 < min_distance:
        min_distance = min_distance2
        min_spectrum = min_spectrum2
        min_call = min_call2
        best_vars = best_vars2

    print "CURRENT INNER MINIMUM:"
    print min_distance
    print min_spectrum
    print min_call
    global min_distance_global
    print "(global: ", min_distance_global, " )"

    return min_distance, min_spectrum, min_call, best_vars


#print "Starting for..."

def brute_force():
    for it in range(min_it, max_it, step_it):
        for part in range(min_part, max_part, step_part):
            for size in range(min_size, max_size, step_size):
                for rand in np.arange(min_rand, max_rand, step_rand):
                    for rand_z in np.arange(min_rand_z, max_rand_z, step_rand_z):
                        min_distance, min_spectrum, min_call = compare(it, part, size, rand, rand_z, min_distance)

def follow_gradient_dumb():

    min_call = ""

    best_vars=[]


    while True:

      print "Generating random position..."

      # generate random position in hyperspace
      it = int(floor(random.uniform(min_it, max_it)))
      part = int(floor(random.uniform(min_part, max_part)))
      size = int(floor(random.uniform(min_size, max_size)))
      rand = random.uniform(min_rand, max_rand)
      rand_z = random.uniform(min_rand_z, max_rand_z)

      global min_distance_global
      min_distance, min_spectrum, min_call, _ = compare(it, part, size, rand, rand_z, BIG_NUMBER)

      # Generate a random position close to the last distance found
      while min_distance - min_distance_global > 0.1 and not(min_distance_global==BIG_NUMBER) :
          print "Generating random position..."

          it = int(floor(random.uniform(min_it, max_it)))
          part = int(floor(random.uniform(min_part, max_part)))
          size = int(floor(random.uniform(min_size, max_size)))
          rand = random.uniform(min_rand, max_rand)
          rand_z = random.uniform(min_rand_z, max_rand_z)

          min_distance, min_spectrum, min_call, _ = compare(it, part, size, rand, rand_z, BIG_NUMBER)
          print "Too high, recomputing... ", min_distance



      already_visited = np.zeros((5))

      # randomly choose one variable
      var_i = random.randint(0,4)

      min_distance, min_spectrum, min_call, best_vars = go_variable(var_i, it, part, size, rand, rand_z, min_distance)

      already_visited[var_i] = 1

      while(already_visited.sum() < 5):

          # randomly choose another variable
          var_i = random.randint(0,4)

          while already_visited[var_i] > 0:
              var_i = random.randint(0,4)

          print "Trying another variable... ", var_i

          min_distance2, min_spectrum2, min_call2, best_vars2 = go_variable(var_i, best_vars[0], best_vars[1], best_vars[2], best_vars[3], best_vars[4], min_distance)

          already_visited[var_i] = 1
          print "Already visited: ", already_visited


          if min_distance2 < min_distance:
              min_distance = min_distance2
              min_spectrum = min_spectrum2
              min_call = min_call2
              best_vars = best_vars2

              # start over
              already_visited = np.zeros((5))
              print "Re starting counters"


      if min_distance < min_distance_global:
        min_distance_global = min_distance
        min_spectrum_global = min_spectrum
        min_call_global = min_call
        best_vars_global = best_vars

      print "CURRENT GLOBAL MINIMUM:"
      print min_distance_global
      print min_spectrum_global
      print min_call_global
      print best_vars_global
      print ""
    
    return min_distance_global, min_spectrum_global, min_call_global, best_vars_global




min_distance, min_spectrum, min_call, best_vars = follow_gradient_dumb()
print "..............Result............. "
print "MINIMUM:"
print min_distance
print "SYNTH:" , min_spectrum
print min_call
print best_vars
