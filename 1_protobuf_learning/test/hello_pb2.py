# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hello.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hello.proto',
  package='test',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0bhello.proto\x12\x04test\"-\n\x10hello_hu_request\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03\x61ge\x18\x02 \x01(\x05\" \n\x0ehello_hu_reply\x12\x0e\n\x06result\x18\x01 \x01(\t2G\n\tSay_hello\x12:\n\x08hello_hu\x12\x16.test.hello_hu_request\x1a\x14.test.hello_hu_reply\"\x00\x62\x06proto3'
)




_HELLO_HU_REQUEST = _descriptor.Descriptor(
  name='hello_hu_request',
  full_name='test.hello_hu_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='test.hello_hu_request.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='age', full_name='test.hello_hu_request.age', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=66,
)


_HELLO_HU_REPLY = _descriptor.Descriptor(
  name='hello_hu_reply',
  full_name='test.hello_hu_reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='test.hello_hu_reply.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=100,
)

DESCRIPTOR.message_types_by_name['hello_hu_request'] = _HELLO_HU_REQUEST
DESCRIPTOR.message_types_by_name['hello_hu_reply'] = _HELLO_HU_REPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

hello_hu_request = _reflection.GeneratedProtocolMessageType('hello_hu_request', (_message.Message,), {
  'DESCRIPTOR' : _HELLO_HU_REQUEST,
  '__module__' : 'hello_pb2'
  # @@protoc_insertion_point(class_scope:test.hello_hu_request)
  })
_sym_db.RegisterMessage(hello_hu_request)

hello_hu_reply = _reflection.GeneratedProtocolMessageType('hello_hu_reply', (_message.Message,), {
  'DESCRIPTOR' : _HELLO_HU_REPLY,
  '__module__' : 'hello_pb2'
  # @@protoc_insertion_point(class_scope:test.hello_hu_reply)
  })
_sym_db.RegisterMessage(hello_hu_reply)



_SAY_HELLO = _descriptor.ServiceDescriptor(
  name='Say_hello',
  full_name='test.Say_hello',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=102,
  serialized_end=173,
  methods=[
  _descriptor.MethodDescriptor(
    name='hello_hu',
    full_name='test.Say_hello.hello_hu',
    index=0,
    containing_service=None,
    input_type=_HELLO_HU_REQUEST,
    output_type=_HELLO_HU_REPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SAY_HELLO)

DESCRIPTOR.services_by_name['Say_hello'] = _SAY_HELLO

# @@protoc_insertion_point(module_scope)
