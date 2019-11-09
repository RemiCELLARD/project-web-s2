# ---------
# Connection to the db 'gigondas'
# ---------
import pymysql.cursors

class RC_DB_CONNECT:
    def __init__(self, my_settings):
        if not isinstance(my_settings, dict):
            raise TypeError
        try:
            self.db = pymysql.connect(autocommit=True, host=my_settings['db']['address'],user=my_settings['db']['login'],password=my_settings['db']['password'],db=my_settings['db']['database'])
            self.cursor = self.db.cursor()
        except Exception as error:
            print(error)
    def getCursor(self):
        return self.cursor
    def cmd_exec(self, cmd):
        if not isinstance(cmd, str):
            raise TypeError
        try:
            self.cursor.execute(cmd, ())
        except Exception as error:
            print(error)
    def save(self):
        self.db.commit()
    def stop(self):
        self.cursor.close()
        self.db.close()

class RC_DB(RC_DB_CONNECT):
    def __init__(self, my_settings):
        RC_DB_CONNECT.__init__(self, my_settings)
    def getCursor(self):
        return RC_DB_CONNECT.getCursor(self)
    def exec(self, cmd):
        RC_DB_CONNECT.cmd_exec(self, cmd)
    def save(self):
        RC_DB_CONNECT.save(self)
    def stop(self):
        RC_DB_CONNECT.stop(self)
    def answer(self, cmd):
        try:
            self.exec(cmd)
            return self.getCursor()
        except Exception as error:
            print(error)
    def fa(self, cmd):
        try:
            answer = self.answer(cmd).fetchall()
        except Exception as error:
            print(error)
        if not isinstance(answer, tuple):
            print(answer)
            raise TypeError
        return answer
    def fo(self, cmd):
        try:
            answer = self.answer(cmd).fetchone()
        except Exception as error:
            print(error)
        if not isinstance(answer, tuple):
            raise TypeError
        return answer
    def insert(self, cmd):
        try:
            self.exec(cmd)
            self.save()
        except Exception as error:
            print(error)

class RC_DB_CMD :
    def __init__(self):
        pass
    ## Order BY generator
    def orderBy(self, data, order="ASC"):
        cmd = "ORDER BY "
        for e in data:
            cmd += e+","
        cmd = "{} {} ".format(cmd[:-1], order)
        return cmd

    ## joinOn
    def joinOn(self, table, data):
        cmd = "JOIN {} ON ".format(table)
        for condition in data:
            cmd += condition+","
        cmd = cmd[:-1]+" "
        return cmd

    ## Command SQL for the page theme 
    def theme_cmd(self, data):
        cmd = self.build_cmd("theme", data)
        return cmd

    ## Command SQL for the page theme 
    def boites_cmd(self, data):
       cmd = self.build_cmd("boite", data)
       return cmd
    
    ## Command builder v0.1
    def build_cmd(self, table, data):
        if "specificSelect" in data :
            src = data["specificSelect"]
        else :
            src = "*"
        cmd = "SELECT {} FROM {} ".format(src, table)         
        if "join" in data:
            cmd += self.joinOn(data['join']['table'], data['join']['conditions'])
        if "where" in data:
            cmd += "WHERE "+data["where"]+" "
        if "order" in data:
            cmd += self.orderBy(data['order']['info'], data['order']['sort'])
        if "limit" in data:
            cmd += "LIMIT 0,{}".format(data['limit'])
        cmd += ";"
        return cmd