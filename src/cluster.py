import Pycluster
import eventutils
import utils
import sys
import getopt

def print_usage_and_exit():
	print "Usage: python cluster.py <input file> [OPTIONS]"
	print "  -h, --help"
	print "  -o, --output <path>        (default: ./output_clusters)"
	print "  -c, --clusters-num <num>   (default: 10)"
	print "  -i, --iters-num <num>      (default: 100)"
	print "  -d, --distance <char>      (default: e)"
	print "  -m, --method <char>        (default: a)"
	print "  -D, --differential         (default: false)"
	print "  -w, --weekly-data          (default: false)"
	print "  -e, --events               (default: <none>; possible values: ceop)"
	print "  -t, --trim                 (default: 0)"
	print "  -x, --xgrid                (default: 3, for selforgmaps)"
	print "  -y, --ygrid                (default: 3, for selforgmaps)"
 	print "  --kmeans                   (default: true)"
	print "  --hierarchical             (default: false)"
	print "  --selforgmaps              (default: false)"
	sys.exit(0)

if __name__ == "__main__":

	# Parse command line arguments.

	if len(sys.argv) < 2:
		print_usage_and_exit()

	input_file_path = sys.argv[1]

	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], "hc:o:i:d:m:Dwe:t:x:y:",
				["help", "output=", "clusters-num=", "iters-num=",
				 "dist=", "method=", "differential", "weekly-data", 
				 "hierarchical", "kmeans", "selforgmaps", "events",
				 "trim", "xgrid=", "ygrid="])
	except getopt.GetoptError, err:
		sys.exit(err)

	# Default values.

	output_file_path = "output_clusters"
	number_of_clusters = 10
	number_of_iters = 100

	# If you want to experiment with different distance measures
	# and methods it's crucial to read pycluster documentation,
	# because depeneding on the algorithm these characters have
	# different meaning.

	dist_measure = 'e'
	dist_method = 'a'

	class ClusterAlg:
		KMEANS=1
		HIERARCHICAL=2
		SELFORGMAPS=3

	algorithm_type = ClusterAlg.KMEANS

	treat_data_differentially = False
	compress_to_weekly_data = False

	# Different events can be imported here to be matched against
	# prices on the plot.

	import_catastrophic_events = False
	import_political_events = False
	import_economical_events = False
	import_other_events = False

	# Indicates whether the data should be trimmed to nearest dates
	# surrounding imported events and - if so - tells what is the size 
	# of the neighbourhood.

	trimming_range = 0

	# Self-organizing maps (SOM) idea is around rectangular grid of points. 
	# We choose the size of this grid by defining its x (xgrid) and y 
	# (ygrid) sizes. In SOM number of clusters is equal to number of points
	# on such a grid that is x * y. Each of our vector is mapped on some
	# point and that is generally how SOM works. Each vector is assigned to
	# some point.

	xgrid = 3
	ygrid = 3

	for option, arg in opts:
		if option in ("-h", "--help"):
			print_usage_and_exit()
		elif option in ("-o", "--output"):
			output_file_path = arg
		elif option in ("-c", "--clusters-num"):
			number_of_clusters = int(arg)
		elif option in ("-i", "--iters-num"):
			number_of_iters = int(arg)
		elif option in ("-d", "--distance"):
			dist_measure = arg
		elif option in ("-m", "--method"):
			dist_method = arg
		elif option in ("-D", "--differential"):
			treat_data_differentially = True
		elif option in ("-w", "--weekly-data"):
			compress_to_weekly_data = True                        
		elif option in ("--kmeans"):
			algorithm_type = ClusterAlg.KMEANS
		elif option in ("--hierarchical"):
			algorithm_type = ClusterAlg.HIERARCHICAL
		elif option in ("--selforgmaps"):
			algorithm_type = ClusterAlg.SELFORGMAPS
   		elif option in ("-e", "--events"):
			for value in arg:
				if value == 'c':
					import_catastrophic_events = True
				elif value == 'e':
					import_economical_events = True
				elif value == 'o':
					import_other_events = True
				elif value == 'p':
					import_political_events = True
		elif option in ("-t", "--trim"):
			if arg > 0: trimming_range = int(arg)			
		elif option in ("-x", "--xgrid"):
			xgrid = int(arg)
		elif option in ("-y", "--ygrid"):
			ygrid = int(arg)

	print "Number of clusters:", number_of_clusters
	print "Output file:", output_file_path
	print "Number of iterations:", number_of_iters
	print "Distance measure:", dist_measure
	print "Distance method:", dist_method
	print "Data treated as differential:", treat_data_differentially
	print "Data compressed to weekly data:", compress_to_weekly_data

	print "Events included:"
	if not (import_catastrophic_events
		or import_economical_events
		or import_other_events
		or import_political_events):
		print "\tNone"
	else:
		if import_catastrophic_events: print "\t -catastrophic"
		if import_economical_events: print "\t -economical"
		if import_other_events: print "\t -other"
		if import_political_events: print "\t -political"

	print "Data trimming:",
	if trimming_range > 0:
		print trimming_range 
	else: 
		print "no trimming"

	print "Algorithm type:",
	if algorithm_type == ClusterAlg.KMEANS:
		print "kmeans"
	elif algorithm_type == ClusterAlg.HIERARCHICAL:
		print "hierarchical"
	elif algorithm_type == ClusterAlg.SELFORGMAPS:
		print "selforgmaps"
		print "Number of points in SOM grid (xgrid * ygrid):", xgrid * ygrid

	# Parse input data.

	try:
		data = utils.parse_data(input_file_path)
	except IOError, err:
		sys.exit(err)

	# Import requested events.
 	# TODO(karol): this may have to be moved from here to the plotting
	# file.

	try:
		events = { }
		if import_catastrophic_events:
			catastrophic_events = eventutils.import_events(
					"../data/wydarzenia-katastrofy-polska.txt")
			events[catastrophic_events[0]] = catastrophic_events[1]
		if import_economical_events:
			economical_events = eventutils.import_events(
					"../data/wydarzenia-ekonomiczne-polska.txt")
			events[economical_events[0]] = economical_events[1]
		if import_other_events:
			other_events = eventutils.import_events(
					"../data/wydarzenia-inne-polska.txt")
			events[other_events[0]] = other_events[1]
		if import_political_events:
			political_events = eventutils.import_events(
					"../data/wydarzenia-polityczne-polska.txt")
			events[political_events[0]] = political_events[1]
	except IOError, err:
		sys.exit(err)

	# TODO(patryk): plot events.

	# Preprocessing phase.

	if compress_to_weekly_data:
		data = utils.compress_data_weekly(data)		

	if trimming_range > 0:
		data = eventutils.trim_data_to_events(data, events, trimming_range)

	input_vecs = []
	if treat_data_differentially:
		input_vecs = utils.make_prices_diffs_vecs(data)
	else:
		input_vecs = utils.make_prices_vecs(data)

	# Run clustering algorithm.

	if algorithm_type == ClusterAlg.KMEANS:
		labels, wcss, n = Pycluster.kcluster(input_vecs, number_of_clusters, 
				dist = dist_measure, npass = number_of_iters, 
				method = dist_method)
	elif algorithm_type == ClusterAlg.HIERARCHICAL:
		tree = Pycluster.treecluster(input_vecs, method = dist_method,
				dist = dist_method)
		labels = tree.cut(number_of_clusters)
	elif algorithm_type == ClusterAlg.SELFORGMAPS:
		labels, celldata = Pycluster.somcluster(input_vecs, nxgrid = xgrid, 
				nygrid = ygrid, niter = number_of_iters)

	# If algorithm is self-organizing maps each item is assigned to
	# a particular 2D point, so we need to create groups from 2D points.
	# See implementation of making groups from labels for details.

	if algorithm_type == ClusterAlg.SELFORGMAPS:
		clusters = utils.make_groups_from_labels(labels, data, True)
	else:
		clusters = utils.make_groups_from_labels(labels, data)

	# Check with which type of key we have to deal with.
	# Any better idea how to check if object is a pair? :)

	keys_are_2D_points = True
	sample_key = clusters.keys()[0]
	try:
		a, b = sample_key
	except TypeError:
		keys_are_2D_points = False	

	# Print output to file.

	idx = 0
	output_file = open(output_file_path, 'w')
	for key, val in clusters.iteritems():
		if keys_are_2D_points:
			output_file.write(str(idx) + "\n")
			idx = idx + 1
		else:
			output_file.write(str(key) + "\n")
		map(lambda name: output_file.write(name + "\n"), val)
	
	output_file.close()
