from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="REST example",
    description="REST example",
    version="1.0"
)

# Models
class Hotel(BaseModel):
    id: Optional[int] = None
    city: str
    description: str
    name: str
    rating: int = Field(..., ge=1, le=5)

class HotelCreate(BaseModel):
    city: str
    description: str
    name: str
    rating: int = Field(..., ge=1, le=5)

class HotelUpdate(BaseModel):
    city: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class PaginatedResponse(BaseModel):
    content: List[Hotel]
    last: bool
    totalElements: int
    totalPages: int
    size: int
    number: int
    sort: Optional[str]
    numberOfElements: int
    first: bool

# In-memory database
hotels_db = {}
next_id = 1

# Endpoints
@app.get("/example/v1/hotels", response_model=PaginatedResponse, tags=["Hotel Controller"],
         summary="Get a paginated list of all hotels.")
async def get_all_hotels(
    page: int = 0,
    size: int = 100,
    sort: Optional[str] = None
):
    """Get a paginated list of all hotels."""
    hotels_list = list(hotels_db.values())
    
    total = len(hotels_list)
    start = page * size
    end = start + size
    paginated_hotels = hotels_list[start:end]
    
    return PaginatedResponse(
        content=paginated_hotels,
        last=(end >= total),
        totalElements=total,
        totalPages=(total + size - 1) // size if size > 0 else 0,
        size=size,
        number=page,
        sort=sort,
        numberOfElements=len(paginated_hotels),
        first=(page == 0)
    )

@app.post("/example/v1/hotels", response_model=Hotel, status_code=status.HTTP_201_CREATED,
          tags=["Hotel Controller"], summary="Create a hotel resource.")
async def create_hotel(hotel: HotelCreate):
    """Create a hotel resource."""
    global next_id
    
    new_hotel = Hotel(
        id=next_id,
        city=hotel.city,
        description=hotel.description,
        name=hotel.name,
        rating=hotel.rating
    )
    
    hotels_db[next_id] = new_hotel
    next_id += 1
    
    return new_hotel

@app.get("/example/v1/hotels/{id}", response_model=Hotel, tags=["Hotel Controller"],
         summary="Get a single hotel.")
async def get_hotel_by_id(id: int):
    """Get a single hotel."""
    if id not in hotels_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {id} not found"
        )
    return hotels_db[id]

@app.put("/example/v1/hotels/{id}", response_model=Hotel, tags=["Hotel Controller"],
         summary="Update a hotel resource.")
async def update_hotel(id: int, hotel_update: HotelUpdate):
    """Update a hotel resource."""
    if id not in hotels_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {id} not found"
        )
    
    existing_hotel = hotels_db[id]
    update_data = hotel_update.dict(exclude_unset=True)
    
    updated_hotel = existing_hotel.copy(update=update_data)
    hotels_db[id] = updated_hotel
    
    return updated_hotel

@app.delete("/example/v1/hotels/{id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Hotel Controller"], summary="Delete a hotel resource.")
async def delete_hotel(id: int):
    """Delete a hotel resource."""
    if id not in hotels_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {id} not found"
        )
    
    del hotels_db[id]
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8090)
