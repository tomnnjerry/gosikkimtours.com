from django.db import models


class Enquiry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    lands = models.CharField(max_length=200, blank=True)
    month = models.CharField(max_length=40, blank=True)
    nights = models.PositiveSmallIntegerField(null=True, blank=True)
    travellers = models.PositiveSmallIntegerField(null=True, blank=True)
    budget = models.CharField(max_length=60, blank=True)
    message = models.TextField(blank=True)
    contact_pref = models.CharField("Best way to reach you", max_length=20, blank=True,
                                    choices=[("whatsapp", "WhatsApp"), ("call", "Phone call"), ("email", "Email")])
    kind = models.CharField(max_length=20, default="full",
                            choices=[("full", "Full form"), ("quick", "Quick form"), ("callback", "Call back")])
    source_page = models.CharField(max_length=300, blank=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "enquiries"

    def __str__(self):
        return f"{self.name} · {self.lands or 'any land'} · {self.created:%d %b %Y}"


class Subscriber(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    source_page = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.email
