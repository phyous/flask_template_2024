from flask import Flask, jsonify, request
from models import SessionLocal, UserDB, UserCreate, UserResponse
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

app = Flask(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/healthcheck")
def healthcheck():
    return jsonify({"status": "healthy"}), 200

@app.route("/users", methods=["POST"])
def create_user():
    try:
        # Validate input data using Pydantic
        user_data = UserCreate(**request.json)
        
        # Create SQLAlchemy model instance
        db = next(get_db())
        db_user = UserDB(
            email=user_data.email,
            name=user_data.name
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Use model_validate instead of from_orm
        response = UserResponse.model_validate(db_user)
        return jsonify(response.model_dump()), 201
    
    except ValidationError as e:
        return jsonify({"error": "Invalid input data", "details": e.errors()}), 400
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Email already exists"}), 400

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    db = next(get_db())
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Replace from_orm with model_validate
    response = UserResponse.model_validate(user)
    return jsonify(response.model_dump())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 