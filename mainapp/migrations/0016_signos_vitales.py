# Generated by Django 3.2.12 on 2022-03-19 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_agendar_cita'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signos_vitales',
            fields=[
                ('id_signo_vital', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('id_paciente', models.IntegerField(null=True)),
                ('fecha_cita', models.DateField(null=True)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('talla', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('imc', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('f_cardica', models.IntegerField(null=True)),
                ('F_respiratoria', models.IntegerField(null=True)),
                ('sistolica', models.IntegerField(null=True)),
                ('distolica', models.IntegerField(null=True)),
                ('oximetria', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('estado', models.IntegerField(default=1)),
            ],
        ),
    ]
