import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os, glob

# get csv files
os.chdir('/Users/darrell32/Documents/WeeklyReports')
csv_files = glob.glob('*.csv')

sender = 'darrell.s.nabors.1@vanderbilt.edu'
# recipients = ['darrell.s.nabors.1@vanderbilt.edu', 'miguel.herrera@vanderbilt.edu'] 
recipients = ['darrell.s.nabors.1@vanderbilt.edu','cara.b.sutcliffe@Vanderbilt.Edu','miguel.herrera@vanderbilt.edu','iulia.coultis@vanderbilt.edu'] 

msg = MIMEMultipart()
 
msg['From'] = sender
msg['To'] = ','.join(recipients)
msg['Subject'] = 'Weekly DNA/Blood Reports'
 
body = "Here are the requested blood/DNA reports. \n\n If there are any questions, please let me know. \n Thanks!  \n\n Darrell"
 
msg.attach(MIMEText(body, 'plain'))
 
#  attach csv files
for filename in csv_files:
    f = filename
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)

 
server = smtplib.SMTP('smtpauth.vanderbilt.edu', 587)
server.starttls()
server.login('nabords1','@Krs0n3BDP')
text = msg.as_string()
server.sendmail(sender, recipients, text)
server.quit()

# move csv_files to archive folder
os.system('mv *.csv /Users/darrell32/Documents/WeeklyReports/ReportArchive/')

print('done!')