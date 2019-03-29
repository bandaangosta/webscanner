#!/bin/bash

unix="$(date +%s)"
folderMerged=/home/daredevil/SCAN/merged
pdfMergedFile=$folderMerged/merged.pdf

cp $pdfMergedFile $folderMerged/saved_$unix.pdf
echo 
echo "Saved PDF file: $folderMerged/saved_$unix.pdf"
