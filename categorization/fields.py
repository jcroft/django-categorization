from django.forms.models import ModelChoiceIterator
from django.utils.encoding import smart_unicode
from django import forms
                                
class CategoryModelChoiceField(forms.ModelChoiceField):
  def label_from_instance(self, obj):
      """
      This method is used to convert objects into strings; it's used to
      generate the labels for the choices presented by this object. Subclasses
      can override this method to customize the display of the choices.
      """
      return smart_unicode(obj.form_display_name)