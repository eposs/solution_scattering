""" This part of the package is for loading data of various types and then 
making traces.

Benjamin Barad
"""
from numpy import recarray, load
from trace import Trace

# Q = [0.0175 + 0.0025 * i for i in range(2125)]
# print Q

def parse(filename, mode="tpkl"):
	"""Wrapper function for any loader functions that I may write besides 
	tpkl. Just passes through to the appropriate place based on the `mode` 
	variable."""
	if mode == "tpkl":
		return parse_tpkl(filename)

def parse_tpkl(filename):
	"""Loads tpkl files and generates a corresponding Trace object. Requires
	table.py from the Anfinrud lab, which we will not distribute.
	"""
	try:
		from table import table
	except ImportError:
		print """You do not have the required code accessible to parse tpkl
		files. Try using a different file format for input"""
		raise
	data = load(filename)
	q = data.q
	sigS = data.sigS
	S = data.S
	sigSA = data.sigSA
	SA = data.SA
	Nj = data.Nj
	return Trace(q, sigS, S, sigSA, SA, Nj)

def alg_scale(ref, var):
	SA_ref = ref.SA
	SA_var = var.SA
	# q = SA_ref.q
	# print q
	# return SA_var
	# top = sum([SA_ref[i]*Q[i]*SA_var[i]*Q[i] for i in range(len(SA_ref))])
	top = sum([SA_ref[i]*ref.q[i]*SA_var[i]*ref.q[i] for i in range(1792,2073)])
	# bottom = sum([(SA_var[i]*Q[i])**2 for i in range(len(SA_var))])
	bottom = sum([(SA_var[i]*ref.q[i])**2 for i in range(1792, 2073)]) # 552,633
	scalar = top/bottom
	print "scalar: ", scalar
	SA_adjusted = [i*scalar for i in SA_var]
	sig_SA_adjusted = [i*scalar for i in var.sigSA]
	return SA_adjusted, sig_SA_adjusted

# Little stub for testing
if __name__ == "__main__":
	from sys import argv
	filename = argv[1]
	trace = parse_tpkl(filename)
	print trace