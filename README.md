# EMWI Auto Moto

This is a website for the EMWI Auto Moto company. 

## Prod Setup
1. Create a file in `/etc/emwiautomoto.env` to store the application environment variables.

File content:
```bash
API_CREDENTIALS_GENERATOR_SECRET_KEY=secretKeyOne
API_CREDENTIALS_REFRESH_TOKEN_SECRET_KEY=secretKeyTwo

DATABASE_HOST=host
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE=database

BUCKET_STORAGE_BUCKET_NAME=bucketname
BUCKET_STORAGE_OBJECT_BASE_URL=objUrl
BUCKET_STORAGE_ENDPOINT_URL=endpointUrl
BUCKET_STORAGE_ACCESS_KEY=accessKey
BUCKET_STORAGE_SECRET_ACCESS_KEY=secretAccessKey
```

2. Create the following directories and empty files:
```bash
/root/prod_logs/output/output.log
/root/prod_logs/error/error.log
````

3. Download SSL Certs and place them in:
```bash
/root/cf_certs/origin_cert.pem
/root/cf_certs/private_key.key
```

4. Create a file: `/etc/systemd/system/emwiautomoto.service`
```bash
[Unit]
Description=EmwiAutoMoto
After=network.target

[Service]
EnvironmentFile=/etc/emwiautomoto.env
ExecStart=backend/.venv/bin/python3 -m uvicorn backend.app:app --host 0.0.0.0 --port 443 --ssl-keyfile=/root/cf_certs/private_key.key --ssl-certfile=/root/cf_certs/origin_cert.pem
WorkingDirectory=/root/MotorcycleStore
User=root
Restart=always
StandardOutput=file:/root/prod_logs/output/output.log
StandardError=file:/root/prod_logs/error/error.log

[Install]
WantedBy=multi-user.target
```

If you add this file, OR make any changes to this file, you must run the following command:
```bash
systemctl daemon-reload
systemctl restart emwiautomoto
```

## Prod Deployments

### Frontend
All frontend deployments are automatically handled by GitHub Action, and deploy directly to Cloudflare.

### Backend

1. SSH into the server
2. `cd MotorcycleStore`
3. `git pull`
4. `sudo systemctl restart emwiautomoto.service`
