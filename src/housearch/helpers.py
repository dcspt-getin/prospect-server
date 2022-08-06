import json
from housearch.models import TerritorialCoverage, TerritorialUnit, TerritorialUnitImage


def load_geo_json(data, save_result=False):
    all_territorial = TerritorialCoverage.objects.all()
    all_municods = []
    loaded_data = []

    for item in all_territorial:
        all_municods.append(item.municod)

    print(all_municods)

    for feature in data['features']:
        #   if 'lhavo' in feature['properties']['FREG18_la']:
        # print(feature['properties']['MUNICOD'])
        if feature['properties']['MUNICOD'] in all_municods:

            loaded_data.append(feature)

            tucode = feature['properties']['TUCod'] if 'TUCod' in feature['properties'] else ''
            name = feature['properties']['name'] if 'name' in feature['properties'] else tucode

            print('tucode')
            print(tucode)

            territorial = TerritorialCoverage.objects.get(
                municod__exact=feature['properties']['MUNICOD'])
            territorial_units = TerritorialUnit.objects.filter(
                territorial_coverage_id=territorial.id, name__exact=name)

            if territorial_units.count() > 0:
                territorial_unit = TerritorialUnit.objects.get(
                    territorial_coverage_id=territorial.id, name__exact=name)
                territorial_unit.properties = feature['properties']
                territorial_unit.geometry = feature
                territorial_unit.save()
            else:
                TerritorialUnit.objects.create(
                    territorial_coverage=territorial,
                    tucode=tucode,
                    name=name,
                    properties=feature['properties'],
                    geometry=feature
                )

    if save_result:
        with open('media/loaded_geo_data.json', "w") as out:
            json.dump({'features': loaded_data}, out)


def import_territorial_unit_images_json(data):

    for image in data:
        tucode = image['TUCod']
        name = image['IMG_name'] if 'IMG_name' in image else tucode
        image_url = image['Image_url'] if 'Image_url' in image else ''
        territorial_unit = TerritorialUnit.objects.get(tucode__exact=tucode)

        if territorial_unit:
            TerritorialUnitImage.objects.update_or_create(
                territorial_unit=territorial_unit,
                name=name,
                image_url=image_url,
                geometry={
                    "lat": image['Long_y'],
                    "lng": image['Long_x'],
                }
            )
