# test.sh
echo "Starting test..."
python -m unittest discover -s src 2>&1 | tee output.log
echo "Finished test..."