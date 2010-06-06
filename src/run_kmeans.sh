#!/bin/bash

for clusters_num in 5 10 15 20  
do
  mkdir -p ../report/v2/kmeans/$clusters_num
  rm -rf ../report/v2/kmeans/$clusters_num/*
  
  xrange="" # dni, np dla wykresu na dni 100..200:  xrange="100:200"
  events_type="ekonomiczne polityczne katastrofy inne"
  # katastrofy
  # polityczne
  # ekonomiczne
  # inne
  output_path="../report/v2/kmeans/"$clusters_num"/"
  output_file="output_kmeans_"$clusters_num

  echo "====================================================="
  echo "RUNNING KMEANS CLUSTERING FOR ${clusters_num} CLUSTERS"
  echo ""
  python cluster.py ../data/notowania.txt \
	--output $output_path$output_file \
    --clusters-num $clusters_num \
    --iters-num 300 \
    --method a \
    --kmeans
  
  for event in $events_type
  do
    mkdir -p $output_path/$event/
    rm -rf $output_path/$event/*
 
    plot_output_path=$output_path/$event/
  	echo "----------------------------------------------------"
  	echo "PLOTTING SEPARATE CLUSTERS ("$event")"
  	for ((cluster=0; cluster<clusters_num; cluster++))
  	do
    	plot_output_file=$output_file"_"$cluster
    	python plot_group.py $output_path$output_file $plot_output_path$plot_output_file $cluster events:$event xrange:$xrange
  	done 

  	echo "-----------------------------------------------------"
  	echo "PLOTTING SEPARATE CLUSTERS AVERAGES ("$event")"
  	for ((cluster=0; cluster<clusters_num; cluster++))
  	do
    	plot_output_file=$output_file"_"$cluster"_average"
    	python plot_group.py $output_path$output_file $plot_output_path$plot_output_file $cluster average events:$event xrange:$xrange
  	done
  
  	echo "-----------------------------------------------------"
  	echo "PLOTTING ALL INDIVIDUALS ("$event")"
   	plot_output_file=$output_file"__all"
  	python plot_group.py $output_path$output_file $plot_output_path$plot_output_file all events:$event xrange:$xrange

  	echo "-----------------------------------------------------"
  	echo "PLOTTING ALL AVERAGES ("$event")"
    plot_output_file=$output_file"_all_average"
  	python plot_group.py $output_path$output_file $plot_output_path$plot_output_file all average events:$event xrange:$xrange
  done
done
