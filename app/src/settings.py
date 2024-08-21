from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    TITLE: str = "FastAPI App"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "FastAPI App"
    CONTACT_NAME: str = "John Doe"
    CONTACT_EMAIL: str = "johndoe@gmail.com"
    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"

    @property
    def allowed_origins(self):
        return self.CORS_ALLOW_ORIGINS.split(',')
    
    @property
    def allowed_credentials(self):
        return self.CORS_ALLOW_CREDENTIALS
    
    @property
    def allowed_methods(self):
        return self.CORS_ALLOW_METHODS.split(',')
    
    @property
    def allowed_headers(self):
        return self.CORS_ALLOW_HEADERS.split(',')
    

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    DB_DRIVER: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_NAME: str = ""
    DB_OVERRIDE_URL: str = ""

    @property
    def url(self) -> str:
        if self.DB_OVERRIDE_URL != "":
            return self.DB_OVERRIDE_URL
        
        if self.DB_DRIVER == "" or self.DB_USER == "" or self.DB_PASSWORD == "" or self.DB_HOST == "" or self.DB_PORT == "" or self.DB_NAME == "":
            raise ValueError("Database settings not set")
        
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
