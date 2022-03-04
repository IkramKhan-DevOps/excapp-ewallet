# Generated by Django 3.2.10 on 2022-03-04 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_wallet_qr_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSanction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_app_allowed', models.BooleanField(default=True)),
                ('is_top_up_allowed', models.BooleanField(default=False)),
                ('is_transaction_allowed', models.BooleanField(default=False)),
                ('is_withdrawal_allowed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Sanctions',
            },
        ),
    ]
