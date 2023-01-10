from .utils import get_user_current_balance


def get_context(request):

    context = {'title': "FinanceApp"}

    if request.user.is_authenticated:
        context.update({'username': request.user})
        bc = get_user_current_balance(request.user)
        if bc:
            context.update({'bc': bc})

    return context
