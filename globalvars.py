# some variables for global use
import System
from System.IO import Path, FileInfo

FOLDER = FileInfo(__file__).DirectoryName + "\\"
INIFILE = Path.Combine(FOLDER, 'msp.ini')
LOGFILE = Path.Combine(FOLDER, 'markpage.log')
ICON_SMALL = Path.Combine(FOLDER, 'scan-icon48px.ico')
ICON = Path.Combine(FOLDER, 'scan-icon48px')

# the processes the backgroundWorker shall handle
PROCESS_TEST = 0
PROCESS_OFF = 1
PROCESS_ON = 2

COMPARE_CASE_INSENSITIVE = True

VERSION = '0.2.3'