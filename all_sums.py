import itertools, math
from sys import argv
from functools import cache

# Goal
# ============================================
#
# Given an integer `n` and a step size `size`,
# find all combinations 
# of integers greater than or equal to `size`
# that sum to `n`, ignoring order. 
# 
# E.g. If n = 4 and step = 1, return
#      {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)} 
#
# Method
# ============================================
#
# Take n and find the set of pairs summing to it.
# For example, if n = 4 and step = 1,
# the pairs summing to 4 are:
#
#     {(3, 1), (2, 2)}
#
# Then, go through each number in each tuple in that set...
#
#     {(3, 1), (2, 2)}
#       ^
#     Start
#
# If the selected number is greater than 2 × step,
# get all the tuples that sum to it
# by using the method described here.
#
#                          Note: Recursion can feel like cheating,
#     {(3, 1), (2, 2)}     but notice that finding everything that sums to 3        
#       ^                  is easier than finding everything that sums to 4.
#      / \                 Finding everything that sums to 2 or 1 is trivial.
#  (2,1) (1,1,1)       <-- The problem gets easier on each nested reccurance
#                          until it no longer requires going down further.
#
# Then, for each resulting tuple,
# Find the tuple that results from
# replacing the originally selected number
# with the tuple that sums to it.
#
#
#     {(3, 1), (2, 2)}
#       ^
#      / \
#  (2,1) (1,1,1)
#    |      |
#    |   (1,1,1) replaces 3 in (3, 1)  = (1, 1, 1, 1)
#    |
#  (2,1) replaces 3 with (3, 1)        = (2, 1, 1)
#                                           /         
#                                          /          
# Then, take the resulting tuples         /
# and add them to the original set       /
#                                       /
#                      +++++++++++++++++++++++
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)}
#       ^              +++++++++++++++++++++++
#
# Then move to the next number and continue the process.
#
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)}
#          ^
#
# If the select number is less than 2 × step, just move on...
#
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)}
#               ^
#
# If the selected number is _equal to_ 2 × step,
# Get the tuple that results from replacing it
# with a tuple containing `n` elements of value `step`.
#
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)}
#               ^
#             (1,1)
#               |    Then replace the selected number 
#               |    with the resulting tuple
#            (1,1,2) 
#
# Then add it to the result set:
#                                               +++++++++
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1), (1, 1, 2)}
#               ^                               +++++++++
#
# Except actually, don't do that 
# if it's the same as a number already in the set,
# only in a different order.
#
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1), (1, 1, 2)}
#               ^      *********                *********
#
# Instead just move on.
#
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)}
#                  ^
# This is the same as before.
#
#
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)}
#                       ^          **********
# This results in (1, 1, 1, 1), which we already have.
#
#
#     {(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)}
#                          ^  ^    ^  ^  ^  ^
# And we can skip all of the 1s, so we're done.

def main():
	n    = int(argv[1]) if len(argv) > 1 else 10
	step = int(argv[2]) if len(argv) > 2 else 1

	for e in sorted(list(all_tuples_summing_to(n, step))):
		print(e)

@cache
def all_tuples_summing_to(n: int, step: int) -> set[tuple[int]]:
	"""
	>>> all_tuples_summing_to(5, 1)
	{(1, 1, 1, 1, 1), (1, 1, 1, 2), (1, 1, 3), (1, 2, 2), (1, 4), (2, 3)}
	"""
	                                           # e.g. n = 5, step = 1

	sum_tuples = all_pairs_summing_to(n, step) # e.g. {(1, 4), (2, 3)}

	for sum_tuple in sum_tuples:               # e.g.  (1, 4)
		for e in sum_tuple:                    # e.g.      4
			if e >= 2*step:
				# Take the sum tuple and replace e
				# with each tuple summing to e.

				sum_tuple_dropping_e = list(sum_tuple)
				del sum_tuple_dropping_e[sum_tuple_dropping_e.index(e)]
				sum_tuple_dropping_e = tuple(sum_tuple_dropping_e)
				# e.g. (1, 4) dropping 4 = (1)

				all_tuples_summing_to_e = (
					all_tuples_summing_to(e, step) if e > 2*step else

					# If e is less than 2 * step,
					# then only remaining combination is the one containing only `step`s.
					# For example, if step = 1 and e = 2,
					# then the only remaining combo is (1, 1).
					# This is the base case preventing infinite recursion.
					{tuple([step] * e)}  
				)
				# e.g. {(3, 1), (2, 2), (2, 1, 1)}

				for tuple_summing_to_e in all_tuples_summing_to_e: # e.g. (3, 1)
					 sum_tuples = sum_tuples.union({ tuple(sorted(
						  sum_tuple_dropping_e + tuple_summing_to_e
						  # e.g. (1) + (3, 1)
						  #  ... (1) + (2, 2)
						  #  ... (1) + (2, 1, 1)
					 )) })

	return sum_tuples 

@cache
def all_pairs_summing_to(n: int, step: int) -> set[tuple[int]]:
	"""
	>>> all_pairs_summing_to(5, 1)
	{(1, 4), (2, 3)}
	"""
	return set([
		tuple(sorted((i*step, n - (i*step))))
		for i in range(1, math.floor(n/step))
	])

main()
