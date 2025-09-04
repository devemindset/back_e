from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
from payment.models import StripeProduct

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        name = request.data.get("name")
        payment_place = request.data.get("payment_place")

        if not name:
            return Response({"error": "Missing name"}, status=400)

        try:
            product = StripeProduct.objects.get(name=name)


            # Créer la session Checkout
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price": product.stripe_price_id,
                    "quantity": 1,
                }],
                mode="subscription" if product.product_type == "subscription" else "payment",
                customer_email=user.email,
                payment_intent_data={
                    "statement_descriptor": "Down Time Note",
                    "metadata": {
                        "user_id": user.id,
                        "amount": str(product.amount/100),
                        "payment_place": payment_place,
                        "payment_type": product.product_type,
                    }
                },
                success_url=f"{settings.FRONTEND_URL}/payment_success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/payment_failed",
                custom_text={
                    "submit": {
                        "message": "Thank you for supporting Down Time Note"
                    }
                },
            )

            return Response({"url": session.url})
        except StripeProduct.DoesNotExist:
            return Response({"error": "No matching product for this amount"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)