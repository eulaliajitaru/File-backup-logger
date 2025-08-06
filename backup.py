import os
import shutil
import zipfile
from datetime import datetime

class BackupManager:
    def __init__(self, source_folder, destination_folder, version="v1.0", zip_backup=False):
        self.source = source_folder
        self.destination = destination_folder
        self.version = version
        self.zip_backup = zip_backup
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = "backup.log"

    def get_backup_name(self):
        folder_name = os.path.basename(self.source.rstrip("/\\"))
        backup_name = f"{folder_name}_backup_{self.timestamp}_{self.version}"
        return os.path.join(self.destination, backup_name)

    def log(self, message):
        with open(self.log_file, "a") as log:
            log.write(f"[{self.timestamp}] {message}\n")

    def perform_backup(self):
        try:
            backup_path = self.get_backup_name()
            if self.zip_backup:
                backup_path += ".zip"
                self._create_zip_backup(backup_path)
                self.log(f"ZIP backup created at: {backup_path}")
            else:
                shutil.copytree(self.source, backup_path)
                self.log(f"Backup created at: {backup_path}")

        except Exception as e:
            self.log(f"Error: {str(e)}")

    def _create_zip_backup(self, zip_path):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for foldername, subfolders, filenames in os.walk(self.source):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, self.source)
                    zipf.write(filepath, arcname)
