from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# THIS IS THE MISSING VARIABLE THAT IS NOW ADDED
TECH_CHOICES = [
    ('python', 'Python'), ('django', 'Django'), ('php', 'PHP'),
    ('wordpress', 'WordPress'), ('odoo', 'Odoo'), ('javascript', 'JavaScript'),
    ('vuejs', 'Vue.js'), ('react', 'React'), ('postgresql', 'PostgreSQL'),
    ('mysql', 'MySQL'), ('ui_ux', 'UI/UX Design'),
]

class PersonalizationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_("Profile Name"), max_length=100)
    technologies = models.CharField(_("Selected Technologies"), max_length=255, blank=True)
    custom_prompt = models.TextField(_("Your Custom Instructions"), blank=True, help_text=_("Add any other specific instructions or project context here."))
    system_prompt = models.TextField(_("Generated System Prompt"), blank=True, editable=False, help_text=_("This is auto-generated based on your selections."))
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class PromptTemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_("Template Name"), max_length=100)
    template_text = models.TextField(_("Template Content"), help_text=_("Use {{user_message}} as a placeholder."))
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name
