from sqlalchemy.orm import Session

class BaseRepository:

    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get_by_id(self, id):
        return self.db.query(self.model)\
            .filter(self.model.id == id)\
            .first()

    def get_by_field(self, field, value):
        return self.db.query(self.model)\
            .filter(getattr(self.model, field) == value)\
            .first()

    def get_all(self, filters=None):
        query = self.db.query(self.model)
        if filters:
            for field, value in filters.items():
                query = query.filter(
                    getattr(self.model, field) == value
                )
        return query.all()

    def create(self, data: dict):
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id, data: dict):
        obj = self.get_by_id(id)
        for key, value in data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        self.db.delete(obj)
        self.db.commit()
        return True