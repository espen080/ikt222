"""
Module containing database ORM class
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound


class DataBase:
    def __init__(self, database_url, base_model, echo=False):
        self._engine = create_engine(database_url, echo=echo)
        self._base_model = base_model
        self._base_model.metadata.create_all(self._engine)

    def create(self, model):
        session = self._get_session()
        try:
            session.add(model)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error inserting model instance: {e}")
        finally:
            session.close()

    def query(self, model, **kwargs):
        session = self._get_session()
        result = session.query(model).filter_by(**kwargs)
        session.close()
        return result

    def update(self, model, filters, new_values):
        session = self._get_session()
        try:
            session.query(model).filter_by(**filters).update(new_values)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating model instance: {e}")
        finally:
            session.close()

    def delete(self, model, **kwargs):
        session = self._get_session()
        try:
            instance = session.query(model).filter_by(**kwargs).one()
            session.delete(instance)
            session.commit()
        except NoResultFound:
            print("No matching record found for deletion.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting model instance: {e}")
        finally:
            session.close()

    def delete_all_in_table(self, model):
        session = self._get_session()
        try:
            session.query(model).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error deleting all items in {model.__name__}: {e}")
        finally:
            session.close()

    def delete_all_in_all_tables(self):
        for table in reversed(self._base_model.metadata.sorted_tables):
            self.delete_all_in_table(table)

    def _get_session(self):
        # Create a session to interact with the database
        session = sessionmaker(bind=self._engine)
        return session()


