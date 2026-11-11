# memory_plot.gnuplot  -  peak extra memory (tracemalloc) vs input size.
# Same input file and variables as runtime_plot.gnuplot.
#   gnuplot -e "datafile='results/plots/sorting_random.dat'; out='memory.png'; n=3; plot_title='Sorting'" \
#           visualization/gnuplot/memory_plot.gnuplot

if (!exists("logscale")) logscale = 1
if (!exists("plot_title")) plot_title = "Peak memory vs input size"

set terminal pngcairo size 1000,650 enhanced font "Sans,11"
set output out

set datafile separator "\t"
set datafile missing "NaN"
set key autotitle columnhead
set key top left box opaque

set title plot_title font "Sans,14"
set xlabel "Input size (n)"
set ylabel "Peak extra memory (KiB)"
set grid
if (logscale) set logscale xy

plot for [i=0:n-1] datafile using 1:(column(4+3*i)) \
     with linespoints lw 2 pt 5 ps 1.0 title columnheader(4+3*i)
