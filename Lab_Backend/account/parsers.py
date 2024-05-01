# from rest_framework import parsers

# class MultiPartJSONParser(parsers.MultiPartParser):
#     def parse(self, stream, *args, **kwargs):
#         data = super().parse(stream, *args, **kwargs)

#         # Any 'File' found having application/json as type will be moved to data
#         mutable_data = data.data.copy()
#         unmarshaled_blob_names = []
#         json_parser = parsers.JSONParser()
#         for name, blob in data.files.items():
#             if blob.content_type == 'application/json' and name not in data.data:
#                 mutable_data[name] = json_parser.parse(blob)
#                 unmarshaled_blob_names.append(name)
#         for name in unmarshaled_blob_names:
#             del data.files[name]
#         data.data = mutable_data

#         return data


from rest_framework import parsers
from django.http import QueryDict
import json

class MultipartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )


        data = {}
    

        #For nested serializers, drf accepts values in dotted notaion (if sent as Multipart/Formdata). E.g if location is nested serializer.
        # It will accept location.x and location.y if data is to be entered in form fields.
        # the 2 nested for loops, ensures that the JSON data sent in form field is converted to the above format.
        #e.g if the key is asset_location. and it has x and y keys inside. It will be converted to asset_location.x, and asset_location.y


        for key, value in result.data.items():
            if type(value) != str:
                data[key] = value
                continue
            if '{' in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                
                    if type(data[key]) == dict:
                        for inner_key,inner_value in data[key].items():
                            data[f'{key}.{inner_key}']=inner_value
                except ValueError:
                    data[key] = value
            else:
                data[key] = value

        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        # print(qdict)
        return parsers.DataAndFiles(qdict, result.files)