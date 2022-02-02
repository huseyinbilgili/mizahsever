from django.utils.translation import gettext_lazy as _
from model_utils import Choices

GENDER_TYPES = Choices(
    (1, _("Male")),
    (2, _("Female")),
)

USER_TYPES = Choices(
    (1, "default", _("Default")),
    (2, "editor", _("Editor")),
)

USER_STATUSES = Choices(
    (1, "active", _("Active")),
    (2, "passive", _("Passive")),
)
