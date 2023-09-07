import tornado.web
import tornado.ioloop
from mysql.connector import connection
import json
import asyncio
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
async def init_db():
    myDb =connection.MySQLConnection( host="localhost",
    user="root",
    password="hari123",
    database="flask") 
    return myDb

class MyFormHandler(tornado.web.RequestHandler):
    async def get(self,id=None):
        if id == None:
            self.write('<html><body><form action="/myform" method="POST">'
                    '<input type="text" name="message">'
                    '<input type="submit" value="Submit">'
                    '</form></body></html>')
        else:
            data = await getalldata(id)
            self.finish(json.dumps(data))

    async def post(self):
        self.set_header("Content-Type", "text/plain")
        try:
            connectiondb = await init_db()
            cur = connectiondb.cursor()
            values = (self.get_body_argument("message",default=None, strip=False))
            sql = "INSERT INTO users (username) VALUES (%s)"
            cur.execute(sql,(values,))
            connectiondb.commit()
            data = await getalldata()
            self.finish(json.dumps(data))
        except Exception as e:
            print(e)
            self.write(e)
# class PostHandler(tornado.web.RequestHandler):
#     def get(self,topic_id):
        


async def getalldata(topic_id=None):
    connectiondb = await init_db()
    cur = connectiondb.cursor(dictionary=True)
    if topic_id == None:
        sql = "select * from users"
        cur.execute(sql)
    else:
        sql = "select * from users where id= %s"
        cur.execute(sql,(topic_id,))
    result=cur.fetchall()
    return result

async def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/",MyFormHandler),
        (r"/myform",MyFormHandler),
        (r"/([0-9]+)",MyFormHandler)
    ],
    autoreload=True
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    await asyncio.Event().wait()
       

if __name__== '__main__':
   asyncio.run(main())


