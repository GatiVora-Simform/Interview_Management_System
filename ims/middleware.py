from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponse
import time

class RoleBasedThrottlingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Process request for throttling based on user roles
        """
        # Skip throttling for admin pages, static files, and token endpoints
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/static/') or
            request.path == '/api/auth/token/' or 
            request.path == '/api/auth/token/refresh/'):
            return None
            
        # Client IP and path for cache key
        ip = self.get_client_ip(request)
        path = request.path
        
        # Create unique cache key for this IP/path combination
        cache_key = f"throttle:{ip}:{path}"
        
        # Set different rate limits based on user role
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                # for admins - 500 requests per minute
                rate_limit = 500
                window = 60  # 1 minute
            elif request.user.role == 'interviewer':
                # for interviewers - 200 requests per minute
                rate_limit = 200
                window = 60 
            elif request.user.role == 'candidate':
                # for candidates - 100 requests per minute
                rate_limit = 100
                window = 60  
            else:
                # Default user rate
                rate_limit = 100
                window = 60  # 1 minute
        else:
            # For unauthenticated users
            rate_limit = 30
            window = 60  # 1 minute
        
        # Check if this request exceeds the rate limit
        request_history = cache.get(cache_key, [])
        
        # Clean old requests from history (older than the window)
        current_time = time.time()
        request_history = [t for t in request_history if current_time - t < window]
        
        # Check if we've hit the limit 
        if len(request_history) >= rate_limit:
            return HttpResponse(
                "Too many requests. Please try again later.",
                status=429,
                headers={"Retry-After": str(window)}
            )
        
        # Add current request to history
        request_history.append(current_time)
        
        # Update cache
        cache.set(cache_key, request_history, window)
        
        return None
    
    def get_client_ip(self, request):
        """
        Get client IP from request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 