#!/bin/bash
set -e
PROJECT_DIR="/var/www/bsepar_panel"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
echo -e "${BLUE}--- Starting AI Panel Phase 1 Final Setup ---${NC}"
cd "$PROJECT_DIR"
echo -e "${BLUE}Verifying 'core' app registration...${NC}"
python3 manage.py shell -c "from django.apps import apps; apps.get_app_config('core')"
echo -e "${GREEN}'core' app is registered!${NC}"
echo -e "${BLUE}Cleaning up old migration records...${NC}"
python3 manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute(\"DELETE FROM django_migrations WHERE app = 'core'\")"
echo -e "${BLUE}Creating project files...${NC}"
cat <<'EOF' > core/models.py
from django.db import models
class AIProviderSetting(models.Model):
    class ProviderChoices(models.TextChoices): OPENAI='openai', 'OpenAI'; CLAUDE='claude', 'Anthropic (Claude)'; GEMINI='gemini', 'Google (Gemini)'; GROQ='groq', 'Groq'
    provider = models.CharField(max_length=50, choices=ProviderChoices.choices, unique=True); api_key = models.CharField(max_length=255); is_active = models.BooleanField(default=True)
EOF
cat <<'EOF' > core/admin.py
from django.contrib import admin
from .models import AIProviderSetting
@admin.register(AIProviderSetting)
class AIProviderSettingAdmin(admin.ModelAdmin): list_display = ('provider', 'is_active')
EOF
mkdir -p core/management/commands; touch core/management/__init__.py core/management/commands/__init__.py
cat <<'EOF' > core/management/commands/index_project.py
import json; from django.core.management.base import BaseCommand; from django.apps import apps; from django.core.cache import cache
class Command(BaseCommand):
    def handle(self, *a, **kw): print('Indexing schema...'); cache.set('project_db_schema', {m._meta.app_label: {m._meta.model_name: {f.name: f.get_internal_type() for f in m._meta.get_fields()}} for m in apps.get_models() if m._meta.app_label not in ['admin','auth','contenttypes','sessions','messages','staticfiles','core','rest_framework']}, timeout=None); print('Schema cached.')
EOF
echo -e "${YELLOW}Running Django database commands...${NC}"
python3 manage.py makemigrations core; python3 manage.py migrate; python3 manage.py index_project
echo -e "${GREEN}--- Phase 1 is Finally COMPLETE! ---${NC}"
