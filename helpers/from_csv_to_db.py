"""
From CSV to DB migration script
"""

import pandas as pd

from seller.constants import FRIENDS, INSTAGRAM, OTHERS
from seller.models import Seller, DeliveryMean, OrderMean, ProductImage


print('Opening CSV...')
df = pd.read_csv('~/sellers.csv')
print('Successfully opened CSV...')


print('Creating auxiliary variables...')
# Lists to store objs to create
sellers_to_create = []
images_to_create = []

# DeliveryMeans data structs
delivery_table = {
    'delivery': 'Delivery',
    'takeout': 'Retirada',
    'dispatch': 'Envio'
}
delivery_dict = {value: [] for value in delivery_table.values()}

# OrderMeans data structs
order_table = {
    'telephone': 'Telefone',
    'whatsapp': 'Whatsapp',
    'website': 'Site',
    'instagram': 'DM no Instagram',
    'ifood': 'Ifood',
    'uber_eats': 'Uber Eats',
    'rappi': 'Rappi',
}
order_dict = {value: [] for value in order_table.values()}

referrals_table = {
    'Indicação de amigos': FRIENDS,
    'Instagram': INSTAGRAM,
    'Outras formas': OTHERS,
}

existing_sellers_profiles = Seller.objects.all().values_list('instagram_profile', flat=True)

print('Starting loop...')
for index, row in df.iterrows():
    print(f'Processing Seller {index}/{len(df.index)}...')

    if row['instagram'] in existing_sellers_profiles:
        print(f'Seller {row["instagram"]} already in DB, continuing...')
        continue

    # Seller declaration
    seller = Seller(
        name=row['name'],
        description=row['obs'],
        neighborhood=row['neighborhood'],
        city=row['Cidade (se aceito)'],
        state=row['state'],
        telephone_number=row['phoneNumber'],
        whatsapp=row['whatsapp'],
        site_url=row['site'],
        instagram_profile=row['instagram'],
        ifood_url=row['Ifood'],
        uber_eats_url=row['UberEats'],
        rappi_url=row['Rappi'],
        referrals=referrals_table[row['Como você nos achou?']] if row['Como você nos achou?'] in referrals_table.keys() else None,
        cover_image=row['photo'],
        is_approved=True if row['accepted'] == 'TRUE' else False
    )

    row_delivery_means = row['howToReceive'].split(', ')
    for mean in row_delivery_means:
        delivery_dict[mean].append(seller)

    row_order_means = row['delivery'].split(', ')
    for mean in row_order_means:
        order_dict[mean].append(seller)

    row_images = row['allPhotos'].split(', ')
    for idx, image_url in enumerate(row_images):
        image = ProductImage(
            seller=seller,
            order=idx,
            image=image_url
        )
        images_to_create.append(image)

    sellers_to_create.append(seller)

print('Finished processing Sellers.\nBulk creating Sellers...')
Seller.objects.bulk_create(sellers_to_create)
print('Finished bulk creating Sellers.\nBulk creating ProductImages...')
ProductImage.objects.bulk_create(images_to_create)
print('Finished bulk creating ProductImages.')


print('Attaching Sellers to OrderMeans...')
order_means = OrderMean.objects.all()
for mean in order_means:
    try:
        mean.sellers.add(order_dict[order_table[mean.slug]])
    except KeyError:
        continue

print('Finished attaching Sellers to OrderMeans.\nAttaching Sellers to DeliveryMeans...')
delivery_means = DeliveryMean.objects.all()
for mean in delivery_means:
    try:
        mean.sellers.add(delivery_dict[delivery_table[mean.slug]])
    except KeyError:
        continue
print('Finished attaching Sellers to DeliveryMeans.')
print('Finished.')
