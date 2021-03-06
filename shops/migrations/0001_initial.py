#  Copyright (c) Code Written and Tested by Ahmed Emad in 21/02/2020, 20:11

# Generated by Django 3.0.3 on 2020-02-21 17:28

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import shops.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('sort', models.PositiveIntegerField(null=True)),
                ('changes_price', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='OptionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('sort', models.PositiveIntegerField(null=True)),
                ('price', models.FloatField(null=True)),
                ('option_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options',
                                                   to='shops.OptionGroupModel')),
            ],
            options={
                'ordering': ['sort'],
                'unique_together': {('option_group', 'sort')},
            },
        ),
        migrations.CreateModel(
            name='ProductGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('sort', models.PositiveIntegerField(null=True)),
            ],
            options={
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='ShopProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(upload_to=shops.models.shop_photo_upload)),
                ('phone_number', models.BigIntegerField()),
                ('description', models.TextField()),
                ('shop_type',
                 models.CharField(choices=[('F', 'Food'), ('G', 'Groceries'), ('P', 'Pharmacy')], max_length=1)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('is_active', models.BooleanField(default=False)),
                ('is_open', models.BooleanField(default=True)),
                ('currency',
                 models.CharField(choices=[('$', 'Dollar'), ('€', 'Euro'), ('egp', 'Egyptian Pound')], max_length=3)),
                ('minimum_charge', models.FloatField(default=0)),
                ('delivery_fee', models.FloatField()),
                ('vat', models.FloatField(default=0, max_length=2,
                                          validators=[django.core.validators.MaxValueValidator(100),
                                                      django.core.validators.MinValueValidator(0)])),
                ('opens_at', models.TimeField()),
                ('closes_at', models.TimeField()),
                ('time_to_prepare', models.IntegerField()),
                ('account',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_profile',
                                      to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShopTagsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=10)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags',
                                           to='shops.ShopProfileModel')),
            ],
        ),
        migrations.CreateModel(
            name='ShopAddressModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('building', models.CharField(max_length=255)),
                ('special_notes', models.TextField(blank=True)),
                ('location_longitude', models.FloatField(default=0,
                                                         validators=[django.core.validators.MaxValueValidator(180),
                                                                     django.core.validators.MinValueValidator(-180)])),
                ('location_latitude', models.FloatField(default=0,
                                                        validators=[django.core.validators.MaxValueValidator(90),
                                                                    django.core.validators.MinValueValidator(-90)])),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address',
                                              to='shops.ShopProfileModel')),
            ],
        ),
        migrations.CreateModel(
            name='RelyOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choosed_option_group',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.OptionGroupModel')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.OptionModel')),
                ('option_group',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rely_on',
                                      to='shops.OptionGroupModel')),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=shops.models.product_photo_upload)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('is_available', models.BooleanField(default=True)),
                ('is_offer', models.BooleanField(default=False)),
                ('num_sold', models.PositiveIntegerField(default=0)),
                ('product_group',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products',
                                   to='shops.ProductGroupModel')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products',
                                           to='shops.ShopProfileModel')),
            ],
            options={
                'unique_together': {('shop', 'slug')},
            },
        ),
        migrations.AddField(
            model_name='productgroupmodel',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_groups',
                                    to='shops.ShopProfileModel'),
        ),
        migrations.AddField(
            model_name='optiongroupmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_groups',
                                    to='shops.ProductModel'),
        ),
        migrations.CreateModel(
            name='ShopReviewModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField()),
                ('stars', models.FloatField(validators=[django.core.validators.MaxValueValidator(5),
                                                        django.core.validators.MinValueValidator(0.5)])),
                ('text', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews',
                                           to='shops.ShopProfileModel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           to='users.UserProfileModel')),
            ],
            options={
                'ordering': ['sort'],
                'unique_together': {('shop', 'sort')},
            },
        ),
        migrations.CreateModel(
            name='ProductReviewModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveIntegerField()),
                ('stars', models.FloatField(validators=[django.core.validators.MaxValueValidator(5),
                                                        django.core.validators.MinValueValidator(0.5)])),
                ('text', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews',
                                              to='shops.ProductModel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           to='users.UserProfileModel')),
            ],
            options={
                'ordering': ['sort'],
                'unique_together': {('product', 'sort')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='productgroupmodel',
            unique_together={('shop', 'sort'), ('shop', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='optiongroupmodel',
            unique_together={('product', 'sort')},
        ),
        migrations.CreateModel(
            name='AddOnModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('added_price', models.FloatField()),
                ('sort', models.PositiveIntegerField(null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_ons',
                                              to='shops.ProductModel')),
            ],
            options={
                'ordering': ['sort'],
                'unique_together': {('product', 'sort')},
            },
        ),
    ]
