# runtime_plot.gnuplot  -  average runtime vs input size, one curve per algorithm.
#
# Input: tab-separated .dat file made by visualization/gnuplot_runner.py
#        columns: input_size | A | A std | A mem | B | B std | B mem | ...
#
# Run directly:
#   gnuplot -e "datafile='results/plots/sorting_random.dat'; out='runtime.png'; n=3; plot_title='Sorting'" \
#           visualization/gnuplot/runtime_plot.gnuplot
#   (n = number of algorithms in the file; optional: logscale=0|1, errbars=0|1)

if (!exists("logscale")) logscale = 1
if (!exists("errbars"))  errbars  = 1
if (!exists("plot_title")) plot_title = "Runtime vs input size"

set terminal pngcairo size 1000,650 enhanced font "Sans,11"
set output out

set datafile separator "\t"
set datafile missing "NaN"
set key autotitle columnhead
set key top left box opaque

set title plot_title font "Sans,14"
set xlabel "Input size (n)"
set ylabel "Average runtime (seconds)"
set grid
if (logscale) set logscale xy

if (errbars) {
    plot for [i=0:n-1] datafile using 1:(column(2+3*i)):(column(3+3*i)) \
         with yerrorlines lw 2 pt 7 ps 1.0 title columnheader(2+3*i)
} else {
    plot for [i=0:n-1] datafile using 1:(column(2+3*i)) \
         with linespoints lw 2 pt 7 ps 1.0 title columnheader(2+3*i)
}
