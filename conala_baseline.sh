set -e

SDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WDIR=`pwd`
cd $WDIR

# Train and package seq2seq models on annotated+mined and annotated only data
for setting in annotmined annot; do

  # Train and test a seq2seq model
  xnmt --dynet-gpu $SDIR/config/$setting.yaml
  
  # Package the output in the appropriate way
  python $SDIR/preproc/seq2seq_output_to_code.py results/$setting.test.hyp conala-corpus/conala-test.json.seq2seq results/$setting.test.json

  # Calculate the BLEU score
  python $SDIR/eval/conala_eval.py --strip_ref_metadata --input_ref conala-corpus/conala-test.json --input_hyp results/$setting.test.json
  
  # Package the output for CodaLab
  cd $WDIR/results
  cp $setting.test.json answer.txt
  zip $setting.zip answer.txt

  cd $WDIR

done

# annotmined.zip and annot.zip can be submitted to the CodaLab leaderboard:
# 