import Pycluster
import utils
import sys
import getopt

if __name__ == "__main__":

	# Parse command line arguments.

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hc:o:i:d:D", 
				["help", "output=", "clusters-num=", "iters-num=", 
				 "dist="])
	except getopt.GetoptError, err:
		print str(err)
		sys.exit(2)

	# Default values.

	output_file_path = "output_kmeans"
	number_of_clusters = 10
	number_of_iters = 100
	dist_measure = 'e'
        treat_data_differentially = False

	for option, arg in opts:
		if option in ("-h", "--help"):
			print "Usage: python kmeans.py [OPCJE]\n"
			print "  -h, --help"
			print "  -o, --output <path>        (default: ./output)"
			print "  -c, --clusters-num <num>   (default: 10)"
			print "  -i, --iters-num <num>      (default: 100)"
			print "  -d, --distance <char>      (default: e)"
			print "  -D, --differential         (default: true)"
                        sys.exit(1)
		elif option in ("-o", "--output"):
			output_file_path = arg
		elif option in ("-c", "--clusters-num"):
			number_of_clusters = int(arg)
		elif option in ("-i", "--iters-num"):
			number_of_iters = int(arg)
		elif option in ("-d", "--distance"):
			dist_measure = arg
                elif option in ("-D", "--differentially"):
                        treat_data_differentially = True;
                        
			
	print "Number of clusters is ", number_of_clusters
	print "Output file is ", output_file_path
	print "Number of iterations is ", number_of_iters
	print "Distance measure is ", dist_measure
        print "Data treated as differential: ", treat_data_differentially

	# Prepare data. I'm not giving possibilty of defining
	# different input data file via command line, I think 
	# there's no need for it now.

	data = utils.parse_data("../data/notowania.txt")
      
        price_vecs = []
        if (treat_data_differentially):
		price_vecs = utils.make_prices_diffs_vecs(data)
        else:
		price_vecs = utils.make_prices_vecs(data)

	# FIXME: Place for vector preprocessing is somewhere here eg.
	# computing prices differences vector.

	# Run K-means.

	labels, wcss, n = Pycluster.kcluster(price_vecs, number_of_clusters, 
			dist = dist_measure, npass = number_of_iters, method = 'a')
	clusters = utils.make_groups_from_labels(labels, data)

	# Print output to file.

	output_file = open(output_file_path, 'w')
	for key, val in clusters.iteritems():
		output_file.write(str(key) + "\n")
		map(lambda name: output_file.write(name + "\n"), val)
	
	output_file.close()
