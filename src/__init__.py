from .app import init_app

app = init_app()


def create_app():
    from .endpoints import all_routes

    [app.register_blueprint(rout) for rout in all_routes]
    create_tables()

    return app


def create_tables() -> None:
    from .models import all_models

    with app.database:
        app.database.create_tables(models=[*all_models])
