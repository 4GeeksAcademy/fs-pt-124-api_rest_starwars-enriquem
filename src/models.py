from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    #foreign key

    #relationship
    characters: Mapped[List["Character"]] = relationship(back_populates="first_account", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "last_login": self.last_login,
            # do not serialize the password, its a security breach
        }

    def __repr__(self):
        return self.username

class Character(db.Model):

        __tablename__ = "character"

        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
        level: Mapped[int] = mapped_column(nullable=False, default=1)

        #foreign key
        first_account_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
        race_choice_id: Mapped[int] = mapped_column(ForeignKey("race.id"), nullable=True)
        class_base_choice_id: Mapped[int] = mapped_column(ForeignKey("class_base.id"), nullable=True)
        location_character_id: Mapped[int] = mapped_column(ForeignKey("location.id"), nullable=True)

        #relationship
        first_account: Mapped["User"] = relationship(back_populates="characters")
        race_choice: Mapped["Race"] = relationship(back_populates="races")
        class_base_choice: Mapped["ClassBase"] = relationship(back_populates="classes_base")
        location_character: Mapped["Location"] = relationship(back_populates="character_locations")
        friendship_from: Mapped[List["Friendship"]] = relationship(foreign_keys="Friendship.friendship_from_character_id", back_populates="friendship_from_character")
        friendship_to: Mapped[List["Friendship"]] = relationship(foreign_keys="Friendship.friendship_to_character_id", back_populates="friendship_to_character")

        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "level": self.level,
                # do not serialize the password, its a security breach
            }

        def __repr__(self):
            return self.name

class Race(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    #foreign key

    #relationship
    races: Mapped[List["Character"]] = relationship(back_populates="race_choice")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
    def __repr__(self):
        return self.name

class ClassBase(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    #foreign key

    #relationship
    classes_base: Mapped[List["Character"]] = relationship(back_populates="class_base_choice")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
    def __repr__(self):
        return self.name

class Zone(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    zone_type: Mapped[str] = mapped_column(String(120), nullable=False)

    #foreign key

    #relationship
    zone_locations: Mapped[List["Location"]] = relationship(back_populates="location_zone")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "zone_type": self.zone_type,
            # do not serialize the password, its a security breach
        }
    
    def __repr__(self):
        return f"{self.name}({self.zone_type})"

class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[int] = mapped_column(nullable=False)
    y: Mapped[int] = mapped_column(nullable=False)
    z: Mapped[int] = mapped_column(nullable=False)

    #foreign key
    location_zone_id: Mapped[int] = mapped_column(ForeignKey("zone.id"))
    #relationship
    location_zone: Mapped["Zone"] = relationship(back_populates="zone_locations")
    character_locations: Mapped[List["Character"]] = relationship(back_populates="location_character")

    def serialize(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            # do not serialize the password, its a security breach
        }
    
    def __repr__(self):
        return f"Location in {self.location_zone.name}"

class Friendship(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    #foreign key
    friendship_from_character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    friendship_to_character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    #relationship
    friendship_from_character: Mapped["Character"] = relationship(foreign_keys=[friendship_from_character_id], back_populates="friendship_from")
    friendship_to_character: Mapped["Character"] = relationship(foreign_keys=[friendship_to_character_id], back_populates="friendship_to")
    
    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }
