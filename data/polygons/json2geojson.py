"""
converts a json of the following schema to a geojson:
{
    out_edge: [
        {
            geo_array: [ [lat:float, lon:float], ...],
            geo_id: id:String
        },
        ...
    ]
}
where each geo_array holds points representing a polygon.

writes the resultant geojson to disk with name '<input_filename>.geojson'.
"""
import json
import sys


def convert(filename):
    input_json = None
    geojson = None

    with open(filename, 'r') as f:
        input_json = json.load(f)

    geojson = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [polygon_data['geo_array']]
                }
            }

            for polygon_data in input_json['out_edge']
        ]
    }

    return geojson


def write_json_to_disk(json_data, filename):
    with open(filename, 'w') as f:
        json.dump(json_data, f)


if __name__ == '__main__':
    assert len(sys.argv) == 2, ('Invalid args, use this format:\n'
                                'python json2geojson.py <input_json_filename>'
                                )

    input_filename = sys.argv[1]
    output_filename = input_filename.replace('.json', '.geojson')

    geojson = convert(input_filename)
    write_json_to_disk(geojson, output_filename)
