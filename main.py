from menu import run_cli
import db

if __name__ == "__main__":
    db.init_db()   # make sure tables exist
    run_cli()