""" This module contains just a base class for both configuration values (Options)
and configuration containers ("Sections")
"""

from typing import Union

class BaseConfiguration:
  """ Common base class for all configurations values and containers. I.e.
  for options and sections

  """

  def __init__(self, definition, container=None):
      """
      Create the object. Just sets

      Parameters
      ----------
      definition: ase2sprkkr.common.configuration_definitions.BaseDefinition
      This configuration object definition.

      container: ase2sprkkr.common.configuration_containers.ConfigurationContainer
      The container, that will own the configuration item.
      """

      self._definition = definition
      """
      The "definition" of the option or section. The definition determines
      the name(s), value type(s) etc... contained in the configuration object.
      Instance of :class:`ase2sprkkr.common.configuration_definitions.BaseDefinition`
      """

      self._container = container
      """
      The parent container. I.e. the container that holds this object (e.g.
      for a value it is the section that owns the value)
      Instance of :class:`ase2sprkkr.common.configuration_containers.ConfigurationContainer`
      """

  def _get_path(self, include_root=False):
      """ Return the dot-delimited path to the item in the configuration tree.

      E.g. the ``ENERGY`` option in the ``CONTROL`` section has the path
      ``CONTROL.ENERGY``
      """
      name = self.name
      if self._container and (include_root or self._container._container):
         return f'{self._container._get_path()}.{name}'
      return name

  def _get_root_container(self):
      """ Return the root object of the configuration tree.

      I.E. the object, that represents the whole configuration or problem-definition file
      """
      return self._container._get_root_container() if self._container else self

  @property
  def name(self):
      """ Return the name of the option/section. The name is defined by the definition
      of the object.

      Returns
      -------
      name: str
      The name of the object.
      """
      return self._definition.name

  def as_dict(self, only_changed:Union[bool,str]='basic'):
      """ Return the value of self, in the case of container as a dictionary. To be redefined in the descendants.

      Parameters
      ----------
      only_changed
        Return only changed values, or all of them?
        If True, return only the values, that differ from the defaults.
        If False, return all the values.
        The default value 'basic' means, return all non-expert values
        and all changed expert values.
      """
      raise NotImplemented()

  def to_dict(self, only_changed:Union[bool,str]='basic'):
      """ Alias of the method :meth:`as_dict`. """
      return self.as_dict(only_changed)

  def show(self):
      """ Print the configuration, as it will be saved into the configuration/problem definition file. """
      print(self.to_string())

  @property
  def info(self):
      return self._definition.info()

  @property
  def doc(self):
      try:
         return self._definition.description()
      except AttributeError as e:
         raise Exception("Cannot retrieve documentation") from e

  def help(self):
      print(self.doc)

  def __repr__(self):
      d = self._definition
      out = d.configuration_type_name
      out = out + ' ' + d.name.upper()
      return out
