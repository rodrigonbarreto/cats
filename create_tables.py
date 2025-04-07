from core.database import create_db
from models.__all_models import PetModel


def main():
    create_db()
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    main()
