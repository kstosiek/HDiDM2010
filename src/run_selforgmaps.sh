#!/bin/bash

for n in 2 3 4
do
  clusters_num=$(($n * $n))
  mkdir -p ../report/v2/selforgmaps/$clusters_num
  rm -rf ../report/v2/selforgmaps/$clusters_num/*  

  events_type="katastrofy"

  output_file="../report/v2/selforgmaps/"$clusters_num"/output_selforgmaps_"$clusters_num
  echo "====================================================="
  echo "RUNNING HIERARCHICAL CLUSTERING FOR ${clusters_num} CLUSTERS"
  echo ""
  python cluster.py ../data/notowania.txt \
	--output $output_file \
	--xgrid $n \
	--ygrid $n \
    --iters-num 5000 \
    --method a \
    --selforgmaps

  echo "-----------------------------------------------------"
  echo "PLOTTING SEPARATE CLUSTERS"
  for ((cluster=0; cluster<clusters_num; cluster++))
  do
    plot_output_file=$output_file"_"$cluster
    python plot_group.py $output_file $plot_output_file $cluster events:$events_type
  done 

  echo "-----------------------------------------------------"
  echo "PLOTTING SEPARATE CLUSTERS AVERAGES"
  for ((cluster=0; cluster<clusters_num; cluster++))
  do
    plot_output_file=$output_file"_"$cluster"_average"
    python plot_group.py $output_file $plot_output_file $cluster average events:$events_type
  done
  
  echo "-----------------------------------------------------"
  echo "PLOTTING ALL INDIVIDUALS"
  plot_output_file=$output_file"_all"
  python plot_group.py $output_file $plot_output_file all events:$events_type

  echo "-----------------------------------------------------"
  echo "PLOTTING ALL AVERAGES"
  plot_output_file=$output_file"_all_average"
  python plot_group.py $output_file $plot_output_file all average events:$events_type

done
