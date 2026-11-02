from django.conf import settings
from django.db.models.functions import Lower
from django.core.validators import RegexValidator
from django.db import models


hex_color_validator = RegexValidator(
    regex=r"\A#[0-9A-Fa-f]{6}\Z",
    message="Enter a valid hex color, such as #F97316."
)

class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=7,
        validators=[hex_color_validator]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "user",
                name="unique_category_name_per_user_ci"
            )
        ]

    def __str__(self):
        return self.name
