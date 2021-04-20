import datetime as dt
import pandas_datareader.data as web
import numpy as np

print("""
               Comparing Trading Philosophies: 
         "Time in the Market" VS "Timing the Market" 
         -------------------------------------------\n""")

print("""We will compare three trading strategies.
      
Case 1 - (Buy and Hold):
Buy stocks every 30 days in the price of 6000$.

Case 2 - (Dollar-Cost Averaging): 
Buy stocks every 5 days in the price of 1000$.

Case 3 - (Value Investing):
Using the same amount of cash, case 3 will try to predict the market and buy mostly when below market value using 241 days moving average and polynomial fitting. """ )

ticker = str(input('\nPlease enter Yahoo finance stock-ticker (at least 3 years old):') or "SPY")  

print('\n------------------------------------------------------------------\n')
print('\nCALCULATING...\n')

start = dt.datetime(1999,1,1)
end = dt.datetime.today()
df = web.DataReader(ticker, 'yahoo', start, end)

Total_len = len(df.index)
df['NumIndex'] = list(range(len(df.index)))
MA241 = [None]*Total_len


location = S_location = int(2000)
Stocks_BnH = Stocks_DCA = Stocks_Smart = Cash  = int(0)
#-------------------------------------------------------------------------

def Buy( df, index, cash ):
    stocks = cash/df['Adj Close'][index]
    return stocks

def Sell( df, index, stocks ):
    cash = stocks*df['Adj Close'][index]
    return cash

def BnH( df, index):
    if df['NumIndex'][index]%30 == 0:
        stocks = Buy( df, index, 6000)
        return stocks
    else: 
        return 0

def DCA( df, index):
    if df['NumIndex'][index]%5 == 0:
        stocks = Buy( df, index, 1000)
        return stocks
    else: 
        return 0
    
def SMART( df, index, cash2, AllStocks):
    
    MA241[0:index] = df['Adj Close'][0:index].rolling(window=241,center = True).mean()
    pol_coeff = np.polyfit(df['NumIndex'][120:index-120], MA241[120:index-120], 2)
    yfit = np.poly1d(pol_coeff)
    cash=int(0)
    
    if df['NumIndex'][index]%30 == 0:
        cash +=6000
        
    if yfit(index) >= df['Adj Close'][index]:
        if df['Adj Close'][index]/yfit(index) <= 0.85:
            stocks = Buy( df, index, cash + 0.8*cash2)
            return -0.8*cash2, stocks
        else:
            stocks = Buy( df, index,cash +0.05*cash2)
            return -0.05*cash2, stocks
    else:
        if df['Adj Close'][index]/yfit(index) <= 1.05:
            stocks = Buy( df, index, 0.95*cash)
            return 0.05*cash, stocks
        elif df['Adj Close'][index]/yfit(index) >= 1.4:
            sh = Sell( df, index, 0.01*AllStocks )
            cash += sh
            return cash, -0.01*AllStocks
        else:
            return cash, 0
            
#-------------------------------------------------------------------------        
            
while df['NumIndex'][location] < Total_len-1:
    Stocks_BnH += BnH(df,location)
    Stocks_DCA += DCA(df,location)
    sh, st = SMART(df, location, Cash, Stocks_Smart)
    Cash +=sh
    Stocks_Smart += st
    location +=1

if Cash != 0:
    st= Buy( df, location, Cash)
    Stocks_Smart += st

df['MA241'] = MA241
df.to_csv(ticker+'.csv')

percent1 = (Stocks_DCA/Stocks_BnH-1)*100
percent2 = (Stocks_Smart/Stocks_BnH-1)*100
Years = (location-S_location)/365
Months = (Years%1)*12
sdate = df.index[S_location].strftime("%d-%m-%Y")
edate = df.index[location].strftime("%d-%m-%Y")


print('For the Yahoo finance stock-ticker', ticker, ':\n')
print('Start Date: ',sdate,'\nEnd Date:   ',edate, '\nTime Runing:', "%.0f Years and" %Years, "%.0f Months" %Months )
print('\n\nThe amount of stocks each strategy acquired:\n') 
print('Buy and Hold:          ', "%.2f" %Stocks_BnH, '..... (Default)' ) 
print('Dollar-Cost Averaging: ', "%.2f" %Stocks_DCA, "..... %.3f" %percent1, '% from default')
print('Value Investing:       ', "%.2f" %Stocks_Smart, "..... %.3f" %percent2, '% from default')

if Stocks_BnH > Stocks_DCA and Stocks_BnH > Stocks_Smart:
    print('\nThe winning strategy for this run is: Buy and Hold.')
elif Stocks_DCA > Stocks_BnH and Stocks_DCA > Stocks_Smart:
    print('\nThe winning strategy for this run is: Dollar-Cost Averaging.')
else:
    print('\nThe winning strategy for this run is: Value Investing.')

print('\n------------------------------------------------------------------')
input('Press ENTER to exit')





 

