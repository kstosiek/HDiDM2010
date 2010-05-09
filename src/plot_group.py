import tempfile
import utils
import sys
import os

def generate_gnuplot_command(files_list):
	if not files_list:
		return ''
	colours_str = """
	blue red gold green navyblue violet salmon
	#87CEEB #8B008B #FFA07A #00FF00 #800000 #808000 #4169E1 #708090 
	"""
	colours = colours_str.split()
	plots_colours = zip(files_list, colours)
	plots = [ '"%s" lt rgb "%s" with lines'%pair for pair in plots_colours]
	return 'plot %s\n' % ', '.join(plots)

def detect_cluster_number(clusters_file_path):
	n = 0
	for line in open(clusters_file_path):
		line = line.strip()
		if(line.isdigit()):
			tmp_n = int(line)
			if tmp_n > n:
				n = tmp_n
	return n+1

def plot_single_cluster(clusters_file_path, cluster_number):
	clusters_file = open(clusters_file_path, "r")	

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
	clusters_file.close()
	return found_cluster, plot_data_tmpfile_path


if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: python plot_group.py <clusters file> <cluster number>"
		print "Usage: python plot_group.py <clusters file> all"
		sys.exit(1)
	

	# Parse command line arguments.

	err_msg = ""
	all_clusters = False

	try:
		clusters_file_path = sys.argv[1]
		clusters_file = open(clusters_file_path, "r")	
		clusters_file.close()
		if(sys.argv[2] == "all"):
			all_clusters = True
		else:
			cluster_number = int(sys.argv[2])
	except ValueError:	
		err_msg = "error: wrong cluster number"
	except IOError:
		err_msg = "error: couldn't open file with clusters"
	
	# If error message is not empty print it and exit.
	
	if err_msg != "":
		print err_msg
		sys.exit(1)

	# Parse stock data.

	data = utils.parse_data("../data/notowania.txt")

	found_cluster = False
	plot_tmpfiles = []
	if all_clusters:
		cluster_number = detect_cluster_number(clusters_file_path)
		for i in range(cluster_number):
			_, plot_data = plot_single_cluster(clusters_file_path, i)
			plot_tmpfiles.append(plot_data)
	else:
		found_cluster, plot_data_tmpfile_path = plot_single_cluster(clusters_file_path, cluster_number)
	
	if found_cluster:

		# Generate file with commands for gnuplot.

		gnuplot_commands_tmpfile_path = tempfile.mkstemp()[1]
		gnuplot_commands_tmpfile = open(gnuplot_commands_tmpfile_path, "r+")
		gnuplot_commands_tmpfile.write("plot '" + plot_data_tmpfile_path +
				"'  with lines \n")
		gnuplot_commands_tmpfile.write("pause mouse any")
		gnuplot_commands_tmpfile.close()

		print "Click in the plot to exit... (hit Ctrl-C if hangs)"

		print gnuplot_commands_tmpfile_path
		os.system("gnuplot " + gnuplot_commands_tmpfile_path)

		gnuplot_commands_tmpfile.close()
		os.remove(gnuplot_commands_tmpfile_path)
	
		os.remove(plot_data_tmpfile_path)
	elif all_clusters:
		plot_cmd = generate_gnuplot_command(plot_tmpfiles)
		#print plot_cmd

		gnuplot_commands_tmpfile_path = tempfile.mkstemp()[1]
		gnuplot_commands_tmpfile = open(gnuplot_commands_tmpfile_path, "r+")
		gnuplot_commands_tmpfile.write(plot_cmd)
		gnuplot_commands_tmpfile.write("pause mouse any")
		gnuplot_commands_tmpfile.close()
		print "Click in the plot to exit... (hit Ctrl-C if hangs)"
		print gnuplot_commands_tmpfile_path
		os.system("gnuplot " + gnuplot_commands_tmpfile_path)
		gnuplot_commands_tmpfile.close()
		os.remove(gnuplot_commands_tmpfile_path)
		for tmpfile_path in plot_tmpfiles:
			os.remove(tmpfile_path)
	else:
		print "No group with this number."
	
