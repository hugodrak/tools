#!/bin/bash
path1="$PWD/$1"
cd $path1
echo “The largest files/directories in $1 are:”
du -sh * | sort -hr | head | cat -n -
