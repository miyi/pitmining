# pitmining

Toy pit-mining problem.  Currently, we have two sets of constraints:

  1. For a block to be dug, the block immediately above, as well as above and
  left, and above and right, must also be dug.
  2. We can only dig a fixed number of blocks.

Quality of dirt is completely random valued, on the range [0,1).  To run the
program, you'll need python3 with PuLP installed.  Run it like:

    ./pitmining.py <width> <num_holes>

Where `width` is the width of the 2-D scene, and `num_holes` is the number of
holes that can be dug out.
