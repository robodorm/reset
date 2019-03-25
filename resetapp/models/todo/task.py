import enum
from datetime import datetime

from pgmagic import get_base
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    text,
    Enum,
    SmallInteger)


class Task(get_base()):
    __tablename__ = "task"
    __table_args__ = {"schema": "resetapp"}

    class Status(enum.Enum):
        """
        Use Task.Status.New for access from outside
        """
        NEW = "NEW"
        IN_PROGRESS = "IN_PROGRESS"
        ARCHIVED = "ARCHIVED"
        REMOVED = "REMOVED"

    id = Column(Integer, primary_key=True, autoincrement=True)

    uid = Column(Integer,
                 doc="Owner's ID")

    title = Column(Text(64),
                   doc="This field should remind you what happenings inside this task")

    desc = Column(Text(8196),
                  doc="Here you can put detailed task description")

    status = Column(Enum(Status), default=Status.NEW.value, nullable=False,
                    doc="The lifecycle of the task should be controlled by this field")

    weight = Column(SmallInteger, nullable=False, default=0,
                    doc="This field helps you to understand tasks priority")

    created = Column(DateTime(timezone=True), server_default=text('NOW()'), default=datetime.now(),
                     doc="Immutable creation date")

    updated = Column(DateTime(timezone=True), onupdate=datetime.now(),
                     doc="This field will be changes everytime when you will modify task fields")

