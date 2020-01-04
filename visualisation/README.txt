##################################################

#####  INSTRUCTIONS FOR VISUALISER.PY  ###########

##################################################


------- Requirements ----------

python (I've been using 3.6.9, don't know if other versions will work)

python packages
	
	pandas
	matplotlib


------- Usage ----------------

Has one positional arguments:

1) number-runs n = number of simulation runs which has to be a positive number

----- Example ----------------

python3 visualiser.py 1  // for one run of the simulation

--------Input & Output------

It will take n input csv files from multi-agent-system/csv with names test[0..n-1].csv
And will produce in the same folder n zips for each of the csv with names [0..n-1].zip
