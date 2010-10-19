from django.core.mail import send_mail
from appsettings.mamboms.prod import RETURN_EMAIL
from webhelpers import siteurl 

def sendAccountModificationEmail(request, toemail, fromemail = RETURN_EMAIL):
    subject = 'MAMBO MS Account Change'
    body = 'Your MAMBO MS account has been modified\r\n\r\n'
    body += 'Either you, or an administrator has modified your account details or status\r\n\r\n'
    body += 'Please click the following link to login to Madas:\r\n'
    body += '%s\r\n\r\n' % (siteurl(request))
    try:
        print '\tSending email from: %s, to: %s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail],fail_silently = False)
    except Exception, e:
        print 'Error sending mail to user: ',toemail , ':', str(e)

