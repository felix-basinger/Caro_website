# Generated by Django 5.0.6 on 2024-08-20 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_favorite_options_favorite_added_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='image',
            field=models.ImageField(default='images/noimage_detail.png', upload_to='products/'),
        ),
    ]
