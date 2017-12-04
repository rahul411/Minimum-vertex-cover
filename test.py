import sys
import os
import argparse
# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--inst", "-inst", help="set output width")
parser.add_argument("--alg", "-alg", help="set output width")
parser.add_argument("--time", "-time", help="set output width")
parser.add_argument("--seed", "-seed", help="set output width")

# read arguments from the command line
args = parser.parse_args()

# check for --width
if args.inst:  
	fileName = args.inst
if args.alg:  
	algorithm = args.alg
if args.time:  
	cutoff = args.time
if args.seed:  
	seed = args.seed



if algorithm == 'BnB':
	os.system('python MVC_BnB.py '+fileName+' '+ cutoff)
