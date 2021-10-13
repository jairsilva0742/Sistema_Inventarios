from flask import Flask
from flask import render_template,request,redirect,url_for,flash
import mysql.connector
import cv2 
from pyzbar.pyzbar import decode
import time


app=Flask(__name__)
app.secret_key="Programacion"


#esto es nuevo
@app.route('/readBarCode')
def barCode():
    
    return redirect('/')



@app.route('/')
def index():
    
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    selectquery="select * from repuestos_1"
    cursor.execute(selectquery)
    repuestos=cursor.fetchall()
 
     
    cursor.close()
    conn.close
    return render_template('repuestos/index.html', repuestos=repuestos)


@app.route("/destroy/<int:id>")
def func(id):
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    sql_Delete="Delete from repuestos_1 where id=%s"
    cursor.execute(sql_Delete,(id,))
    conn.commit()

    return redirect('/')

@app.route("/edit/<int:id>")
def editar(id):
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    selectquery="select * from repuestos_1 where id=%s"
    cursor.execute(selectquery,(id,))
    repuestos=cursor.fetchall()
    conn.commit()

    return render_template('/repuestos/editar.html',repuestos=repuestos)

@app.route("/update",methods=['POST'])
def update():
    
    id=request.form['txtID']
    _nombre=request.form['txtNombre']
    _marca=request.form['txtMarca']
    _serie=request.form['txtSerie']
    _precioUnitario=request.form['txtPrecioUnitario']
    _cantidad=request.form['txtCantidad']
    if _cantidad=='' and _precioUnitario=='':
        _CostoTotal=''
    else:
        _costoTotal=str(int(_cantidad)*int(_precioUnitario))

    
    _codigoProducto=request.form['txtCodigoProducto']
    datos=(_nombre,_marca,_serie,_precioUnitario,_cantidad,_costoTotal,_codigoProducto,id)
    sql="UPDATE repuestos_1 SET `Nombre`=%s, `Marca`=%s,`Serie`=%s,`Precio Unitario`=%s,`cantidad`=%s, `Costo Total`=%s, `Codigo Producto`=%s WHERE id=%s;"
    
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')


@app.route('/crear')
def crear():
    return render_template('repuestos/crear.html')

@app.route('/store',methods=['POST'])
def storage():
    cap=cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    camera=True
    while camera==True:
        sucess, frame=cap.read()
        for code in decode(frame):
            print('Código Ingresado')
            codigo_Producto=int(code.data.decode('utf-8'))
            time.sleep(5)
            camera=False
        if camera==False:
            cv2.destroyAllWindows()
            cap.release()
        else:
            cv2.imshow('Testing-code-scan',frame)
            cv2.waitKey(1)
    _nombre=request.form['txtNombre']
    _marca=request.form['txtMarca']
    _serie=request.form['txtSerie']
    _precioUnitario=request.form['txtPrecioUnitario']
    _cantidad=request.form['txtCantidad']
    if _cantidad=='' and _precioUnitario=='':
        _CostoTotal=''
    else:
        _costoTotal=str(int(_cantidad)*int(_precioUnitario))
    _codigoProducto=str(codigo_Producto)[3:13]
    print(codigo_Producto)
    print(_codigoProducto)
    if _nombre=='' or _marca=='' or _serie=='' or _precioUnitario=='' or _cantidad=='' or _codigoProducto=='':
        
        flash('Diligencie todos los campos')
        return redirect(url_for('crear'))

    
    datos=(_nombre,_marca,_serie,_precioUnitario,_cantidad,_costoTotal,_codigoProducto)
    sql="INSERT INTO `repuestos_1` (`ID`,`Nombre`, `Marca`,`Serie`,`Precio Unitario`,`cantidad`, `Costo Total`, `Codigo Producto`) VALUES (NULL,%s, %s, %s, %s, %s, %s, %s);"
    
    conn=mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="sistema")
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

if __name__=='__main__':
        app.run(debug=True)


