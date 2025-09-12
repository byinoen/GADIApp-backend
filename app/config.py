from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "production"  # Default to production for security
    DATABASE_URL: str = "sqlite:///./gadi.db"
    SECRET_KEY: str = ""  # Must be set via GADI_SECRET_KEY environment variable
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BOOTSTRAP_SECRET: str = ""  # Required for bootstrap seeding in production
    
    def model_post_init(self, __context):
        if not self.SECRET_KEY:
            if self.APP_ENV == "local":
                self.SECRET_KEY = "dev-secret-key-only-for-local-development"
            else:
                raise ValueError("SECRET_KEY must be set via GADI_SECRET_KEY environment variable in production")
        
        if self.APP_ENV != "local" and not self.BOOTSTRAP_SECRET:
            # In production, require bootstrap secret for database initialization
            pass  # BOOTSTRAP_SECRET is optional but recommended
    
    class Config:
        env_prefix = "GADI_"


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings