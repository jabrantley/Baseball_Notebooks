This is a collection of notebooks related to baseball analysis. Some are more about the techniques and others are about interesting baseball stuff. The first several notebooks have to do with predicting on-base percentage (OBP). If there is one metric that has persisted into the post-moneyball era into today's statcast era, its the value of OBP. 

| Notebook | Description |
| :---     | :---        |
| 1_PredictingOBP-ML.ipynb| Prediciting end of season OBP given early season data. Focuses on regression and simple ML techniques |
| 2_PredictingOBP-EmpericalBayes.ipynb | This adapts code from my [Emperical Bayes repo](https://github.com/jabrantley/EmpericalBayes-Baseball) to estimate OBP using the same technique used for batting average. Does a shrunken estimate that accounts for plate appearances approximately estimate end of season OBP?|
| 3_PredictingOBP-ARIMA-Forecasting-basic.ipynb | Instead of a classic train/test split using ML, we use a running OBP to try to forecast out to the end of season. This notebook only considers using past OBP to predict future OBP w/o any additional exogenous variables | 
| 4__PredictingOBP-ARIMA-Forecasting-addExog.ipynb | Similar to the last notebook but we introduce exogenous variables to facilitate the forecasting. | 
| 5_OBP_to_SLG.ipynb | OPS is a common metric but it is often critized since the denominators of on-base % and slugging % are different, making the addition mathematically... eh. My question is, what is the relationship between the two? How much is 1 point of OBP worth compared to 1 point of slugging %?
| 6_6_TheBook-Chapter1.ipynb | This notebook replicates some of the tables in Chapter 1 of  "The Book" by Tom Tango et al. e.g., run expectancy, wOBA