from rest_framework_simplejwt.tokens import RefreshToken


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user_with_tenant(cls, user, application_id):
        """Cria token JWT com application_id no payload"""
        token = cls.for_user(user)
        token['application_id'] = application_id
        return token