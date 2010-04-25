import Pycluster
import utils
import sys

if __name__ == "__main__":

	# FIXME: Add other arguments e.g. number of iterations, distance etc.

	if len(sys.argv) != 3:
		print "Usage: python kmenas.py <num of clusters> <output>"
		sys.exit(1)

	number_of_clusters = int(sys.argv[1])
	output_file_path = sys.argv[2]

	# Prepare data.

	data = utils.parse_data("../data/notowania.txt")
	price_vecs = utils.make_prices_vecs(data)

	# Run K-means.

	labels, wcss, n = Pycluster.kcluster(price_vecs, number_of_clusters, 
			dist = 'e', npass = 500, method = 'a')
	
	# Print output to file.

	clusters = utils.make_groups_from_labels(labels, data)
	output_file = open(output_file_path, 'w')

	for key, val in clusters.iteritems():
		output_file.write(str(key))
		output_file.write("\n")
		for company_name in val:
			output_file.write(company_name)
			output_file.write("\n")
	
	output_file.close()
