from celery import shared_task
from .models import InstagramAccount
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def refresh_instagram_tokens():
    accounts = InstagramAccount.objects.filter(is_active=True)
    for account in accounts:
        if account.needs_token_refresh():
            try:
                if account.refresh_token():
                    logger.info(f"Successfully refreshed token for account {account.id}")
                else:
                    logger.error(f"Failed to refresh token for account {account.id}")
            except Exception as e:
                logger.error(f"Error refreshing token for account {account.id}: {e}")
