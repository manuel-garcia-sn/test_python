from sqlalchemy import Column, Integer, String
from database.database import Base


class Item(Base):
    __tablename__ = 'items'

    STATUS_NOT_STARTED = 'Not Started'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_COMPLETED = 'Completed'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    status = Column(String(50), unique=False)

    def __init__(self, name=None):
        self.name = name
        self.status = self.STATUS_NOT_STARTED

    def __repr__(self):
        return {'id': self.id, 'name': self.name, 'status': self.status}

    def __toString__(self):
        return '<Item name %r ' % self.item + ' on status %r ' % self.status

    # def __repr__(self):
    #     return '<Item name %r ' % self.item + ' on status %r ' % self.status