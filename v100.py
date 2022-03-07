from indicators import *
'''
    Momentum for v100 h1 is 56 and rsi 14 and atr 14
    while momentum for H4 is between 21 and 56 but 56 has fewer trades and better signals
'''


def v100Condition(df):
    '''
        for signals 2 is a buy signal while 1 is a sell signal
        high_diff = high different
        low_diff = low difference
        l_ratio = low ratio
    '''
    
    df = df
    df_length = len(df)
    high = list(df['high'])
    low = list(df['low'])
    close = list(df['close'])
    open_ = list(df['open'])
    signal = [0] * df_length
    high_diff = [0] * df_length
    low_diff = [0] * df_length
    body_diff = [0] * df_length
    h_ratio = [0] * df_length
    lo_ratio = [0] * df_length
    
    
    rsi(df, 21)
    
    no_before = 3 
    no_after = 2
    backCandles = 15 #45 or 90 or 180 use for checking backward if the structure occurred thus the higher the backcandle the number of levels
    lookback = backCandles*2
    # print(df_length)
    
    # print(df.tail(2))
    
    sup_lvl = []
    resist_lvl = []
    
    # Finding Structure from data candles
    for row in range(backCandles, len(df)-no_after):
       
        for subrow in range(row - backCandles + no_before, row + 1):
          
            if support(df, subrow, no_before, no_after):
                sup_lvl.append(df.low[subrow])
                
            if resistance(df, subrow, no_before, no_after):
                resist_lvl.append(df.high[subrow])
        
    sup_lvl.sort()
    resist_lvl.sort()
    
    # Checking to see if structure is too close | sorting
    for i in range(len(sup_lvl)):
        if i >= len(sup_lvl):
            break
        elif abs(sup_lvl[i] - sup_lvl[i-1]) <= 1.0:
            sup_lvl.pop(i)
    for i in range(len(resist_lvl)):
        if i >= len(resist_lvl):
            break
        elif abs(resist_lvl[i] - resist_lvl[i-1]) <= 1.0:
            resist_lvl.pop(i)
        
        
    # Checking for Conditions
    for current_candle in range(len(df)-lookback, len(df)):
        # Selling signal
        if (Engulfing(current_candle, close, open_, body_diff) == 1 and closeResistance(current_candle, resist_lvl, 1.0, df) == 1):  #DarkLine(row, close, open_, body_diff) == 1 or Harami(row, close, open_, body_diff) == 1 or
            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] < 0  or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50  ): # df['MACD'][row] < df['MACDsignal'][row] or df['MACDsignal'][row] <= 0 // df['RSI'][row] < 90 and df['RSI'][row] > 50  // \\ 
                signal[current_candle] = 1
        
        elif priceRejection(current_candle, open_, high, close, low, high_diff, body_diff, low_diff, h_ratio, lo_ratio) == 1 and closeResistance(current_candle, resist_lvl, 1.0, df) == 1:
            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] < 0  or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50  ):
                signal[current_candle] = 1

        elif (DarkLine(current_candle, close, open_, low, high, body_diff) == 1 and closeResistance(current_candle, resist_lvl, 0.9, df) == 1):
            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50  ):  
                signal[current_candle] = 1
        
        elif (Harami(current_candle, close, open_, low,  high, body_diff) == 1 and closeResistance(current_candle, resist_lvl, 1.0, df) == 1):
            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] < 0 or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50 ):  
                signal[current_candle] = 1
                
        # Buying signal     
        elif(Engulfing(current_candle, close, open_, body_diff) == 2 and closeSupport(current_candle, sup_lvl, 0.9, df) == 2 ): # DarkLine(row, close, open_, body_diff) == 2 or
            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] > 0 or df['RSI'][current_candle] < 50 and df['RSI'][current_candle] > 20 ): # df['MACD'][row] > df['MACDsignal'][row] or df['MACDsignal'][row] >= 0 //  df['RSI'][row] < 50 and df['RSI'][row] > 10 //\\ 
                signal[current_candle] = 2
                
        elif (priceRejection(current_candle, open_, high, close, low, high_diff, body_diff, low_diff, h_ratio, lo_ratio) == 2 and closeSupport(current_candle, sup_lvl, 1.3, df) == 2):
            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] > 0 or df['RSI'][current_candle] < 50 and df['RSI'][current_candle] > 20 ): 
                signal[current_candle] = 2
                
        elif (DarkLine(current_candle, close, open_, low, high, body_diff) == 2 and closeSupport(current_candle, sup_lvl, 1.0, df) == 2):
            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle]  or df['RSI'][current_candle] < 50 and df['RSI'][current_candle] > 20 ): 
                signal[current_candle] = 2
        
        elif(Harami(current_candle, close, open_, low,  high, body_diff) == 2 and closeSupport(current_candle, sup_lvl, 0.9, df) == 2):
            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] > 0  ): 
                signal[current_candle] = 2
                
        else:
            signal[current_candle] = 0
        df['signal'] = signal
    
    # print(df.tail(2))   
    # print(sup_lvl, 'sup_lvl')
    # print(resist_lvl, 'resist_lvl')
   
    return signal


'''
        if (Engulfing(current_candle, close, open_, body_diff) == 1 and closeResistance(current_candle, resist_lvl, 1.0, df) == 1):  #DarkLine(row, close, open_, body_diff) == 1 or Harami(row, close, open_, body_diff) == 1 or
            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] < 0  or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50  ): # df['MACD'][row] < df['MACDsignal'][row] or df['MACDsignal'][row] <= 0 // df['RSI'][row] < 90 and df['RSI'][row] > 50  // \\ 
                signal[current_candle] = 1
        
        elif priceRejection(current_candle, open_, high, close, low, high_diff, body_diff, low_diff, h_ratio, lo_ratio) == 1 and closeResistance(current_candle, resist_lvl, 1.0, df) == 1:
            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] < 0  or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50  ):
                signal[current_candle] = 1

        elif (DarkLine(current_candle, close, open_, body_diff) == 1 and closeResistance(current_candle, resist_lvl, 0.2, df) == 1):
            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] < 0  or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50  ):  
                signal[current_candle] = 1
        
        elif (Harami(current_candle, close, open_, body_diff) == 1 and closeResistance(current_candle, resist_lvl, 1.0, df) == 1):
            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] < 0  or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50  ):  
                signal[current_candle] = 1
                
        # Buying signal     
        elif(Engulfing(current_candle, close, open_, body_diff) == 2 and closeSupport(current_candle, sup_lvl, 0.9, df) == 2 ): # DarkLine(row, close, open_, body_diff) == 2 or
            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] > 0 or df['RSI'][current_candle] < 50 and df['RSI'][current_candle] > 20 ): # df['MACD'][row] > df['MACDsignal'][row] or df['MACDsignal'][row] >= 0 //  df['RSI'][row] < 50 and df['RSI'][row] > 10 //\\ 
                signal[current_candle] = 2
                
        elif (priceRejection(current_candle, open_, high, close, low, high_diff, body_diff, low_diff, h_ratio, lo_ratio) == 2 and closeSupport(current_candle, sup_lvl, 0.9, df) == 2):
            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] > 0 or df['RSI'][current_candle] < 50 and df['RSI'][current_candle] > 20 ): 
                signal[current_candle] = 2
                
        elif (DarkLine(current_candle, close, open_, body_diff) == 2 and closeSupport(current_candle, sup_lvl, 0.1, df) == 2):
            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] > 0 or df['RSI'][current_candle] < 50 and df['RSI'][current_candle] > 20 ): 
                signal[current_candle] = 2
        
        elif(Harami(current_candle, close, open_, body_diff) == 2 and closeSupport(current_candle, sup_lvl, 0.9, df) == 2):
            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] > 0 or df['RSI'][current_candle] < 50 and df['RSI'][current_candle] > 20 ): 
                signal[current_candle] = 2
                
        else:
            signal[current_candle] = 0
        df['signal'] = signal
'''

'''
            if (Harami(current_candle, close, open_, body_diff) == 1 and 
                closeResistance(current_candle, resist_lvl, 1.0, df) == 1): #DarkLine(row, close, open_, body_diff) == 1 or

            if (df['Momentum'][current_candle] < 0 and df['MACD'][current_candle] < df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] < 0  or df['RSI'][current_candle] < 80 and df['RSI'][current_candle] > 50  ): # df['MACD'][row] < df['MACDsignal'][row] or df['MACDsignal'][row] <= 0 // df['RSI'][row] < 90 and df['RSI'][row] > 50  // \\ 
                signal[current_candle] = 1
        
        # Buying signal     
        elif (Harami(current_candle, close, open_, body_diff) == 2 and 
                closeSupport(current_candle, sup_lvl, 0.9, df) == 2): # DarkLine(row, close, open_, body_diff) == 2 or

            if (df['Momentum'][current_candle] > 0 and df['MACD'][current_candle] > df['MACDsignal'][current_candle] or df['MACDsignal'][current_candle] > 0 or df['RSI'][current_candle] < 50 and df['RSI'][current_candle] > 20 ): # df['MACD'][row] > df['MACDsignal'][row] or df['MACDsignal'][row] >= 0 //  df['RSI'][row] < 50 and df['RSI'][row] > 10 //\\ 
                signal[current_candle] = 2
                
        else:
            signal[current_candle] = 0
    df['signal'] = signal
'''