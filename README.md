
# XPS Spectra Plotter with Custom Error Datapoint Exclusion.

----------------------------------------------------------------------------------------------------------------------
A script which creates average (mean) plots from experimental X-ray photoelectron spectroscopy (XPS) data.
It allows the user to set an error threshold to exclude datapoints based on datapoint standard deviations.
The script is provided as well as real XPS sample data from the P22 beamline at the German Electron Synchrotron DESY.
Users can use the sample data to test whether the program runs correctly on their device before using their own data.

----------------------------------------------------------------------------------------------------------------------
Note: this is a final year university coding project for a scientific programming module. This project was tested on 
more extensive sample data however only one set has been posted here for simplicity. If further sample data or the full
report would be of use, feel free to request it.

----------------------------------------------------------------------------------------------------------------------
Installation:

The following things need to be installed by the user:
    * Anaconda (version 2022.05)
    * Python (version 3.9.12)
    * numpy (version 1.21.5) 
    * matplotlib (version 3.5.1)
    * An IDE such as VSCode

Download files provided.

----------------------------------------------------------------------------------------------------------------------
Information on the data provided:

The folder called "Experimental data" contains .dat files and the python code called xps_plotter.py.
Every .dat file regards the GdH2 metal hydride and the scans were taken at a photon energy of 2410 eV.

----------------------------------------------------------------------------------------------------------------------
To run the this program:
1. Run the xps_plotter from one of the subfolders within the "Experimental data" folder in an IDE.
2. Enter the inputs requested by the terminal prompts.

Note:
* The selected folder must be the one containg the current version of the python script.
* The photon energy can be found from the subfolder name. 
    E.g. the photon energy of GdH2_pSi_2410 is 2410 eV.
* The selected standard deviation threshold values must be a positive float or integer. 
* The output type must be selected by entering "i", "b" or "f" (individual plot, final combined plot, both).
  
-----------------------------------------------------------------------------------------------------------------------
Important notes to prevent errors:

* In order for this program to run, xps_plotter.py py needs to be saved in the same folder as the .dat files 
for which plots will be created. The user may have saved this script into a folder but then want to run this
script on a folder which it is not present within. In this case, the user must copy and paste the script 
file into this other folder and run this new copy of the script.

* Outputting both plot types is recommended. Any output option can be chosen. However, if you want to output only 
individual plots for one standard deviation (std1), make sure to delete the individual plots before 
re-running and choosing to make the final plot for a different standard deviation (std2). This is because 
the results for std1 and std2 will appear mixed together which might cause confusion. All other operations
are fine as they overwrite the outputs from the previous run.

* Generally, figures are named in a way such that the output figures from one run overwrite those from the 
next. This is because the user most likely only needs the figures with the most suitable self-defined 
exclusion threshold and so this saves the user from having to delete figures with unsuitable thresholds
whilst experimenting.

-----------------------------------------------------------------------------------------------------------------
