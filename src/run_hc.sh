#!/bin/bash

for clusters_num in 5 #10 15 20  # w ten sposob sie nadpisuja!
do
  mkdir -p ../report/v2/hierarchical/
  rm -rf ../report/v2/hierarchical/*
  
  xrange="" # dni, np dla wykresu na dni 100..200:  xrange="100:200"
  events_type="ekonomiczne"
  # katastrofy
  # polityczne
  # ekonomiczne
  # inne
  output_file="../report/v2/hierarchical/output_hierarchical_"$clusters_num
  echo "====================================================="
  echo "RUNNING HIERARCHICAL CLUSTERING FOR ${clusters_num} CLUSTERS"
  echo ""
  python cluster.py ../data/notowania.txt \
	--output $output_file \
    --clusters-num $clusters_num \
    --iters-num 300 \
    --method a \
    --hierarchical

  echo "-----------------------------------------------------"
  echo "PLOTTING SEPARATE CLUSTERS"
  for ((cluster=0; cluster<clusters_num; cluster++))
  do
    plot_output_file=$output_file"_"$cluster
    python plot_group.py $output_file $plot_output_file $cluster events:$events_type xrange:$xrange
  done 

  echo "-----------------------------------------------------"
  echo "PLOTTING SEPARATE CLUSTERS AVERAGES"
  for ((cluster=0; cluster<clusters_num; cluster++))
  do
    plot_output_file=$output_file"_"$cluster"_average"
    python plot_group.py $output_file $plot_output_file $cluster average events:$events_type xrange:$xrange
  done
  
  echo "-----------------------------------------------------"
  echo "PLOTTING ALL INDIVIDUALS"
  plot_output_file=$output_file"_all"
  python plot_group.py $output_file $plot_output_file all events:$events_type xrange:$xrange

  echo "-----------------------------------------------------"
  echo "PLOTTING ALL AVERAGES"
  plot_output_file=$output_file"_all_average"
  python plot_group.py $output_file $plot_output_file all average events:$events_type xrange:$xrange

done
