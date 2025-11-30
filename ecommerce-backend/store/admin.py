from django.contrib import admin
from . import models

admin.site.register([
    models.User, models.Role, models.Category, models.Vendor,
    models.Product, models.ProductVariant, models.Inventory,
    models.Cart, models.Order, models.Payment, models.Coupon
])
