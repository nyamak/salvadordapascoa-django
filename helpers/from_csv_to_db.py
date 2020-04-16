"""
From CSV to DB migration script
"""
from collections import defaultdict

import pandas as pd

from seller.constants import FRIENDS, INSTAGRAM, OTHERS
from seller.models import Seller, DeliveryMean, OrderMean, ProductImage


def is_nan(val):
    if str(val) == 'nan':
        return None
    else:
        return val


print('Opening CSV...')
df = pd.read_csv('sellers.csv')
print('Successfully opened CSV...')


print('Creating auxiliary variables...')
# Lists to store objs to create
sellers_to_create = []
images_to_create = defaultdict(list)

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

existing_sellers_profiles = list(Seller.objects.all().values_list('instagram_profile', flat=True))

print('Starting loop...')
for index, row in df.iterrows():
    print(f'Processing Seller {index}/{len(df.index)}...')

    if row['instagram'] in existing_sellers_profiles:
        print(f'Seller {row["instagram"]} already in DB, continuing...')
        continue
    else:
        existing_sellers_profiles.append(row['instagram'])

    print(row['accepted'])
    # Seller declaration
    seller = Seller(
        name=row['name'],
        description=row['obs'],
        neighborhood=row['neighborhood'],
        city=is_nan(row['city']),
        state=is_nan(row['state']),
        telephone_number=row['phoneNumber'],
        whatsapp_number=is_nan(row['whatsapp']),
        site_url=is_nan(row['site']),
        instagram_profile=row['instagram'],
        ifood_url=is_nan(row['Ifood']),
        uber_eats_url=is_nan(row['UberEats']),
        rappi_url=is_nan(row['Rappi']),
        referrals=referrals_table[row['Como você nos achou?']] if row['Como você nos achou?'] in referrals_table.keys() else None,
        cover_image=is_nan(row['photo']),
        is_approved=True if str(row['accepted']) == 'True' else False
    )

    row_delivery_means = row['howToReceive'].split(', ') if str(row['howToReceive']) != 'nan' else []
    for mean in row_delivery_means:
        try:
            delivery_dict[mean].append(seller)
        except KeyError:
            continue

    row_order_means = row['delivery'].split(', ') if str(row['delivery']) != 'nan' else []
    for mean in row_order_means:
        try:
            order_dict[mean].append(seller)
        except KeyError:
            continue

    row_images = row['allPhotos'].split(', ') if str(row['allPhotos']) != 'nan' else []
    for idx, image_url in enumerate(row_images):
        image = ProductImage(
            order=idx,
            image=image_url
        )
        images_to_create[seller.instagram_profile].append(image)

    sellers_to_create.append(seller)

print('Finished processing Sellers.\nBulk creating Sellers...')
Seller.objects.bulk_create(sellers_to_create)
print('Finished bulk creating Sellers.\n Creating ProductImages...')
final_images_to_create = []
sellers = list(Seller.objects.all())

for seller in sellers:
    if seller.instagram_profile in images_to_create:
        for image in images_to_create[seller.instagram_profile]:
            image.seller = seller
            final_images_to_create.append(image)
ProductImage.objects.bulk_create(final_images_to_create)
print('Finished bulk creating ProductImages.')


print('Attaching Sellers to OrderMeans...')
order_means = OrderMean.objects.all()
for mean in order_means:
    try:
        mean.sellers.add(*order_dict[order_table[mean.slug]])
    except KeyError:
        continue

print('Finished attaching Sellers to OrderMeans.\nAttaching Sellers to DeliveryMeans...')
delivery_means = DeliveryMean.objects.all()
for mean in delivery_means:
    try:
        mean.sellers.add(*delivery_dict[delivery_table[mean.slug]])
    except KeyError:
        continue
print('Finished attaching Sellers to DeliveryMeans.')
print('Finished.')
