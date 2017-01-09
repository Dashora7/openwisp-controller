# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 16:48
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_netjsonconfig.base.config
import django_netjsonconfig.base.template
import jsonfield.fields
import model_utils.fields
import re
import sortedm2m.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pki', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('backend', models.CharField(choices=[('netjsonconfig.OpenWrt', 'OpenWRT'), ('netjsonconfig.OpenWisp', 'OpenWISP')], help_text='Select netjsonconfig backend', max_length=128, verbose_name='backend')),
                ('config', jsonfield.fields.JSONField(blank=True, default=dict, help_text='configuration in NetJSON DeviceConfiguration format', verbose_name='configuration')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('modified', 'modified'), ('running', 'running'), ('error', 'error')], default='modified', help_text='modified means the configuration is not applied yet; running means applied and running; error means the configuration caused issues and it was rolledback', max_length=100, no_check_for_status=True)),
                ('key', models.CharField(db_index=True, default=django_netjsonconfig.base.config.get_random_key, help_text='unique key that can be used to download the configuration', max_length=64, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[^\\s/\\.]+$', 32), code='invalid', message='Key must not contain spaces, dots or slashes.')])),
                ('mac_address', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', 32), code='invalid', message='Must be a valid mac address.')])),
                ('last_ip', models.GenericIPAddressField(blank=True, help_text='indicates the last ip from which the configuration was downloaded from (except downloads from this page)', null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization', verbose_name='organization')),
            ],
            options={
                'verbose_name': 'configuration',
                'verbose_name_plural': 'configurations',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('backend', models.CharField(choices=[('netjsonconfig.OpenWrt', 'OpenWRT'), ('netjsonconfig.OpenWisp', 'OpenWISP')], help_text='Select netjsonconfig backend', max_length=128, verbose_name='backend')),
                ('config', jsonfield.fields.JSONField(blank=True, default=dict, help_text='configuration in NetJSON DeviceConfiguration format', verbose_name='configuration')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('type', models.CharField(choices=[('generic', 'Generic'), ('vpn', 'VPN-client')], db_index=True, default='generic', help_text='template type, determines which features are available', max_length=16, verbose_name='type')),
                ('default', models.BooleanField(db_index=True, default=False, help_text='whether new configurations will have this template enabled by default', verbose_name='enabled by default')),
                ('auto_cert', models.BooleanField(db_index=True, default=django_netjsonconfig.base.template.default_auto_cert, help_text='whether x509 client certificates should be automatically managed behind the scenes for each configuration using this template, valid only for the VPN type', verbose_name='auto certificate')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization', verbose_name='organization')),
            ],
            options={
                'verbose_name': 'template',
                'verbose_name_plural': 'templates',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vpn',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('config', jsonfield.fields.JSONField(default=dict, help_text='configuration in NetJSON DeviceConfiguration format', verbose_name='configuration')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('host', models.CharField(help_text='VPN server hostname or ip address', max_length=64)),
                ('backend', models.CharField(choices=[('django_netjsonconfig.vpn_backends.OpenVpn', 'OpenVPN')], help_text='Select VPN configuration backend', max_length=128, verbose_name='VPN backend')),
                ('notes', models.TextField(blank=True)),
                ('dh', models.TextField(blank=True)),
                ('ca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pki.Ca', verbose_name='Certification Authority')),
                ('cert', models.ForeignKey(blank=True, help_text='leave blank to create automatically', null=True, on_delete=django.db.models.deletion.CASCADE, to='pki.Cert', verbose_name='x509 Certificate')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization', verbose_name='organization')),
            ],
            options={
                'verbose_name': 'VPN server',
                'verbose_name_plural': 'VPN servers',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VpnClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_cert', models.BooleanField(default=False)),
                ('cert', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pki.Cert')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Config')),
                ('vpn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Vpn')),
            ],
            options={
                'verbose_name': 'VPN client',
                'verbose_name_plural': 'VPN clients',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='template',
            name='vpn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='config.Vpn', verbose_name='VPN'),
        ),
        migrations.AddField(
            model_name='config',
            name='templates',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text='configuration templates, applied fromfirst to last', related_name='config_relations', to='config.Template', verbose_name='templates'),
        ),
        migrations.AddField(
            model_name='config',
            name='vpn',
            field=models.ManyToManyField(blank=True, related_name='vpn_relations', through='config.VpnClient', to='config.Vpn'),
        ),
        migrations.AlterUniqueTogether(
            name='vpnclient',
            unique_together=set([('config', 'vpn')]),
        ),
    ]
