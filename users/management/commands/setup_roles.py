from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile

class Command(BaseCommand):
    help = 'Creates default roles and assigns them to WhiteDevil and DummyUser'

    def handle(self, *args, **kwargs):
        # Ensure all existing users have a profile
        for u in User.objects.all():
            UserProfile.objects.get_or_create(user=u)

        # 1. WhiteDevil (ADMIN)
        admin_user, created = User.objects.get_or_create(username='WhiteDevil')
        if created:
            admin_user.set_password('Admin@123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created WhiteDevil user'))
        
        admin_profile = admin_user.userprofile
        admin_profile.role = 'ADMIN'
        admin_profile.save()
        self.stdout.write(self.style.SUCCESS('Set WhiteDevil to ADMIN'))

        # 2. DummyUser (DUMMY)
        dummy_user, created = User.objects.get_or_create(username='DummyUser')
        if created:
            dummy_user.set_password('Dummy@9392')
            dummy_user.save()
            self.stdout.write(self.style.SUCCESS('Created DummyUser user'))
        else:
            # Set password anyway just in case
            dummy_user.set_password('Dummy@9392')
            dummy_user.save()
            
        dummy_profile = dummy_user.userprofile
        dummy_profile.role = 'DUMMY'
        dummy_profile.save()
        self.stdout.write(self.style.SUCCESS('Set DummyUser to DUMMY'))

        self.stdout.write(self.style.SUCCESS('Successfully configured role-based access system.'))
