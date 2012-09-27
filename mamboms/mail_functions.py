from django.core.mail import send_mail
from django.conf import settings
from ccg.utils import webhelpers
from ccg.utils.webhelpers import siteurl, url

import os.path


def default_return_email():
    return getattr(settings, "RETURN_EMAIL", "noreply@ccg.murdoch.edu.au")

def sendAccountModificationEmail(request, toemail, fromemail=None):
    if not fromemail:
        fromemail = default_return_email()

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

def sendPasswordResetEmail(request, token, toemail, fromemail=None):
    if not fromemail:
        fromemail = default_return_email()

    subject = "MAMBO MS Password Reset"
    body = "You, or somebody pretending to be you, have requested that your\r\n"
    body += "MAMBO MS password be reset.\r\n\r\n"
    body += "To reset the password, please follow this link:\r\n"
    body += "%s?token=%s\r\n\r\n" % (os.path.join(siteurl(request), "user", "resetPassword"), token)
    body += "If you have received this e-mail in error, or no longer need to reset\r\n"
    body += "your password, please ignore this message."

    send_mail(subject, body, fromemail, [toemail], fail_silently=False)
