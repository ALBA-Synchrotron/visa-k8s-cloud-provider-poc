import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from cloud_provider.models.proposal_account import ProposalAccount
from cloud_provider.utils.ldap.ldap_client import LDAPClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetches all users under AlbaUsers directory and stores them in the database."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--members", dest="members", default=None,
                            help="The username list - comma separated - to be fetched from the LDAP server")

    def handle(self, *args, **options) -> None:
        logger.debug("###############################################################")
        logger.debug("###### DJANGO CUSTOM COMMAND create object from template ######")
        logger.debug("###############################################################")
        logger.info("fetch_proposal_accounts.py start")

        members_str: str = options["members"]
        members: list = [member.strip() for member in members_str.split(",")] if members_str else None

        client: LDAPClient = LDAPClient(
            ldap_url=settings.LDAP_URL,
            bind_dn=None,
            bind_password=None,
            base_dn=settings.LDAP_BASE_DN
        )

        try:
            client.connect()
            _ = client.fetch_proposal_accounts(members=members, exclude_industrial=True, update_or_create=True)
        except Exception as e:
            logger.error(f"Error fetching proposal accounts: {e}")
            raise e
        finally:
            client.disconnect()

        logger.info("fetch_proposal_accounts.py end")
        logger.debug("########################################################################")
