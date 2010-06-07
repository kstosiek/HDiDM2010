import tempfile
import utils
import sys
import os

global event_file_path
event_file_path = '../data/wydarzenia-polityczne-polska.txt'

global set_xrange
set_xrange = ''

def shorten(s):
	if len(s) > 40:
		return s[:40]+'...'
	return s

def parse_date(s):
	date = s[-8:]
	year = int(date[:4])
	month = int(date[4:6])
	day = int(date[-2:])
	print year, "-", month, "-", day
	if year == 2009:
		day_no = ((month-1)*30+day) * (227./365)
	elif year == 2010:
		day_no = 227 + ((month-1)*30+day) * (145./365)
	return (day_no, "%s-%s" % (month,day))

def gen_labels(include_events):

	if not include_events:
		return ""

	labels = []
	days = []
	x = 10

	# Show grid.

	labels.append("set grid\n")
	labels.append("set xrange [0:]\n")
	labels.append("set yrange [0:]\n")

	# Don't show anything on x axis.

	#labels.append("set format x \"\"\n")

	for line in open(event_file_path):
		tokens = line.split(';')
		if(len(tokens) > 1):
			day, date = parse_date(tokens[0])
			days.append(day)
			labels.append("set label \"   %s (%s)\" at %f,0 rotate front\n" % (shorten(tokens[2].strip()), date, day))
			labels.append("set xtics add (%f)\n" % day)
			x += 20
	return '\n'.join(labels)


def generate_gnuplot_command(files_list, output_file, include_events):
	if not files_list:
		return ""
	colours_str = """
	blue red gold green navyblue violet salmon
	#87CEEB #8B008B #FFA07A #00FF00 #800000 #808000 #4169E1 #708090 
	"""
	colours = colours_str.split()
	plots_colours = zip(files_list, colours)
	plots = [ '"%s" lt rgb "%s" with lines'%pair for pair in plots_colours]
	cmd ="""
	set term gif size 1024, 768
	%s
	%s
	set output '%s.gif'
	plot %s
	""" % ( set_xrange, gen_labels(include_events), output_file, ', '.join(plots) )
	return cmd

def detect_clusters_count(clusters_file_path):
	'''Detect how many clusters are in clusters file.'''

	def aux(acc, x):
		if x.strip().isdigit() and int(x) > acc:
			return int(x)
		else:
			return acc
	
	return reduce(aux, open(clusters_file_path).readlines(), 0) + 1

def plot_single_cluster(clusters_file_path, cluster_number, average=False):
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

			if average:
				# We will now average price vectors from all
				# companies in this group.
				company_name = clusters_file.readline().strip()
				vec = utils.make_prices_vec_by_company(data, company_name)
				company_number = 1
				company_name = clusters_file.readline().strip()
				while not company_name.isdigit() and company_name != "":
					vec2 = utils.make_prices_vec_by_company(data, company_name)
					company_number += 1
					vec = [x+y for x,y in zip(vec,vec2)]
					company_name = clusters_file.readline().strip()
				vec = [ (x/company_number) for x in vec ]
				map(lambda p: plot_data_tmpfile.write(str(p) + "\n"), vec)
				plot_data_tmpfile.write("\n\n")

			else:
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

	if len(sys.argv) < 4:
		print "Usage: python plot_group.py <clusters file> <output file> <cluster number> "
		print "       python plot_group.py <clusters file> <output file> <cluster number> average"
		print "       python plot_group.py <clusters file> <output file> all"
		print "       python plot_group.py <clusters file> <output file> all average"
		sys.exit(1)
	

	# Parse command line arguments.

	err_msg = ""
	all_clusters = False
	average_plot = False

	try:
		clusters_file_path = sys.argv[1]
		clusters_file = open(clusters_file_path, "r")	
		clusters_file.close()
		output_file_path = sys.argv[2]
		if(sys.argv[3] == "all"):
			all_clusters = True
		else:
			cluster_number = int(sys.argv[3])
		if len(sys.argv)>4 and sys.argv[4]=="average":
			average_plot = True
	except ValueError:	
		err_msg = "error: wrong cluster number"
	except IOError:
		err_msg = "error: couldn't open file with clusters"

	include_events = False
	
	for arg in sys.argv:
		if arg.startswith('events:'):
			include_events = True
			event_paths = {}
			event_paths['polityczne'] = '../data/wydarzenia-polityczne-polska.txt'
			event_paths['katastrofy'] = '../data/wydarzenia-katastrofy-polska.txt'
			event_paths['ekonomiczne'] = '../data/wydarzenia-ekonomiczne-polska.txt'
			event_paths['inne'] = '../data/wydarzenia-inne-polska.txt'
			event_file_path = event_paths[arg[7:]]
		if arg.startswith('xrange:'):
			if arg[7:]:
				set_xrange = 'set xrange [%s]' % arg[7:]
	
	# If error message is not empty print it and exit.
	
	if err_msg != "":
		print err_msg
		sys.exit(1)

	# Parse stock data.

	data = utils.parse_data("../data/notowania.txt")

	found_cluster = False
	plot_tmpfiles = []
	if all_clusters:
		clusters_count = detect_clusters_count(clusters_file_path)
		for i in range(clusters_count):
			_, plot_data = plot_single_cluster(clusters_file_path, i, average_plot)
			plot_tmpfiles.append(plot_data)
	else:
		found_cluster, plot_data_tmpfile_path = plot_single_cluster(clusters_file_path, cluster_number, average_plot)
	
	if found_cluster:

		# Generate file with commands for gnuplot.

		gnuplot_commands_tmpfile_path = tempfile.mkstemp()[1]
		gnuplot_commands_tmpfile = open(gnuplot_commands_tmpfile_path, "r+")
		gnuplot_commands_tmpfile.write("""
		set term gif size 1024, 768
		%s
		%s
		set output '%s.gif'
		plot '%s' with lines
		""" % ( set_xrange, gen_labels(include_events), output_file_path, plot_data_tmpfile_path))

		gnuplot_commands_tmpfile.close()

		print gnuplot_commands_tmpfile_path
		os.system("gnuplot " + gnuplot_commands_tmpfile_path)

		gnuplot_commands_tmpfile.close()
		#os.remove(gnuplot_commands_tmpfile_path)
	
		#os.remove(plot_data_tmpfile_path)
	elif all_clusters:
		plot_cmd = generate_gnuplot_command(plot_tmpfiles, output_file_path,
				include_events)
		#print plot_cmd

		gnuplot_commands_tmpfile_path = tempfile.mkstemp()[1]
		gnuplot_commands_tmpfile = open(gnuplot_commands_tmpfile_path, "r+")
		gnuplot_commands_tmpfile.write(plot_cmd)
		gnuplot_commands_tmpfile.close()
		print gnuplot_commands_tmpfile_path
		os.system("gnuplot " + gnuplot_commands_tmpfile_path)
		gnuplot_commands_tmpfile.close()
		#os.remove(gnuplot_commands_tmpfile_path)
		for tmpfile_path in plot_tmpfiles:
			os.remove(tmpfile_path)
	else:
		print "No group with this number."
	
