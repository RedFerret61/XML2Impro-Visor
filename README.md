#XML2Impro-Visor
XML2Impro-Visor converts a musicxml leadsheet (single melody with harmony chord symbols) 
file (or files in a directory) to impro-visor style leadsheet(s).

    usage: XML2Impro-Visor.py [-h] [-m MXLFILEORPATHORPATH]
    optional arguments:
    -h, --help            show this help message and exit
    -m MXLFILEORPATH, --music MXLFILEORPATH
                     music file or path, relative to current working directory e.g. XML2Impro-Visor/music.mxl or XML2Impro-Visor/leadsheets


XML2Impro-Visor only converts leadsheet chords not the melody. 

Workaround example to rejoin melody to accompaniment (e.g. exported from Impro-visor):
*   In MuseScore, File > Open “accompaniment MIDI export”.mid
*   Edit > Instruments… add melody instrument
*   File > Open > original musicxml leadsheet with melody.mxl
*   Click on a note , select all (^A), copy ^C
*   Click on “accompaniment MIDI export” tab, scroll to new melody stave, select 2nd bar rest (if accompaniment has count in), Paste ^V


The latest release has been tested on: 
* Windows 10.0.19044
  - with MuseScore 3.6.2, Python 3.9.6, music21 v 7.1.0 
* Ubuntu 20.04
  - with MuseScore 3.2.3, Python 3.8.10, music21 v 7.1.0

**Table of Contents**

1. [XML2Impro-Visor Installation instructions for Windows](#XML2Impro-Visor Installation instructions for Windows)
2. [XML2Impro-Visor Installation instructions for macOS](#XML2Impro-Visor Installation instructions for macOS)
3. [XML2Impro-Visor Installation instructions for Ubuntu](#XML2Impro-Visor Installation instructions for Ubuntu)



*Note: GitHub has a full table of contents with links in the header icon (top left of the readme.md).*

---

##XML2Impro-Visor Installation instructions for Windows
Pre-requisites for XML2Impro-Visor include Python, and Music21.

###Python Windows installation
 1. Firstly check python version required by Music21.
 see https://web.mit.edu/music21/doc/installing/installWindows.html

      in October 2021 this stated  "Windows users should download and install Python version 3.8 or higher."
* For example
  * Python 3.9.6 worked for me with music21 versions 6.7.1 and 7.1.0 
  * Python 3.10.0 did not work for me with music21 version 7.1.0 (numpy not compatible)

2. Browse to https://www.python.org/downloads/windows
    
    Download desired version (may not be the latest) and run.
    
    Select "Add Python to PATH". Install.


3. Check it works: Start, search, cmd, click on Command Prompt, type:
   
    python --version

    Expect the version to be displayed e.g. Python 3.9.6

###Music21 Windows installation
 
1. Music21 Installation details at https://web.mit.edu/music21/doc/installing/installWindows.html

    At command prompt:

    pip install music21

3. Check music21 version installed with:

   pip list

4. Configure with (press return to accept defaults):

   python -m music21.configure

if you have problems and want to try different versions. Uninstall music21 with:

   pip uninstall music21

Uninstall Python by opening Control Panel, Click "Uninstall a Program", Scroll down to Python and click uninstall for each version you don't want anymore.

To upgrade music21 at a later date to the latest version, 'pip uninstall music21' then 'pip install music21' again.

###XML2Impro-Visor Windows installation

####Install XML2Impro-Visor on Windows
 Download release zip to desired directory for XML2Impro-Visor and unzip with right click Extract All ...
####Run XML2Impro-Visor on Windows 

 In a Command Prompt window change to install directory and show XML2Impro-Visor help e.g.:

    cd C:\Users\paul\Documents\XML2Impro-Visor

    XML2Impro-Visor.py -h
    :: or
    python XML2Impro-Visor.py -h

Then run using supplied mxl:

    python XML2Impro-Visor.py -m Impromusic.mxl
    :: or
    XML2Impro-Visor.py -m Impromusic.mxl
    XML2Impro-Visor.py -m XML2Impro-Visor/music.mxl
    XML2Impro-Visor.py -m XML2Impro-Visor/leadsheets

 This converts supplied musicxml (.mxl) examples to Impo-Visor leadsheets (.ls).


##XML2Impro-Visor Installation instructions for macOS
Pre-requisites for XML2Impro-Visor include Python, and Music21.

###Python on macOS:
 1. Firstly check python version required by Music21.
see https://web.mit.edu/music21/doc/installing/installMac.html
in December 2021 this recommended Python 3.9 or later.

 2. Use https://docs.python.org/3/using/mac.html and https://www.python.org/downloads/macos/
 3. To check the installed version of python, click the Launchpad icon in the Dock, type Terminal in the search field, then click Terminal. Then type:
    

    python3 --version
    Python 3.10.0



###Music21 on macOS
 

1. Install Music21. In a Terminal type:


        pip3 install music21


2. Check music21 version installed with:

       pip3 list



####Install XML2Impro-Visor on macOS
 Download release zip to desired directory for XML2Impro-Visor and unzip by double-clicking on the zipped file .
####Run XML2Impro-Visor on macOS

 In command prompt change to install directory, make run files executable and run XML2Impro-Visor e.g.:

 ```  
 cd ~/XML2Impro-Visor
 
 # display help    
 python3 XML2Impro-Visor.py -h
 
 # Then run using supplied mxl:
 
 python3 XML2Impro-Visor.py -m Impromusic.mxl
 python3 XML2Impro-Visor.py -m XML2Impro-Visor/music.mxl
 python3 XML2Impro-Visor.py -m XML2Impro-Visor/leadsheets
 
```
---

##XML2Impro-Visor Installation instructions for Ubuntu
Pre-requisites for XML2Impro-Visor include Python, and Music21.

###Python on Ubuntu:
 1. Firstly check python version required by Music21.
see https://web.mit.edu/music21/doc/installing/installLinux.html
in October 2021 this stated Music21 requires Python 3.7+.

 2. Check default installed version of python Ctrl+Alt+T
    

    python3 --version
    Python 3.8.10

The default python on Ubuntu 20.04 is compatible.


###Music21 on Ubuntu
 
1. If the package installer for Python (pip3) is not yet installed, in terminal :

       sudo apt install python3-pip


2. Install Music21


        pip3 install music21

Ignore Fortran to Python warning:  WARNING: The scripts f2py, f2py3 and f2py3.8 are installed in 
    '/home/admin3/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, 
  use --no-warn-script-location.



3. Check music21 version installed with:

       pip3 list



####Install XML2Impro-Visor on Ubuntu
 Download release zip to desired directory for XML2Impro-Visor and unzip.
####Run XML2Impro-Visor on Ubuntu

 In command prompt change to install directory and run XML2Impro-Visor e.g.:

 ```  
 cd ~/pycharm     

  # display help    
 python3 XML2Impro-Visor.py -h
 
# Then run using supplied mxl:
 
 python3 XML2Impro-Visor.py -m Impromusic.mxl
 python3 XML2Impro-Visor.py -m XML2Impro-Visor/music.mxl
 python3 XML2Impro-Visor.py -m XML2Impro-Visor/leadsheets
 
