from .models import Comment
from django.http import JsonResponse
from django.conf import settings  # Import the settings module

class DynamicCommentsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == "POST" and response.status_code == 200:
            # If it's an AJAX POST request, update the response with the latest comments
            try:
                # Assuming you've defined movie_id somewhere, adjust this part accordingly
                movie_id = request.path.split('/')[-2]
                data = {
                    'comments': [{'user': c.user.username, 'created_at': c.created_at.strftime("%Y-%m-%d %H:%M:%S"), 'comment': c.comment}
                                 for c in Comment.objects.filter(movie_id=movie_id).order_by('-created_at')]
                }
                response = JsonResponse(data)
            except Exception as e:
                print(f"Error in middleware: {e}")
                # Print the error for debugging purposes

        return response