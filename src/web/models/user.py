import datetime

from sqlalchemy import Column, Integer, String, DateTime
from models import db
from cfg.urls import cloud_front


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    credit = db.Column(db.Integer, default=10)
    name = db.Column(db.String(50), default="no name")
    about = db.Column(db.String(500))
    has_avatar = db.Column(db.Integer, default=0)
    role = db.Column(db.Integer, default=0)
    rooms = db.Column(db.String(100))
    # block_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # last_checkin = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<User %r>" % self.id

    def is_mod(self):
        return self.role >= 300

    def is_banned(self):
        return False
        # return self.block_until and datetime.datetime.now() < self.block_until

    def to_dict(self):
        if self.has_avatar:
            avatar_src = f"{cloud_front}{self.uuid}.jpg?v={self.has_avatar}"
        else:
            avatar_id = self.id % 150
            avatar_src = f"{cloud_front}avatar/{avatar_id}.jpg"
        rooms = []
        if self.rooms:
            rooms = self.rooms.split(',')
        return {

            "id": self.id,
            "name": self.name,
            "credit": self.credit,
            "about": self.about,
            "role": self.role,
            "isMod": self.is_mod(),
            "isBanned": self.is_banned(),
            "avatarSrc": avatar_src,
            "rooms": rooms
        }
