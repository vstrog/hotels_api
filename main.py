from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI(
    title="REST API Example",
    description="REST API example with SQLite persistence",
    version="1.0"
)

# --- SQLAlchemy Setup ---
# Path to the SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./hotels.db"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# --- SQLAlchemy Model (Database Table) ---
class HotelDB(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    name = Column(String, index=True, nullable=False)
    rating = Column(Integer, nullable=False) # Validation handled by Pydantic model

# Create tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# --- Pydantic Models (for request/response validation) ---
class HotelBase(BaseModel):
    city: str
    description: str
    name: str
    rating: int = Field(..., ge=1, le=5)

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    city: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class Hotel(HotelBase):
    id: int
    class Config:
        from_attributes = True # Important for SQLAlchemy

class PaginatedResponse(BaseModel):
    content: List[Hotel]
    last: bool
    totalElements: int
    totalPages: int
    size: int
    number: int
    sort: Optional[str] = None # Sorting can be a string or None
    numberOfElements: int
    first: bool

# --- Dependency to get the database session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---
@app.get("/api/v1/hotels", response_model=PaginatedResponse, tags=["Hotel Controller"],
         summary="Get a paginated list of all hotels.")
async def get_all_hotels(
    page: int = 0,
    size: int = 100,
    sort: Optional[str] = None, # Sorting not implemented in this example
    db: Session = Depends(get_db)
):
    """Get a paginated list of all hotels."""
    # Validate pagination parameters
    if page < 0:
        page = 0
    if size <= 0:
        size = 100 # Or raise an HTTPException
    if size > 1000: # Set a maximum limit
        size = 1000

    offset = page * size

    # Get total count
    total = db.query(HotelDB).count()

    # Get paginated results
    hotels_list_db = db.query(HotelDB).offset(offset).limit(size).all()

    # Convert SQLAlchemy objects to Pydantic models
    hotels_list = [Hotel.model_validate(h) for h in hotels_list_db]

    total_pages = (total + size - 1) // size if size > 0 else 0
    is_last = (offset + len(hotels_list) >= total)
    is_first = (page == 0)

    return PaginatedResponse(
        content=hotels_list,
        last=is_last,
        totalElements=total,
        totalPages=total_pages,
        size=size,
        number=page,
        sort=sort,
        numberOfElements=len(hotels_list),
        first=is_first
    )

@app.post("/api/v1/hotels", response_model=Hotel, status_code=status.HTTP_201_CREATED,
          tags=["Hotel Controller"], summary="Create a hotel resource.")
async def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    """Create a hotel resource."""
    # Create SQLAlchemy object
    db_hotel = HotelDB(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel) # Refresh to get the ID from the database
    # Return Pydantic model
    return Hotel.model_validate(db_hotel)

@app.get("/api/v1/hotels/{id}", response_model=Hotel, tags=["Hotel Controller"],
         summary="Get a single hotel.")
async def get_hotel_by_id(id: int, db: Session = Depends(get_db)):
    """Get a single hotel."""
    db_hotel = db.query(HotelDB).filter(HotelDB.id == id).first()
    if db_hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {id} not found"
        )
    return Hotel.model_validate(db_hotel)

@app.put("/api/v1/hotels/{id}", response_model=Hotel, tags=["Hotel Controller"],
         summary="Update a hotel resource.")
async def update_hotel(id: int, hotel_update: HotelUpdate, db: Session = Depends(get_db)):
    """Update a hotel resource."""
    db_hotel = db.query(HotelDB).filter(HotelDB.id == id).first()
    if db_hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {id} not found"
        )

    # Convert updates to a dictionary, excluding unset fields
    update_data = hotel_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_hotel, field, value)

    db.commit()
    db.refresh(db_hotel)
    return Hotel.model_validate(db_hotel)

@app.delete("/api/v1/hotels/{id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Hotel Controller"], summary="Delete a hotel resource.")
async def delete_hotel(id: int, db: Session = Depends(get_db)):
    """Delete a hotel resource."""
    db_hotel = db.query(HotelDB).filter(HotelDB.id == id).first()
    if db_hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {id} not found"
        )
    db.delete(db_hotel)
    db.commit()
    return # Return empty response (204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8090)
