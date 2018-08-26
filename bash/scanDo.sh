#!/bin/bash

unix="$(date +%s)"
folder=/home/pi/SCAN
folderMerged=/home/pi/SCAN/merged
tiffFile=$folder/$unix.tiff
pdfFile=$folder/$unix.pdf
pdfMergedFile=$folderMerged/merged.pdf

scanimage --device "brother4:bus3;dev1" -l 0 -t 0 -x 215.9mm -y 355.6mm --source FlatBed --resolution 150 --mode="24bit Color[Fast]" --progress --verbose --format=tiff > $tiffFile
tiff2pdf -p A4 -j -q 90 -t "Document" -f -o $pdfFile $tiffFile
sed -i 's|/DecodeParms << /ColorTransform 0 >>||' $pdfFile
rm $tiffFile
ls $folder/*.pdf
pdftk $folder/*.pdf cat output $pdfMergedFile
echo 
echo "Merged PDF file: $pdfMergedFile"
