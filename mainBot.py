import MetaTrader5 as mt5
from liveData import getAccountInfo, getTradeAble_Data
from indicators import momentum, atr, rsi, macd
from trades import entries_ST
from alert import email_alert
import schedule
import time



# display data on the MetaTrader 5 package
# print("MetaTrader5 package author: ", mt5.__author__)
# print("MetaTrader5 package version: ", mt5.__version__)



# establish MetaTrader 5 connection to a specified trading account
if not mt5.initialize():
    # print("initialize() failed, error code = ", mt5.last_error())
    quit()
    


def startBot():
    timer_on = time.perf_counter()
    # print('Starting.......')
    fun_acc_info = getAccountInfo()
    li_acc_info = fun_acc_info[1]
    # print(li_acc_info)
    
    
    tradeables = getTradeAble_Data() 

    for index in tradeables:   
        symbolName = index.get('symbolName')
        df1 = index.get('df_M5')   

        macd(df1)
        momentum(df1)
        atr(df1)

        print('Sending df to trades')
        
        trade_request = entries_ST (df1, symbolName)
        
        print(['main bot'], trade_request)
        
        # symbol = 'Volatility 100 (1s) Index'
        # pos_type = 0
        # price = mt5.symbol_info_tick(symbol).ask 
        # point = mt5.symbol_info(symbol).point
        # SL = price - 3000 * point
        # TP = price + 3000 * point
        # lot = 0.2 
        # deviation = 1

        print('ready to process')
        if trade_request:
            print('processing.... [trade request]')
            symbol = trade_request[0]
            pos_type = trade_request[1] 
            lot = trade_request[2]
            price = trade_request[3]
            SL = trade_request[4]
            TP = trade_request[5]
            deviation = 1
            
           
            # send a trading request and Money Management
            for key in li_acc_info:
                accountBal = key.get('Balance')
                leverage = key.get('Leverage')

            risk = accountBal * 0.1 
            riskPerTrade = accountBal * 0.01
            action = mt5.TRADE_ACTION_DEAL
            orderType = mt5.ORDER_TYPE_BUY if pos_type == 2 else mt5.ORDER_TYPE_SELL 
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL, 
                "symbol": symbol, 
                "volume": lot, 
                "type": mt5.ORDER_TYPE_BUY if pos_type == 2 else mt5.ORDER_TYPE_SELL, 
                "price": price, 
                "sl": SL, 
                "tp": TP, 
                "deviation": deviation, 
                "magic": 606060, 
                "comment": "Trade Volatile V1", 
            } 
            # print(['main trades'], request)
            
            with open('Details of signal request.txt', 'a+') as file :
                file.write(str(request) + '\n')
                file.write(' ' + '\n')
                
            
            #Checking for open positions and number
            position_total = mt5.positions_total()
            position_symbol = mt5.positions_get(symbol = symbol)
            if position_total <= 8 and len(position_symbol) < 2:
                print('checking request')
                req_risk = mt5.order_calc_profit(orderType,symbol,lot,price,SL)
                order_risk = abs(req_risk)
                order_margin = mt5.order_calc_margin(action,symbol,lot,price)
                if order_risk <= risk:
                ## LAST EFFECT MUILT ##
                    if  accountBal < 100:
                        result = mt5.order_send(request)
                        print(result)
                        print('done !!!!')
                        with open('Details of signal result.txt', 'a+') as files :
                            files.write(str(result) + '\n' + 'DONE')
                            files.write(' ' + '\n')
                        # check the execution result
                        try:
                            # print("1. order_send(): by {} {} lots at {} with deviation = {} points".format(symbol, lot, price, deviation));
                            if result.retcode != mt5.TRADE_RETCODE_DONE:
                                # print("2. order_send failed, retcode = {}".format(result.retcode))
                                with open('error log.txt', 'a+') as error:
                                    error.write('retcode =' + str(result.retcode) + '\n')
                            else:
                                print("2. order_send  no retcode")   
                        except:
                            pass
                        
                    elif accountBal >= 100 and accountBal <= 1000:
                        result1 = mt5.order_send(request)
                        result2 = mt5.order_send(request)
                        with open('Details of signal result.txt', 'a+') as files :
                            files.write(str(result1) + '\n' + 'DONE')
                            files.write(' ' + '\n')
                        
                        # check the execution result
                        try:
                            # print("1. order_send(): by {} {} lots at {} with deviation = {} points".format(symbol, lot, price, deviation));
                            if result1.retcode != mt5.TRADE_RETCODE_DONE:
                                # print("2. order_send failed, retcode = {}".format(result1.retcode))
                                with open('error log.txt', 'a+') as error:
                                    error.write(f'retcode = {result1.retcode}')
                            else:
                                print("2. order_send  no retcode")   
                        except:
                            pass
                    elif accountBal >= 1000:
                        result1 = mt5.order_send(request)
                        result2 = mt5.order_send(request)
                        result3 = mt5.order_send(request)
                        with open('Details of signal result.txt', 'a+') as files :
                            files.write(str(result1) + '\n' + 'DONE')
                            files.write(' ' + '\n')

                        # check the execution result
                        try:
                            # print("1. order_send(): by {} {} lots at {} with deviation = {} points".format(symbol, lot, price, deviation));
                            if result1.retcode != mt5.TRADE_RETCODE_DONE:
                                # print("2. order_send failed, retcode = {}".format(result1.retcode))
                                with open('error log.txt', 'a+') as error:
                                    error.write(f'retcode = {result1.retcode}')
                            else:
                                print("2. order_send  no retcode")   
                        except:
                            pass
                else:
                    continue
    timer_off = time.perf_counter()
    print(f"// Finished processing in {round(timer_off - timer_on, 2)} second(s) //")


def Mail():
    accounts = getAccountInfo()
    msg = accounts[1][0]
    msg = str(msg)
    email_alert(msg)


def endBot():
    positions = mt5.positions_total()
    if positions == None:
        mt5.shutdown()
        quit()


def check():
    print("Checking ....  1 min")

# Task to do In time
def startTask():
    print('Starting in 5 minutes....')
    schedule.every(5).minutes.do(startBot)
    schedule.every(12).hours.do(Mail)
    schedule.every().saturday.at("23:59").do(endBot)
    

    start = True
    while start:
        schedule.run_pending()
        time.sleep(1)
            
        
# starting trading MainBot
startTask()