from rest_framework import permissions
 
class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
         return request.user.is_authenticated and request.user.role == 'admin'
 
class IsInterviewer(permissions.BasePermission):

    def has_permission(self, request, view):
         return request.user.is_authenticated and request.user.role == 'interviewer'
 
class IsCandidate(permissions.BasePermission):

    def has_permission(self, request, view):
         return request.user.is_authenticated and request.user.role == 'candidate'
 
class IsAdminOrInterviewer(permissions.BasePermission):

    def has_permission(self, request, view):
         return request.user.is_authenticated and request.user.role in ['admin', 'interviewer'] 
 
class AdminFullInterviewerReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
             return False
         
        if request.user.role == 'admin':
             return True
             
        if request.user.role == 'interviewer' and request.method in permissions.SAFE_METHODS:
             return True
             
        return False 