from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

DATABASE_URL = 'sqlite:///freebies.db'  

def debug():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("=== Companies ===")
    for company in session.query(Company).all():
        print(company)
    print()

    print("=== Devs ===")
    for dev in session.query(Dev).all():
        print(dev)
    print()

    print("=== Freebies ===")
    for freebie in session.query(Freebie).all():
        print(freebie.print_details())
    print()

    # Test Company.oldest_company
    oldest = Company.oldest_company(session)
    print(f"Oldest company: {oldest.name} founded in {oldest.founding_year}")
    print()

    # Pick a dev and check received_one()
    dev = session.query(Dev).filter_by(name="Alice").first()
    print(f"Has {dev.name} received a 'T-Shirt'? {dev.received_one('T-Shirt')}")
    print(f"Has {dev.name} received a 'Pen'? {dev.received_one('Pen')}")
    print()

    # Check company.devs property
    company = session.query(Company).filter_by(name="OpenAI").first()
    print(f"Developers who collected freebies from {company.name}: {[dev.name for dev in company.devs]}")
    print()

    # Check dev.companies property
    print(f"Companies that {dev.name} has collected freebies from: {[comp.name for comp in dev.companies]}")
    print()

    # Test Dev.give_away()
    dev_bob = session.query(Dev).filter_by(name="Bob").first()
    freebie_to_give = session.query(Freebie).filter_by(item_name="Mug").filter(Freebie.dev==dev_bob).first()
    if freebie_to_give:
        print(f"Before give_away: {freebie_to_give.dev.name} owns {freebie_to_give.item_name}")
        # Bob gives Mug to Alice
        success = dev_bob.give_away(dev, freebie_to_give)
        session.commit()
        print(f"Give away successful? {success}")
        print(f"After give_away: {freebie_to_give.dev.name} owns {freebie_to_give.item_name}")
    else:
        print("No Mug freebie owned by Bob to give away.")
    print()

if __name__ == "__main__":
    debug()
