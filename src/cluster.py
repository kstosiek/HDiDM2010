import Pycluster
import utils
import sys
import getopt

def print_usage_and_exit():
	print "Usage: python cluster.py <input file> [OPTIONS]\n"
	print "  -h, --help"
	print "  -o, --output <path>        (default: ./output_clusters)"
	print "  -c, --clusters-num <num>   (default: 10)"
	print "  -i, --iters-num <num>      (default: 100)"
	print "  -d, --distance <char>      (default: e)"
	print "  -m, --method <char>      	(default: a)"
	print "  -D, --differential         (default: false)"
	print "  -w, --weekly-data          (default: false)"
	print "  --kmeans          			(default: true)"
	print "  --hierarchical          	(default: false)"
	print "  --selforgmaps          	(default: false)"
	sys.exit(0)

if __name__ == "__main__":

	# Parse command line arguments.

	if len(sys.argv) < 2:
		print_usage_and_exit()

	input_file_path = sys.argv[1]

	try:
		opts, args = getopt.getopt(sys.argv[2:], "hc:o:i:d:m:Dw",
				["help", "output=", "clusters-num=", "iters-num=",
				 "dist=", "method=", "differential", "weekly-data", 
				 "hierarchical", "kmeans", "selforgmaps"])
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

	print "Number of clusters:", number_of_clusters
	print "Output file:", output_file_path
	print "Number of iterations:", number_of_iters
	print "Distance measure:", dist_measure
	print "Distance method:", dist_method
	print "Data treated as differential:", treat_data_differentially
	print "Data compressed to weekly data:", compress_to_weekly_data

	print "Algorithm type:",
	if algorithm_type == ClusterAlg.KMEANS:
		print "kmeans"
	elif algorithm_type == ClusterAlg.HIERARCHICAL:
		print "hierarchical"
	elif algorithm_type == ClusterAlg.SELFORGMAPS:
		print "selforgmaps"

	# Parse input data.

	try:
		data = utils.parse_data(input_file_path)
	except IOError, err:
		sys.exit(err)

	# Preprocessing phase.

	if compress_to_weekly_data:
		data = utils.compress_data_weekly(data)		

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
		# FIXME
		print "selforgmaps"
		labels = []

	clusters = utils.make_groups_from_labels(labels, data)

	# Print output to file.

	output_file = open(output_file_path, 'w')
	for key, val in clusters.iteritems():
		output_file.write(str(key) + "\n")
		map(lambda name: output_file.write(name + "\n"), val)
	
	output_file.close()
