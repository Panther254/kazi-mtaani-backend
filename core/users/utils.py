from django.core.mail import EmailMessage, send_mail

class Util:
	@staticmethod
	def send_email(data):
		email = EmailMessage(subject=data['email_subject'],body=data['email_body'], to=[data['to_email'],])
		email.send()

	def email_user(data):
		subject = data['email_subject']
		body = data['email_body']
		to = data['to_email']
		send_mail("Password Reset for {subject}".format(subject=subject),body,"noreply@somehost.local",[to,])