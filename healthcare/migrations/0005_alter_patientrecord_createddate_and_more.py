# Generated by Django 4.2.7 on 2024-02-29 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0004_remove_patientrecord_estimateddelivery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientrecord',
            name='createdDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='patientrecord',
            name='updatedDate',
            field=models.DateField(auto_now=True),
        ),
    ]
