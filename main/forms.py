from django import forms


class FormStyleMixin:
    def __int__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


