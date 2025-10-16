# payment/emails.py
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

# Utilitaire pour envoyer un email HTML
def send_html_email(subject, to_email, html_content, text_content=None):
    from_email = settings.DEFAULT_FROM_EMAIL 
    msg = EmailMultiAlternatives(subject, text_content or "", from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_payment_confirmation_to_client(order):
    """
    Send a beautiful confirmation email to the client after payment.
    """
    subject = f"Thank you for your order #{order.id} – Goldy Seas"
    client_name = order.full_name.split(" ")[0] if order.full_name else "Dear Customer"

    html_content = f"""
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f8f9fb; padding: 40px 0;">
      <div style="max-width: 600px; background: white; border-radius: 10px; overflow: hidden; margin: auto; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <div style="background: linear-gradient(90deg, #d4af37, #f5d76e); padding: 20px 30px; color: white; text-align: center;">
          <h1 style="margin: 0; font-size: 26px; letter-spacing: 1px;">Goldy Seas</h1>
        </div>

        <div style="padding: 30px;">
          <h2 style="color: #333;">Hi {client_name},</h2>
          <p style="color: #555; line-height: 1.6; font-size: 16px;">
            We’re thrilled to confirm that we’ve <strong>successfully received your payment</strong> for 
            <strong>Order #{order.id}</strong>.
          </p>
          <p style="color: #555; line-height: 1.6; font-size: 16px;">
            Our team is now preparing your items for shipment. You’ll receive an update once your order is on its way.
          </p>

          <div style="background-color: #faf3dd; border-left: 4px solid #d4af37; padding: 15px 20px; margin: 25px 0;">
            <p style="margin: 0; color: #6b5e3c; font-size: 15px;">
              Need help or have questions? Contact us anytime at 
              <a href="mailto:gold@goldyseas.com" style="color: #d4af37; text-decoration: none;">gold@goldyseas.com</a>.
            </p>
          </div>

          <p style="font-size: 16px; color: #555;">Thank you for choosing <strong>Goldy Seas</strong> – your trust means the world to us.</p>

          <p style="margin-top: 35px; color: #999; font-size: 14px; text-align: center;">
            © Goldy Seas {order.created_at.year}. All rights reserved.
          </p>
        </div>
      </div>
    </div>
    """

    text_content = f"""
    Dear {client_name},

    We’ve successfully received your payment for Order #{order.id}.
    Our team is preparing your items for shipment.

    For any inquiries, reach out to us at gold@goldyseas.com.

    — Goldy Seas Team
    """

    send_html_email(subject, order.email, html_content, text_content)


def notify_admin_of_payment(order):
    """
    Notify Goldy Seas admin when a new payment is received.
    """
    subject = f"💰 New Payment Received – Order #{order.id}"
    html_content = f"""
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f9fafb; padding: 40px;">
      <div style="max-width: 600px; background: #ffffff; border-radius: 10px; margin: auto; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
        <div style="background: #d4af37; padding: 15px 20px; color: white; border-top-left-radius: 10px; border-top-right-radius: 10px;">
          <h2 style="margin: 0;">Goldy Seas – Payment Notification</h2>
        </div>
        <div style="padding: 25px;">
          <p style="color: #333;">A new payment has been recorded:</p>

          <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
            <tr><td style="padding: 6px 0;"><strong>Order ID:</strong></td><td>#{order.id}</td></tr>
            <tr><td style="padding: 6px 0;"><strong>Client:</strong></td><td>{order.full_name}</td></tr>
            <tr><td style="padding: 6px 0;"><strong>Email:</strong></td><td>{order.email}</td></tr>
            <tr><td style="padding: 6px 0;"><strong>Amount:</strong></td><td>${order.total_amount}</td></tr>
            <tr><td style="padding: 6px 0;"><strong>Status:</strong></td><td>{order.status}</td></tr>
            <tr><td style="padding: 6px 0;"><strong>Date:</strong></td><td>{order.created_at.strftime('%B %d, %Y')}</td></tr>
          </table>

          <p style="margin-top: 25px; color: #555;">
            Please log into the admin dashboard for details and next steps.
          </p>

          <p style="margin-top: 30px; color: #999; font-size: 13px; text-align: center;">
            © Goldy Seas. Internal payment alert.
          </p>
        </div>
      </div>
    </div>
    """

    text_content = f"""
    New payment received:

    Order #{order.id}
    Client: {order.full_name}
    Email: {order.email}
    Amount: ${order.total_amount}
    Status: {order.status}

    — Goldy Seas Notification System
    """

    send_html_email(subject, "gold@goldyseas.com", html_content, text_content)

def forward_contact_message(user_email, user_message):
    """
    Transfère un message de contact vers ton adresse support avec version HTML.
    """
    subject = f"📩 Nouveau message de {user_email}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = ["gold@goldyseas.com",]

    # ✅ Version texte brut (fallback)
    text_content = f"""
    Nouveau message de contact :

  
    Email : {user_email}

    Message :
    {user_message}
    """

    # ✅ Version HTML stylisée
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>📩 Nouveau message de contact</h2>
        <p><strong>Email :</strong> {user_email}</p>
        <p><strong>Message :</strong></p>
        <p style="background:#f5f5f5;padding:10px;border-left:4px solid #00bfff;">{user_message}</p>
        <hr>
        <p>Ce message provient du formulaire de contact de downtimenote.</p>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to,
        reply_to=[user_email],  # ✅ Ici tu pourras répondre directement au visiteur
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
