from instagram.client import InstagramAPI
from instagram.oauth2 import OAuth2AuthExchangeError
from django.conf import settings
from django.core.cache import cache
import datetime
from requests.exceptions import RequestException
import logging
from django.utils import timezone
from django.core.management.base import BaseCommand
from core.models import InstagramAccount

logger = logging.getLogger(__name__)


class InstagramServiceError(Exception):
    """Custom exception for Instagram service errors"""
    pass

class InstagramTokenManager:
    @staticmethod
    def is_token_expired(token_timestamp):
        """Check if token is expired or will expire in the next 7 days"""
        if not token_timestamp:
            return True
        expiration_date = token_timestamp + timezone.timedelta(days=60)
        buffer_date = expiration_date - timezone.timedelta(days=7)
        return timezone.now() > buffer_date


class InstagramService:
    def __init__(self, access_token=None, token_timestamp=None):
        self.access_token = access_token or settings.INSTAGRAM_CONFIG.get('access_token')
        self.token_timestamp = token_timestamp

        # Check if token needs renewal
        if self.access_token and InstagramTokenManager.is_token_expired(self.token_timestamp):
            try:
                self.access_token = self.refresh_access_token(self.access_token)
                self.token_timestamp = timezone.now()
            except InstagramServiceError as e:
                logger.error(f"Token refresh failed: {e}")

        try:
            self.api = InstagramAPI(
                client_id=settings.INSTAGRAM_CONFIG['client_id'],
                client_secret=settings.INSTAGRAM_CONFIG['client_secret'],
                access_token=self.access_token
            )
        except KeyError as e:
            logger.error(f"Missing Instagram configuration: {e}")
            raise InstagramServiceError("Instagram service is not properly configured")

    def refresh_access_token(self, token):
        """Refresh an expiring access token"""
        try:
            api = InstagramAPI(
                client_id=settings.INSTAGRAM_CONFIG['client_id'],
                client_secret=settings.INSTAGRAM_CONFIG['client_secret']
            )
            new_token = api.refresh_access_token(token)
            if not new_token:
                raise InstagramServiceError("Empty token received during refresh")
            return new_token
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            raise InstagramServiceError("Failed to refresh access token")

    def get_recent_posts(self, user_id='self', count=12):
        cache_key = f'instagram_posts_{user_id}_{count}'

        try:
            # Try to get from cache first
            posts = cache.get(cache_key)
            if posts is not None:
                return posts

            if not self.access_token:
                logger.warning("No Instagram access token available")
                return []

            # Fetch from API
            recent_media, next_ = self.api.user_recent_media(
                user_id=user_id,
                count=count
            )

            posts = []
            for media in recent_media:
                try:
                    post = {
                        'id': media.id,
                        'caption': media.caption.text if media.caption else '',
                        'link': media.link,
                        'type': media.type,
                        'created_time': datetime.datetime.fromtimestamp(
                            int(media.created_time)
                        ),
                        'images': {
                            'thumbnail': media.images['thumbnail'].url,
                            'low_resolution': media.images['low_resolution'].url,
                            'standard_resolution': media.images['standard_resolution'].url
                        },
                        'videos': {}
                    }

                    if media.type == 'video':
                        post['videos'] = {
                            'low_resolution': media.videos['low_resolution'].url,
                            'standard_resolution': media.videos['standard_resolution'].url
                        }

                    posts.append(post)

                except AttributeError as e:
                    logger.error(f"Error processing Instagram media: {e}")
                    continue

            # Cache results
            cache.set(cache_key, posts, timeout=3600)
            return posts

        except OAuth2AuthExchangeError as e:
            logger.error(f"Instagram OAuth error: {e}")
            raise InstagramServiceError("Authentication with Instagram failed")
        except RequestException as e:
            logger.error(f"Instagram API request failed: {e}")
            return cache.get(cache_key, [])  # Return cached if available
        except Exception as e:
            logger.error(f"Unexpected Instagram error: {e}")
            return []

    def get_oauth_authorize_url(self):
        try:
            return self.api.get_authorize_url(
                scope=['user_profile', 'user_media'],
                redirect_uri=settings.INSTAGRAM_CONFIG['redirect_uri']
            )
        except Exception as e:
            logger.error(f"Error generating OAuth URL: {e}")
            raise InstagramServiceError("Could not generate authorization URL")

    def get_access_token(self, code):
        try:
            access_token, user = self.api.exchange_code_for_access_token(code)
            if not access_token:
                raise InstagramServiceError("No access token received")
            return access_token
        except OAuth2AuthExchangeError as e:
            logger.error(f"Token exchange failed: {e}")
            raise InstagramServiceError("Failed to exchange code for token")
        except Exception as e:
            logger.error(f"Unexpected error during token exchange: {e}")
            raise InstagramServiceError("Token exchange failed")

    @staticmethod
    def get_long_lived_token(short_lived_token):
        try:
            api = InstagramAPI(
                client_id=settings.INSTAGRAM_CONFIG['client_id'],
                client_secret=settings.INSTAGRAM_CONFIG['client_secret'],
                access_token=short_lived_token
            )
            return api.exchange_token()
        except Exception as e:
            logger.error(f"Error getting long-lived token: {e}")
            raise InstagramServiceError("Could not exchange for long-lived token")


class RefreshInstagramTokensCommand:
    def handle(self, *args, **options):
        accounts = InstagramAccount.objects.filter(is_active=True)
        refreshed = 0
        failed = 0

        for account in accounts:
            if account.needs_token_refresh():
                if account.refresh_token():
                    print(f'Successfully refreshed token for account {account.id}')
                    refreshed += 1
                else:
                    print(f'Failed to refresh token for account {account.id}')
                    failed += 1

        print(f'Token refresh completed. {refreshed} succeeded, {failed} failed.')
