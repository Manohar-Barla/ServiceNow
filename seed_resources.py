import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicenow_csa.settings')
django.setup()

from resources.models import Resource

# Create a dummy PDF content
dummy_pdf_content = b"%PDF-1.1\n% \n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 20 >>\nstream\nBT /F1 12 Tf ET\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"

r = Resource(title="ServiceNow CSA Study Guide", description="Official study guide for the CSA exam.")
r.file.save('csa_guide.pdf', ContentFile(dummy_pdf_content))
r.save()

print(f"Created Resource: {r.title}")
