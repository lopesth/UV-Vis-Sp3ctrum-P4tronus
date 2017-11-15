# -*- coding: utf-8 -*-
__author__ = ["Thiago Lopes", "Daniel Machado", "Heibbe Oliveira"]
__credits__ = "LEEDMOL group - Institute of Chemistry at Universidade de Brasília"
__maintainer__ = "Thiago Lopes"
__email__ = "lopes.th.o@gmail.com"
__date__ = "Nov 14 of 2017"
__version__ = "1.0.1"

from APP.tools.start_spc import Opening, Take_Files
from APP.tools.get_osc import Get_Osc
from APP.tools.gaussian_conv import Gaussian_Convolution
from APP.tools.print_spectrum import Print_Spectrum
from APP.tools.
import sys

class Sp3ctrum_UVvis_P4tronum(object):

    def __init__(self, version):
        self.version = version

    def run_friendly_terminal(self):
        Opening(self.version).welcome()
        answer = True
        while answer:
            self.execute_loop()
            while True:
                try:
                    answer = (input("\nWould you like to run it again? Type \'y\' or \'yes\' to continue: ").split()[0].lower() in ["y", "yes"])
                    break
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    continue
        print("\nOK. Have a nice day and enjoy your results.\n")

    def take_wl_range(self):
        while True:
            try:
                range_wl = input(
                "\nType the beginning of the range and the end (in nm), separated by commas (only integers or decimals): ").split(
                ",")
                range_wl = [float(x) for x in range_wl]
                if(len(range_wl) == 2):
                    if (range_wl[1] > range_wl[0]):
                        break
                    else:
                        print("Type the beginning and the end, in that order!")
                        continue
                else:
                    print("Type two numbers, the beginning and the end of the range!")
                    continue
            except KeyboardInterrupt:
                sys.exit()
            except:
                print("Type only numbers!")
                continue
        return range_wl

    def take_nmb_ptos(self):
        print("\nWould you like to use the default number of points (2000), for wavelength range?")
        while True:
            try:
                answer = input("If yes, type \'yes\' or \'y\', otherwise, type anything: ").split()[0].lower()
                break
            except KeyboardInterrupt:
                sys.exit()
            except:
                continue
        if (answer in ["y", "yes"]):
            numb_of_points = 2000
        else:
            while True:
                try:
                    numb_of_points = int(input("Then type the number of points: ").split()[0])
                    break
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    print("Type an integer!")
                    continue
        return numb_of_points

    def take_fwhm(selfself):
        print("\nWould you like to use the default Full width at half maximum (3226.22 cm^(-1))?")
        while True:
            try:
                answer = input("If yes, type \'yes\' or \'y\', otherwise, type anything: ").split()[0].lower()
                break
            except KeyboardInterrupt:
                sys.exit()
            except:
                continue
        if(answer in ["y", "yes"]):
            sdt_wl_nm = 3226.22
        else:
            while True:
                try:
                    sdt_wl_nm = float(input("Enter the Full width at half maximum in cm^(-1) (numbers only): ").split()[0])
                    break
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    print("Type a number!")
                    continue
        return sdt_wl_nm

    def execute_loop(self):
        files_to_combine = Take_Files().get_files()
        print("\nType the base name for the output files.")
        while True:
            try:
                name_file = input("If the name has more than one word, separate them by '_' and not by space: ").split()[0]
                break
            except KeyboardInterrupt:
                sys.exit()
            except:
                continue
        print("\nType the wavelength range to be processed.")
        range_wl = self.take_wl_range()
        start = float(range_wl[0])
        end = float(range_wl[1])
        numb_of_points = self.take_nmb_ptos()
        sdt_wl_cm = self.take_fwhm()
        self.make_it_happen(files_to_combine, name_file, start, end, sdt_wl_cm, numb_of_points)


    def make_it_happen(self, files_to_combine, name_file, start, end, sdt_wl_cm, numb_of_points):
        total_oscillators = Get_Osc(files_to_combine).take_osc()
        spectrum = Gaussian_Convolution(total_oscillators, sdt_wl_cm)
        greater_epslon_osc = spectrum.make_spectrum(start, end, numb_of_points, sdt_wl_cm)
        spectrum.write_spectrum(name_file)
        Print_Spectrum(name_file, start, end, greater_epslon_osc[0], greater_epslon_osc[1])
