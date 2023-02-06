from src import create_app

app = create_app()


if __name__ == "__main__":
    app.logger.info("Running serer")
    app.run(port=5002)
