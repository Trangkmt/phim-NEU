from main import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Visit http://127.0.0.1:5000/ in your browser")
    app.run(debug=True)
