import sys

def parse_data(file_path):
	file = open(file_path, 'r')

	output = []
	idx = 0

	for line in file:
		before, sep, after = line.partition(',')
		if sep == "" and after == "":
			company_name = before[0:-1]
			output.append([company_name.strip(), {}])
			idx = idx + 1
		else:
			date = before
			price = after[0:-1]
			company_date_price_dict = output[idx - 1][1]
			company_date_price_dict[int(date)] = float(price)
	
	file.close()
	
	return output

def make_prices_vec_by_company(data, company_name):
	"""Get prices vector for concrete company. Oldest records are at the
	begining of vector."""

	# Find stock prices for company company_name.

	elem = filter(lambda x: x[0].strip() == company_name.strip(), data)
	sorted_keys = elem[0][1].keys()
	sorted_keys.sort()

	date_price_dict = elem[0][1]

	return [date_price_dict[key] for key in sorted_keys]
	
def make_prices_vecs(data):
	"""Get price vectors. Oldest records are at the begining of 
	each vector."""

	output = []

	# We have the same set of dates (keys) for all companies,
	# so we have to sort keys only once (keys from whatever element).

	some_el = data[0]
	sorted_keys = some_el[1].keys()
	sorted_keys.sort()

	for elem in data:
		date_price_dict = elem[1]
		output.append([date_price_dict[key] for key in sorted_keys])
	
	return output;

def make_prices_diffs_vecs(data):
	"""Make vectors of prices differences."""

	output = []

	prices_vecs = make_prices_vecs(data)

	print "len(prices_vecs) = ", len(prices_vecs)

	vec_num = 0
	for price_vec in prices_vecs:
		output.append([])
		for idx in range(0, len(price_vec) - 1):
			output[vec_num].append(price_vec[idx + 1] - price_vec[idx])
		vec_num = vec_num + 1
	
	return output

def make_groups_from_labels(labels, data):
	"""Make list of clusters based on computed labels."""

	output = {}
	idx = 0
		
	for label in labels:
		if label not in output:
			output[label] = []

		output[label].append(data[idx][0])
		idx = idx + 1
	
	return output
