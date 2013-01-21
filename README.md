Pycasa
======

Synchronize your local folder to Picasa

Create a file as follow 

	#!/usr/bin/python
	from syncpicassalib import SyncPicassa
	
	s = SyncPicassa("AccountEmail", "AccountPassword")
	
	s.sync_folder("/path/to/folder/to/sync/with/photos")
