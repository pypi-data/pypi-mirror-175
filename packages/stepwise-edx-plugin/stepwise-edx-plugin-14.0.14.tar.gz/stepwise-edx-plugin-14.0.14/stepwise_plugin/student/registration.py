"""
Written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

Date:   Jan-2022

Usage:  Custom functionality that runs after successful account registration.
"""
import logging

from django.dispatch import receiver

log = logging.getLogger(__name__)

try:
    from openedx.core.djangoapps.user_authn.views.register import REGISTER_USER

    @receiver(REGISTER_USER, dispatch_uid="stepwise_REGISTER_USER")
    def register_user(sender, user, registration, **kwargs):  # pylint: disable=unused-argument
        log.info("stepwise_plugin received REGISTER_USER signal for {username}".format(username=user.username))

except ImportError:
    pass


# Coming in Maple
# ----------------
# from openedx_events.learning.signals import STUDENT_REGISTRATION_COMPLETED
# from openedx_events.learning.signals import COURSE_ENROLLMENT_CREATED
# from openedx_events.learning.signals import CERTIFICATE_CREATED  # lint-amnesty, pylint: disable=wrong-import-order
