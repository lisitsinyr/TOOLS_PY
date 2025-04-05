import os
import shutil
from datetime import datetime

# Путь к директории, которую необходимо скопировать
source_dir = '/path/to/source/directory'

# Путь к директории назначения (например, внешний диск или сетевая папка)
destination_dir = '/path/to/backup/directory'

# Создание метки времени для создания уникальной папки для каждой копии
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_dir = os.path.join(destination_dir, 'backup_' + timestamp)

try:
    # Копирование директории
    shutil.copytree(source_dir, backup_dir)
    print(f'Backup of {source_dir} was successfully created at {backup_dir}')
except Exception as e:
    print(f'Error creating backup: {e}')