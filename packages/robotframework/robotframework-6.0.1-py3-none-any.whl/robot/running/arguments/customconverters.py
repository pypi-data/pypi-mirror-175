#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from robot.utils import getdoc, is_union, seq2str, type_name

from .argumentparser import PythonArgumentParser


class CustomArgumentConverters:

    def __init__(self, converters):
        self.converters = converters

    @classmethod
    def from_dict(cls, converters, error_reporter):
        valid = []
        for type_, conv in converters.items():
            try:
                info = ConverterInfo.for_converter(type_, conv)
            except TypeError as err:
                error_reporter(str(err))
            else:
                valid.append(info)
        return cls(valid)

    def get_converter_info(self, type_):
        if isinstance(type_, type):
            for conv in self.converters:
                if issubclass(type_, conv.type):
                    return conv
        return None

    def __iter__(self):
        return iter(self.converters)

    def __len__(self):
        return len(self.converters)


class ConverterInfo:

    def __init__(self, type, converter, value_types):
        self.type = type
        self.converter = converter
        self.value_types = value_types

    @property
    def name(self):
        return type_name(self.type)

    @property
    def doc(self):
        return getdoc(self.converter) or getdoc(self.type)

    @classmethod
    def for_converter(cls, type_, converter):
        if not isinstance(type_, type):
            raise TypeError(f'Custom converters must be specified using types, '
                            f'got {type_name(type_)} {type_!r}.')
        if converter is None:
            def converter(arg):
                raise TypeError(f'Only {type_.__name__} instances are accepted, '
                                f'got {type_name(arg)}.')
        if not callable(converter):
            raise TypeError(f'Custom converters must be callable, converter for '
                            f'{type_name(type_)} is {type_name(converter)}.')
        arg_type = cls._get_arg_type(converter)
        if arg_type is None:
            accepts = ()
        elif is_union(arg_type):
            accepts = arg_type.__args__
        elif hasattr(arg_type, '__origin__'):
            accepts = (arg_type.__origin__,)
        else:
            accepts = (arg_type,)
        return cls(type_, converter, accepts)

    @classmethod
    def _get_arg_type(cls, converter):
        spec = PythonArgumentParser(type='Converter').parse(converter)
        if spec.minargs > 1:
            required = seq2str([a for a in spec.positional if a not in spec.defaults])
            raise TypeError(f"Custom converters cannot have more than one mandatory "
                            f"argument, '{converter.__name__}' has {required}.")
        if not spec.positional:
            raise TypeError(f"Custom converters must accept one positional argument, "
                            f"'{converter.__name__}' accepts none.")
        if spec.named_only and set(spec.named_only) - set(spec.defaults):
            required = seq2str(sorted(set(spec.named_only) - set(spec.defaults)))
            raise TypeError(f"Custom converters cannot have mandatory keyword-only "
                            f"arguments, '{converter.__name__}' has {required}.")
        return spec.types.get(spec.positional[0])
