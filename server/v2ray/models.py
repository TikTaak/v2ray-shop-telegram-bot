from django.db import models

class V2ray(models.Model):

    operator           = models.ManyToManyField("Operator", related_name="v2ray_operator", blank=False)
    expire_time        = models.PositiveIntegerField(blank=False)
    volume             = models.PositiveIntegerField(blank=False)
    price              = models.PositiveIntegerField(blank=False)
    reason_disability  = models.TextField(default='', blank=True, editable=False)
    referral_bonus     = models.PositiveIntegerField(default=0, blank=False)
    date               = models.DateTimeField(auto_now_add=True)
    update_time        = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        operator = ", ".join(str(seg1) for seg1 in self.operator.all())

        return (f"V2ray\
            - {int(self.price):,}T\
            - {str(self.volume)}GB\
            - {str(self.expire_time)}Day's\
            - {operator} id : {self.id}"
        )
    
    
class Operator(models.Model):
    title = models.CharField(max_length=100, blank=False)
    reason_disability = models.TextField(default='', blank=True, editable=False)
    def __str__(self):
        return (f"operator\
            - title : {self.title}\
            - id : {self.id}"
        )

