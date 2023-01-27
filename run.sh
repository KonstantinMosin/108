protoc --python_out=. ./proto/message.proto
python3 -m unittest ./tests/test_pd.py
python3 -m unittest ./tests/test_dmsp.py
