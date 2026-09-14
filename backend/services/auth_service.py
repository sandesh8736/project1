import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from services.database.postgres import PostgreSQL


class AuthService:

    def __init__(self, password):

        self.db = PostgreSQL(password=password)

        self.password_hash = PasswordHash.recommended()

        self.secret_key = os.getenv("JWT_SECRET_KEY")

        if not self.secret_key:
            raise ValueError("JWT_SECRET_KEY is missing from the .env file")

        self.algorithm = "HS256"

    def hash_password(self, password):

        return self.password_hash.hash(password)

    def verify_password(self, password, hashed_password):

        return self.password_hash.verify(password,hashed_password)

    def create_user(self, name, email, password):

        password_hash = self.hash_password(password)

        query = """
            INSERT INTO users(name,email,password_hash)

            VALUES(%s,%s,%s)

            RETURNING id, name, email;
        """

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,(name,email,password_hash))

                user = cursor.fetchone()

            connection.commit()

        return {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }

    def authenticate_user(self, email, password):

        query = """
            SELECT
                id,
                name,
                email,
                password_hash

            FROM users

            WHERE email = %s;
        """

        with self.db.connect() as connection:

            with connection.cursor() as cursor:

                cursor.execute(query, (email,))

                user = cursor.fetchone()

        if not user:
            return None

        user_id, name, user_email, password_hash = user

        if not self.verify_password(password, password_hash):
            return None

        return {
            "id": user_id,
            "name": name,
            "email": user_email
        }

    def create_access_token(self, user_id):

        expire_time = datetime.now(timezone.utc) + timedelta(hours=2)

        payload = {
            "sub": str(user_id),
            "exp": expire_time
        }

        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )

        return token

    def get_user_id_from_token(self, token):

        try:

            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            user_id = payload.get("sub")

            if user_id is None:
                return None

            return int(user_id)

        except jwt.InvalidTokenError:

            return None