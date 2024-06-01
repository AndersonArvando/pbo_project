from django.db import models

# Create your models here.


class Produk(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=500, choices=(
        ("Makanan", "Makanan"), ("Minuman", "Minuman"), ("Utilitas", "Utilitas"),), default="Makanan")
    price = models.PositiveIntegerField(default=0)
    shelf_life = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.ename
    
class Vendor(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    mobile_no = models.CharField(max_length=500)
    location = models.CharField(max_length=500)

    class Meta:
        db_table = "vendor"

class Transaction(models.Model):
    date = models.CharField(max_length=500)
    demand = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    rusak = models.PositiveIntegerField(default=0)
    cuaca = models.CharField(max_length=500, choices=(("Makanan", "Makanan"), ("Minuman", "Minuman"), ("Utilitas", "Utilitas"),), default="Makanan")
    holiday = models.BooleanField()
    diskon = models.PositiveIntegerField(default=0)
    men = models.PositiveIntegerField(default=0)
    women = models.PositiveIntegerField(default=0)
    restok = models.BooleanField()
    jumlah_restok = models.PositiveIntegerField(default=0)

    product = models.OneToOneField(
        Produk,
        on_delete=models.CASCADE,
        # name="karyawan_id"
    )
    vendor = models.OneToOneField(
        Vendor,
        on_delete=models.CASCADE,
        # name="karyawan_id"
    )

    class Meta:
        db_table = "transaction"
