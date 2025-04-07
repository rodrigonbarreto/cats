from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select

from models.pet_model import PetModel
from core.deps import get_db_session
from services.external_dog import get_external_dogs


router = APIRouter()


@router.get("/", response_model=List[Dict[str, Any]])
async def list_external_dogs(limit: int = 10):
    """
    Get dogs from external TheDogAPI
    """
    try:
        dogs = await get_external_dogs(limit)
        return dogs
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching external dogs: {str(e)}"
        )


@router.get("/my_dogs", response_model=List[PetModel])
async def list_my_dogs(db: Session = Depends(get_db_session)):
    """
    List all dogs saved in the database
    """
    dogs = db.execute(select(PetModel).where(PetModel.type == "dog")).scalars().all()
    return dogs


@router.get("/{dog_id}", response_model=PetModel)
async def get_dog(dog_id: int, db: Session = Depends(get_db_session)):
    """
    Get a specific dog from the database by ID
    """
    dog = db.get(PetModel, dog_id)
    if not dog or dog.type != "dog":
        raise HTTPException(status_code=404, detail=f"Dog with ID {dog_id} not found")
    return dog


dog_example = {
    "width": 800,
    "height": 600,
    "url": "https://cdn2.thedogapi.com/images/xyz789.jpg",
    "name": "Rex",
}


@router.post("/", response_model=PetModel, status_code=201)
async def create_dog(
    dog_data: Dict[str, Any] = Body(..., example=dog_example),
    db: Session = Depends(get_db_session),
):
    """
    Create a new dog in the database
    """
    new_dog = PetModel(
        type="dog",
        code_pet="dog",
        width=dog_data.get("width", 0),
        height=dog_data.get("height", 0),
        url=dog_data.get("url", ""),
        name=dog_data.get("name", "Unknown Dog"),
    )
    db.add(new_dog)
    db.commit()
    db.refresh(new_dog)
    return new_dog


@router.put("/{dog_id}", response_model=PetModel)
async def update_dog(
    dog_id: int,
    dog_data: Dict[str, Any] = Body(..., example=dog_example),
    db: Session = Depends(get_db_session),
):
    """
    Update an existing dog in the database
    """
    dog_found = db.get(PetModel, dog_id)
    if not dog_found or dog_found.type != "dog":
        raise HTTPException(status_code=404, detail=f"Dog with ID {dog_id} not found")

    dog_found.width = dog_data.get("width", dog_found.width)
    dog_found.height = dog_data.get("height", dog_found.height)
    dog_found.url = dog_data.get("url", dog_found.url)
    dog_found.name = dog_data.get("name", dog_found.name)

    db.add(dog_found)
    db.commit()
    db.refresh(dog_found)
    return dog_found


@router.delete("/{dog_id}", status_code=204)
async def delete_dog(dog_id: int, db: Session = Depends(get_db_session)):
    """
    Remove a dog from the database
    """
    dog_found = db.get(PetModel, dog_id)
    if not dog_found or dog_found.type != "dog":
        raise HTTPException(status_code=404, detail=f"Dog with ID {dog_id} not found")

    db.delete(dog_found)
    db.commit()
