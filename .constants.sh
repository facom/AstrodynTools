echo > .constants
for line in $(egrep -v "^\"" constants.py)
do
    variable=$(echo $line | cut -f 1 -d "=")
    echo "double $variable;" >> .constants
done
