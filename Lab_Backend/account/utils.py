# from django.http import QueryDict
# import json
# from rest_framework import parsers

# class MultipartJsonParser(parsers.MultiPartParser):

#     def parse(self, stream, media_type=None, parser_context=None):
#         result = super().parse(
#             stream,
#             media_type=media_type,
#             parser_context=parser_context
#         )
#         data = {}
#         # find the data field and parse it
#         data = json.loads(result.data["data"])
#         qdict = QueryDict('', mutable=True)
#         qdict.update(data)
#         return parsers.DataAndFiles(qdict, result.files)



# from rest_framework import parsers
# import json

# class MultiPartJSONParser(parsers.MultiPartParser):
#     def parse(self, stream, *args, **kwargs):
#         data = super().parse(stream, *args, **kwargs)
#         json_data_field = data.data.get('_data')
#         if json_data_field is not None:
#             parsed = json.loads(json_data_field)
#             mutable_data = {}
#             for key, value in parsed.items():
#                 mutable_data[key] = value
#             mutable_files = {}
#             for key, value in data.files.items():
#                 if key != '_data':
#                     mutable_files[key] = value
#             return parsers.DataAndFiles(mutable_data, mutable_files)

#         json_data_file = data.files.get('_data')
#         if json_data_file:
#             parsed = parsers.JSONParser().parse(json_data_file)
#             mutable_data = {}
#             for key, value in parsed.items():
#                 mutable_data[key] = value
#             mutable_files = {}
#             for key, value in data.files.items():
#                 mutable_files[key] = value
#             return parsers.DataAndFiles(mutable_data, mutable_files)

#         return data
    

# class MultiPartJSONParser(parsers.MultiPartParser):
#     def parse(self, stream, *args, **kwargs):
#         data = super().parse(stream, *args, **kwargs)

#         # Any 'File' found having application/json as type will be moved to data
#         mutable_data = data.data.copy()
#         unmarshaled_blob_names = []
#         json_parser = parsers.JSONParser()
#         for name, blob in data.files.items():
#             if blob.content_type == 'application/json' and name not in data.data:
#                 parsed = json_parser.parse(blob)
#                 if isinstance(parsed, list):
#                     # need to break it out into [0], [1] etc
#                     for idx, item in enumerate(parsed):
#                         mutable_data[name+f"[{str(idx)}]"] = item
#                 else:
#                     mutable_data[name] = parsed
#                 unmarshaled_blob_names.append(name)
#         for name in unmarshaled_blob_names:
#             del data.files[name]
#         data.data = mutable_data

#         return data


