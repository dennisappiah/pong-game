from quickie import db, jwt
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    type = Column(String(255))
    questions = relationship("Question", backref="category", lazy=True)

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "type": self.type}


class Question(db.Model):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    difficulty = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))

    def __init__(self, question, answer, category_id, difficulty):
        self.question = question
        self.answer = answer
        self.category_id = category_id
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category_id": self.category_id,
            "difficulty": self.difficulty,
        }


class Leaderboard(db.Model):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True)
    player = Column(String)
    score = Column(Integer)

    def __init__(self, player, score):
        self.player = player
        self.score = score

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "player": self.player,
            "score": self.score,
        }


# A user may have many roles and a role may be referenced by many users
class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(20), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    image_file = Column(String(20), nullable=False, default="default.jpg")
    roles = relationship("Role", secondary="user_roles", back_populates="users")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "username": self.username, "email": self.email}

    def has_role(self, role):
        return bool(
            Role.query.join(Role.users)
            .filter(User.id == self.id)
            .filter(Role.slug == role)
            .count()
            == 1
        )


@jwt.user_identity_loader
def _user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_loader_callback(jwt_identity, jwt_data):
    identity = jwt_data["sub"]
    user = User.query.filter_by(id=identity).first()
    return user


class Role(db.Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    slug = Column(String(20), unique=True, nullable=False)
    users = db.relationship("User", secondary="user_roles", back_populates="roles")

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
