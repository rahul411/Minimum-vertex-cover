import sys
import os
import argparse
import MVC_BnB as BnB
import LS1 as ls1
import LS2 as ls2
import approx as appro
# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--inst", "-inst", help="set output width")
parser.add_argument("--alg", "-alg", help="set output width")
parser.add_argument("--time", "-time", help="set output width")
parser.add_argument("--seed", "-seed", help="set output width")

# read arguments from the command line
args = parser.parse_args()

if args.inst:  
	fileName = args.inst
if args.alg:  
	algorithm = args.alg
if args.time:  
	cutoff = args.time
if args.seed:  
	seed = args.seed



if algorithm == 'BnB':
	# os.system('python MVC_BnB.py '+fileName+' '+ cutoff)
	BnB.BNB(fileName,cutoff)
	

if algorithm == 'LS1':
	# os.system('python LS1.py '+fileName+' '+ cutoff+' '+seed)
	ls1.mvc_ls1(fileName,cutoff,seed)

if algorithm == 'LS2':
	# os.system('python LS2.py '+fileName+' '+ cutoff+' '+seed)
	ls2.mvc_ls2(fileName,cutoff,seed)

if algorithm == 'approx':
	# os.system('python approx.py '+fileName)
	appro.test_and_run(fileName)
