# UOHI_PCI_Log


### On MACOS:

1) Install Github
https://gist.github.com/derhuerst/1b15ff4652a867391f03

2) On MacOS : Open Terminal by doing CMD + SPACE and searching for 'Terminal'

3) In the new window clone this GitHub reposity by typing 'git clone https://github.com/robertavram-md/UOHI_PCI_Log.git'

4) You will have a new folder where Terminal or command Prompt was opened called `UOHI_PCI_Log`

5) Install Python https://www.python.org/downloads/

6) Get your PCI data from Richard Jung as an XLSX file. Make sure you save the file without a password so that the Terminal can open it (Open it in Excel -> Go to File - > Passwords and type the current password, then under 'New Password' leave the field empty)

7) Put your PCI data .xlsx file into the folder called `UOHI_PCI_Log`

8) Run in terminal `pip install pandas`

9) Run this command in terminal `python ComputeMetrics.py '**filename**'`

For example if your PCI Log book is named `avram_18_11_2020.xlsx` then you should run `python ComputeMetrics.py 'avram_18_11_2020.xlsx'`

### On Windows:


1) Install Github
https://gist.github.com/derhuerst/1b15ff4652a867391f03

2) On Windows : Use Windows+R on your keyboard to open “Run” box. Type “cmd” and then click “OK” to open a regular Command Prompt. 

3) In the new window clone this GitHub reposity by typing 'git clone https://github.com/robertavram-md/UOHI_PCI_Log.git'

4) You will have a new folder where Terminal or command Prompt was opened called `UOHI_PCI_Log`

5) Install Python https://www.python.org/downloads/

6) Get your PCI data from Richard Jung as an XLSX file. Make sure you save the file without a password so that the Terminal can open it (Open it in Excel -> Go to File - > Passwords and type the current password, then under 'New Password' leave the field empty)

7) Put your PCI data .xlsx file into the folder called `UOHI_PCI_Log`

8) Run in Command Prompt `pip install pandas`

9) Run in Command Prompt `python ComputeMetrics.py '**filename**'`

For example if your PCI Log book is named `avram_18_11_2020.xlsx` then you should run `python ComputeMetrics.py 'avram_18_11_2020.xlsx'`


### Results

You will get three files

1) condensed_summary_.csv Contains the summary of number of cases breakdown as required by the royal college
2) overall_.csv Contains all your cases, including diagnostics. The last columns in the file can be used to 'filter' the required data
3) interventions_.csv Contains all the intervention data. The last columns in the file can be used to 'filter' the required data (i.e. select all the Bifurcation cases