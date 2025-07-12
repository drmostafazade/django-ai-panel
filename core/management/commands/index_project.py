import json
from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.cache import cache
class Command(BaseCommand):
    def handle(self, *a, **kw):
        print('Indexing project schema...')
        EXCLUDED_APPS = ['admin','auth','contenttypes','sessions','messages','staticfiles','core','rest_framework']
        project_schema = {}
        for model in apps.get_models():
            app_label = model._meta.app_label
            if app_label in EXCLUDED_APPS: continue
            if app_label not in project_schema: project_schema[app_label] = {}
            fields_info = {f.name: f.get_internal_type() for f in model._meta.get_fields()}
            project_schema[app_label][model._meta.model_name] = fields_info
        cache.set('project_db_schema', project_schema, timeout=None)
        print('Schema successfully cached.')
