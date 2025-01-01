from neomodel import config

from models import Company, Group, HasCommitteeMember, Person, Society

# Configure the connection to Neo4j
config.DATABASE_URL = "bolt://neo4j:neotest123@localhost:7687"


def create_nodes():
    # Create Group nodes
    tapu_sena: Group = Group(name="Tapu Sena").save()
    purush_mandal: Group = Group(name="Purush Mandal").save()
    mahila_mandal: Group = Group(name="Mahila Mandal").save()

    # Create Company
    gada_electronics: Company = Company(name="Gada Electronics").save()

    champaklal: Person = Person(
        first_name="Champaklal", surname="Gada", gender="M"
    ).save()
    jethalal: Person = Person(
        first_name="Jethalal", surname="Gada", nick_name="Jethia", gender="M"
    ).save()
    daya: Person = Person(first_name="Daya", surname="Gada", gender="F").save()
    tipendra: Person = Person(
        first_name="Tipendra", surname="Gada", nick_name="Tapu", gender="M"
    ).save()
    jethalal.parents.connect(champaklal)
    jethalal.spouse.connect(daya)
    gada_electronics.owners.connect(jethalal)
    tipendra.parents.connect(jethalal)
    tipendra.parents.connect(daya)

    aatmaram: Person = Person(
        first_name="Aatmaram", surname="Bhide", nick_name="Bhidu", gender="M"
    ).save()
    madhavi: Person = Person(
        first_name="Madhavi", surname="Bhide", nick_name="Madhu", gender="F"
    ).save()
    sonalika: Person = Person(
        first_name="Sonalika", nick_name="Sonu", surname="Bhide", gender="F"
    ).save()
    aatmaram.spouse.connect(madhavi)
    sonalika.parents.connect(aatmaram)
    sonalika.parents.connect(madhavi)

    hansraj: Person = Person(
        first_name="Hansraj", surname="Haathi", nick_name="Hans", gender="M"
    ).save()
    komal: Person = Person(first_name="Komal", surname="Haathi", gender="F").save()
    gulabkumar: Person = Person(
        first_name="Gulabkumar", nick_name="Goli", surname="Haathi", gender="M"
    ).save()
    hansraj.spouse.connect(komal)
    gulabkumar.parents.connect(hansraj)
    gulabkumar.parents.connect(komal)

    roshan_m: Person = Person(first_name="Roshan", surname="Sodhi", gender="M").save()
    roshan_f: Person = Person(first_name="Roshan", surname="Sodhi", gender="F").save()
    gurucharand: Person = Person(
        first_name="Gurucharand", nick_name="Gogi", surname="Sodhi", gender="M"
    ).save()
    roshan_m.spouse.connect(roshan_f)
    gurucharand.parents.connect(roshan_m)
    gurucharand.parents.connect(roshan_f)

    taarak: Person = Person(first_name="Taarak", surname="Mehta", gender="M").save()
    anjali: Person = Person(first_name="Anjali", surname="Mehta", gender="F").save()
    taarak.spouse.connect(anjali)

    krishnan: Person = Person(first_name="Krishnan", surname="Iyer", gender="M").save()
    babita: Person = Person(first_name="Babita", surname="Iyer", gender="F").save()
    krishnan.spouse.connect(babita)

    popatlal: Person = Person(
        first_name="Popatlal", surname="Pandey", gender="M"
    ).save()
    pankaj: Person = Person(
        first_name="Pankaj", nick_name="Pinku", surname="Sahay", gender="M"
    ).save()

    tipendra.groups.connect(tapu_sena)
    gulabkumar.groups.connect(tapu_sena)
    sonalika.groups.connect(tapu_sena)
    pankaj.groups.connect(tapu_sena)
    gurucharand.groups.connect(tapu_sena)

    jethalal.groups.connect(purush_mandal)
    aatmaram.groups.connect(purush_mandal)
    hansraj.groups.connect(purush_mandal)
    roshan_m.groups.connect(purush_mandal)
    taarak.groups.connect(purush_mandal)
    krishnan.groups.connect(purush_mandal)
    popatlal.groups.connect(purush_mandal)

    daya.groups.connect(mahila_mandal)
    madhavi.groups.connect(mahila_mandal)
    komal.groups.connect(mahila_mandal)
    roshan_f.groups.connect(mahila_mandal)
    anjali.groups.connect(mahila_mandal)
    babita.groups.connect(mahila_mandal)

    gokuldham: Society = Society(
        name="Gokuldham Society, Pavdar Galli, Goregaon East"
    ).save()
    gokuldham.committee_members.connect(
        aatmaram, {HasCommitteeMember.position.name: "Secretary"}
    )
    gokuldham.committee_members.connect(
        krishnan, {HasCommitteeMember.position.name: "Treasurer"}
    )
    gokuldham.committee_members.connect(
        popatlal, {HasCommitteeMember.position.name: "Member"}
    )


if __name__ == "__main__":
    create_nodes()
