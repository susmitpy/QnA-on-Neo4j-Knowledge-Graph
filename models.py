from neomodel import StructuredNode, StringProperty, ArrayProperty, FloatProperty,UniqueIdProperty, RelationshipTo, RelationshipFrom
from typing import Optional, Callable
from functools import wraps

def filter_out_none_values(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        values = func(*args, **kwargs)
        return [value for value in values if value is not None]
    return wrapper

class RELATIONSHIPS:
    IS_SPOUSE_OF = "IS_SPOUSE_OF"
    IS_PARENT_OF = "IS_PARENT_OF"
    IS_PART_OF = "IS_PART_OF"
    IS_OWNER_OF = "IS_OWNER_OF"


class Model:
    def get_values(self) -> list[str]:
        raise NotImplementedError

    def get_node_info(self) -> dict:
        raise NotImplementedError

class Person(StructuredNode, Model):
    unique_id = UniqueIdProperty() #TODO: Replace this with custom property that uses ULID
    first_name = StringProperty(required=True)
    surname = StringProperty()
    nick_name = StringProperty()
    gender = StringProperty(choices={"M":"M", "F":"F"}, required=True)
    embedding = ArrayProperty(base_property=FloatProperty(default=None))
    # Relationships
    spouse = RelationshipTo('Person', RELATIONSHIPS.IS_SPOUSE_OF)
    parents = RelationshipFrom('Person', RELATIONSHIPS.IS_PARENT_OF)
    groups = RelationshipTo('Group', RELATIONSHIPS.IS_PART_OF)

    @filter_out_none_values
    def get_values(self) -> list[str]:
        return [self.first_name, self.surname, self.nick_name, self.gender]
    
    def get_node_info(self) -> dict:
        return {
                "unique_id": self.unique_id,
                'first_name': self.first_name,
                'surname': self.surname,
                'nick_name': self.nick_name,
                "gender": self.gender
            }

class Group(StructuredNode, Model):
    unique_id = UniqueIdProperty()
    name = StringProperty(required=True)
    # Relationships
    members = RelationshipFrom('Person', RELATIONSHIPS.IS_PART_OF)
    embedding = ArrayProperty(base_property=FloatProperty(default=None))

    @filter_out_none_values
    def get_values(self) -> list[str]:
        return [self.name]

    def get_node_info(self) -> dict:
        return {
            "unique_id": self.unique_id,
            'name': self.name
        }

class Company(StructuredNode, Model):
    unique_id = UniqueIdProperty()
    name = StringProperty(required=True)
    # Relationships
    owners = RelationshipFrom('Person', RELATIONSHIPS.IS_OWNER_OF)
    embedding = ArrayProperty(base_property=FloatProperty(default=None))

    @filter_out_none_values
    def get_values(self) -> list[str]:
        return [self.name]
    
    def get_node_info(self) -> dict:
        return {
            "unique_id": self.unique_id,
            'name': self.name
        }

