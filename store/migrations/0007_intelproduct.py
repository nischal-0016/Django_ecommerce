# Generated by Django 5.1 on 2024-10-27 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_profile_address_alter_profile_contact_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntelProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='product_images/intel/')),
                ('stock', models.IntegerField(default=0)),
            ],
        ),
    ]