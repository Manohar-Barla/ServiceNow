import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicenow_csa.settings')
django.setup()

from syllabus.models import Domain, Topic

domains_data = [
    {"name": "Platform", "weightage": 20, "description": "Manage the Platform, UI, and Branding."},
    {"name": "Instance", "weightage": 15, "description": "Configure Instance, Users, and Roles."},
    {"name": "Collaboration", "weightage": 15, "description": "Task Management, Notification, and Reporting."},
    {"name": "Automation", "weightage": 20, "description": "Workflows, Flow Designer, and Service Catalog."},
    {"name": "DB & Security", "weightage": 20, "description": "Data Management, Security, and ACLs."},
    {"name": "Integration", "weightage": 10, "description": "Import Sets, Update Sets, and App Integration."},
]

for d in domains_data:
    domain, created = Domain.objects.get_or_create(
        name=d['name'],
        defaults={'weightage': d['weightage'], 'description': d['description']}
    )
    if created:
        print(f"Created Domain: {domain.name}")
        # Add a placeholder topic for each domain
        Topic.objects.create(
            domain=domain,
            title=f"Introduction to {domain.name}",
            content=f"This topic covers the fundamental concepts of {domain.name} in ServiceNow."
        )
    else:
        print(f"Domain already exists: {domain.name}")

print("Seeding completed.")
