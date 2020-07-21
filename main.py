from connect import get_db, close_connection
from flask import Flask, render_template, url_for, request, redirect
from forms import UpdateForm
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
@app.route('/home',  methods=['GET', 'POST'])
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
        #print(i)

    return render_template('group_desc.html', group_info=group_info)


@app.route('/view_update', methods=['GET', 'POST'])
def viewandupdatefood():
    food_detail = []
    
    cur = get_db().cursor()
    sql = "SELECT food.id, name, long_desc, short_desc, manufac_name, sci_name FROM food INNER JOIN food_group ON food_group.id = food.food_group_id"
    cur.execute(sql)
    
    try:
        for a in cur:
            food_detail.append(a)
            #print(a)
    except:
        pass
            
    return render_template('view_update.html', food_detail=food_detail)

@app.route('/update_food', methods=['GET', 'POST'])
def update_food():
    if request.method == 'POST':
        if request.form['postButton'] == 'Update':
            degerler = request.form.getlist('selected')
            for id in degerler:
                print(id)
    return render_template('update_food.html', id=id)


@app.route('/updated_food/<id>', methods=['GET', 'POST'])
def updated_food(id):
    form=UpdateForm(request.form)

    cur = get_db().cursor()
    cur = query_db("UPDATE food SET food_group_id=?, long_desc=?, short_desc=?, manufac_name=?, sci_name=? WHERE id=?",
                 [form.food_group_id.data, form.long_desc.data, form.short_desc.data, form.manufac_name.data,form.sci_name.data, id])
    get_db().commit()
    
    return redirect(url_for('viewandupdatefood'))

@app.route('/nutrition_weight_detail', methods=['GET', 'POST'])
def nutrition_weight():
    food_detailll = []

    cur = get_db().cursor()
    sql5 = "SELECT fg.name, long_desc, short_desc, manufac_name, sci_name, nu.name, n.amount, units, w.amount, description, gm_weight " \
          "FROM food AS f INNER JOIN nutrition AS n ON f.id = n.food_id " \
          "INNER JOIN nutrient AS nu ON n.nutrient_id = nu.id " \
          "INNER JOIN weight AS  w ON f.id = w.food_id " \
          "INNER JOIN food_group AS fg ON f.food_group_id = fg.id"
    cur.execute(sql5)

    try:
        for i in cur:
            food_detailll.append(i)
    except:
        pass

    return render_template('nutrition_weight.html', food_detailll=food_detailll)