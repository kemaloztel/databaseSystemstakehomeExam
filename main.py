from connect import get_db
from flask import Flask, render_template

app = Flask(__name__)

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/',  methods=['GET', 'POST'])
def index(): 
    food_groups = []
    food_groups_id = []
    
    cur = get_db().cursor()
    sql = "select id, name from food_group"
    cur.execute(sql)
    
    for i in cur:
        food_groups.append(i)
    
    return render_template('index.html', food_groups=food_groups)

@app.route('/group/<id>', methods=['GET', 'POST'])
def foodgroupdesc(id):
    group_info = []
    
    cur = get_db().cursor()
    cur = query_db("SELECT short_desc, nitrogen_factor, protein_factor, fat_factor, calorie_factor FROM food WHERE food_group_id = ?", [id])

    for i in cur:
        group_info.append(i)
        print(i)

    return render_template('group_desc.html', group_info=group_info)
