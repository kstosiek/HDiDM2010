#!/bin/bash

for n in 2 3 4  
do
  clusters_num=$(($n * $n))
  mkdir -p ../report/v2/selforgmaps/$clusters_num
  rm -rf ../report/v2/selforgmaps/$clusters_num/*
  
  events_type="ekonomiczne polityczne katastrofy inne"
  # katastrofy
  # polityczne
  # ekonomiczne
  # inne
  output_path="../report/v2/selforgmaps/"$clusters_num"/"
  output_file="output_selforgmaps_"$clusters_num

  echo "====================================================="
  echo "RUNNING SELFORGMAPS CLUSTERING FOR ${clusters_num} CLUSTERS"
  echo ""
  python cluster.py ../data/notowania.txt \
	--output $output_path$output_file \
    --xgrid $n \
    --ygrid $n \
    --iters-num 5000 \
    --method a \
    --selforgmaps
  
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
