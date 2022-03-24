# KryptoOracle: A Real-Time Cryptocurrency Price Prediction Platform Using Twitter Sentiments

The source code repository for the IEEE Big Data 2019 workshop publication: https://arxiv.org/abs/2003.04967.

KryptoOracle, a novel real-time and adaptive cryptocurrency price prediction platform based on Twitter sentiments. The integrative and modular platform is based on (i) a Spark-based architecture which handles the large volume of incoming data in a persistent and fault tolerant way; (ii) an approach that supports sentiment analysis which can respond to large amounts of natural language processing queries in real time; and (iii) a predictive method grounded on online learning in which a model adapts its weights to cope with new prices and sentiments.

The jupyter notebooks (1-4) must be executed in order. They obtain historical twitter data, perform preprocessing to clean it and perform sentiment analysis using VADER to obtain a compound score. Further, they obtain the cryptocurrency price data. Both datas are moved to seperate csv files.

Next the first half of notebook 6 must be executed. This will load the data, process it to obtain features, setup the Spark context and load the processed data into Spark. It will also bootstrap the ML model by using the processed data. This will make the model ready for making future predictions.

Next notebook 6 must be executed. This will launch the Twitter streamer that will fetch the real-time tweets and obtain sentiment scores.

Lastly, the second half of notebook 5 must be executed. This will launch the prediction engine which will make a price prediction based on the last minute twitter scores and then retrain the model once the actual price value arrives a minute later.


The 'validation_script.py' was run for a few weeks to accumulate the twitter data for bootstrapping the model.

We give acknowledgement to the Github repo: https://github.com/Drabble/TwitterSentimentAndCryptocurrencies. It helped us obtain starter code which we were able to extend further to create this project.

## Citation
If you find this work useful, please cite:

```
@INPROCEEDINGS{9006554,
  author={S. {Mohapatra} and N. {Ahmed} and P. {Alencar}},
  booktitle={2019 IEEE International Conference on Big Data (Big Data)}, 
  title={KryptoOracle: A Real-Time Cryptocurrency Price Prediction Platform Using Twitter Sentiments}, 
  year={2019},
  volume={},
  number={},
  pages={5544-5551},
  doi={10.1109/BigData47090.2019.9006554}}
```
