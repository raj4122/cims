# Generated by Django 3.2.7 on 2022-03-21 07:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('course_category', models.CharField(max_length=100)),
                ('course_name', models.CharField(max_length=100)),
                ('course_full_form', models.CharField(max_length=150)),
                ('course_duration', models.CharField(max_length=20)),
                ('course_detail', models.CharField(blank=True, max_length=250, null=True)),
                ('course_package', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('gender', models.CharField(max_length=10)),
                ('father', models.CharField(max_length=150)),
                ('mother', models.CharField(max_length=150)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=250)),
                ('contact', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=25)),
                ('lpc', models.CharField(max_length=50)),
                ('passing_year', models.CharField(max_length=10)),
                ('board', models.CharField(max_length=100)),
                ('gread', models.CharField(max_length=20)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='edu/images')),
                ('reg_year', models.CharField(blank=True, max_length=10, null=True)),
                ('reg_mon', models.CharField(blank=True, max_length=10, null=True)),
                ('session_year', models.CharField(blank=True, max_length=10, null=True)),
                ('session_month', models.CharField(blank=True, max_length=10, null=True)),
                ('exam_year', models.CharField(blank=True, max_length=10, null=True)),
                ('exam_month', models.CharField(blank=True, max_length=10, null=True)),
                ('enroll_number', models.CharField(blank=True, max_length=15, null=True)),
                ('cretificate_no', models.CharField(blank=True, max_length=10, null=True)),
                ('cretificate_file', models.CharField(blank=True, max_length=100, null=True)),
                ('theory_s1', models.CharField(blank=True, max_length=100, null=True)),
                ('os', models.CharField(blank=True, max_length=100, null=True)),
                ('pretical_s1', models.CharField(blank=True, max_length=100, null=True)),
                ('oral_s1', models.CharField(blank=True, max_length=100, null=True)),
                ('theory_s2', models.CharField(blank=True, max_length=100, null=True)),
                ('pretical_s2', models.CharField(blank=True, max_length=100, null=True)),
                ('oral_s2', models.CharField(blank=True, max_length=100, null=True)),
                ('is_registerd', models.BooleanField(default=False)),
                ('is_enrolled', models.BooleanField(default=False)),
                ('is_examinee', models.BooleanField(default=False)),
                ('is_certified', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eduapi.course')),
            ],
        ),
    ]
