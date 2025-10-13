from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import stripe
from tools.client_email import send_payment_confirmation_to_client,notify_admin_of_payment
from orders.models import Order
from payment.models import Payment  # ton modèle
from custom_user.models import CustomUser  # adapte selon ton app

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSession(APIView):
    """
    Crée une session de paiement Stripe pour une commande existante.
    """

    def post(self, request):
        order_id = request.data.get("order_id")

        if not order_id:
            return Response({"error": "Missing order_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Order #{order.id}",
                            },
                            "unit_amount": int(order.total_amount * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                customer_email=order.email,
                metadata={"order_id": str(order.id)},
                success_url=f"{settings.FRONTEND_URL}/payment_success",
                cancel_url=f"{settings.FRONTEND_URL}/payment_failed",
            )

            return Response({"url": session.url})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook handler : enregistre le paiement et met à jour la commande.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_checkout_session(session)

    return HttpResponse(status=200)


def handle_checkout_session(session):
    """
    Sauvegarde le paiement Stripe et met à jour la commande.
    """
    order_id = session.get("metadata", {}).get("order_id")
    if not order_id:
        print("⚠️ Aucun order_id dans metadata Stripe")
        return

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        print(f"⚠️ Order {order_id} introuvable")
        return

    # Récupérer l'ID de paiement Stripe
    stripe_payment_id = session.get("payment_intent")
    if not stripe_payment_id:
        print("⚠️ Pas de payment_intent dans la session")
        return

    # Vérifier si déjà payé
    if Payment.objects.filter(stripe_payment_id=stripe_payment_id).exists():
        print(f"⛔ Paiement {stripe_payment_id} déjà enregistré")
        return

    # Récupérer l'objet PaymentIntent pour plus de détails
    payment_intent = stripe.PaymentIntent.retrieve(stripe_payment_id)

    # Créer l’enregistrement Payment
    Payment.objects.create(
        user=order.user if hasattr(order, "user") else None,
        email=order.email,
        stripe_payment_id=stripe_payment_id,
        amount=payment_intent["amount_received"] / 100,
        currency=payment_intent["currency"].upper(),
    )

    # Marquer la commande comme payée
    order.status = "paid"
    order.save()

    print(f"💰 Paiement enregistré & Order {order_id} marqué comme payé")

     # ✅ Send confirmation & admin notification
    send_payment_confirmation_to_client(order)
    notify_admin_of_payment(order)
