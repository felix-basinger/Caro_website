# Generated by Django 5.0.6 on 2024-07-15 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_billing_city_userprofile_billing_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stripe_card_token',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
