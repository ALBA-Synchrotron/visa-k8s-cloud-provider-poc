from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User


class ALBASSOAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, _):
        return False


class ALBASSOSocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, _, __):
        return True

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return
        if 'preferred_username' in sociallogin.account.extra_data.keys():
            try:
                username = sociallogin.account.extra_data['preferred_username']
                user = User.objects.get(username=username)

                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
