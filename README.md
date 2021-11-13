# NBA_Draft_Projections_Project

See requirements.txt for dependencies



## Creating ARFF files from Web Parser CSV Files

1. Edit the end of the file `csv_to_arff.py` to use the input file and output file names
2. Run the following code

```
$ python3 csv_to_arff.py
```

3. The output should be `Nominal Values: {array of nominal values found}`
4. Go to the output arff file and replace "string" attributes with values from the output of the python script
4. Remove all occurences of "'" char (apostraphe)