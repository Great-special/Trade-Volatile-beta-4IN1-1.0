import MetaTrader5 as mt5
from liveData import getAccountInfo, getSymbolsInfo

from rules import isCondition
from v100 import v100Condition
from v75 import v75Condition
from v100_1s import v100_1sCondition

# from Conditions import Condition


''' work error
        # for index, row in df.iterrows():
    #     # print(index, row['signal'])
        # if index + no_after == length and row['signal'] == 2:
        #     pos_type = 2
        #     close_price = row['close']
        #     # print(close_price, 'close price')
        #     low_price = row['low']
        #     # print(low_price, 'low price')
        #     # print("buy")
            
        # elif index + no_after == length and row['signal'] == 1:
        #     pos_type = 1
        #     close_price = row['close']
        #     # print(close_price, 'close price')
        #     high_price = row['high']
        #     # print(high_price, 'high price')
        #     # print("sell")
        # else:
        #     continue
    
    # print('Here.......', index)
        
'''

def entries_ST(df, symbol):
    request_list = []
    length = len(df)
    no_after = 1
    
    if symbol == 'Volatility 75 Index':
        v75Condition(df)
    elif symbol == 'Volatility 100 Index':
        v100Condition(df)
    elif symbol == 'Volatility 100 (1s) Index':
        v100_1sCondition(df)

    # Condition(df, symbol)
    
    acc_info = getAccountInfo()
    li_acc_info = acc_info[1]

    print(df.iloc[-2, -3], 'atr')
    # print(df.iloc[-2, 8], 'ATR')
    print(df.columns)
    print(df.tail(2))
    info_sym = mt5.symbol_info(symbol)
    lot_min = info_sym.volume_min 
    tick_val = info_sym.trade_tick_value  
    pos_type = 0       
    
    
    for key in li_acc_info:
        global acc_bal
        acc_bal = key.get('Balance')
        leverage = key.get('Leverage')
    
    # Getting or Checking for Signal to enter the market (-1) == signal column | df.signal[-2]
    print(df.iloc[-2, -1], 'iloc')
    if df.iloc[-2, -1]  == 2: 
        pos_type = 2
        close_price = df.iloc[-2, -7]
        print(close_price, 'close price')
        low_price = df.iloc[-2, 3]
    elif df.iloc[-2, -1] == 1:
        pos_type = 1
        close_price = df.iloc[-2, -7]
        print(close_price, 'close price')
        high_price = df.iloc[-2, 2]


    if pos_type != 0:
        # print("pos_type")
        request_list.append(symbol)
        request_list.append(pos_type)
        
        # print('bal and lot size')
        # print('bal.....', acc_bal)
        
        if acc_bal >= 5 and acc_bal < 30:
            lot = lot_min
            request_list.append(lot)
        
        if acc_bal >= 30 and acc_bal < 60:
            lot = lot_min * 2
            request_list.append(lot)
            
        if acc_bal >= 60 and acc_bal < 90:
            lot = lot_min * 3
            request_list.append(lot)
            
        if acc_bal >= 90 and acc_bal < 140:
            lot = lot_min * 4
            request_list.append(lot)
            
        if acc_bal >= 140 and acc_bal < 190:
            lot = lot_min * 5
            request_list.append(lot)
            
        if acc_bal >= 190 and acc_bal < 240:
            lot = lot_min * 7
            request_list.append(lot)
            
        if acc_bal >= 240 and acc_bal < 320:
            lot = lot_min * 9
            request_list.append(lot)
            
        if acc_bal >= 320  and acc_bal < 640:
            lot = lot_min * 11
            request_list.append(lot)
            
        if acc_bal >= 640 and acc_bal < 1280:
            lot = lot_min * 13
            request_list.append(lot)
            
        if acc_bal >= 1280 and acc_bal < 2560:
            lot = lot_min * 15
            request_list.append(lot)
            
        if acc_bal >= 2560 and acc_bal < 5120:
            lot = lot_min * 17
            request_list.append(lot)
            
        if acc_bal >= 5120 and acc_bal < 7680:
            lot = lot_min * 19
            request_list.append(lot)
            
        if acc_bal >= 7680 and acc_bal < 9600:
            lot = lot_min * 21
            request_list.append(lot)
            
        if acc_bal >= 9600 and acc_bal < 12100:
            lot = lot_min * 23
            request_list.append(lot)
        
        if acc_bal >= 12100 and acc_bal < 14100:
            lot = lot_min * 25
            request_list.append(lot)
        
        if acc_bal >= 14100 and acc_bal < 17100:
            lot = lot_min * 27
            request_list.append(lot)
            
        if acc_bal >= 17100 and acc_bal < 19500:
            lot = lot_min * 28
            request_list.append(lot)
            
        if acc_bal >= 19500 and acc_bal < 22500:
            lot = lot_min * 29
            request_list.append(lot)
        
        if acc_bal >= 22500:
            lot = lot_min * 31
            request_list.append(lot)

                        
        # Getting the ATR value for Stops and Tragets (-3 or 8) == ATR | row['ATR']
        if symbol == 'Volatility 75 Index': # * 0.5
            # print( row['ATR'], 'ATR')
            sltp_ratio = df.iloc[-2, -3]
            sl_range = df.iloc[-2, -3] 
            # print(sl_range, 'sl_range')
        if symbol == 'Volatility 100 Index': # * 0.7
            # print( row['ATR'], 'ATR')
            sltp_ratio = df.iloc[-2, -3]
            sl_range = df.iloc[-2, -3]
            # print(sl_range, 'sl_range')
        if symbol == 'Volatility 100 (1s) Index': #* 0.7
            # print( row['ATR'], 'ATR')
            sltp_ratio = df.iloc[-2, -3]
            sl_range = df.iloc[-2, -3]
            # print(sl_range, 'sl_range')
        
        
        price = mt5.symbol_info_tick(symbol).ask if pos_type == 2 else mt5.symbol_info_tick(symbol).bid
        # print('checking price')
                
        SL = low_price - sl_range if pos_type == 2 else high_price + sl_range
        TP = price + sltp_ratio if pos_type == 2 else price - sltp_ratio
    
    
        request_list.append(price)
        request_list.append(SL)
        request_list.append(TP)

        #print(request_list)
        
    return request_list 
    
        
