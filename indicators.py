import pandas as pd # import the 'pandas' module for displaying data obtained in the tabular form
import pandas_ta as ta # import the 'ta' module for Trade Indicators
import pytz # import pytz module for working with time zone

import datetime as datetime

#df1.index = pd.DatetimeIndex(df1['time']) 
# df1 = pd.read_excel('v100/7 days/Volatility 100 Index m5.xlsx', parse_dates=True)



# df1['time'] = pd.to_datetime(df1['time'], unit='s')
# print(df1.columns)

# df1.index = pd.DatetimeIndex(df1['Local time']) 


# Moving Average Convergence/Divergence(MACD)
def macd(df):
    '''
        How the MACD works
        the macd is the difference between the slow_ema and the fast_ema 
        and the signal is the 9 period ema of the macd
    '''
    Df = df
    fast_ema = 12
    slow_ema = 26
    signal_period = 9
    
    #calculating MACD and signal
    Df['MACD'] = Df['close'].ewm(span=slow_ema, min_periods=slow_ema).mean() - Df['close'].ewm(span=fast_ema, min_periods=fast_ema).mean()
    Df['MACDsignal'] = Df['MACD'].ewm(span=signal_period, min_periods=signal_period).mean()
    
    return Df[['MACD', 'MACDsignal']]


# Average True Range(ATR)
def atr(df):
    '''
        ATR is calculated by getting the average value of the range, 
        which is the difference between the high and low values
        
    '''
    Df = df
    Df['ATR'] = ta.atr(high=Df.high, low=Df.low, close=Df.close, length=1) # 10 
    ATR_val = list(Df['ATR'])
    
    return ATR_val
    


# Relative Strength Index(RSI)
def rsi(df, period):
    '''
        RSI is 
        
    '''
    Df = df
    Df['RSI'] = ta.rsi(close=Df.close, length=period)
    RSI_val = list(Df['RSI'])
    
    return RSI_val
    

#Momentum
def momentum(df):
    '''
        Momentum is the difference between the current candle closing price
        and the closing price of a number of candle before it eg 15 bars or periods 
    '''
    Df = df
    Df['Momentum'] = ta.mom(close=Df.close, length=21)
    momentum_val = list(Df['Momentum'])
    
    return Df['Momentum']


# Standard Deviation(STD)
def std(df):
    Df = df
    deviation_period = 20
    Df['STD_20'] = Df['close'].rolling(deviation_period).std()
    
    return Df['STD_20']

# Exponet Moving Avg (SMA)
def sma_10(df):
    df['SMA_10'] = ta.sma(df.close, length=10, method='Linear Weight') # 10
    return df['SMA_10']


def stoch_osc(df):
    df['stoch_osc'] = ta.stoch(high=df.high, low=df.low, close=df.close, fast_k=60, slow_k=1, slow_d=1, mamode='Exponential')
    return df['stoch_osc']




# Market Direction
def market_direction(df, track, back_candles):
    upTrend = 2
    downTrend = 1
    for index in range(track - back_candles, 0, track + 1):
        if df.low[index] <= df.EMA_200[index]:
            upTrend = 0
        if df.high[index] >= df.EMA_200[index]:
            downTrend = 0
            
    if upTrend:
        return upTrend
    elif downTrend:
        return downTrend
    else:
        return 0


# Support function
def support(df, track, no_before, no_after):
    '''
        track is the candle of interest while no_before is the number of candles,
        before the candle of interest,
        no_after is the number of candles after the candle of interest
        track at 1 equals the frist candle in the data frame
        if the function returned 1 it equals true or level detected
    '''
    Df = df
    
    for i in range(track - no_before + 1, track + 1):
        if (Df.low[i] > Df.low[i-1]):
            return 0
    for i in range(track + 1, track + no_after + 1):
        if (Df.low[i] < Df.low[i-1]):
            return 0
    return 1


def closeSupport(l, levels, lim, df):
    '''
        Note that "l" is the index no of the candle of interest
        iloc is used to locate the index or row in the data frame
        1 = time, 2 = open, 3 = high, 4 = low, 5 = close 
    '''
    if len(levels) == 0:
        return 0
        
    how_close_is_low = abs(df.iloc[l, 4] - min(levels, key=lambda x: abs(x - df.iloc[l, 4]))) <= lim
    how_close_is_OC = abs(max(df.iloc[l, 2], df.iloc[l, 5]) - min(levels, key=lambda x: abs(x - df.iloc[l, 4]))) <= lim
    how_close_is_body = min(df.iloc[l, 2], df.iloc[l, 5]) < min(levels, key=lambda x: abs(x - df.iloc[l, 4]))
    
    if how_close_is_low or how_close_is_OC and how_close_is_body:
        return 2
    else:
        return 0


# Resistance function
def resistance(df, track, no_before, no_after):
    '''
        track is the candle of interest while no_before is the number of candles,
        before the candle of interest,
        no_after is the number of candles after the candle of interest
        track at 1 equals the frist candle in the data frame
        if the function returned 1 it equals true or level detected
    '''
    Df = df
    
    for i in range(track - no_before + 1, track + 1):
        if (Df.high[i] < Df.high[i-1]):
            return 0
    for i in range(track + 1, track + no_after + 1):
        if (Df.high[i] > Df.high[i-1]):
            return 0
    return 1


def closeResistance(l, levels, lim, df):
    '''
        Note that "l" is the index no of the candle of interest
        iloc is used to locate the index or row in the data frame
        1 = time, 2 = open, 3 = high, 4 = low, 5 = close 
    '''
    if len(levels) == 0:
        return 0
        
    how_close_is_high = abs(df.iloc[l, 3]- min(levels, key=lambda x: abs(x - df.iloc[l, 3]))) <= lim
    how_close_is_OC = abs(max(df.iloc[l, 2], df.iloc[l, 5]) - min(levels, key=lambda x: abs(x - df.iloc[l, 3]))) <= lim
    how_close_is_body = min(df.iloc[l, 2], df.iloc[l, 5]) < min(levels, key=lambda x: abs(x - df.iloc[l, 3]))
    
    if how_close_is_high or how_close_is_OC and how_close_is_body:
        return 1
    else:
        return 0


# swingLow
def swingLow(df, track):
    no_before = 3
    no_after = 2
    for i in range(track - no_before + 1, track + 1):
        if (df.low[i] < df.low[i-1]):
            swLow =  df.iloc[i-1, 4]
            return 2
        else:
            return 0
    for i in range(track + 1, track + no_after + 1):
        if (df.low[i] < df.low[i-1]):
            return 2
        else:
            return 0
    
# swingHigh
def swingHigh(df, track):
    no_before = 3
    no_after = 2
    for index in range(track - no_before + 1, track + 1):
        if (df.high[index] > df.high[index-1]):
            swHigh =  df.iloc[index-1, 3]
            return 1
        else:
            return 0
    for index in range(track + 1, track + no_after + 1):
        if (df.high[index] > df.high[index-1]):
            return 1
        else:
            return 0


#Candle Stick Patterns
def priceRejection(l, open_, high, close, low, high_diff, body_diff, low_diff, h_ratio, lo_ratio):
    row = l
    
    high_diff[row] = high[row] - max(open_[row], close[row])
    mid_diff = high[row] - low[row]

    body_diff[row] = abs(open_[row] - close[row])
    low_diff[row] = min(open_[row], close[row]) - low[row]

    mybodyDiff = mid_diff / 9
 
    
    if body_diff[row] < mybodyDiff:
        body_diff[row] = mybodyDiff
           
    
    h_ratio[row] = high_diff[row] / body_diff[row] # for selling signal
    
    lo_ratio[row] = low_diff[row] / body_diff[row] # for buying signal

    
    #sell signal Hammer 
    if h_ratio[row] >= 2.5 and low_diff[row] <= body_diff[row] and body_diff[row]>= mybodyDiff:
        return 1
        
    #buy signal shooting star
    elif lo_ratio[row] >= 2.5 and high_diff[row] <= body_diff[row] and body_diff[row]>= mybodyDiff:
        return 2       
    else:
        return 0
    

def candle_type(row, open_, close):
    if open_[row] > close[row]:
        return 1
    elif open_[row] < close[row]:
        return 2
    


def DarkLine(l, open_, close, low,  high, body_diff): # works more on buys 
    row = l
    
    body_diff[row] = abs(open_[row] - close[row])
    
    candle_size = abs(high[row] - low[row])
    ideal_body_diff = candle_size / 2
    
    if body_diff[row] < ideal_body_diff:
        body_diff[row] = ideal_body_diff
    
    body_diffmin = 1.0
    
    mid = body_diff[row-1] * 0.6
    mid_lvl = max(open_[row-1], close[row-1]) - mid
   
    
    #selling signal Dark Cloud
    if (body_diff[row] > body_diffmin and body_diff[row-1] > body_diffmin and 
        open_[row] > close[row] and open_[row - 1] < close[row] and open_[row] > close[row-1] and close[row] <= mid_lvl
        ):
        
        return 1
    
    #buy signal Piercing Line
    if (body_diff[row] > body_diffmin and body_diff[row-1] > body_diffmin and
        open_[row] < close[row] and open_[row-1] > close[row] and open_[row] < close[row-1] and close[row] >= mid_lvl
        ):
        
        return 2
    


def Engulfing(l, close, open_, body_diff):
    row = l
    
    body_diff[row] = abs(open_[row]-close[row])
   
    if body_diff[row] < 0.01:
        body_diff[row] = 0.01
    
    body_diffmin = 0.02
    
    #selling signal
    if (body_diff[row] > body_diffmin and body_diff[row-1] > body_diffmin and
        open_[row - 1] < close[row - 1] and open_[row] > close[row] and
        close[row-1] <= open_[row]):
        
        return 1
    
    #buying signal
    elif(body_diff[row] > body_diffmin and body_diff[row-1] > body_diffmin and
        open_[row-1] > close[row-1] and open_[row] < close[row] and
        close[row-1] <= open_[row]):
        
        return 2
        
    else:
        return 0
    

def Harami(l, close, open_, low,  high, body_diff): # works more on sells but better with a buy
    row = l
    body_diff[row] = abs(open_[row] - close[row])
    prv_body_diff = abs(open_[row-1] - close[row-1])
    
    prv_candle_size = abs(high[row-1] - low[row-1])
    prv_ideal_body_diff = prv_candle_size / 2
    
    cur_candle_size = abs(high[row] - low[row])
    cur_ideal_body_diff = cur_candle_size / 2
    
    C6 = high[row] <= high[row-1]
    C7 = low[row] >= low[row-1]
    
    
    # selling signal
    if (open_[row-1] < close[row-1] and open_[row] > close[row] and close[row-1] > open_[row] and open_[row-1] < close[row]):
        return 1
    
    # buying signal
    if (open_[row-1] > close[row-1] and open_[row] < close[row] and close[row-1] < open_[row] and open_[row-1] > close[row]):
        return 2
    



#Trending functions
def trendLine(df, candle_id, back_candles):
    
    back_range = int(back_candles/2)
    window = 5
    
    opt_back_candles = back_candles
    sldiff = 10000
    sldist = 10000
    
    for r1 in range(back_candles-back_range, back_candles+back_range):
        
        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])
    
        for i in range(candle_id - back_candles, candle_id + 1, window):
            minim = np.append(minim, df.low.iloc[i : i + window].min())
            xxmin = np.append(xxmin, df.low.iloc[i : i + window].idxmin())

        for i in range(candle_id - back_candles, candle_id + 1, window):
            maxim = np.append(minim, df.low.iloc[i : i + window].max())
            xxmax = np.append(xxmin, df.low.iloc[i : i + window].idxmax())
        
        slmin, intercmin = np.polyfit(xxmin, minim, 1)
        slmax, intercmax = np.polyfit(xxmax, maxim, 1)
        
        dist = (slmax*candle_id + intercmax) - (slmin*candle_id + intercmin)
        if dist < sldist: #abs(slmin - slmax) < sldiff
            #sldiff = abs(slmin-slmax)
            sldist = dist
            opt_back_candles = r1
            slmin_opt = slmin
            slmax_opt = slmax
            intercmin_opt = intercmin
            intercmax_opt = intercmax
            maxim_opt = maxim.copy()
            minim_opt = minim.copy()
            xxmin_opt = xxmin.copy()
            xxmax_opt = xxmax.copy()
            
        
    # print(opt_back_candles)
    #fitting intercepts to warp highest or lowest candle point
    adjust_intercmin = (df.low.iloc[xxmin_opt] - slmin_opt * xxmin_opt).min()
    adjust_intercmax = (df.high.iloc[xxmax_opt] - slmax_opt * xxmax_opt).max()
    # print(adjust_intercmin, 'ADJ InterMIN')
    # print(adjust_intercmax, 'ADJ InterMAX')
    
    return adjust_intercmax, adjust_intercmin


