"""Unit tests for clustering with our utils."""

import Pycluster
import utils 
import unittest

class Clustering(unittest.TestCase):

	def setUp(self):

		# Result for these data are somewhat deterministic. Expected 
		# groups are obvious {0: ['E'], 1: ['A', 'D'], 2: ['B', 'C']}.
		# Why? E growth is equal to 5, A and D growth is equal and
		# equals 0, B and C growth is also equal and equals 1.

		self.data1 = [
			["A", {0: 0, 1: 0}], 
			["B", {0: 5, 1: 6}], 
			["C", {0: 7, 1: 8}], 
			["D", {0: 9, 1: 9}], 
			["E", {0: 10, 1: 15}]
		]

	def testPricesDiffsVecsKmeansClustering(self):
		"""Testing whether kmeans clustering with prices differences
		   vectors works."""

		prices_diffs_vecs = utils.make_prices_diffs_vecs(self.data1)		
		labels, wcss, n = Pycluster.kcluster(prices_diffs_vecs, 3, npass=100)
		clusters = utils.make_groups_from_labels(labels, self.data1)

		# The result should be sth like this modulo group numbers. Probability
		# that this isn't like this with npass=100 is (I think) very low! But
		# it can happen that this grouping will be different.

		suggested_clusters = {0: ['E'], 1: ['A', 'D'], 2: ['B', 'C']}

		# Let's check this.

		num_matches = 0

		for cluster in clusters.values():
			cluster.sort()
			for suggested_cluster in suggested_clusters.values():
				suggested_cluster.sort()
				if cluster == suggested_cluster:
					num_matches = num_matches + 1

		# Ok, so we've found out that each suggested cluster exists
		# in output of our kcluster algorithm and because length of
		# clusters dict is 3 we can be sure these dictionaries are equal.

		self.assertEqual(num_matches, 3)
		self.assertEqual(len(clusters), 3)

if __name__ == "__main__":
	unittest.main()
