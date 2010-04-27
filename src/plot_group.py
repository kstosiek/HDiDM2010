import tempfile
import utils
import sys
import os

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: python plot_group.py <clusters file> <cluster number>"
		sys.exit(1)

	# Parse command line arguments.

	clusters_file_path = sys.argv[1]
	clusters_file = open(clusters_file_path, "r")	
	cluster_number = int(sys.argv[2])

	# Parse stock data.

	data = utils.parse_data("../data/notowania.txt")

	# Create temporary file for plot data.

	plot_data_tmpfile_path = tempfile.mkstemp()[1]
	plot_data_tmpfile = open(plot_data_tmpfile_path, "w")

	# Start searching for cluster we want to plot in file
	# with clusters.

	found_cluster = False

	line = clusters_file.readline().strip()
	while line != "":

		if line.isdigit() == True and int(line) == cluster_number:

			found_cluster = True

			# Ok, we've found our cluster. Now we iterate companies in
			# this group and write their prices vectors seperated by two
			# blank lines to one file (used as input for gnuplot).

			company_name = clusters_file.readline().strip()
			while not company_name.isdigit() and company_name != "":

				vec = utils.make_prices_vec_by_company(data, company_name)
				map(lambda p: plot_data_tmpfile.write(str(p) + "\n"), vec)
				plot_data_tmpfile.write("\n\n")
				company_name = clusters_file.readline().strip()

			# Great, we're done, we wanted data for only one cluster,
			# so break here.

			break

		line = clusters_file.readline().strip()
	
	# Close this file here, we'll need file buffers to be flushed for this
	# file before running gnuplot.

	plot_data_tmpfile.close()
	
	if found_cluster:

		# Generate file with commands for gnuplot.

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

		print "No group with this number."
	
	os.remove(plot_data_tmpfile_path)
	clusters_file.close()
