from app import app

# This one's for running flask via python filename.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)