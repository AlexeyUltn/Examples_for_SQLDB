import sqlite3
from keys import x
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

##Использую ORM

app = Flask(__name__, template_folder='путь/до/папки/с/вебкой', static_folder='путь/до/папки/с/bootstrap или картинки')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///путь/до/папки/с/базой данных в sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

##Использую классический вариант соединения

connection = sqlite3.connect('путь/до/папки/с/базой данных в sqlite', check_same_thread=False)
cur = connection.cursor()

def max_id(cur):
  query = """select max("id") from sqlite_table;"""
  cur.execute(query)
  result = cur.fetchone()[0]
  return result

@app.route('/')
def main():
  data = []
  for i in range(1, max_id(cur)):
    x = dict()
    cur.execute("""select * from sqlite_table where id={};""".format(i))
    result = cur.fetchone()
    x['company_name'] = result[1]
    x['company_logo'] = result[2]
    x['IPO_date'] = result[3]
    data.append(x)
  return render_template('main_page_with_info.html' data=data)

@app.route('/add_info_to_main_page')
def add_info_to_main_page():
  return render_template(add_info_to_main_page.html)

class database(db.model):
  __tablename__ = 'sqlite_table'
  Id = db.Column(db.Integer, primary_key=True)
  Company_name =  db.Column(db.Text)
  Company_logo =  db.Column(db.Text) ## Путь до изображения
  IPO_date =  db.Column(db.Timestamp)
  
@app.route('/add_info_to_main_page', methods = ['POST', 'GET'],)
def add_info()
  if request.method == 'GET':
    return render_template('main_page_with_info.html')
  elif request.method == 'POST':
    Company_name = request.form['Company_name']
    Company_logo = request.form['Company_logo']
    IPO_date = request.form['IPO_date']
    
    record = database(Company_name=Company_name, Company_logo= Company_logo, IPO_date=IPO_date)
    
    db.session.add(record)
    db.session.commit()
    return redirect('/')
if __name__ == "__main__":
  print(db)
  app.run(port=1111, debug=True)
