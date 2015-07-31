# Procurement Charts - domain calculations
# -*- coding: latin-1 -*-


def min_max(domain, slice_domain):
  """
  Updates the minimum and maximum value of a domain. Used to define a domain
  for a group of slices.

  :param domain:
    List with values
  :type domain:
    List
  :param slice_domain:
    The domain of the current slice
  :type current_domain:
    List

  :returns:
    List with updated domain
  """

  domain[0] = min(domain[0], slice_domain[0])
  domain[-1] = max(domain[-1], slice_domain[-1])
  
  return domain


def no_update(domain, current_slice):
  """
  This simply returns the domain without updating.
  Used when the domain is the same across slices (eg. list of dates)

  :param domain:
    List with values
  :type domain:
    List

  :returns:
    List with original domain
  """
  return domain