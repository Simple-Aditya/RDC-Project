Python version 3.10 required, I worked with 3.10.12

first create a fresh virtual environment preferably and run
pip install -r .\req.txt

then, run either of the .py files

BERT prediction file uses the BERT neural network to convert text to numbers

tfidf prediction file uses tfidf algortithm for text to number conversion

I used BERT one but you can use both to check which is giving better results

then rest lreg_finetuned.pkl and logreg_pipeline.pkl are model files 
and labels.pkl is used for mapping numeric prediction to dark pattern category

contact if any errors arise