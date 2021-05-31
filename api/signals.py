from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import get_ip, differentIp
import logging


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_ip(request)
    if differentIp(ip, request.user):
        logging.warning('You logged from different location')
