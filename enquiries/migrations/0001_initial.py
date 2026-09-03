from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('company', models.CharField(blank=True, max_length=160)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(blank=True, max_length=40)),
                ('service', models.CharField(max_length=120)),
                ('message', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('contacted', 'Contacted'), ('in_progress', 'In Progress'), ('closed', 'Closed')], default='new', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Website Enquiry',
                'verbose_name_plural': 'Website Enquiries',
                'ordering': ['-created_at'],
            },
        ),
    ]
