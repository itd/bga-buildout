from Products.CMFCore.utils import getToolByName


def getMembers(self):
  retval = ''
  context = getToolByName(self, 'portal_url').getPortalObject()
  passwords = context.acl_users.source_users._user_passwords
  for member in context.portal_membership.listMembers():
    uname = member.getProperty('id')
    pas = passwords.get(uname)
    email = member.getProperty('email')
    fn =  member.getProperty('fullname')
    add =  member.getProperty('address')
    city =  member.getProperty('city')
    st =  member.getProperty('state')
    zp =  member.getProperty('zip')
    ph =  member.getProperty('phone')
    retval+= "%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (uname,pas,email,fn,add,city,st,zp,ph)
  return retval
