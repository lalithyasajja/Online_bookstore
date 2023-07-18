from app.models import User

def user_context_processor(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return {'user': user}