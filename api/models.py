from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class LoginSystem(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=200)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = 'Login System'
        verbose_name_plural = 'Login systems'

# class OrderAddFiltering(models.Model):
#     which_service = models.ForeignKe

class Services(models.Model):
    class whoHasThisChoice(models.TextChoices):
        Standard = "ST", "Standard"
        Lyuks = "LY", "Lyuks"

    title = models.CharField(max_length=50, unique=True)
    open = models.CharField(max_length=10)
    close = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    who_has_this = models.CharField(max_length=2, choices=whoHasThisChoice.choices,
                                    default=whoHasThisChoice.Standard)  # kimlar ushbu xizmatdan foydalana olishadi
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tel_number = models.CharField(max_length=20)
    info = models.TextField(max_length=200)
    image = models.ImageField(upload_to='image/')
    more_images = models.ManyToManyField('MultipleServiceImages', blank=True)
    qr_code = models.ImageField(upload_to='qr_code/', blank=True)

    users_for = models.ManyToManyField(LoginSystem, blank=True, null=True)
    duration = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.pk)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        filename = f'qr_code_{self.pk}.png'
        self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MultipleServiceImages(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.service.title


class Profile(models.Model):
    class GenderChoice(models.TextChoices):
        Erkak = "ER", "Erkak"
        Ayol = "AY", "Ayol"

    class UserStatusChoice(models.TextChoices):
        Standard = "ST", "Standard"
        Lyuks = "LY", "Lyuks"

    who = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=GenderChoice.choices)
    status = models.CharField(max_length=2, choices=UserStatusChoice.choices, default=UserStatusChoice.Standard)
    arrival_date = models.DateField()
    time_to_leave = models.DateField()
    tel_number = models.CharField(max_length=20)

    def __str__(self):
        return self.who.username


class UsedServices(models.Model):
    who_used = models.ForeignKey(Profile, on_delete=models.CASCADE)
    which_services = models.ForeignKey(Services, on_delete=models.CASCADE)
    when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.who_used)

    def clean(self):
        # Foydalanuvchining status ini aniqlash
        user_status = self.who_used.status
        # Shu xizmat uchun allaqachon qo'shilgan xizmatlar sonini hisoblash
        existing_services_count = UsedServices.objects.filter(
            who_used=self.who_used,
            which_services=self.which_services
        ).count()

        # Statusga qarab cheklovni belgilash
        if user_status == Profile.UserStatusChoice.Standard and existing_services_count >= 2:
            raise ValidationError('Standard foydalanuvchilar har bir xizmat uchun faqat 2 marta qo\'shishlari mumkin.')
        elif user_status == Profile.UserStatusChoice.Lyuks and existing_services_count >= 4:
            raise ValidationError('Lyuks foydalanuvchilar har bir xizmat uchun faqat 4 marta qo\'shishlari mumkin.')

    def save(self, *args, **kwargs):
        # Obyekt uchun clean metodini chaqirish (bu cheklovlarni qo'llaydi)
        self.clean()
        # Agar clean metodida hech qanday muammo bo'lmasa, obyektni saqlash
        super().save(*args, **kwargs)


class Ordering(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    user = models.ForeignKey(LoginSystem, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unique_together = ('service', 'user')
        ordering = ['id']

    def __str__(self):
        return f"{self.service} | {self.user} | {self.order_date}"

    # def used_services_count(self):
    #     return self.usedservices_set.count()