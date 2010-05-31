#!/bin/bash

# TODO(flojdek): adjust the parameters accordingly to SOM. 

for clusters_num in 5 10 15 20
do
  output_file="output_kmeans_"$clusters_num
  echo "====================================================="
  echo "RUNNING HIERARCHICAL CLUSTERING FOR ${clusters_num} CLUSTERS"
  echo ""
  python cluster.py ../data/notowania.txt \
	--output $output_file \
    --clusters-num $clusters_num \
    --iters-num 300 \
    --method a \
    --selforgmaps

  echo "-----------------------------------------------------"
  echo "PLOTTING SEPARATE CLUSTERS"
  for ((cluster=0; cluster<clusters_num; cluster++))
  do
    plot_output_file=$output_file"_"$cluster
    python plot_group.py $output_file $plot_output_file $cluster
  done 

  echo "-----------------------------------------------------"
  echo "PLOTTING SEPARATE CLUSTERS AVERAGES"
  for ((cluster=0; cluster<clusters_num; cluster++))
  do
    plot_output_file=$output_file"_"$cluster"_average"
    python plot_group.py $output_file $plot_output_file $cluster average
  done
  
  echo "-----------------------------------------------------"
  echo "PLOTTING ALL INDIVIDUALS"
  plot_output_file=$output_file"_all"
  python plot_group.py $output_file $plot_output_file all

  echo "-----------------------------------------------------"
  echo "PLOTTING ALL AVERAGES"
  plot_output_file=$output_file"_all_average"
  python plot_group.py $output_file $plot_output_file all average

done
