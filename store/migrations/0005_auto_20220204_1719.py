# Generated by Django 4.0.2 on 2022-02-04 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_adress_address'),
    ]

    operations = [
        migrations.RunSQL("""
            INSERT INTO store_collection (title)
            VALUES ('collection1')
        """, """
            DELETE FROM store_collection
            WHERE title='collection1'
        """)
    ]
