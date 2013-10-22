# OSI uploader & killer

`post.py` is a simple script to grab the OSI report source and post it onto the OpenSpending WordPress site as a tree of Pages, with a nice hierarchical structure for slugs.

Also includes `kill.py`, which reads a list of Page IDs from `kill.yaml` and sends them to the trash. When `post.py` runs, it writes the IDs of the Pages it creates to `kill.yaml` so that they can be easily erased on the next iteration. *Note that you still have to empty the trash before running `post.py`, as the slugs of Pages in the trash are not usable.*