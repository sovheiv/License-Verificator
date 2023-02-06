from src import create_app

app = create_app()


if __name__ ==           "__main__":
    print("Running serer")
    app.run(port=app.config["DEBUG_PORT"])
