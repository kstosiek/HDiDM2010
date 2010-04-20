import Pycluster

if __name__ == "__main__":
	
	# Define a set of 3d vectors.
	
	points = [[1, 1, 0], [0, 0, 1], [5, 5, 6], [6, 6, 5]]

	# Cluster them with euclide distance using arithmetic means.
	# Run clustering algorithm 100 times. Divide into 2 groups.

	labels, wcss, n = Pycluster.kcluster(points, 2, 
			dist = 'e', npass = 100, method = 'a')

	print "Labels ", labels

	# Within cluster sum of squares (???).

	print "WCSS ", wcss

	# How many times optimal solution was found (???).

	print "Opt found ", n, " times" 
