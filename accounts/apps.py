from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


class DateLimitAppConfig(AppConfig):
    name = 'accounts'
    def ready(self):
        import accounts.signals

default_app_config = 'accounts.apps.AccountsConfig'
