from django.db import models
from .utils import create_new_ref_number




class TelegramUser(models.Model):
    user_id            = models.CharField(max_length=50, blank=True, unique=True)
    wallet_balance     = models.PositiveIntegerField(default=0, blank=False)
    promo_code         = models.CharField(max_length=6, editable=False, unique=True, default=create_new_ref_number)
    s_promo_code       = models.CharField(max_length=6, blank=True )
    is_active          = models.BooleanField(default=True)
    
    
    def __str__(self):
        return (f"{self.user_id}\
            - {self.promo_code}\
            - wallet : {int(self.wallet_balance):,}\
            - id : {self.id}"
        )
    