# Generated by Django 3.2 on 2021-04-14 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storedb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inv_buff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_name', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('inv_no', models.IntegerField()),
                ('prod_name', models.CharField(max_length=30)),
                ('prod_size', models.CharField(max_length=30)),
                ('prod_unit', models.CharField(max_length=10)),
                ('prod_quant', models.IntegerField()),
                ('prod_rate', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_name', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('inv_no', models.IntegerField()),
                ('prod_name', models.CharField(max_length=30)),
                ('prod_size', models.CharField(max_length=30)),
                ('prod_unit', models.CharField(max_length=10)),
                ('prod_quant', models.IntegerField()),
                ('prod_rate', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
    ]
