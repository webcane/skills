def can_delete(role):
    return role in {"owner", "member"}

def can_view(role):
    return role in {"owner", "member"}
