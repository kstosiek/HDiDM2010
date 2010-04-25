import tempfile
import utils
import sys
import os

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: python plot_group.py <clusters file> <cluster number>"
		sys.exit(1)

	clusters_file_path = sys.argv[1]
	clusters_file = open(clusters_file_path, "r")	

	cluster_number = int(sys.argv[2])

	# Parse stock data.

	data = utils.parse_data("../data/notowania.txt")

	# Create temporary file for plot data.

	plot_data_tmpfile_path = tempfile.mkstemp()[1]
	plot_data_tmpfile = open(plot_data_tmpfile_path, "w")

	found_cluster = False

	line = clusters_file.readline().strip()
	while line != "":

		# Check if we've found our group.

		if line.isdigit() == True and int(line) == cluster_number:
			
			found_cluster = True

			# Extract company names and write their prices vectors
			# to temporary data file in gnuplot format.

			company_name = clusters_file.readline().strip()
			while not company_name.isdigit() and company_name != "":
				vec = utils.make_prices_vec_by_company(data, company_name)
				for elem in vec:
					plot_data_tmpfile.write(str(elem))
					plot_data_tmpfile.write("\n")
				plot_data_tmpfile.write("\n\n")
				company_name = clusters_file.readline().strip()

		line = clusters_file.readline().strip()
	
	if found_cluster:

		# Plot with gnuplot.

		gnuplot_commands_tmpfile_path = tempfile.mkstemp()[1]	
		gnuplot_commands_tmpfile = open(gnuplot_commands_tmpfile_path, "r+")
		gnuplot_commands_tmpfile.write("plot '" + plot_data_tmpfile_path +
				"' with lines\n")
		gnuplot_commands_tmpfile.write("pause mouse any")
		gnuplot_commands_tmpfile.close()

		print "Click in the plot to exit... (hit Ctrl-C if hangs)"

		os.system("gnuplot " + gnuplot_commands_tmpfile_path)

		gnuplot_commands_tmpfile.close()
		os.remove(gnuplot_commands_tmpfile_path)
	
	else:
		print "No group with this number"
	
	# Cleanup.
	
	plot_data_tmpfile.close()
	os.remove(plot_data_tmpfile_path)
	clusters_file.close()
