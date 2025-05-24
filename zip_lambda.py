import os
import zipfile

zipf = zipfile.ZipFile('lambda.zip', 'w', zipfile.ZIP_DEFLATED)

for root, _, files in os.walk('package'):
    for file in files:
        filepath = os.path.join(root, file)
        arcname = os.path.relpath(filepath, 'package')
        zipf.write(filepath, arcname)

zipf.close()