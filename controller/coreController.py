from datetime import datetime,timezone,timedelta
from logging import Logger
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import config as conf
from controller.dataBaseController import DataBase

chrome_options = Options()

class Core :
    def exec(logger:Logger,url:str):
        db = DataBase()
        err,con = db.connect()
        tzoffset = timedelta(hours=-3)
        if conf.showBrowser == False:
                chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(conf.pathChromeDriver, options=chrome_options)        
        logger.info(f">> Configurando Chrome ...")
        driver.get(url)
        ultimo_good=''
        ultimo_bad=''
        last_state = 'G'
        fisrt = True
        entries = []
        bad_seguidos=True
        while True:
            sleep(1)
            try:
                goods = driver.find_element("xpath","//div[@class='entries']").find_elements("xpath","//span[@class='good']")
                bads = driver.find_element("xpath","//div[@class='entries']").find_elements("xpath","//span[@class='bad']")
            except Exception as e:
                driver.close()
                driver.get(url)
                sleep(5)
                logger.error(e)

            if fisrt:
                ultimo_good=goods[0].text
                ultimo_bad=bads[0].text
                fisrt=False
                pass
            else:
                if ultimo_good!=goods[0].text:
                    totals =driver.find_element("xpath","//div[@class='totals']")
                    players = driver.find_element("xpath","//div[@class='totals']").find_elements("xpath","//div[@class='left']")
                    total_cache = totals.find_elements("xpath","//div[@class='right']")
                    print('=======================================================')
                    print(f'player > {players[0].text}')
                    print('=======================================================')
                    print(f'total_cache index {total_cache[len(total_cache)-1].text}')
                    print('=======================================================')
                    ultimo_good=goods[0].text
                    last_state = 'G'
                    try:
                        state = (float(str(goods[0].text).replace('X','')),int(str(players[0].text).split(' ')[0]),
                        float(str(total_cache[len(total_cache)-1].text).replace('R$','')),
                        'G',
                        datetime.now(timezone(tzoffset)).strftime('%d-%m-%Y %H:%M:%S.%f')[:-3],
                        datetime.timestamp(datetime.now(timezone(tzoffset))))
                        db.createDocument(con, state[0], state[1], state[2], state[3], state[4], state[5])
                        #entries.append(state)
                    except Exception as e:
                        logger.error(str(e)+'>>'+str(goods[0].text)+','+str(players[0].text)+','+str(total_cache[len(total_cache)-1].text)+' bads >>{'+str(bads)+'} goods >> {'+str(goods)+'}')
                    print('ENTROU GOOD > '+goods[0].text)
                    logger.info('ENTROU GOOD > '+goods[0].text)
                    


                if ultimo_bad != bads[0].text:
                    totals =driver.find_element("xpath","//div[@class='totals']")
                    players = driver.find_element("xpath","//div[@class='totals']").find_elements("xpath","//div[@class='left']")
                    total_cache = totals.find_elements("xpath","//div[@class='right']")
                    print('=======================================================')
                    print(f'player > {players[0].text}')
                    print('=======================================================')   
                    print(f'total_cache index {total_cache[len(total_cache)-1].text}')
                    print('=======================================================')
                    ultimo_bad=bads[0].text
                    last_state = 'B'

                    try:
                        state = (float(str(bads[0].text).replace('X','')),int(str(players[0].text).split(' ')[0]),
                        float(str(total_cache[len(total_cache)-1].text).replace('R$','')),
                        'B',
                        datetime.now(timezone(tzoffset)).strftime('%d-%m-%Y %H:%M:%S.%f')[:-3],
                        datetime.timestamp(datetime.now(timezone(tzoffset))))
                        db.createDocument(con, state[0], state[1], state[2], state[3], state[4], state[5])
                        #entries.append(state) 
                    except Exception as e:
                        logger.error(str(e)+'>>'+str(bads[0].text)+','+str(players[0].text)+','+str(total_cache[len(total_cache)-1].text)+' bads >>{'+str(bads)+'} goods >> {'+str(goods)+'}')
                    
                    print('ENTROU BAD > '+bads[0].text)
                    logger.info('ENTROU BAD >'+bads[0].text) 
                    bad_seguidos= True
                    

                elif ultimo_bad == bads[0].text and  ultimo_bad == bads[1].text and last_state!='G' and bad_seguidos==True:
                    bad_seguidos= False
 
                    totals =driver.find_element("xpath","//div[@class='totals']")
                    players = driver.find_element("xpath","//div[@class='totals']").find_elements("xpath","//div[@class='left']")
                    total_cache = totals.find_elements("xpath","//div[@class='right']")
                    print('=======================================================')
                    print(f'player > {players[0].text}')
                    print('=======================================================')   
                    print(f'total_cache index {total_cache[len(total_cache)-1].text}')
                    print('=======================================================')
                    ultimo_bad=bads[0].text
                    last_state = 'B'
                    
                    try:
                        state = (float(str(bads[0].text).replace('X','')),int(str(players[0].text).split(' ')[0]),
                        float(str(total_cache[len(total_cache)-1].text).replace('R$','')),
                        'B',
                        datetime.now(timezone(tzoffset)).strftime('%d-%m-%Y %H:%M:%S.%f')[:-3],
                        datetime.timestamp(datetime.now(timezone(tzoffset))))
                        db.createDocument(con, state[0], state[1], state[2], state[3], state[4], state[5])
                        #entries.append(state) 
                    except Exception as e:
                        logger.error(str(e)+'>>'+str(bads[0].text)+','+str(players[0].text)+','+str(total_cache[len(total_cache)-1].text)+' bads >>{'+str(bads)+'} goods >> {'+str(goods)+'}')
                        
                    print('ENTROU BAD > '+bads[0].text)
                    logger.info('ENTROU BAD > '+bads[0].text) 
                    
                
                      
                
       
        