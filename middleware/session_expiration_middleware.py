from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.utils import timezone

class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user is authenticated and has an active session
        if request.user.is_authenticated and request.session.session_key:
            session_key = request.session.session_key
            try:
                # Get the session object
                session = Session.objects.get(session_key=session_key)
                
                # Check if the session has expired
                expiry_date = session.expire_date
                current_time = timezone.now()
                if current_time > expiry_date:
                    # Session has expired, delete session data
                    session.delete()
                    
                    # Log out the user
                    logout(request)
            except Session.DoesNotExist:#pylint:disable=no-member
                pass  # Session not found, do nothing
        
        return response
