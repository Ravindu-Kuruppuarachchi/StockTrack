from database import engine, Base, SessionLocal, User

# Note: We removed the 'passlib' imports

Base.metadata.create_all(bind=engine)
db = SessionLocal()

existing_user = db.query(User).filter(User.email == "admin@isa.com").first()

if not existing_user:
    # STORE PLAIN TEXT DIRECTLY
    admin_user = User(email="admin@isa.com", password="airarabia")
    
    db.add(admin_user)
    db.commit()
    print("✅ Admin user created (Plain Text)!")
else:
    print("⚠️ Admin user already exists.")

db.close()