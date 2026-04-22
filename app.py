from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'citas.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota     TEXT NOT NULL,
            propietario TEXT NOT NULL,
            especie     TEXT,
            fecha       TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def agenda():
    conn = get_db()
    citas = conn.execute('SELECT * FROM pacientes ORDER BY fecha').fetchall()
    conn.close()
    return render_template('agenda.html', citas=citas)


@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        conn = get_db()
        conn.execute(
            'INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?, ?, ?, ?)',
            (request.form['mascota'], request.form['propietario'],
             request.form['especie'], request.form['fecha'])
        )
        conn.commit()
        conn.close()
        return redirect(url_for('agenda'))
    return render_template('agendar.html')


@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    conn = get_db()
    cita = conn.execute('SELECT * FROM pacientes WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        conn.execute(
            'UPDATE pacientes SET mascota=?, propietario=?, especie=?, fecha=? WHERE id=?',
            (request.form['mascota'], request.form['propietario'],
             request.form['especie'], request.form['fecha'], id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('agenda'))
    conn.close()
    return render_template('modificar.html', cita=cita)


@app.route('/cancelar/<int:id>', methods=['POST'])
def cancelar(id):
    conn = get_db()
    conn.execute('DELETE FROM pacientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('agenda'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
