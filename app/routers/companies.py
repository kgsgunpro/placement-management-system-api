from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Company, User
from app.dependencies import require_roles
from app.schemas.placement import Company as CompanySchema, CompanyInput


router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/", response_model=list[CompanySchema])
def list_companies(database: Session = Depends(get_db)):
    return database.scalars(select(Company).order_by(Company.name)).all()


@router.get("/{company_id}", response_model=CompanySchema)
def get_company(company_id: int, database: Session = Depends(get_db)):
    company = database.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=CompanySchema, status_code=201)
def create_company(
    company_data: CompanyInput,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    company = Company(**company_data.model_dump(mode="json"))
    database.add(company)
    try:
        database.commit()
    except IntegrityError:
        database.rollback()
        raise HTTPException(status_code=409, detail="Company already exists")
    database.refresh(company)
    return company


@router.put("/{company_id}", response_model=CompanySchema)
def update_company(
    company_id: int,
    company_data: CompanyInput,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    company = database.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for field, value in company_data.model_dump(mode="json").items():
        setattr(company, field, value)
    try:
        database.commit()
    except IntegrityError:
        database.rollback()
        raise HTTPException(status_code=409, detail="Company already exists")
    database.refresh(company)
    return company


@router.delete("/{company_id}", status_code=204)
def delete_company(
    company_id: int,
    database: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    company = database.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    if company.drives:
        raise HTTPException(status_code=409, detail="Cannot delete a company with placement drives")
    database.delete(company)
    database.commit()