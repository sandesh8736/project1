from services.database.postgres import PostgreSQL

from services.database.schema import DatabaseSchema


db = PostgreSQL(
    password="Documind@123"
)


schema = DatabaseSchema(db)

schema.create_all()