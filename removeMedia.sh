#!/bin/sh
# Remove all media files from the current directory

for file in * ; do
    if [ -f "$file" ] ; then
        if [ -n "$(file -i "$file" | grep -E 'video|audio|image')" ] ; then
            rm "$file"
        fi
    fi
done