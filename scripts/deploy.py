"""Publish dist through verified explicit FTPS; preserve unrelated server files."""
import ftplib, os, ssl, posixpath, sys
from pathlib import Path
from urllib.parse import urlsplit
required=['DEPLOY_HOST','DEPLOY_USER','DEPLOY_PASSWORD']
missing=[x for x in required if not os.environ.get(x)]
if missing:
    sys.exit('Fehlende GitHub-Secrets: '+', '.join(missing)+'. Unterstützt: HETZNER_HOST/HETZNER_USER/HETZNER_PASSWORD oder FTP_SERVER/FTP_USERNAME/FTP_PASSWORD.')
host=os.environ['DEPLOY_HOST'].strip()
if '://' in host: host=urlsplit(host).hostname
port=int(os.environ.get('DEPLOY_PORT') or '21')
target=os.environ.get('DEPLOY_PATH','.')
if any(x in target for x in ['\n','\r','"']): sys.exit('Ungültiger Zielordner.')
if port == 22:
    import paramiko
    class SFTPConnection:
        def __init__(self):
            self.client=paramiko.SSHClient()
            self.client.load_system_host_keys()
            # First connection to the user's configured SSH endpoint.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(host,port=port,username=os.environ['DEPLOY_USER'],password=os.environ['DEPLOY_PASSWORD'],look_for_keys=False,allow_agent=False,timeout=45)
            self.sftp=self.client.open_sftp()
        def cwd(self,path):
            try: self.sftp.chdir(path)
            except OSError as e: raise ftplib.error_perm(str(e)) from e
        def pwd(self): return self.sftp.getcwd() or self.sftp.normalize('.')
        def nlst(self): return self.sftp.listdir('.')
        def mkd(self,path): return self.sftp.mkdir(path)
        def retrbinary(self,command,callback):
            with self.sftp.open(command.removeprefix('RETR '),'rb') as f: callback(f.read())
        def storbinary(self,command,stream): self.sftp.putfo(stream,command.removeprefix('STOR '))
        def quit(self): self.sftp.close();self.client.close()
    ftp=SFTPConnection()
else:
    ftp=ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=45)
    ftp.connect(host,port)
    ftp.login(os.environ['DEPLOY_USER'],os.environ['DEPLOY_PASSWORD'])
    ftp.prot_p()
ftp.cwd(target)
entries=ftp.nlst()
names={x.rstrip('/').rsplit('/',1)[-1] for x in entries}-{'.','..'}
print('Verbindung zu Hetzner erfolgreich. Zielordner enthält:', ', '.join(sorted(names)))
# A server/account root must never receive a site by accident.
if target in ('.','/','') and names.intersection({'public_html','httpdocs','www','htdocs'}):
    sys.exit('DEPLOY_PATH muss auf den Website-Ordner zeigen; der aktuelle FTP-Ordner enthält Hosting-Verzeichnisse.')
index_name=next((x for x in ('index.html','index.htm','index.php') if x in names),None)
if index_name and '.autopflege-deploy' not in names:
    previous=[]
    ftp.retrbinary('RETR '+index_name,previous.append)
    text=b''.join(previous).decode('utf-8',errors='replace').lower()
    is_ours=any(x in text for x in ('berliner autopflege','berliner-autopflege','berlinerautopflege','november-aktion'))
    is_placeholder=any(x in text for x in ('hetzner','domain wurde','domain has been','under construction'))
    if not (is_ours or is_placeholder): sys.exit('Zielordner gehört nicht eindeutig zur Berliner Autopflege. DEPLOY_PATH prüfen.')
base=ftp.pwd()
files=list(Path('dist').rglob('*'))
files=sorted((p for p in files if p.is_file()),key=lambda p:(p.name=='index.html',str(p)))
for path in files:
    rel=path.relative_to('dist').as_posix()
    ftp.cwd(base)
    for part in Path(rel).parts[:-1]:
        try: ftp.cwd(part)
        except ftplib.error_perm:
            ftp.mkd(part);ftp.cwd(part)
    with path.open('rb') as f: ftp.storbinary('STOR '+path.name,f)
    print('Hochgeladen:',rel)
ftp.cwd(base)
from io import BytesIO
ftp.storbinary('STOR .autopflege-deploy',BytesIO(b'eure_berliner_autopflege\n'))
ftp.quit()
print('Website erfolgreich veröffentlicht. Keine fremden Dateien gelöscht.')
