from pydantic import BaseModel, Field


class Property(BaseModel):
    area: int = Field(
        ...,
        gt=0,
        description="Superficie construida en metros cuadrados.",
        examples=[120],
    )
    bedrooms: int = Field(
        ...,
        ge=0,
        description="Cantidad de dormitorios.",
        examples=[3],
    )
    bathrooms: int = Field(
        ...,
        ge=0,
        description="Cantidad de baños.",
        examples=[2],
    )
    neighborhood: str = Field(
        ...,
        description="Barrio donde se ubica la propiedad.",
        examples=["Pocitos"],
    )


class ClassifiedProperty(BaseModel):
    property: Property = Field(..., description="Características originales de la propiedad.")
    predicted_price: float = Field(
        ...,
        description="Precio estimado por el modelo (USD).",
        examples=[185000.0],
    )

