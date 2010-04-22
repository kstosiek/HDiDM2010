#!/bin/sh

# Mały skrypt do przerabiania danych w formacie metastock.

set -e

STOCKFILE="$1"
OUTPUTFILE="$2"

if [ ! $# -eq "2" ];
then
	echo "Usage: sh convert_stock_data.sh <stockfile> <outputfile>"
	exit 1
fi

echo "Clean up"

rm -rf $OUTPUTFILE
touch $OUTPUTFILE

echo "Unpack data"

TMPDIR="/tmp/mytempdirectory123"
rm -rf $TMPDIR

unzip -d $TMPDIR $STOCKFILE 1> /dev/null

echo "Generate output file"

for file in $TMPDIR/*;
do
	# Cut data a little bit.

	TMPFILE=$(mktemp /tmp/tmpfile.XXXXXX)

	cat -n $file | sort -nr | cut -f 2 | sed -n '1,300 p' > $TMPFILE
	cat $TMPFILE > $file

	# Generate new ONE file with stock data.

	STOCKNAME="$(cat $file | cut -d ',' -f 1 | sed -n '1,1 p')"
	printf "%s\n" $STOCKNAME >> $OUTPUTFILE

	for line in "$(cat $file | cut -d ',' -f 2,3)";
	do
		printf "%s\n" $line >> $OUTPUTFILE
	done
done

rm -rf $TMPFILE
rm -rf $TMPDIR

exit 0
