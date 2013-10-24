#!/bin/bash
# Run unit tests
START_TIME=$(date +%s)

echo "Running Scale Mapper unit tests"
python ./test_scale_mapper.py
#echo "Running Scale Reducer unit tests"
#python ./test_scale_reducer.py

# Run data tests
echo "Range Batting.csv"
cat ../testdata/baseball/Batting.csv | python ./scale_mapper.py --rangedata test_range_batting_reducer.tmp > test_scale_batting.tmp

echo ""; echo ""

#echo "Range Fielding.csv"
#cat ../testdata/baseball/Fielding.csv | python ./scale_mapper.py --rangedata test)range_fielding_reducer.tmp > test_scale_fielding.tmp
echo ""; echo ""

END_TIME=$(date +%s)
DIFF_SECONDS=$(( $END_TIME - $START_TIME ))
echo "Ran tests in $DIFF_SECONDS seconds"

