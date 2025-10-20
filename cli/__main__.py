from utils.logger import setup_logging
from utils.environment import config
from bridges.http import Http, HttpConfig
from services.HiRISE import HiRISEService, HiRISEConfig

def main():
    setup_logging()
    hirise_config = config().get("hirise")

    hirise_service = HiRISEService(
        config=HiRISEConfig(
            samples=hirise_config["samples"],
            http=Http(
                config=HttpConfig(
                    host=hirise_config["host"],
                )
            ),
        )
    )

    hirise_service.download_samples()

if __name__ == "__main__":
    main()
