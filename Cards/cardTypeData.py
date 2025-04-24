class TypeData:
    def __init__(self, front_face_supertypes=None, front_face_types=None, front_face_subtypes=None,
                 back_face_supertypes=None, back_face_types=None, back_face_subtypes=None):
        self._front_face_supertypes = front_face_supertypes
        self._front_face_types = front_face_types
        self._front_face_subtypes = front_face_subtypes
        self._back_face_supertypes = back_face_supertypes
        self._back_face_types = back_face_types
        self._back_face_subtypes = back_face_subtypes

    @property
    def front_face_supertypes(self):
        return self._front_face_supertypes

    @property
    def front_face_types(self):
        return self._front_face_types

    @property
    def front_face_subtypes(self):
        return self._front_face_subtypes

    @property
    def back_face_supertypes(self):
        return self._back_face_supertypes

    @property
    def back_face_types(self):
        return self._back_face_types

    @property
    def back_face_subtypes(self):
        return self._back_face_subtypes

    @property
    def has_multiple_faces(self):
        return False if self._back_face_types is None else True

    def __str__(self):
        result = f'Front Face\nSupertypes: {self._front_face_supertypes}\n'\
               f'Types: {self._front_face_types}\nSubtypes: {self._front_face_subtypes}\n'

        if self.has_multiple_faces:
               result += f'\nBack Face\nSupertypes: {self._back_face_supertypes}\n'\
               f'Types: {self._back_face_types}\nSubtypes: {self._back_face_subtypes}\n'

        return f'--\n{result}--\n'