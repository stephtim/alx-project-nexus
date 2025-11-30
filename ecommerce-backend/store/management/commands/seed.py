from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductVariant

class Command(BaseCommand):
    help = "Seed minimal data"

    def handle(self, *args, **options):
        cat, _ = Category.objects.get_or_create(name="Default", slug="default")
        p, created = Product.objects.get_or_create(
            slug="demo-product",
            defaults={"name":"Demo Product", "price":9.99, "currency":"USD", "category":cat}
        )
        if created:
            ProductVariant.objects.create(product=p, sku="DEMO-1", attributes={"size":"M"}, price=9.99)
        self.stdout.write(self.style.SUCCESS("Seed completed"))
