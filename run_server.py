from app import create_app

app = create_app()
def main():

    # if app.config["run_ngrok"]:
    #     from flask_ngrok import run_with_ngrok
    #     run_with_ngrok(app)
    #     app.run()
    #     print("ngrok serer runned")
    #     return

    app.run(port=app.config["port"])
    print("serer runned")
        


if __name__ == "__main__":
    main()