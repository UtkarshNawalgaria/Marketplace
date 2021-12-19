from django.contrib.auth.decorators import user_passes_test


def role_required(role):
    """
    Requires the user to be customer to access the page
    """

    def is_role(user):
        if user.is_authenticated and user.is_active and user.profile_type == role:
            return True
        return False

    return user_passes_test(is_role)
