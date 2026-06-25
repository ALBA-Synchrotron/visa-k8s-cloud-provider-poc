import logging
from logging import Logger
from typing import Any

import ldap

from cloud_provider.models.proposal_account import ProposalAccount


class LDAPClient:
    def __init__(self, ldap_url: str, bind_dn: str | None = None, bind_password: str | None = None,
                 base_dn: str | None = None):
        self.ldap_url: str = ldap_url
        self.bind_dn: str | None = bind_dn
        self.bind_password: str | None = bind_password
        self.base_dn: str | None = base_dn
        self.connection: ldap.ldapobject.LDAPObject | None = None

        self.logger: Logger = logging.getLogger(__name__)

    def connect(self):
        try:
            self.connection = ldap.initialize(self.ldap_url)
            self.connection.set_option(ldap.OPT_REFERRALS, 0)
            self.connection.simple_bind_s(self.bind_dn, self.bind_password)
            self.logger.info("LDAP connection and bind successful.")
        except ldap.LDAPError as e:
            self.logger.error(f"LDAP connection failed: {e}")
            raise e

    def fetch_proposal_accounts(self, members: list[str | bytes] | None = None, exclude_industrial: bool | None = True,
                                update_or_create: bool = False):
        if members is None:
            members = []
        try:
            proposal_accounts: list[dict[str, str]] = []
            if not members:
                self.logger.info("Fetching all users under AlbaUsers directory.")
                search_filter: str = "(cn=AlbaUsers)"
                attributes: list[str] = ['memberUid']
                result: list[tuple[Any, Any, list]] | None = self.connection.search_s(self.base_dn, ldap.SCOPE_SUBTREE,
                                                                                      search_filter, attributes)
                _, entry = result[0] if result and len(result) else (None, None)
                if entry:
                    members = entry.get('memberUid', [])

            for username in members:
                if isinstance(username, bytes):
                    username = username.decode('utf-8')
                if exclude_industrial and username.startswith('uind-'):
                    self.logger.info(f"Excluding industrial user: {username}")
                    continue
                self.logger.info(f"Fetching member UID: {username}")
                search_filter = f"(uid={username})"
                user_result: list[tuple[Any, Any, list]] | None = self.connection.search_s(self.base_dn, ldap.SCOPE_SUBTREE, search_filter, ['uidNumber', 'gidNumber', 'homeDirectory'])
                _, user_entry = user_result[0] if len(user_result) else (None, None)
                if user_entry:
                    try:
                        uid_number: bytes | None = user_entry.get('uidNumber', None)[0]
                        gid_number: bytes | None = user_entry.get('gidNumber', None)[0]
                        home_directory: bytes | None = user_entry.get('homeDirectory', None)[0]
                        self.logger.info(
                            f"Found {username} - UID: {uid_number.decode('utf-8')}, GID: {gid_number.decode('utf-8')}")
                        proposal_account_dict: dict[str, str] = {
                            'username': username,
                            'uid': uid_number.decode('utf-8') if uid_number else None,
                            'gid': gid_number.decode('utf-8') if gid_number else None,
                        }
                        proposal_accounts.append(proposal_account_dict)
                        if update_or_create:
                            try:
                                self.logger.info(
                                    f'Creating/Updating proposal account: {proposal_account_dict["username"]}')
                                proposal_account, created = ProposalAccount.objects.update_or_create(defaults=proposal_account_dict,
                                                                                      username=proposal_account_dict[
                                                                                          'username'])
                                if created:
                                    self.logger.debug(
                                        f'{"Created" if created else "Updated"} proposal account: {proposal_account_dict["username"]}')

                                home_directory_str: str = home_directory.decode('utf-8') if home_directory else None
                                if home_directory_str:
                                    if proposal_account.home_directory_list.filter(path=home_directory_str).exists():
                                        self.logger.debug(f'Home directory already exists for {username}: {home_directory_str}')
                                        self.logger.debug(f'Skipping...')
                                    else:
                                        self.logger.debug(f'Creating home directory for {username}: {home_directory_str}')
                                        proposal_account.home_directory_list.create(path=home_directory_str)
                                        self.logger.debug(f'Home directory created for {username}: {home_directory_str}')
                            except Exception as e:
                                self.logger.error(f'Error creating/updating proposal account: {e}')
                    except IndexError:
                        self.logger.error(f'Error: uidNumber or gidNumber not found for {username}')
            self.logger.info(f"Fetched {len(proposal_accounts)} proposal accounts")
            return proposal_accounts
        except ldap.LDAPError as e:
            self.logger.error(f"LDAP search failed: {e}")
            raise e

    def disconnect(self):
        if self.connection:
            self.connection.unbind_s()
            self.logger.info("Disconnected from LDAP.")
