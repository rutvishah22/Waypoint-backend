"""
Request models - define what data API accepts.
"""

from pydantic import BaseModel, Field, validator


class AnalyzeRequest(BaseModel):
    """
    Model for analysis request.
    """

    product_idea: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Product idea in one sentence"
    )

    tier: str = Field(
        default="prelaunch",
        description="prelaunch or postlaunch"
    )

    email: str = Field(
        ...,
        description="User email"
    )

    @validator("product_idea")
    def validate_idea(cls, v):
        if not v.strip():
            raise ValueError("Product idea cannot be empty")
        return v.strip()

    @validator("tier")
    def validate_tier(cls, v):
        # Accept both formats for compatibility
        allowed = {"prelaunch", "postlaunch", "pre_launch", "post_launch"}
        if v not in allowed:
            raise ValueError("Tier must be prelaunch or postlaunch")
        
        # Normalize to no underscore format
        return v.replace("_", "")

    @validator("email")
    def validate_email(cls, v):
        if not v or "@" not in v:
            raise ValueError("Please provide a valid email")
        return v.strip().lower()