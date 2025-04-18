from rest_framework import permissions
 
class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
 
class IsInterviewer(permissions.BasePermission):
    """
    Allows access only to interviewer users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'interviewer'
 
class IsCandidate(permissions.BasePermission):
    """
    Allows access only to candidate users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'candidate'
 
class AdminFullInterviewerReadOnly(permissions.BasePermission):
    """
    Allows full access to admin users and read-only access to interviewer users.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
         
        if request.user.role == 'admin':
            return True
             
        if request.user.role == 'interviewer' and request.method in permissions.SAFE_METHODS:
            return True
             
        return False 