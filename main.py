from core.app_config import AppConfig



def main():
    
    cfg = AppConfig()
    logger = cfg.logger
    logger.error("[ERROR] message dawg!")
    
    
    
if __name__ == "__main__":
    main()