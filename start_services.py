import subprocess
import os
import signal
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QGISServiceManager:
    def __init__(self):
        self.processes = {}
        self.base_dir = Path(__file__).parent
        self.xpra_display = ":100"
        self.xpra_port = 14500

    def start_auth_service(self):
        cmd = ["python", str(self.base_dir / "services/sso-auth/sso_service.py")]
        self.processes['auth'] = subprocess.Popen(cmd)
        logger.info("Started authentication service")

    def start_xpra(self):
        cmd = [
            "xpra", "start",
            "--start-child=qgis",
            "--html=on",
            "--bind-tcp=0.0.0.0:14500",
            "--start-via-proxy=yes",
            "--exit-with-children",
            self.xpra_display
        ]
        self.processes['xpra'] = subprocess.Popen(cmd)
        logger.info("Started Xpra service")

    def start_all(self):
        try:
            self.start_auth_service()
            self.start_xpra()
            logger.info("All services started successfully")
            
            # Wait for interrupt signal
            signal.signal(signal.SIGINT, self.cleanup)
            signal.signal(signal.SIGTERM, self.cleanup)
            signal.pause()
            
        except Exception as e:
            logger.error(f"Error starting services: {e}")
            self.cleanup()
            sys.exit(1)

    def cleanup(self, *args):
        logger.info("Cleaning up services...")
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"Terminated {name} service")
            except Exception as e:
                logger.error(f"Error terminating {name} service: {e}")
                process.kill()
        sys.exit(0)

if __name__ == "__main__":
    manager = QGISServiceManager()
    manager.start_all()