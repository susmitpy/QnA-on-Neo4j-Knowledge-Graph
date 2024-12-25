from models import Person, Group, Company
from neomodel import config

# Configure the connection to Neo4j
config.DATABASE_URL = 'bolt://neo4j:neotest123@localhost:7687'

def create_nodes():
    # Create Group nodes
    tapu_sena:Group = Group(name="Tapu Sena").save()
    # purush_mandal:Group = Group(name="Purush Mandal").save()
    # mahila_mandal:Group = Group(name="Mahila Mandal").save()
    
    # Create Company
    gada_electronics: Company = Company(name="Gada Electronics").save()
    
    # Create Person nodes
    jethalal: Person = Person(first_name="Jethalal",surname="Gada", nick_name="Jethia", gender="M").save()
    daya: Person = Person(first_name="Daya",surname="Gada", gender="F").save()
    tipendra: Person = Person(first_name="Tipendra",surname="Gada", nick_name="Tapu", gender="M").save()
    gulabkumar: Person = Person(first_name="Gulabkumar",nick_name="Goli",surname="Haathi", gender="M").save()
    sonalika: Person = Person(first_name="Sonalika",nick_name="Sonu",surname="Bhide", gender="F").save()
    pankaj: Person = Person(first_name="Pankaj",nick_name="Pinku",surname="Sahay", gender="M").save()
    gurucharand: Person = Person(first_name="Gurucharand",nick_name="Gogi",surname="Sodhi", gender="M").save()
    # aatmaran: Person = Person(first_name="Aatmaran", surname="Bhide",nick_name="Bhidu", gender="M").save()
    # madhavi: Person = Person(first_name="Madhavi",surname="Bhide",nick_name="Madhu", gender="F").save()
    
    # Establish relationships
    jethalal.spouse.connect(daya)
    gada_electronics.owners.connect(jethalal)

    tipendra.parents.connect(jethalal)
    tipendra.parents.connect(daya)

    tipendra.groups.connect(tapu_sena)
    gulabkumar.groups.connect(tapu_sena)
    sonalika.groups.connect(tapu_sena)
    pankaj.groups.connect(tapu_sena)
    gurucharand.groups.connect(tapu_sena)
    
    # aatmaran.spouse.connect(madhavi)
    # sonalika.parents.connect(aatmaran)
    # sonalika.parents.connect(madhavi)

if __name__ == "__main__":
    create_nodes()
