from pydantic_settings import BaseSettings, SettingsConfigDict
#BaseSettings is designed specifically to configure the application
#helps read the values from the environment variables

class Settings(BaseSettings):
#Class represents what configuration our backend needs
# we define what settings we EXPECT here and keep their actual values
# inside .env.
#
# This is useful because development, testing and production can use
# different configuration without changing our Python source code.


    DATABASE_URL: str
#contains postgresql connection url
#Default is for local development; override it in .env for your environment.

    SECRET_KEY: str
# JWT secret key
# Later, when we implement authentication, users will log in and
# our backend will generate JWT access tokens.
# SECRET_KEY is used to SIGN those tokens.
# It allows our backend to verify that a token was actually created
# by our application and has not been modified.
# The real secret belongs in .env, not in source code.

    ALGORITHM: str = "HS256"
#JWT signing algorithm
#States which JWT Library algorithm we want to use when signing /verifying tokens

    ACCESS_TOKEN_EXPIRE_HOURS : int = 12
#Access Token lifetime
#According to our project tokens remain valid for only 12 hours not more than that


    INITIAL_ADMIN_NAME: str
    INITIAL_ADMIN_LOGIN_ID:str
    INITIAL_ADMIN_PASSWORD:str
    INITIAL_ADMIN_PHONE: str


    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding= "utf-8"
    )
# tells the system from where the configuration details come from
#and the utf-8 tells us how the text inside the .env file should come from
#

settings = Settings()
# Create one Settings object
# -------------------------------------------------------------------
#
# When this line runs, Pydantic creates our Settings object and loads
# the corresponding values from the environment/.env file.
#
# For example:
#
# .env:
#
#     DATABASE_URL=...
#     SECRET_KEY=...
#
# becomes available in Python as:
#
#     settings.DATABASE_URL
#     settings.SECRET_KEY
#
# Other modules can simply import this object:
#
#     from app.core.config import settings
#
# We therefore have one central place from which the application reads
# its configuration.