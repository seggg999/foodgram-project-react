from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from djoser.views import UserViewSet


class CastomDjUserViewSet(UserViewSet):
    '''Кастомный UserViewSet от djoser'''

    @action(["get"], detail=False,
            permission_classes=[IsAuthenticated]
            )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(["get"], detail=False,
            permission_classes=[IsAuthenticated]
            )
    def subscriptions(self, request, *args, **kwargs):
        '''Мои подписки.'''
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(["post", "delete"], detail=True,
            permission_classes=[IsAuthenticated]
            )
    def subscribe(self, request, pk=None):
        '''Добавить/удалить рецепт в подписки. '''
        self.get_object = self.get_instance
        return self.retrieve(request)

    def activation(self, request, *args, **kwargs):
        '''pass'''
        pass

    def resend_activation(self, request, *args, **kwargs):
        '''pass'''
        pass

    def reset_password(self, request, *args, **kwargs):
        '''pass'''
        pass

    def reset_password_confirm(self, request, *args, **kwargs):
        '''pass'''
        pass

    def set_username(self, request, *args, **kwargs):
        '''pass'''
        pass

    def reset_username(self, request, *args, **kwargs):
        '''pass'''
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        '''pass'''
        pass
