# Generated by Django 5.0.3 on 2024-06-16 03:05

import cloudinary.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('Cư Dân', 'Resident'), ('Quản Lý', 'Manager')], default='Cư Dân', max_length=20)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('sex', models.CharField(choices=[('Nam', 'Male'), ('Nữ', 'Female')], default='Nam', max_length=20)),
                ('avatar', cloudinary.models.CloudinaryField(max_length=255, null=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('is_first_login', models.BooleanField(default=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('floor', models.IntegerField(default=1)),
                ('room', models.IntegerField(choices=[(1, 'Room 1'), (2, 'Room 2'), (3, 'Room 3')], default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('content', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('fee_name', models.CharField(max_length=30)),
                ('price', models.IntegerField(null=True)),
                ('types', models.CharField(choices=[('Nha', 'Tiền nhà'), ('Dien', 'Tiền điện'), ('Dich vu', 'Tiền phí dịch vụ')], default='Nha', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=30)),
                ('data_expire', models.DateField()),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='manager_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('area', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('user_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='resident_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('apartment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='apartment.apartment')),
            ],
        ),
        migrations.CreateModel(
            name='ElectronicLockerItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('name', models.CharField(default='Tủ đồ', max_length=30)),
                ('apartment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='electronic_locker', to='apartment.apartment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('item_name', models.CharField(default='Tên sản phẩm', max_length=255, null=True)),
                ('received_date', models.DateField(auto_now=True, null=True)),
                ('created_date', models.DateField(auto_now=True)),
                ('electronic_lock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='apartment.electroniclockeritem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('content_choice', models.CharField(max_length=30)),
                ('letter', models.CharField(help_text='A, B, C, D', max_length=1)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='apartment.question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResidentFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Chuyển khoản Ngân Hàng', 'Chuyển khoản Ngân Hàng'), ('Chuyển khoản Momo', 'Chuyển khoản MoMo')], max_length=50, null=True)),
                ('payment_proof', cloudinary.models.CloudinaryField(max_length=255, null=True)),
                ('payment_date', models.DateField(auto_now_add=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Đang chờ xử lý', 'Đang xử lý'), ('Không thể xử lý', 'Thất Bại'), ('Thành Công', 'Thành Công')], default='Đang chờ xử lý', max_length=50)),
                ('amount', models.IntegerField(default=1)),
                ('fee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident_fees', to='apartment.service')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident_fees', to='apartment.resident')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='apartment.survey'),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40, null=True)),
                ('content', models.CharField(max_length=50, null=True)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, null=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_manager', to='apartment.manager')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='service',
            name='residents',
            field=models.ManyToManyField(related_name='service', through='apartment.ResidentFee', to='apartment.resident'),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateField(auto_now_add=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='apartment.survey')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='apartment.resident')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField(max_length=50, null=True)),
                ('status', models.CharField(choices=[('Đang chờ xử lý', 'Pending'), ('Không thể xử lý', 'Deny'), ('Đã xử lý', 'Done')], default='Đang chờ xử lý', max_length=20)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reflection_forms', to='apartment.resident')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReservationVehicle',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apartment.service')),
                ('vehicle_number', models.CharField(max_length=10)),
                ('vehicle_owner', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Đang chờ xử lý', 'Đang chờ xử lý'), ('Không thể xử lý', 'Không thể xử lý'), ('Đã đăng ký', 'Đã đăng ký')], default='Đang chờ xử lý', max_length=50)),
                ('resident', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='apartment.resident')),
            ],
            options={
                'abstract': False,
            },
            bases=('apartment.service',),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='apartment.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='apartment.question')),
                ('response', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='apartment.response')),
            ],
            options={
                'unique_together': {('response', 'question')},
            },
        ),
    ]
