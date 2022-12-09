import os
from fastapi import Depends
from jwtdown_fastapi.authentication import Authenticator
from queries.users import (
    UserOut,
    UserRepository,
    UserOutWithPassword,
)


class MyAuthenticator(Authenticator):
    async def get_account_data(
        self,
        username: str,
        accounts: UserRepository,
    ):
        # Use your repo to get the account based on the
        # username (which could be an email)
        return accounts.get_by_username(username)

    def get_account_getter(
        self,
        accounts: UserRepository = Depends(),
    ):
        # Return the accounts. That's it.
        return accounts

    def get_hashed_password(self, account: UserOutWithPassword):
        # Return the encrypted password value from your
        # account object
        print("AUTHENTICATOR account:::", account)
        return account.hashed_password

    def get_account_data_for_cookie(self, account: UserOut):
        # Return the username and the data for the cookie.
        # You must return TWO values from this method.
        return account.username, UserOut(**account.dict())


authenticator = MyAuthenticator(os.environ["SIGNING_KEY"])
