import pymongo

class DataBase:
    
    def connect(self):
        err = False
        try:
           print(f'>> Conectando ao banco...')
           client = pymongo.MongoClient("URI")
           db = client.db_blaze
           print(f'conectado com sucesso')
           return err,db
        except Exception as e:
            err = True
            print(f'>> Erro na conexão >{e}')
            return err,e.args

    def createDocument(self,db,candle,qt_player,total_newsstand,target,data_string,data_timestamp):
        err = False
        record = {
            "candle":candle,
            "qtd_players":qt_player,
            "total_newsstand":total_newsstand,
            "target":target,
            "data_string":data_string,
            "data_timestamp":data_timestamp
           }
        try:
           db.history.insert_one(record).inserted_id
           return err,'ok'
        except Exception as e:
            print(f'erro ao inserir >{e}')
            err = False
            return err,e.args

        
        
