from pydantic import BaseModel, SecretStr

from wg_federation.data.input.log_level import LogLevel


class UserInput(BaseModel):
    """
    Data class containing all user inputs
    """
    verbose: bool = None
    debug: bool = None
    quiet: bool = None
    log_level: LogLevel = None
    root_passphrase: SecretStr = None

    arg0: str = None
    arg1: str = None
    arg2: str = None
    arg3: str = None

    # root_password_readable:
    # 1. passed as --root-passphrase
    # 2. passed as WG_FEDERATION_ROOT_PASSPHRASE
    # 3. passed as configuration file, in /etc/wg-federation/main.yaml or $XDG_CONFIG_HOME/wg-federation/main.yaml
    # WARNING if 3.
    # The root passphrase was read from a configuration file. This is unsecure.
    # We recommend using the environment variable “WG_FEDERATION_ROOT_PASSPHRASE” or the argument “--root-passphrase XXX” in combination of a dynamic vault or password manager.
    # E.g. “wg-federation --root-passphrase $(vault get root password)” or “export WG_FEDERATION_ROOT_PASSPHRASE=$(vault get root password)”

    # credential_file_secret_ready
    # 1. /etc/wg-federation/secrets.enc.yaml or $XDG_CONFIG_HOME/wg-federation/secrets.enc.yaml can be decryoted and read
    # If not but file exist: throw an error:
    # 2. The federation private_key exist
    # 3. The federation tpm_secret exist

    # already_bootstraped:
    # 1. root_password_readable
    # 2. credential_file_secret_ready

    # hq bootstrap

    # If already_bootstraped:
    # WARNING + User validation: this operation might break an existing federation
    # If you want to proceed type in uppercase: "YES I WANT TO PROCEED"
    # Or run hq bootstrap with --force-renew
    # If not:
    # 1. Generate a tpm_secret
    # 2. Generate a federation public/private key
    # 3. pre. check if $XDG_CONFIG_HOME/wg-federation/secrets.enc.yaml is locked
    # 3. Read $XDG_CONFIG_HOME/wg-federation/secrets.enc.yaml if exist, decrypt and lock.
    # 4. Deep merge with new tpm_secret and federation private key
    # 5. Encrypt the content and write it to $XDG_CONFIG_HOME/wg-federation/secrets.enc.yaml and unlock

    # TODO HA/ DEAMON:
    # Watch for any change in $XDG_CONFIG_HOME/wg-federation/ and update according to that.
    # If any change in secrets.enc.yaml: restart all the WG interface, phone line and forums

    # TODO Check that two instance of wg-federation cannot run at the same time

    # TODO
