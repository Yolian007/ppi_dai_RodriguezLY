from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Lo usaremos para otra cosa

df = pd.DataFrame(columns=['Nombre', 'Email', 'password'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    new_data = {'Nombre': fullname, 'Email': email, 'password': password}
    global df
    df = pd.concat([df, new_data], ignore_index=True)
    # Guardar el DataFrame en un archivo Excel cada vez que se reciba un nuevo registro
    df.to_excel('registro_usuarios.xlsx', index=False)
    return f"Registro recibido de {fullname} con email {email}"
    
print(df.head())

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


# Guardar formulario en firebase


    #if request.method == 'POST':    
    #    fullname = request.form['fullname']
    #    email = request.form['email']
    #    password = request.form['password']
    #    print("Received data:", fullname, email, password) 
#
    #    user_data = {
    #        'fullname': fullname,
    #        'email': email,
    #        'password': password 
    #    }
#
    #    fb_db.write_record('/users/'+ fullname, user_data)
#
    #    return jsonify({'message': 'Usuario registrado correctamente'})
    #
    #    
    #else:
    #    return 'No entro al metodo post'


