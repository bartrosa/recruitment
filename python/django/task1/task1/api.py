from typing import Tuple, Dict, Any
from ninja import NinjaAPI, Path, Router # Router is good for organization
from django.shortcuts import get_object_or_404
from django.db import models as django_db_models
from django.db import transaction
from django.utils import timezone

from .models import SomeModel
from .schemas import SomeModelUpdatePayload, SomeModelResponse

# This router will group all endpoints related to SomeModel
some_model_router = Router()

@some_model_router.put(
    "/{model_id}/update",
    response={200: SomeModelResponse, 404: Dict[str, str], 422: Dict[str, str]},
    summary="Update a SomeModel instance",
    description="Updates `field_a` and `field_b` of a specified SomeModel instance, "
                "increments its `number_of_updates` counter, and updates the "
                "`last_modified` timestamp.",
    tags=["SomeModel Operations"] # Tag for OpenAPI documentation grouping
)
@transaction.atomic # Ensure all database operations are atomic
def update_some_model(
    request,
    model_id: int = Path(..., description="The ID of the SomeModel instance to update."),
    payload: SomeModelUpdatePayload = None
) -> Tuple[int, Any]:
    """
    Updates an instance of SomeModel based on the provided payload.
    """
    instance = get_object_or_404(SomeModel, id=model_id)

    instance.field_a = payload.field_a
    instance.field_b = payload.field_b
    instance.number_of_updates = django_db_models.F('number_of_updates') + 1
    
    instance.save()
    instance.refresh_from_db()

    return 200, instance
    