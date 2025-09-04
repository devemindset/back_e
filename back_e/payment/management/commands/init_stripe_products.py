import stripe
from django.core.management.base import BaseCommand
from django.conf import settings
from payment.models import StripeProduct

stripe.api_key = settings.STRIPE_SECRET_KEY

class Command(BaseCommand):
    help = "Supprime les anciens produits et recrée la liste des nouveaux produits Stripe"

    def handle(self, *args, **kwargs):
        # ❌ Supprimer les anciens produits StripeProduct locaux
        old_products = StripeProduct.objects.all()
        for prod in old_products:
            try:
                # Facultatif : désactiver le produit dans Stripe
                stripe.Product.modify(prod.stripe_product_id, active=False)
                self.stdout.write(self.style.WARNING(f"⛔ Produit désactivé sur Stripe : {prod.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erreur lors de la désactivation de {prod.name} : {e}"))
            prod.delete()

        self.stdout.write(self.style.SUCCESS("✅ Tous les anciens produits ont été supprimés."))

        # ✅ Nouvelle liste de produits
        products = [
            {
                "name": "Starter Monthly",
                "description": "For indie hackers and freelancers. All basic features included.",
                "amount": 900,  # $9.00/month
                "currency": "usd",
                "product_type": "subscription",
                "interval": "month",
            },
            {
                "name": "Pro Monthly",
                "description": "For SaaS founders and small teams. Includes everything.",
                "amount": 1900,  # $19.00/month
                "currency": "usd",
                "product_type": "subscription",
                "interval": "month",
            },
            {
                "name": "Starter Annual",
                "description": "Same as Starter Monthly. Save 20% with annual billing.",
                "amount": 9000,  # $90/year
                "currency": "usd",
                "product_type": "subscription",
                "interval": "year",
            },
            {
                "name": "Pro Annual",
                "description": "Same as Pro Monthly. Save 20% and priority support included.",
                "amount": 19000,  # $190/year
                "currency": "usd",
                "product_type": "subscription",
                "interval": "year",
            },
        ]

        # ➕ Créer les nouveaux produits
        for data in products:
            product = stripe.Product.create(
                name=data["name"],
                description=data.get("description", "")
            )

            price_data = {
                "unit_amount": data["amount"],
                "currency": data.get("currency", "usd"),
                "product": product.id,
                "recurring": {"interval": data.get("interval", "month")},
            }

            price = stripe.Price.create(**price_data)

            StripeProduct.objects.create(
                name=data["name"],
                description=data.get("description", ""),
                stripe_product_id=product.id,
                stripe_price_id=price.id,
                amount=data["amount"],
                currency=data.get("currency", "usd"),
                product_type=data["product_type"],
                interval=data.get("interval"),
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Produit créé : {data['name']}"))
