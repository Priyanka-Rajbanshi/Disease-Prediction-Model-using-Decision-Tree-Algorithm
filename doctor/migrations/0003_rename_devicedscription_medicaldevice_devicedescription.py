# Generated by Django 4.2.7 on 2024-03-01 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_remove_medicinedirprescriptionmap_medicinedirectionid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicaldevice',
            old_name='deviceDscription',
            new_name='deviceDescription',
        ),
    ]
