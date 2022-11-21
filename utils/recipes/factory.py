# from inspect import signature
from random import randint

from faker import Faker


def rand_ratio():
    return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')
# print(signature(fake.random_number))


def make_recipe(i):
    if i > 10:
        i = i - (i // 10) * 10 
    return {
        'title': fake.sentence(nb_words=6),
        'description': fake.sentence(nb_words=12),
        'preparation_time': fake.random_number(digits=2, fix_len=True),
        'preparation_time_unit': 'Minutos',
        'servings': fake.random_number(digits=2, fix_len=True),
        'servings_unit': 'Porção',
        'preparation_steps': fake.text(3000),
        'created_at': fake.date_time(),
        'author': {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        },
        'category': {
            'name': fake.word()
        },
        'cover': {
            # 'url': 'https://loremflickr.com/%s/%s/food,cook' % rand_ratio(),
            'url': [
                'https://upload.wikimedia.org/wikipedia/commons/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg',
                'https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg',
                'https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2022-03/plant-based-food-mc-220323-02-273c7b.jpg',
                'https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F44%2F2022%2F03%2F29%2Fpasta-power-tout.jpg',
                'https://www.washingtonian.com/wp-content/uploads/2021/07/2Fiftys-1500x1000.jpg',
                'https://health.clevelandclinic.org/wp-content/uploads/sites/3/2021/04/FoodAllergiesSensitivityt-1155240429-770x533-1.jpg',
                'https://food-guide.canada.ca/themes/custom/wxtsub_bootstrap/images/food_guide_visual_en.png',
                'https://www.rbsdirect.com.br/filestore/3/2/8/1/7/3_b2196f37c7706d1/371823_edca5c22e8f1de7.jpg?w=1024&h=1024&a=c',
                'https://cdn.vox-cdn.com/thumbor/KJjKfCBX0DEu7QY7395Sc8fdYBY=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/23957266/Le_Fantome.jpg',
                'https://img.apmcdn.org/3ed4888cab8f559f76a85c295208583a4d2564f6/uncropped/7ee709-splendid-table-food-waste-gettyimages-172481514-lede.jpg'
                ][i]
        }
    }


if __name__ == '__main__':
    from pprint import pprint
    pprint([make_recipe for i in range(5)])