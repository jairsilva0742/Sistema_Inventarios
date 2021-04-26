from flask import Flask
from flask import render_template,request,redirect
import mysql.connector



app=Flask(__name__)



@app.route('/')
def index():
    
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    selectquery="select * from repuestos"
    cursor.execute(selectquery)
    repuestos=cursor.fetchall()
 
     
    cursor.close()
    conn.close
    return render_template('repuestos/index.html', repuestos=repuestos)


@app.route("/destroy/<string:nomb>")
def func(nomb):
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    sql_Delete="Delete from repuestos where Nombre=%s"
    cursor.execute(sql_Delete,(nomb,))
    conn.commit()

    return redirect('/')

@app.route("/edit/<string:nomb>")
def editar(nomb):
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    selectquery="select * from repuestos where Nombre=%s"
    cursor.execute(selectquery,(nomb,))
    repuestos=cursor.fetchall()
    conn.commit()

    return render_template('/repuestos/editar.html',repuestos=repuestos)

@app.route("/update",methods=['POST'])
def update():
    
    return redirect('/')


@app.route('/crear')
def crear():
    return render_template('repuestos/crear.html')

@app.route('/store',methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _marca=request.form['txtMarca']
    _modelo=request.form['txtModelo']
    _serie=request.form['txtSerie']
    _cantidad=request.form['txtCantidad']
    datos=(_nombre,_marca,_modelo,_serie,_cantidad)
    sql="INSERT INTO `repuestos` (`Nombre`, `Marca`, `Modelo`, `Serie`, `cantidad`) VALUES (%s, %s, %s, %s, %s);"
    
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('repuestos/index.html')

if __name__=='__main__':
        app.run(debug=True)


