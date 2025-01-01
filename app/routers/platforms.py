from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.PlatformResponse)
def create_platform(
    platform: schemas.PlatformCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_platform(db=db, platform=platform, user_id=current_user.id)


@router.get("/", response_model=list[schemas.PlatformResponse])
def get_platforms(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    platforms = crud.get_platforms_by_user(db=db, user_id=current_user.id)
    return platforms


@router.get("/{platform_id}", response_model=schemas.PlatformResponse)
def get_platform(
    platform_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    platform = crud.get_platform(db=db, platform_id=platform_id)
    if platform.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view this platform",
        )
    return platform


@router.delete("/{platform_id}", response_model=schemas.PlatformResponse)
def delete_platform(
    platform_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    platform = crud.get_platform(db=db, platform_id=platform_id)
    if platform.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this platform",
        )
    return crud.delete_platform(db=db, platform_id=platform_id)


@router.put("/{platform_id}", response_model=schemas.PlatformResponse)
def update_platform(
    platform_id: int,
    platform: schemas.PlatformCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    existing_platform = crud.get_platform(db=db, platform_id=platform_id)
    if existing_platform.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this platform",
        )

    updated_platform = crud.update_platform(
        db=db, platform_id=platform_id, platform_update=platform
    )
    return updated_platform
