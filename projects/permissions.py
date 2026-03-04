from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCreatorOrReadOnly(BasePermission):
    """
    Custom permission:
    - Authenticated users can create
    - Only project creator can update/delete
    - Others can read
    """
    
    def has_permission(self, request, view):
        # Allow read-only access for anyone
        if request.method in SAFE_METHODS:
            return True
        
        # Allow creation only if user is authenticated
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        
        return True
    
    def has_object_permission(self, request, view, obj):
        # Allow read-only access
        if request.method in SAFE_METHODS:
            return True
        
        # Allow update/delete only if the user is the creator
        return obj.creator == request.user