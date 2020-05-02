

The path generated goes "Red" to "Green" to "Yellow" on the configuration space. Close the config space to start the sim.

You might see at the start that there's some strange behavior. This is because of the joint limits on 
the first joint being between 0 and pi, meaning that we always choose the positive "elbow down" configuration.
Since the arm doesn't start in the simulation at theta1 = 0, theta2 = 0, there's a lot of flailing as it tries 
to properly set itself up in the first couple of steps. These iron out as it moves.

After it hits a waypoint, it accepts an input from your keyboard before going to the next point. This is so you can 
see where the point ends up after it's done.

