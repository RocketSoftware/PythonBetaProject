# UDT Locate vs Python Dictionary

Compare the use of the function Locate in Unidata vs the use of Python Dictionary variables


## Installation

The data source for this analisys was obtained from https://data.medicare.gov/data/physician-compare:
Physician_Compare_Databases.zip

```
unzip Physician_Compare_Databases.zip
```

Remove non ASCII characters:
```
sed -i  "s/[\xd0]//g" Physician_Compare_Databases_National_Downloadable_File.csv
sed -i  "s/[\xa3]//g" Physician_Compare_Databases_National_Downloadable_File.csv
sed -i  "s/[\xa1]//g" Physician_Compare_Databases_National_Downloadable_File.csv
sed -i  "s/[\x9d]//g" Physician_Compare_Databases_National_Downloadable_File.csv
sed -i  "s/[\xd1]//g" Physician_Compare_Databases_National_Downloadable_File.csv
sed -i  "s/[\x97]//g" Physician_Compare_Databases_National_Downloadable_File.csv
sed -i  "s/[\x99]//g" Physician_Compare_Databases_National_Downloadable_File.csv
sed -i  "s/[\x91]//g" Physician_Compare_Databases_National_Downloadable_File.csv
sed -i  "s/[\x85]//g" Physician_Compare_Databases_National_Downloadable_File.csv
```

Import the file into the Unidata table: PHYSICIAN

## Usage

There are two programs provided:

* Unidata:  BP COUNT.PHYSICIAN
* Python:  u2_physician.py

Run each program multiple times changing the "key" to create different breakdowns.

For example. Using the "States" as the "key", each program will sort by the count of records with the same state and provide as output the first 10 states in reverse order.

Python:
```
%./u2_physician.py

2108619 records selected to list 0.

CA => 172339
TX => 163622
PA => 158371
OH => 151319
NY => 133351
FL => 100909
IL => 79985
MA => 70689
MI => 70008
MN => 53854
# of Categories: 58
Time: 30.024521589279175
```

Unidata:
```
:COUNT.PHYSICIAN
CA => 172339
TX => 163622
PA => 158371
OH => 151319
NY => 133351
FL => 100909
IL => 79985
MA => 70689
MI => 70008
MN => 53854

Record count: 2108619

Keys count: 58

Time: 16240ms  or  20.24s

```

Repeat this process by changing the "key". Examples: Key= Gender+State, Specialty, Grad Year, etc

## Resultere

The results were obvious as seen on the graph (LocateVsDictionary.png):
Python dictionaries consistently took about the same time to manipulate and count the sets. The time it took was between 30 to 40 seconds disregarding the amount of categories that the sets broke into.
Unidata's Locate produce better results as long as the number of categories were below 400. When the categories increased, the Locate function performed badly.

## Conclusion

This research shows that Python manipulates memory variables is a more efficient and consistent way than Unidata. This knowledge could help optimize code that manipulates large sets.
