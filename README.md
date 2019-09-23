# PortlandDataScience_StockMarket

## Description
This project was completed at the Appiled Stock Market Analysis Meetup Series of the Portland Data Science Meetup Group. We analyzed the relationship between presidential party and the performance of different stock market sectors, including Basic Industries, Energy, and Healthcare.

## System Requirements
Python 3.6.2, Pandas 0.20.3, Matplotlib 2.0.2, Numpy 1.13.3

## Implementation
We identified patterns in different sectors of the stock market when a presidental party changes from Democrat to Republican or Republican to Democrat. We also looked at if there were patterns in different months throughout the year-- if it is better to buy a stock during January or April. Future, we broked down stocks into different sectors to determine if some sectors (such as healthcare or basic industries) did better with one party whereas some do better with other parties. Overall, we did not find any patterns that were strong enough to dictate a succesful trading algorithm.

Results are shown below. The first plot shows the results for all data together (not broken down into sectors). The top plot shows the percentage change of the stock price for a given month after a transition from a democratic to republican president (blue) or a republican to democratic president (red). The bottom plot shows a histogram of the data so that we can confirm that the distribution is normal and there are not many outliers which could cause statistical irregularities.

![alt text](https://github.com/savanaconda/PortlandDataScience_StockMarket/blob/master/Results_AllData.png)

Below is the plot for the same results, but only for stocks in the Basic Industries sector.

![alt text](https://github.com/savanaconda/PortlandDataScience_StockMarket/blob/master/Results_BasicIndustries.png)

Below is the plot for the same results, but only for stocks in the Energy sector.

![alt text](https://github.com/savanaconda/PortlandDataScience_StockMarket/blob/master/Results_EnergySector.png)

Below is the plot for the same results, but only for stocks in the Healthcare sector.

![alt text](https://github.com/savanaconda/PortlandDataScience_StockMarket/blob/master/Results_HealthcareSector.png)
