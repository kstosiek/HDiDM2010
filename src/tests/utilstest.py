"""Unit test for utils.py"""

import utils 
import unittest

class UtilityFunctions(unittest.TestCase):

	test_file_path1 = "data/input1.txt"
	data1 = []
	
	test_file_path2 = "data/input2.txt"
	data2 = []

	def setUp(self):
		self.data1 = utils.parse_data(self.test_file_path1)
		self.data2 = utils.parse_data(self.test_file_path2)

        def testWeeklyCompression(self):
		"""Testing whether weekly compression works"""
		test_data = [
			["Company1", { 20091101: 1, 20091102: 2, 20091103: 3, 20091104: 4, 20091105: 5}],
			["Company2", { 20091101: 1, 20091102: 1, 20091103: 1, 20091104: 1, 20091105: 1}]
		]

		expected_result = [
			["Company1", { 20091101: 3}],
			["Company2", { 20091101: 1}]
		]

	        
		actual_result = utils.compress_data_weekly(test_data)
		self.assertEqual(actual_result, expected_result)

	def testParsingProperData(self):
		"""Parsing proper data."""

		self.assertEqual(self.data1[0][0], "AMBRA")
		self.assertEqual(self.data1[1][0], "TVN")
		
		dict_ambra = self.data1[0][1]

		self.assertEqual(dict_ambra[20100416], 20.5)
		self.assertEqual(dict_ambra[20100414], 10.5)
		self.assertEqual(dict_ambra[20100413], 9)
		self.assertEqual(dict_ambra[20100412], 9.5)

		dict_tvn = self.data1[1][1]

		self.assertEqual(dict_tvn[20100416], 18.5)
		self.assertEqual(dict_tvn[20100414], 17.5)
		self.assertEqual(dict_tvn[20100413], 16.5)
		self.assertEqual(dict_tvn[20100412], 9.5)
	
	def testGetPricesVecs(self):
		"""Obtaining list of prices vectors."""

		vecs = utils.make_prices_vecs(self.data1)
		self.assertEqual(vecs, [[9.5, 9, 10.5, 20.5], [9.5, 16.5, 17.5, 18.5]])
	
	def testMakeGroupsFromLabels(self):
		"""Test if we group right."""

		# FIXME: This can be done somewhat better by checking if 
		# each partition has ALL necessary elements and if elements 
		# between each group in partition are DISTINCT. 

		labels1 = [0, 1, 0, 0, 1, 1]

		groups = utils.make_groups_from_labels(labels1, self.data2)
		self.assertEqual(groups, {0: ["A1", "A3", "A4"], 1: ["A2", "A5", "A6"]})

		labels2 = [1, 2, 3, 0, 1, 2]

		groups = utils.make_groups_from_labels(labels2, self.data2)
		self.assertEqual(groups, {0: ["A4"], 1: ["A1", "A5"], 2: ["A2", "A6"],
				3: ["A3"]})

		labels3 = [0, 1, 2, 3, 4, 5]

		groups = utils.make_groups_from_labels(labels3, self.data2)
		self.assertEqual(groups, {0: ["A1"], 1: ["A2"], 2: ["A3"],
				3: ["A4"], 4: ["A5"], 5: ["A6"]})
	
	def testMakePricesVecByCompany(self):
		"""Obtaining prices vector by company name."""

		ambra_prices_vec = utils.make_prices_vec_by_company(self.data1, "AMBRA")		
		self.assertEqual(ambra_prices_vec, [9.5, 9, 10.5, 20.5])

		tvn_prices_vec = utils.make_prices_vec_by_company(self.data1, "TVN")		
		self.assertEqual(tvn_prices_vec, [9.5, 16.5, 17.5, 18.5])
	
	def testMakePricesDifferencesVectors(self):

		diff_vecs = utils.make_prices_diffs_vecs(self.data1)
		self.assertEqual(diff_vecs, [[-0.5, 1.5, 10.0], [7.0, 1.0, 1.0]])

		data3 = [["A", {0: 1, 1: 1}], ["B", {0: 1, 1: 1}]]
		diff_vecs = utils.make_prices_diffs_vecs(data3)
		self.assertEqual(diff_vecs, [[0], [0]])


if __name__ == "__main__":
	unittest.main()
