from django.apps import AppConfig

class BewerbungConfig(AppConfig):
    name = 'bewerbung'

    def ready(self):
        import bewerbung.signals  
