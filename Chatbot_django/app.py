from flask import Flask, render_template, request, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to establish connection with PostgreSQL database
def get_db_connection():
    connection = psycopg2.connect(
        dbname='database',
        user='postgres',
        password='System@1234',
        host='localhost',
        port='5432'
    )
    return connection

# Function to get available locations from the database
def get_locations():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT location FROM details.heroes")
    locations = [row[0] for row in cur.fetchall()]
    conn.close()
    return locations

# Function to check availability based on selected options
def check_availability(service, location, date):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM details.heroes WHERE services = %s AND location = %s AND date = %s", (service, location, date))
    available_employees = cur.fetchall()
    conn.close()
    return available_employees

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'service' in session:
        service = session['service']
        if 'location' in session:
            location = session['location']
            if 'date' in session:
                date = session['date']
                if 'check_availability' in request.form:
                    available_employees = check_availability(service, location, date)
                    if available_employees:
                        return render_template('index.html', message="Available Employees:", employees=available_employees)
                    else:
                        return render_template('index.html', message="Sorry, We Don't Have Services On the Precised Date and Location")
    if request.method == 'POST':
        if 'service' in request.form:
            service = request.form['service']
            session['service'] = service
            return render_template('index.html', message=f"You selected: {service}", locations=get_locations())
        elif 'location' in request.form:
            location = request.form['location']
            session['location'] = location
            return render_template('index.html', message=f"You selected location: {location}", date=True)
        elif 'date' in request.form:
            date = request.form['date']
            session['date'] = date
            return render_template('index.html', message=f"You selected date: {date}", button=True)

    return render_template('index.html', message="Hi I am Your Bot! How may I Help You", options=True)

if __name__ == '__main__':
    app.run(debug=True)
