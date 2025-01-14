from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyrebase
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyBQV-T7DUcinv4g3vPNo5kdrmxY6ZgkKl4",
    "authDomain": "danabos-86770.firebaseapp.com",
    "databaseURL": "https://danabos-86770-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "danabos-86770",
    "storageBucket": "danabos-86770.appspot.com",
    "messagingSenderId": "613590127507",
    "appId": "1:613590127507:web:3aa86a3bd8f77f59ab0e66"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def validate_password(password, confirm_password):
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if password != confirm_password:
        return "Passwords do not match."
    return None

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def mlp_manual(jumlah_siswa, dana_diterima, biaya_operasional, gaji_honor, alat_pembelajaran, perawatan, pengembangan):
    # Input layer
    input_data = [jumlah_siswa, dana_diterima, biaya_operasional, gaji_honor, alat_pembelajaran, perawatan, pengembangan]
    
    # Bobot dan bias
    weights = [
        [0.1, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05],  # Hidden layer 1
        [0.3, 0.4, 0.3, 0.2, 0.1]                  # Output layer
    ]
    biases = [
        [0.1, 0.1, 0.1, 0.1, 0.1],                 # Bias untuk hidden layer 1
        [0.2]                                       # Bias untuk output layer
    ]
    
    # Aktivasi Hidden Layer 1
    hidden_layer = []
    for i in range(len(weights[0])):
        z = sum(input_data[j] * weights[0][i] for j in range(len(input_data))) + biases[0][i]
        hidden_layer.append(max(0, z))  # ReLU Activation
    
    # Aktivasi Output Layer
    output = sum(hidden_layer[k] * weights[1][k] for k in range(len(hidden_layer))) + biases[1][0]
    
    # Sigmoid activation
    result = sigmoid(output)
    return result

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['email']
            return redirect(url_for('home'))
        except:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html')
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        error = validate_password(password, confirm_password)
        if error:
            flash(error, 'danger')
            return render_template('register.html')

        try:
            auth.create_user_with_email_and_password(email, password)
            flash('Account created successfully. Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'user' in session:
        return render_template('about.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/team')
def team():
    if 'user' in session:
        return render_template('team.html', user=session['user'])
    return redirect(url_for('login'))


@app.route('/service', methods=['GET', 'POST'])
def service():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        # Ambil data dari form
        jumlah_siswa = int(request.form['jumlah_siswa'])
        dana_diterima = float(request.form['dana_diterima'])
        biaya_operasional = float(request.form['biaya_operasional'])
        gaji_honor = float(request.form['gaji_honor'])
        alat_pembelajaran = float(request.form['alat_pembelajaran'])
        perawatan = float(request.form['perawatan'])
        pengembangan = float(request.form['pengembangan'])
    else:
        # Data default jika method GET
        jumlah_siswa = 139
        dana_diterima = 220000000
        biaya_operasional = 40740400
        gaji_honor = 119515400
        alat_pembelajaran = 26255100
        perawatan = 13580900
        pengembangan = 19927500

    # Dataset
    dataset = [
        ["Jumlah Siswa", jumlah_siswa],
        ["Dana Diterima", dana_diterima],
        ["Biaya Operasional", biaya_operasional],
        ["Gaji dan Honor", gaji_honor],
        ["Alat Pembelajaran", alat_pembelajaran],
        ["Perawatan", perawatan],
        ["Pengembangan", pengembangan]
    ]

    # Hitung prediksi MLP
    mlp_prediction = mlp_manual(jumlah_siswa, dana_diterima, biaya_operasional, 
                              gaji_honor, alat_pembelajaran, perawatan, pengembangan)

    # Analisis data
    total_pengeluaran = biaya_operasional + gaji_honor + alat_pembelajaran + perawatan + pengembangan
    sisa_dana = dana_diterima - total_pengeluaran
    efisiensi = (total_pengeluaran / dana_diterima * 100) if dana_diterima > 0 else 0

    # Persentase kategori pengeluaran
    kategori_pengeluaran = [biaya_operasional, gaji_honor, alat_pembelajaran, perawatan, pengembangan]
    if total_pengeluaran > 0:
        persentase_kategori = (np.array(kategori_pengeluaran) / total_pengeluaran * 100).tolist()
    else:
        persentase_kategori = [0] * 5

    # Hasil analisis
    result = {
        'sisa_dana': sisa_dana,
        'efisiensi': efisiensi,
        'mlp_prediction': mlp_prediction,
        'analisis': {
            'persentase_operasional': persentase_kategori[0],
            'persentase_gaji': persentase_kategori[1],
            'persentase_pembelajaran': persentase_kategori[2],
            'persentase_perawatan': persentase_kategori[3],
            'persentase_pengembangan': persentase_kategori[4],
        },
        'jumlah_siswa': jumlah_siswa,
        'dana_diterima': dana_diterima,
        'biaya_operasional': biaya_operasional,
        'gaji_honor': gaji_honor,
        'alat_pembelajaran': alat_pembelajaran,
        'perawatan': perawatan,
        'pengembangan': pengembangan,
        'dataset': dataset
    }

    return render_template('service.html', user=session['user'], result=result)

if __name__ == '__main__':
    app.run(debug=True)
