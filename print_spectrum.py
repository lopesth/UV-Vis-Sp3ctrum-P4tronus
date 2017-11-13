# -*- coding: utf-8 -*-
__author__ = "Thiago Lopes and LEEDMOL group"
__credits__ = ["LOPES, T. O.", "OLIVEIRA, H. C. B."]
__maintainer__ = "Thiago Lopes"
__email__ = "lopes.th.o@gmail.com"
__date__ = "Nov 11 of 2017"
__version__ = "1.0"

import matplotlib.pyplot
import os, sys

class Print_Spectrum(object):

    def __init__(self, file_name, start_wl, end_wl, end_epslon, end_osc):
        self.file_name = file_name
        self.start_wl = start_wl
        self.end_wl = end_wl
        self.end_osc = end_osc
        self.end_epslon = end_epslon
        print("You can print using Gnuplot (better graphic, however you need to have gnuplot installed, it only works on macOS and Linux) or Matplotlib (you need to have Matplotlib installed, you can install with the pip: `pip3 install matplotlib`.")
        while True:
            try:
                answer = input("\nWould you like to post a title on your chart? Type \'yes\' or \'y\' for yes, otherwise, type anything: ").split()[0].lower() in ["y", "yes"]
                break
            except KeyboardInterrupt:
                sys.exit()
            except:
                continue
        if answer:
            self.title = input("Title your title of choice: ")
        else:
            self.title = ""
        while(True):
            try:
                answer = input("\nType (1) to Gnuplot and (2) to Matplotlib:")
                if answer == "1":
                    self.print_gnuplot()
                    break
                elif answer == "2":
                    self.print_matplotlib()
                    break
                else:
                    continue
            except KeyboardInterrupt:
                sys.exit()
            except:
                continue


    def print_gnuplot(self):
        folder = os.popen("pwd", 'r', 1).read().split('\n')[0]

        gnuplot_command1 = "gnuplot -e \'set term png transparent size 2560,1920; set lmargin screen 0.1; set rmargin screen 0.9 ; set output \""+folder+"/"+self.file_name+".png\"; set xlabel \"Waveleght (nm)\" font \"Verdana,35\" offset 0,-3,0; set ylabel \"Molar Absorptivity (L/mol.cm)\" font \"Verdana,35\" offset -6, 0, 0; set format y2 \"%.2f\"; "
        if len(self.title) > 0 :
            gnuplot_command1 = gnuplot_command1 + " set title \""+self.title+"\" font \"Verdana,25\" offset 0, -1, 0;"
        gnuplot_command2 = "set xrange ["+str(self.start_wl)+":"+str(self.end_wl)+"]; set yrange [0:"+str(self.end_epslon+(self.end_epslon*0.05))+"]; set y2range [0:"+str(self.end_osc+(self.end_osc*0.05))+"]; set y2label \"Oscillator Strength (arbitrary units)\" font \"Verdana,35\" offset 6,0,0; set key off; set xtics font \"Verdana,25\" nomirror offset 0,-1,0; set ytics font \"Verdana,25\" nomirror; set y2tics font \"Verdana,25\";plot \""+self.file_name+"_spectrum.dat\" using 1:2 axis x1y1 with line linewidth 6.000, \""+self.file_name+"_rawData.dat\" using 1:2 axis x1y2 with impulses linewidth 6.000' "
        os.popen(gnuplot_command1 + gnuplot_command2, 'r', 1)
        print("The file named {} was saved in your working directory" .format(self.file_name+".png"))


    def print_matplotlib(self):
        wl = []
        epslon = []
        wl_ref = []
        osc_ref = []
        with open(self.file_name+"_spectrum.dat") as myFile:
            for line in myFile:
                wl.append(float(line.split()[0]))
                epslon.append(float(line.split()[1]))
        with open(self.file_name+"_rawData.dat") as myFile:
            for line in myFile:
                wl_ref.append(float(line.split()[0]))
                osc_ref.append(float(line.split()[1]))
        graph = matplotlib.pyplot.figure()
        a = graph.add_subplot(111)
        b = a.twinx()
        line1, = a.plot(wl, epslon, linestyle = 'solid', fillstyle ='none')
        line2, = b.plot(wl_ref, osc_ref, visible = False)
        for i in range(len(wl_ref)):
            b.vlines(wl_ref[i], 0, osc_ref[i], colors='red', lw =2)
        graph.tight_layout()
        b.set_ylabel("Oscillator Strength (arbitrary unit)")
        a.set_ylabel("Molar Absorptivity (L/mol.cm)")
        a.set_xlabel("Wavelength (nm)")
        if len(self.title) > 0:
            matplotlib.pyplot.title(self.title)
        matplotlib.pyplot.show()