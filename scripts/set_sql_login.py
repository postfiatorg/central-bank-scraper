import argparse
import sys
import getpass
from sqlalchemy import text

from agti.utilities.settings import PasswordMapLoader
from agti.utilities.settings import CredentialManager
from agti.utilities.db_manager import DBConnectionManager


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "create_new":
        # remove file if exists
        new_pass = getpass.getpass('Enter your new encryption password: ')
        credential_manager = CredentialManager()
        file = credential_manager.get_credential_file_path()
        file.unlink(missing_ok=True)

        credential_manager = CredentialManager()

        credential_ref = sys.argv[2] + "__postgresconnstring"
        pw_data = sys.argv[3]

        print(f"Encrypting credential: {credential_ref}")

        credential_manager.enter_and_encrypt_credential__variable_based(
            credential_ref=credential_ref,
            pw_data=pw_data,
            pw_encryptor=new_pass)

    else:
        password_loader = PasswordMapLoader()
        print(password_loader.pw_map)
        # Error handling
        if len(password_loader.pw_map) == 0:
            print("No credentials found. Exiting.")
            sys.exit(1)
        db_connection_manager = DBConnectionManager(
            pw_map=password_loader.pw_map)
        engine = db_connection_manager.spawn_sqlalchemy_db_connection_for_user(
            user_name='postgres')
        try:
            with engine.connect() as con:
                rs = con.execute(text('SELECT VERSION();'))
            print(rs.fetchone())
        except Exception as e:
            print(f"Issue connecting to database: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
