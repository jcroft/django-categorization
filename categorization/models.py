from django.db import models

class Hierarchy(models.Model):
  """
  A Hierarchy is a "tree" of categories.
  """
  name                  = models.CharField(max_length=255, help_text="The name of a category tree. For example, a hierarchy of categories of beer might be called 'Beer'.")
  slug                  = models.SlugField(unique=True, help_text="A URL-friendly version of the name. Auto-populated.")

  def __unicode__(self):
    return u"%s" % self.name
  
  class Meta:
    verbose_name_plural = "Hierarchies"
  
  @property
  def top_level_categories(self):
    return self.categories.filter(parent_category__isnull=True)

  def save(self, *args, **kwargs):
    """
    Update any top level child categories to reflect new path.
    This will cascade down to lower levels, as categories will automatically
    re-save their children.
    """
    super(Hierarchy, self).save(force_insert=force_insert, force_update=force_update)
    for category in self.top_level_categories:
      category.save()


class Category(models.Model):
  hierarchy             = models.ForeignKey(Hierarchy, related_name="categories", default=1, help_text="The hierarchy this category belongs to.")
  parent_category       = models.ForeignKey('self', blank=True, null=True, related_name="direct_descendants", help_text="The parent category, if this is a sub-category.")
  name                  = models.CharField(max_length=255, help_text="The name of this category.")
  slug                  = models.SlugField(blank=True, editable=False, help_text="A URL-friendly version of the name. Auto-populated.")
  description           = models.TextField(blank=True, help_text="A textual description of this category.")
  path                  = models.TextField(blank=True, editable=False, help_text="The path to the category, made up of slugs.")
  full_name             = models.TextField(blank=True, editable=False, help_text="The human readable full path name of the category.")
  form_display_name     = models.TextField(blank=True, editable=False, help_text="The label for this category used in form dropdowns.")

  class Meta:
    ordering = ("path",)
    verbose_name_plural = "Categories"
    unique_together = (
      ("hierarchy", "parent_category", "name"),
    )
  
  def __unicode__(self):
    return u"%s" % self.full_name
  
  @property
  def path_name(self):
    """
    Returns a pretty version of the full path, minus the hierarchy
    """
    hierarchy_prefix = "[" + self.hierarchy.name + "] "
    return self.full_name[len(hierarchy_prefix):]
  
  @property
  def all_parent_categories(self):
    """
    Returns a list of all parents for this category.
    """
    if not self.parent_category:
      return []
    else:
      parents = []
      current = self
      while current.parent_category:
        current = current.parent_category
        parents.insert(0, current)
      return parents
  
  @property
  def all_child_categories(self):
    """
    Returns a QuerySet of all children for this category.
    """
    return Category.objects.filter(hierarchy=self.hierarchy, path__startswith=self.path + '/')
  
  def _create_form_display_name(self):
    """
    Creates a version of the path appropriate for use in a
    select dropdown, such as in a model form.
    """
    whitespace = ""
    for category in self.all_parent_categories:
      whitespace += "-"
    return whitespace + " " + self.name
  
  def _create_full_name(self):
    """
    Creates a pretty version of the full path.
    This is saved in the database for performance reasons.
    """
    if self.parent_category:
      return ": ".join(b.name for b in self.all_parent_categories) + ": " + self.name
    else:
      return self.name
  
  def _create_path(self):
    """
    Creates the path string for this category.
    """
    if self.parent_category:
      return self.hierarchy.slug + "/" + "/".join(b.slug for b in self.all_parent_categories) + "/" + self.slug
    else:
      return self.hierarchy.slug + "/" + self.slug
  
  def _update_child_categories(self, path):
    """
    Updates the child categories with the new path.
    """
    categories = Category.objects.filter(hierarchy=self.hierarchy, path__startswith=path + '/')
    for category in categories:
      category.save(saved_by_parent=True)
  
  def save(self, saved_by_parent=False, *args, **kwargs):
    """
    Creates path and then save the category. 
    If the path has been updated, updates any child categories to reflect new path.
    """
    from django.template.defaultfilters import slugify
    self.slug = slugify(self.name)
    old_path = self.path
    new_path = self._create_path()
    self.path = new_path
    self.full_name = self._create_full_name()
    self.form_display_name = self._create_form_display_name()
    super(Category, self).save(*args, **kwargs)
    if not saved_by_parent:
      if new_path != old_path:
        self._update_child_categories(old_path)
