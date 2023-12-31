from flask import current_app
from api import db, jwt
from itsdangerous.url_safe import URLSafeTimedSerializer


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id if isinstance(user, User) else None


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    questions = db.relationship("Question", backref="category", lazy=True)

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

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

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

    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String)
    score = db.Column(db.Integer)

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

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    file = db.Column(db.String(20), nullable=False, default="default.jpg")
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_super_admin = db.Column(db.Boolean, default=False)
    roles = db.relationship("Role", secondary="user_roles", back_populates="users")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_staff": self.is_staff,
            "is_super_admin": self.is_super_admin,
            "roles": [role.name for role in self.roles],
        }

    def has_role(self, role):
        return bool(
            Role.query.join(Role.users)
            .filter(User.id == self.id)
            .filter(Role.slug == role)
            .count()
            == 1
        )

    def has_permission(self, permission_slug):
        user_roles = self.roles

        for role in user_roles:
            if permission_slug in [p.slug for p in role.permissions]:
                return True
        return False

    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], expires_sec)
        # serialized
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            # deserializing
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    slug = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship("User", secondary="user_roles", back_populates="roles")
    permissions = db.relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

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
            "name": self.name,
            "slug": self.slug,
            "permissions": self.permissions,
        }


class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# A role can have many permissions, a permission can be referenced by different roles
class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    slug = db.Column(db.String(20), unique=True, nullable=False)
    roles = db.relationship(
        "Role", secondary="role_permissions", back_populates="permissions"
    )

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "roles": self.roles,
        }


class RolePermission(db.Model):
    __tablename__ = "role_permissions"

    permission_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    )
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
