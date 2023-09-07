''' 
XPS Spectra Plotter with Custom Error Datapoint Exclusion.

This script allows the user to create average plots from experimental X-ray photoelectron spectroscopy (XPS) data.
The user can import a folder containing (.dat) files for the different surface component scans.
The imported folder must contain this script.
The user will define a standard deviation-based error threshold.
The standard deviation threshold value must be a positive value (float or integer).
Datapoints above the user-specified standard deviation value will be excluded from plots.
This program can produce individual plots for each of the surface component scan files.
This program can produce a final combined plot which combines all the surface component plots.
The user can choose whether they would like to produce individual plots, combined plots or both.
A file containing the standard deviations of all datapoints for all the files in the folder will be generated.
Files containing the excluded datapoints and included datapoints for each individual plot will be created.

It is required that:
    * the experimental files are in .dat file format.
    * this script is saved in the folder which contains the .dat files for which plots will be created.
    * The first column in the files correspond to kinetic energy in eV.
    * The delimiter must be a tab.
    * Each scan file contains 1 or more sweeps and a "sum of all sweeps" column if there are multiple sweeps.
    * Each line of each file has a tab at the end (this is the standard nature of the experimental .dat files)

It is required that the user installs:
    * Anaconda (version 2022.05)
    * Python (version 3.9.12)
    * numpy (version 1.21.5) 
    * matplotlib (version 3.5.1)
This should be done within the python environment where this script is currently being run.

This file contains the following functions:
    * standard_deviation_threshold - removes datapoints which are above the specified standard deviation from plots
'''

# General imports
import os  # lets vscode interact with the operating system
import matplotlib.pyplot as plt  # for plot creation
import numpy as np  # for mathematical calulations

# The following imports will be used to allow the user to import files
# This has been adapted from the following references:
# Stack Overflow, https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder, (accessed 15/01/23).
# Stack Overflow, https://stackoverflow.com/questions/73003417/input-folder-path-and-return-a-list-of-files-on-tkinter, (accessed 18/03/23).
# glob is a module that returns all filepaths that follow a specific pattern
# In this program, glob will be used to return files of the .dat format
# tkinter is Python's standard Graphical User Interface (GUI) creation library
# In this program, tkinter will be used to create the folder selection pop-up
# tkinter has a prebuilt dialogue window to access files within its filedialog module
# The askdirectory() function within the filedialog module allows for the selection of one folder or file
# In this program, this function will be used to select a folder containing the input files
from tkinter import Tk
import tkinter
from tkinter.filedialog import askdirectory
import glob

# Initial message to the user explaining this program
print("You will be prompted to select the folder which contains the .dat files you would like to make plots for.")
print("(Note: files in subfolder will not be selected.)")
initial_message = input("To continue, press 'y' and then enter ")

# Creation of folder selection pop-up
if initial_message == "y":
    # If the user continues after the inital message: dialogue box appears, asks user to select folder and returns the path
    folderpath = askdirectory(title='Select Folder')
else:
    # Message to the user in case they enter the wrong input
    print("Re-run the code and make sure to just enter the letter 'y' with no spaces or apostrophes - just the letter.")
    exit()  # Ends the execution of the program so the user will re-run it

# Statement lets the user check that they imported the right folder
print("This is the selected folderpath: " + folderpath)

# Set up of x-axis and y-axis lists for the final combined plot (of all files in the selected folder)
fp_xaxis = []
fp_yaxis = []

# Definition of variables used to read lines of code in the loop
# A tab is the standard delimiter of experimental XPS (.dat) files
delimit = "\t"
numhead = 1  # Number of header-lines in the file which will not be read as data as they contain column headers

# Section divider printed in terminal for clarity 
print("----------------------------------------------------------------------")

# The user inputs the photon energy at which the scan was run
print("Photon energy must be an integer or float.")
photon_energy = input("Enter photon energy in eV. ")

# Section divider printed in terminal for clarity 
print("----------------------------------------------------------------------")

# The user chooses the threshold standard deviation
print("What standard deviation would you like to specify?")
std_input = input("Just enter the number without any units. It must be positive. ")

# Error trap
# Creation of an error message if a number is not entered for photon energy or standard deviation value
# Creation of an error message if the number entered is negative
user_input_numbers = [photon_energy, std_input]
for entered_value in user_input_numbers:
    try: 
        entered_value = float(entered_value) # Ensuring that the input is a number
        if entered_value >= 0: # Ensuring the number is positive or zero
            pass
        else:
            print("The number you entered for photon energy or standard deviation is negative.")
            print("Re-run the program and try again.")
            exit()
    except ValueError: 
        print ("You did not enter a number for either photon energy or standard deviation.") 
        print("Re-run the program and try again.")
        exit()


# Section divider printed in terminal for clarity 
print("----------------------------------------------------------------------")

# The user chooses what kind of output they want
print("You can choose the type of output plots produced.")
print("If you would like to produce only individual plots for each file, enter 'i'.")
print("If you would like to produce only the final combined plot which uses all files in the folder, enter 'f'.")
output_plot_choice = input("If you would like to produce both, enter 'b'.")
if output_plot_choice == "i" or output_plot_choice == "b" or output_plot_choice == "f":
    pass
elif output_plot_choice == "I" or output_plot_choice == "B" or output_plot_choice == "F":
    pass
else:
    print("You did not enter an appropriate letter when choosing output plot types.")
    print("Re-run the program and try again.")
    exit()  # Ends the execution of the program so the user will re-run it

# Section divider printed in terminal for clarity 
print("----------------------------------------------------------------------")

# Standard deviation, excluded datapoint and included datapoint files which are produced must be reset at the start of every run
# This is in case the the user tries to run the program twice without deleting the files produced by the first run
# This prevents the program from appending the information from the second run onto that of the first
output_file = ["std_file.txt", "excluded_datapoints_file.txt",
                "included_datapoints_file.txt"]
for txt_file in output_file:
    if os.path.exists(txt_file):  # Existance of the files from previous runs is checked
        os.remove(txt_file)  # Old files are deleted
    else:
        pass

# Defining a function

def standard_deviation_threshold():
    '''
    This function removes datapoints with standard deviations above the user-chosen one from the plots.

    Parameters
    ----------
    point_standard_deviation : float
        Standard deviation of the datapoint
    std_input : string
        Standard deviation value chosen by the user
    axes: list[list]
        List of names of all axes
    xaxis: list
        x-axis values for individual file plots
    yaxis: list
        y-axis values for individual file plots
    fp_xaxis: list
        x-axis values for final combined plot
    fp_yaxis: list
        y-axis values for final combined plot
    binding_energy: float
        Binding energy of the datapoint
    mean_intensity: float
        Mean intensity of the datapoint
    excluded_point_numbers: list
        List of excluded datapoint numbers
    datapoint_number: int
        Datapoint number
    included_point_numbers : list
        List of included datapoint numbers

    Returns
    ----------
    The function does not return a value but, instead, updates the axes list
    '''
    # Reference: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch17s02.html
    # This reference helped me redirect the NameError message when user selects the wrong folder
    # try/except statements allow common errors to be redirected to a custom backup action
    try: 
        if point_standard_deviation > float(std_input):
            axes = [xaxis, yaxis, fp_xaxis, fp_yaxis]
            for xax in axes[0::2]:
                xax.remove(binding_energy)  # Removal of x-axis values from plots
            for yax in axes[1::2]:
                yax.remove(mean_intensity)  # Removal of y-axis values from plots
            # Excluded datapoint number stored in a list
            excluded_point_numbers.append(datapoint_number)
        else:
            # Included datapoint number stored in a list
            included_point_numbers.append(datapoint_number)
    except NameError:
        # Section divider printed in terminal for clarity 
        print("----------------------------------------------------------------------") 
        # Substitute for the NameError message
        print("You selected the wrong folder. It must be the folder that this script is saved in.")
        exit() # Ends the execution of the program so the user will re-run it


# Creation of the major loop which gets the filepaths for all the files in the selected folder
# glob is used to return files ending with '.dat'
for count, filename in enumerate(glob.glob("*.dat")):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        # Message to the user so they know the program is running
        if output_plot_choice != "f" and output_plot_choice != "F":
            print("The plot for " + filename + " is currently being created.")
        else: print("Loading...") # If only the final combined plot output is chosen.
    filepath = os.path.join(folderpath, filename)

    # Reference: the UV mini project from the CHEM0062 Moodle page
    # Creation of an average xps plot for all .dat files in the folder
    # Individual plots for each .dat file will be plotted as well as a plot which combines all the individual plots
    # Plots will exclude datapoints - exclusion is based on the threshold set by the user
    if os.path.exists(filepath):
        with open(filepath, 'r') as infile:
            # Definition of list variables
            xaxis = []
            yaxis = []
            standard_deviations_list = []
            excluded_point_numbers = []
            included_point_numbers = []
            intensities_in_a_line_list = []

            # The document is read line-by-line
            for x in range(numhead+1):
                line = infile.readline()
            line_number = 1  # Setting up the line counter
            while line:
                # Saving the current line number
                line_number += 1

                # Save current datapoint number
                datapoint_number = (line_number - 1)

                # Creating a list containing all the values in a line
                # Error trap: common alternative delimiters that may be present are replaced with the standard delimiter
                alternative_delimiter = [",", ";", " "]
                for alternate in alternative_delimiter:
                    line = line.replace(alternate, delimit)
                datapoint = line.split(delimit)

                # Appending energies to the x-axis
                kinetic_energy = float(datapoint[0])
                binding_energy = float(photon_energy) - kinetic_energy
                xaxis.append(binding_energy)
                fp_xaxis.append(binding_energy)

                # Setting a variable for the index of the last column
                # '-2' on the first line is because we want the index and there is a tab at the end of each line that needs to be excluded
                intensity_sum_index = (int(len(datapoint)) - 2)
                num_sweeps = intensity_sum_index - 1

                # Finding the mean intensity and appending it to the y-axis
                if num_sweeps > 0:
                    # Average intensity of all sweeps
                    mean_intensity = float(
                        datapoint[intensity_sum_index])/(num_sweeps)
                elif num_sweeps == 0:
                    # To account for files with only 1 sweep which have no sum column
                    mean_intensity = float(datapoint[intensity_sum_index])/(1)
                else:
                    print(
                        "Something has gone wrong with the mean intensity calculation for this file")
                    continue
                yaxis.append(mean_intensity)
                fp_yaxis.append(mean_intensity)

                # Making a list of intensities for a line (excluding the energy and intensity sum values)
                # print(len(datapoint)) --> test confirmed that the length of a datapoint for a file with only 1 sweep is 3
                intensities_in_a_line_list = []
                if len(datapoint) > 3:
                    # Splitting off the energy and sum columns from the lines
                    intensities_in_a_line_list = datapoint[1:intensity_sum_index]
                elif len(datapoint) == 3:
                    # To account for files with only 1 sweep which have no sum column
                    intensities_in_a_line_list = datapoint[1:(
                        intensity_sum_index+1)]
                else:
                    print("Something has gone wrong with the len(datapoint)")

                # Calculation of standard deviation of the intensities for each datapoint
                # Reference: introduction to python pt1 (from the CHEM0062 Moodle page)
                point_variance = 0
                for intensity in intensities_in_a_line_list:
                    point_variance = point_variance + \
                        ((float(intensity) - mean_intensity)
                            *(float(intensity) - mean_intensity))
                point_variance = point_variance/len(intensities_in_a_line_list)
                point_standard_deviation = np.sqrt(point_variance)
                standard_deviations_list.append(point_standard_deviation)

                # Printing standard deviations to a separate file
                # This file prints: (filename, datapoint number, line in the respective file where the datapoint is, standard deviation)
                # https://howtodoinjava.com/python-examples/python-print-to-file/
                # 'a+' appends each std to the file line by line (rather than 'w' which overwrites each datapoint std after every line)
                standard_deviation_file = open("std_file.txt", "a+")
                print((filename, datapoint_number, line_number,
                        point_standard_deviation), file=standard_deviation_file)
                standard_deviation_file.close()

                # Error threshold application based on user choice of threshold type
                standard_deviation_threshold()

                line = infile.readline()  # Closing the loop

            # Creation of individual scatter plots for each .dat file
            # Dot markers are used and marker size are set
            plt.scatter(xaxis, yaxis, marker="o", s=0.5)
            plt.xlabel("Binding energy / eV")
            plt.ylabel("Average sweep intensity / a.u.")

            # Saving the figure to the folder where the .dat files are located
            # This means the user does not need to keep closing pop-up figure windows as with "plt.show()"
            # Reference: https://stackoverflow.com/questions/17788685/python-saving-multiple-figures-into-one-pdf-file
            # Removal of .dat filename suffix - figure can only save as a .png file if suffix is removed
            filename_stripped = filename.replace(".dat", "")
            if output_plot_choice != "f" and output_plot_choice != "F":
                plt.savefig("Figure for " + str(filename_stripped))
                plt.close()

            # Creation of the excluded and included datapoint files
            # Note: a nested loop was not created for this section as I had trouble with the TextIOWrapper format (see the report)
            excluded_points_file = open("excluded_datapoints_file.txt", "a+")
            print(("The following are the data point numbers for the excluded data points (" +
                    str(filename) + ") : " + str(excluded_point_numbers)), file=excluded_points_file)
            excluded_points_file.close()

            included_points_file = open("included_datapoints_file.txt", "a+")
            print(("The following are the data point numbers for the included data points (" +
                    str(filename) + ") : = " + str(included_point_numbers)), file=included_points_file)
            included_points_file.close()

# Error threshold application based on user choice of threshold type
standard_deviation_threshold()
# Creation of the final combined plot
# Dot markers and marker size are set
plt.scatter(fp_xaxis, fp_yaxis, marker="o", s=0.5)
plt.xlabel("Binding energy / eV")
plt.ylabel("Average sweep intensity / a.u.")
plt.savefig("Final combined plot")
plt.close()

# Removing final combined plot if it was not asked for by the user
if output_plot_choice == "i" or output_file == "I":
    os.remove("Final combined plot.png") # Deletes the final plot if only individual plots are wanted.
elif output_plot_choice == "b" or output_plot_choice == "B":
    pass
elif output_plot_choice == "f" or output_plot_choice == "F":
    pass

# Section divider printed in terminal for clarity 
print("----------------------------------------------------------------------")

# Final statements to aid the users' understanding of their results and aid future uses of this script.
print("Try out different standard deviations to see what suits your needs.")
print("Note that the highest standard deviation in the set was " + str(max(standard_deviations_list)))
print("Also note that plots of files with only 1 sweep cannot be improved using this program.")
print("This is because this program requires more than 1 sweep to calculate error values.")
print("Improve such plots by collecting more experimental data for corresponding files.")
print("Note: it is recommended you output both plots when experimenting with standard deviation values.")