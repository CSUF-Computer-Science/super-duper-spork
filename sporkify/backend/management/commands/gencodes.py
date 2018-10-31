from django.core.management.base import BaseCommand, CommandError
from backend.models import Open_Product_Code

class Command(BaseCommand):
    help = 'Generate item codes and put them in the database'

    def handle(self, *args, **options):
        Bays = ['A', 'B', 'C', 'D', 'E',
                'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O',
                'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
        Sides = ['1', '2']
        SC = ['X', 'Y', 'Z']  # Shelf Column
        SR = ['1', '2', '3', '4']  # Shelf Row
        Bin = ['A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P']

        Codes = []
        for bay in Bays:
            for side in Sides:
                for s_c in SC:
                    for s_r in SR:
                        for x in Bin:
                            code = bay + side + s_c + s_r + x
                            x = Open_Product_Code()
                            x.product_code = code
                            x.save()

        