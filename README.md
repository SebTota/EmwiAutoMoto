# EMWI Auto Moto

This is a website for the EMWI Auto Moto company. 

## Prod Setup

### Postgres Setup
1. Install Postgres
2. Access the postgres shell
```bash
sudo -u postgres psql
```
3. Update the postgres password
```sql
ALTER USER postgres PASSWORD 'newPassword';
```

4. Create the EmwiAutoMoto user
```sql
CREATE USER emwiautomotoreadwrite WITH PASSWORD 'password';
```

5. Create the EmwiAutoMoto database and grant access to the EmwiAutoMoto user
```sql
CREATE DATABASE emwiautomoto OWNER postgres;
GRANT ALL PRIVILEGES ON DATABASE emwiautomoto TO emwiautomotoreadwrite;
```

6. Exit the postgres shell and user
```sql
\q
exit
```

7. Update the `pg_hba.conf` file to allow access from all ips
```bash
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

### Service Setup
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
```

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
sudo systemctl daemon-reload
sudo systemctl restart emwiautomoto
```

## Prod Deployments

### Frontend
All frontend deployments are automatically handled by GitHub Action, and deploy directly to Cloudflare.

### Backend

1. SSH into the server
2. `cd MotorcycleStore`
3. `git pull`
4. `source backend/.venv/bin/activate`
5. `pip install -r backend/requirements.txt`
6. `sudo systemctl restart emwiautomoto.service`

## Issues in Prod

### Access log files
Use the command:
```bash
sudo journalctl -u emwiautomoto -r
```
to get log files from the service in reverse, meaning the most recent logs will be first.

### Can't access host on port 443

Oracle by default blocks all ports on its hosts apart from 22. This means that even if you have the port open on the
network configuration page, you still need to open the port within the host itself. 

Sometimes, the config can get reset on reboot. Run the following commands to fix the issue:

```bash
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT -j ACCEPT

sudo su
iptables-save > /etc/iptables/rules.v4
exit
```

### Database Backups

All database backups are done on the `postgres` user. This user should have read access to the database being backed up.

After a successful backup, a success ping will be sent to https://www.cronitor.com to manage alerting of a failed
backup job.

#### Edit Database Backup Cron Job
To edit the crontab responsible for running these backups, run the following command: `sudo crontab -u postgres -e`

#### Restore from Backup
In the case that you must restore the database from a backup file, follow the steps below:

1. Download the database backup file locally on the host
2. Connect to the host on which the database resides on
3. Create a new Database called `EmwiAutoMoto`
4. Run the following command: `psql -U postgres -d EmwiAutoMoto -f ./YYYY-MM-DD_EmwiAutoMoto_YYYY-MM-DD_HH-MM-SS.sql`
