from datetime import datetime
from openpyxl.workbook import Workbook
import MetaTrader5 as mt5
import pandas as pd # import the 'pandas' module for displaying data obtained in the tabular form
import pytz # import pytz module for working with time zone


# get account info and details
def getAccountInfo():
    list_account_info = []
    account_info=mt5.account_info() 
    #account_info_dict = mt5.account_info()._asdict()
    
    if account_info!=None:
        account_id = account_info.login
        account_name = account_info.name
        account_server = account_info.server
        account_leverage = account_info.leverage
        account_balance = account_info.balance
        account_equity = account_info.equity
        account_profit = account_info.profit
        
        list_account_info.append(
            {
                'Login Id': account_id,
                'Name': account_name,
                'Server': account_server,
                'Leverage': account_leverage,
                'Balance': account_balance,
                'Equity': account_equity,
                'Profit': account_profit,
            }
        )
    
    # convert the dictionary into DataFrame and print
    acc_info_df=pd.DataFrame(list_account_info, columns=['Login Id', 'Name', 'Server', 'Leverage', 'Balance', 'Equity', 'Profit'])
    #acc_info_df.to_excel('Account info.xlsx')
    # print(acc_info_df)
    return acc_info_df, list_account_info



# get all symbols and their info
def getSymbolsInfo():
    symbols = mt5.symbols_get()
    # print('Symbols: ', len(symbols))
    list_symbols_info = []
    count=0
    # display the first five ones
    for sym in symbols:
        count+=1
        
        #display symbol properties / info
        symbol_info = mt5.symbol_info(sym.name)
        
        if symbol_info!=None:
            symbol_name = symbol_info.name
            symbol_min_lotsize = symbol_info.volume_min  
            symbol_max_lotsize = symbol_info.volume_max
            symbol_tick_value = symbol_info.trade_tick_value   
            
            list_symbols_info.append({
                'symbolName': symbol_name,
                'symbolMinLot': symbol_min_lotsize,
                'symbolMaxLot': symbol_max_lotsize,
                'symbolTickValue' : symbol_tick_value
            })
             
    # convert the dictionary into DataFrame and print
    sym_info_df = pd.DataFrame(list_symbols_info)[['symbolName', 'symbolMinLot', 'symbolMaxLot', 'symbolTickValue']]
    #sym_info_df.to_excel('Symbols info.xlsx')
    # print(sym_info_df)
    return sym_info_df, list_symbols_info




# Getting Tradeable symbols, OHCL data to be saved as DataFrame 
def getTradeAble_Data():
 
    list_symbols = [
        'Volatility 75 Index',
        'Volatility 100 Index',
        'Volatility 100 (1s) Index',
        ]
    
    symbols_Data = []
    
    for symbol in list_symbols:
         
        M5_data = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1440)
        
        # create DataFrame out of the obtained data
       
        df_M5 = pd.DataFrame(M5_data)[['time', 'open', 'high', 'low', 'close']]
        symbols_Data.append({
                'symbolName': symbol,
                'df_M5' : df_M5,
            })
        
        # df_M5.to_excel(f'{symbol} m5.xlsx')
        # df_M15.to_excel(f'{symbol} m15.xlsx')
        
    return symbols_Data
