# MCCView

Shows plots like labview, but without labview.

Only works for thermocouples at the moment.

Make sure you have InstaCal installed and open.


If you want to build, run
$ pyinstaller MCCView.py --noconsole --onefile
IDK if it'll work right tho because IDK how this sort of thing handles dependencies.
For the most part, just make sure you have pyinstaller, matploblib, mcculw, and tkinter.
If you want to build on Mac, you'll need to make some changes (use the mac version isntead of mcculw), but the rest will probably work?
