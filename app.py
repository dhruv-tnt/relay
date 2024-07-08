from init import initialize
app=initialize.create_app()
app=initialize.register_bp(app)
if __name__ == '__main__':
    app.run(host='localhost',port=5000)
