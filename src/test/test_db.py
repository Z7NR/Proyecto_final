from data_base import DBAdvanceManager

if __name__ == "__main__":
    db = DBAdvanceManager()
    db.create_user("Carlos", "Pérez", 25, "123456789", "carlos@email.com", "hash123", "Lima", "Perú")
    print(db.read_user())