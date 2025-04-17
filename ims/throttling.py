from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class AdminRateThrottle(UserRateThrottle):
    scope = 'admin'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.role == 'admin':
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk
            }
        return None

class InterviewerRateThrottle(UserRateThrottle):
    scope = 'interviewer'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.role == 'interviewer':
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk
            }
        return None

class CandidateRateThrottle(UserRateThrottle):
    scope = 'candidate'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.role == 'candidate':
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk
            }
        return None

class DefaultUserRateThrottle(UserRateThrottle):
    scope = 'user' 