from django.contrib import admin
from .models import Users, USSDRequest, USSDJobRequest, Jobs, Wallet, Transactions

admin.site.register(Users)
admin.site.register(USSDRequest)
admin.site.register(USSDJobRequest)
admin.site.register(Jobs)
admin.site.register(Wallet)
admin.site.register(Transactions)
