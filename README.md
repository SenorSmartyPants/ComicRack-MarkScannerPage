This script will mark a scanner page as pageType Deleted by default (that can be changed by editing MarkScannerPage.py)

There is currently no progress bar, and the only output is in the script console. ("C:\Program Files\ComicRack\ComicRack.exe" -ssc) So I recommend installing Stonepaw's Books with Pages Marked plugin (I don't see it on his github) to display comics after the scanner page has been marked. It can then be deleted using CR if you so choose.

The logic for this plugin was copied from comicTagger. CT had a routine to find the page, but wasn't exposing that as an easy option.
