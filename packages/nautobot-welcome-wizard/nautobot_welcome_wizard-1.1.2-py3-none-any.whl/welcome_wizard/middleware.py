"""Middleware for the Welcome Wizard plugin."""

import logging
from django.contrib import messages
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe

logger = logging.getLogger("welcome_wizard.middleware")


class Prerequisites:
    """Middleware for determining prerequisites and adding notifications."""

    def __init__(self, get_request):
        """Capture the request on the initialization."""
        self.get_request = get_request

    def __call__(self, request):
        """Capture the response and return it."""
        return self.get_request(request)

    def process_view(self, request, view_func, view_args, view_kwargs):  # pylint: disable=W0613,R0201
        """Process the view to determine if it's one we want to intercept."""
        # If no user or they aren't authenticated, return to hit the default login redirect
        if not hasattr(request, "user") or not request.user.is_authenticated:
            return
        if request.path.endswith("/add/"):
            # Check if using a Nautobot view class.
            if not (
                hasattr(view_func, "view_class")
                and hasattr(view_func.view_class, "model_form")
                and view_func.view_class.model_form is not None
            ):
                return
            base_fields = view_func.view_class.model_form.base_fields
            for field in base_fields:
                if (
                    base_fields[field].required
                    and hasattr(base_fields[field], "queryset")
                    and not base_fields[field].queryset.exists()
                ):
                    name = base_fields[field].label or field.replace("_", " ").title()
                    reverse_name = field.replace("_", "")
                    try:
                        reverse_link = reverse(f"{request.resolver_match.app_names[0]}:{reverse_name}_add")
                    except NoReverseMatch as error:
                        logger.warning("No Reverse Match was found for %s. %s", reverse_name, error)
                        reverse_link = ""
                    msg = f"You need to configure a <a href='{reverse_link}'>{name}</a> before you create this item."
                    messages.error(request, mark_safe(msg))  # nosec
