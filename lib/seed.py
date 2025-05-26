from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie \

DATABASE_URL = 'sqlite:///freebies.db'  

def seed():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data (optional)
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()
    session.commit()

    # Create companies
    c1 = Company(name='OpenAI', founding_year=2015)
    c2 = Company(name='Google', founding_year=1998)
    c3 = Company(name='Microsoft', founding_year=1975)

    session.add_all([c1, c2, c3])
    session.commit()

    # Create devs
    d1 = Dev(name='Alice')
    d2 = Dev(name='Bob')
    d3 = Dev(name='Charlie')

    session.add_all([d1, d2, d3])
    session.commit()

    # Create freebies using give_freebie method
    f1 = c1.give_freebie(d1, 'Stickers', 5)
    f2 = c2.give_freebie(d1, 'T-Shirt', 20)
    f3 = c1.give_freebie(d2, 'Mug', 10)
    f4 = c3.give_freebie(d3, 'Notebook', 15)
    f5 = c3.give_freebie(d2, 'Pen', 3)

    session.add_all([f1, f2, f3, f4, f5])
    session.commit()

    print("Seed data inserted successfully!")

if __name__ == '__main__':
    seed()
