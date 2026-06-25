from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models


class ApplicationSession(AbstractBaseSession):
    uid = models.CharField(max_length=80, blank=True, null=True, default=None)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    class Meta:
        app_label = "mis_template"


class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        return ApplicationSession

    def create_model_instance(self, data):
        obj = super().create_model_instance(data)
        try:
            uid = data['account_authentication_methods'][0]['uid']
        except (ValueError, TypeError, KeyError):
            uid = None
        obj.uid = uid
        return obj

    @classmethod
    def close_session_by_subject_uid(cls, uid):
        sessions = cls.get_model_class().objects.filter(uid=uid)
        for session in sessions:
            session.delete()
