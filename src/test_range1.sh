#!/bin/bash
# Run unit tests
START_TIME=$(date +%s)

echo "Running Range Mapper unit tests"
python ./test_range_mapper.py
echo "Running Range Reducer unit tests"
python ./test_range_reducer.py

# Run data tests
echo "Range Batting.csv"
cat ../testdata/baseball/Batting.csv | python ./range_mapper.py --coltypes TNNTTNNNNNNNNNNNNNNNNNNN | sort | python ./range_reducer.py > test_range_batting.tmp
echo ""; echo ""

echo "Range Fielding.csv"
cat ../testdata/baseball/Fielding.csv | python ./range_mapper.py --coltypes TNNTTTNNNNNNNNNNNN | sort | python ./range_reducer.py > test_range_fielding.tmp
echo ""; echo ""

END_TIME=$(date +%s)
DIFF_SECONDS=$(( $END_TIME - $START_TIME ))
echo "Ran tests in $DIFF_SECONDS seconds"

