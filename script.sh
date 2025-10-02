# to compile the latex report.
rm -f report.aux report.log report.out report.toc && pdflatex -interaction=nonstopmode report.tex && pdflatex -interaction=nonstopmode report.tex