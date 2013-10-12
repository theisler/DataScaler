# Run unit tests
START_TIME=$(date +%s)

python ./test_classify_mapper.py
python ./test_classify_reducer.py

# Run data tests
echo "Classifying Batting.csv"
cat ../testdata/baseball/Batting.csv | python ./classify_mapper.py | sort | python ./classify_reducer.py > test_classify_batting.tmp
cat test_classify_batting.tmp | sort -n | sed "s/[0-9][0-9]*\t//" | tr -d "\n" > test_classify_batting_args.tmp
cat test_classify_batting_args.tmp
echo ""; echo ""

echo "Classifying Fielding.csv"
cat ../testdata/baseball/Fielding.csv | python ./classify_mapper.py | sort | python ./classify_reducer.py > test_classify_fielding.tmp
cat test_classify_fielding.tmp | sort -n | sed "s/[0-9][0-9]*\t//" | tr -d "\n" > test_classify_fielding_args.tmp
cat test_classify_fielding_args.tmp
echo ""; echo ""

END_TIME=$(date +%s)
DIFF_SECONDS=$(( $END_TIME - $START_TIME ))
echo "Ran tests in $DIFF_SECONDS seconds"
