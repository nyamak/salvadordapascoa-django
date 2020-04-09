from django.db import migrations


def create_order_means(apps, schema_editor):
    OrderMean = apps.get_model("seller", "OrderMean")
    db_alias = schema_editor.connection.alias
    OrderMean.objects.using(db_alias).bulk_create([
        OrderMean(name="Telefone", slug="telephone"),
        OrderMean(name="Whatsapp", slug="whatsapp"),
        OrderMean(name="Facebook", slug="facebook"),
        OrderMean(name="Site", slug="website"),
        OrderMean(name="Instagram", slug="instagram"),
        OrderMean(name="iFood", slug="ifood"),
        OrderMean(name="Uber Eats", slug="uber_eats"),
        OrderMean(name="Rappi", slug="rappi"),
    ])


def delete_order_means(apps, schema_editor):
    OrderMean = apps.get_model("seller", "OrderMean")
    db_alias = schema_editor.connection.alias
    OrderMean.objects.using(db_alias).filter(name="Telefone", slug="telephone").delete()
    OrderMean.objects.using(db_alias).filter(name="Whatsapp", slug="whatsapp").delete()
    OrderMean.objects.using(db_alias).filter(name="Facebook", slug="facebook").delete()
    OrderMean.objects.using(db_alias).filter(name="Site", slug="website").delete()
    OrderMean.objects.using(db_alias).filter(name="Instagram", slug="instagram").delete()
    OrderMean.objects.using(db_alias).filter(name="iFood", slug="ifood").delete()
    OrderMean.objects.using(db_alias).filter(name="Uber Eats", slug="uber_eats").delete()
    OrderMean.objects.using(db_alias).filter(name="Rappi", slug="rappi").delete()


def create_delivery_means(apps, schema_editor):
    DeliveryMean = apps.get_model("seller", "DeliveryMean")
    db_alias = schema_editor.connection.alias
    DeliveryMean.objects.using(db_alias).bulk_create([
        DeliveryMean(name="Delivery", slug="delivery"),
        DeliveryMean(name="Retirada", slug="takeout"),
        DeliveryMean(name="Envio", slug="dispatch"),
    ])


def delete_delivery_means(apps, schema_editor):
    DeliveryMean = apps.get_model("seller", "DeliveryMean")
    db_alias = schema_editor.connection.alias
    DeliveryMean.objects.using(db_alias).filter(name="Delivery", slug="delivery").delete()
    DeliveryMean.objects.using(db_alias).filter(name="Retirada", slug="takeout").delete()
    DeliveryMean.objects.using(db_alias).filter(name="Envio", slug="dispatch").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_order_means, delete_order_means),
        migrations.RunPython(create_delivery_means, delete_delivery_means),
    ]
