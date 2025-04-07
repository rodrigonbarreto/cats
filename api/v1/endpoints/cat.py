from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select

from models.pet_model import PetModel
from core.deps import get_db_session
from services.external_cat import get_external_cats


router = APIRouter()


@router.get("/", response_model=List[Dict[str, Any]])
async def list_external_cats(limit: int = 10):
    """
    Get cats from external TheCatAPI
    """
    try:
        cats = await get_external_cats(limit)
        return cats
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching external cats: {str(e)}"
        )


@router.get("/my_cats", response_model=List[PetModel])
async def list_my_cats(db: Session = Depends(get_db_session)):
    """
    List all cats saved in the database
    """
    cats = db.execute(select(PetModel).where(PetModel.type == "cat")).scalars().all()
    return cats


@router.get("/{cat_id}", response_model=PetModel)
async def get_cat(cat_id: int, db: Session = Depends(get_db_session)):
    """
    Get a specific cat from the database by ID
    """
    cat = db.get(PetModel, cat_id)
    if not cat or cat.type != "cat":
        raise HTTPException(status_code=404, detail=f"Cat with ID {cat_id} not found")
    return cat


cat_example = {
    "width": 640,
    "height": 480,
    "url": "https://cdn2.thecatapi.com/images/abc123.jpg",
    "name": "Fluffy",
}


@router.post("/", response_model=PetModel, status_code=201)
async def create_cat(
    cat_data: Dict[str, Any] = Body(..., example=cat_example),
    db: Session = Depends(get_db_session),
):
    """
    Create a new cat in the database
    """
    new_cat = PetModel(
        type="cat",
        code_pet="cat",
        width=cat_data.get("width", 0),
        height=cat_data.get("height", 0),
        url=cat_data.get("url", ""),
        name=cat_data.get("name", "Unknown Cat"),
    )
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat


@router.put("/{cat_id}", response_model=PetModel)
async def update_cat(
    cat_id: int,
    cat_data: Dict[str, Any] = Body(..., example=cat_example),
    db: Session = Depends(get_db_session),
):
    """
    Update an existing cat in the database
    """
    cat_found = db.get(PetModel, cat_id)
    if not cat_found or cat_found.type != "cat":
        raise HTTPException(status_code=404, detail=f"Cat with ID {cat_id} not found")

    cat_found.width = cat_data.get("width", cat_found.width)
    cat_found.height = cat_data.get("height", cat_found.height)
    cat_found.url = cat_data.get("url", cat_found.url)
    cat_found.name = cat_data.get("name", cat_found.name)

    db.add(cat_found)
    db.commit()
    db.refresh(cat_found)
    return cat_found


@router.delete("/{cat_id}", status_code=204)
async def delete_cat(cat_id: int, db: Session = Depends(get_db_session)):
    """
    Remove a cat from the database
    """
    cat_found = db.get(PetModel, cat_id)
    if not cat_found or cat_found.type != "cat":
        raise HTTPException(status_code=404, detail=f"Cat with ID {cat_id} not found")

    db.delete(cat_found)
    db.commit()
