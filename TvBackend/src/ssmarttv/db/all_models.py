"""Import every model module so Alembic sees the full ``Base.metadata``.

Update this file as new domains add models. ``alembic/env.py`` imports it.
"""
from ssmarttv.domains.auth import models as auth_models
from ssmarttv.domains.carousel import models as carousel_models
from ssmarttv.domains.catalog import models as catalog_models
from ssmarttv.domains.channels import models as channels_models
from ssmarttv.domains.engagement import models as engagement_models
from ssmarttv.domains.subscriptions import models as subscription_models

__all__ = [
    "auth_models",
    "carousel_models",
    "catalog_models",
    "channels_models",
    "engagement_models",
    "subscription_models",
]
