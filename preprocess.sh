#!/bin/bash
set -e

SDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WDIR=`pwd`

# Get the data
wget http://www.phontron.com/download/conala-corpus-v1.1.zip
unzip conala-corpus-v1.1.zip

# Extract data 
cd $WDIR/conala-corpus

python $SDIR/preproc/extract_raw_data.py

python $SDIR/preproc/json_to_seq2seq.py conala-train.json.seq2seq conala-train.intent conala-train.snippet
python $SDIR/preproc/json_to_seq2seq.py conala-test.json.seq2seq conala-test.intent conala-test.snippet
python $SDIR/preproc/json_to_seq2seq.py conala-mined.jsonl.seq2seq conala-mined.intent conala-mined.snippet

# Split off a 400-line dev set from the training set
# Also, concatenate the first 100000 lines of mined data
for f in intent snippet; do
  head -n 400 < conala-train.$f > conala-dev.$f
  tail -n +401 < conala-train.$f > conala-trainnodev.$f
  cat conala-trainnodev.$f <(head -n 100000 conala-mined.$f) > conala-trainnodev+mined.$f
done

echo "Done with Preprocessing" 
