try:
    from maya import cmds, mel
    from maya.api import OpenMaya as OM
except ImportError:
    import traceback
    traceback.print_exc()

DEBUG_MODE = True

def add_separator(obj, name_sep="attributes", by_name=False):
    """
    Args:

    Returns:
    
    """
    if not by_name:
        cmds.addAttr(obj, longName=name_sep, attributeType='enum', enumName="------------:")
        cmds.setAttr("{}.{}".format(obj, name_sep), channelBox=True, keyable=False)
    else:
        cmds.addAttr(obj, longName=name_sep, attributeType='enum', enumName="------------:")
        cmds.setAttr("{}.{}".format(obj, name_sep), channelBox=True, keyable=False)

# vector attr
def add_vector_attr(obj, name_attr, keyable=True, lock=False):
    """
    Args:

    Returns:
    
    """
    if name_attr != None:
        # adding the attribute
        cmds.addAttr(obj, longName=name_attr, attributeType='double3')
        cmds.addAttr(obj, longName=name_attr+"X", attributeType='double', parent=name_attr)
        cmds.addAttr(obj, longName=name_attr+"Y", attributeType='double', parent=name_attr)
        cmds.addAttr(obj, longName=name_attr+"Z", attributeType='double', parent=name_attr)
        # set the attributes just added
        cmds.setAttr("{}.{}X".format(obj, name_attr), keyable=keyable, lock=lock)
        cmds.setAttr("{}.{}Y".format(obj, name_attr), keyable=keyable, lock=lock)
        cmds.setAttr("{}.{}Z".format(obj, name_attr), keyable=keyable, lock=lock)
    else:
        cmds.warning("You should declare a #--- Name ---# for the attribute you want to add")

    
# integer attr   
def add_integer_attr(obj, name_attr, min_val=None, max_val=None, def_val=0, keyable=True, lock=False):
    """
    Args:

    Returns:
    
    """
    if name_attr != None:
        if min_val != None and max_val != None:
            if min_val > def_val or max_val < def_val:
                cmds.warning("MinumValue or MaximumValue are not compatible with DefaultValue which is set as default to 0, change them or give to the DefaultValue another number")
            else:
                cmds.addAttr(obj, longName=name_attr, attributeType='long', minValue=min_val, maxValue=max_val, defaultValue=def_val)
                cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
        else:
            cmds.addAttr(obj, longName=name_attr, attributeType='long', defaultValue=def_val)
            cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
    else:
        cmds.warning("You should declare a #--- Name ---# for the attribute you want to add")        

# string attr    
def add_string_attr(obj, name_attr, keyable=True, lock=False):
    """
    Args:

    Returns:
    
    """
    if name_attr != None:
        cmds.addAttr(obj, longName=name_attr, attributeType='string')
        cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
    else:
        cmds.warning("You should declare a #--- Name ---# for the attribute you want to add") 
                
# float attr    
def add_float_attr(obj, name_attr, min_val=None, max_val=None, def_val=0, keyable=True, lock=False):
    """
    Args:

    Returns:
    
    """  
    if name_attr != None:
        if min_val != None and max_val != None:
            if min_val > def_val:
                cmds.warning("MinumValue or MaximumValue are not compatible with DefaultValue which is set as default to 0, change them or give to the DefaultValue another number")
            elif max_val < def_val:
                cmds.warning("MinumValue or MaximumValue are not compatible with DefaultValue which is set as default to 0, change them or give to the DefaultValue another number")
            else:
                cmds.addAttr(obj, longName=name_attr, attributeType='double', minValue=min_val, maxValue=max_val, defaultValue=def_val)
                cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
        elif min_val != None and max_val == None:
            if min_val > def_val:
                cmds.warning("MinumValue not compatible with DefaultValue which is set as default to 0, change them or give to the DefaultValue another number")
            else:
                cmds.addAttr(obj, longName=name_attr, attributeType='double', minValue=min_val, defaultValue=def_val)
                cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
        elif min_val == None and max_val != None:
            if max_val < def_val:
                cmds.warning("MaximumValue not compatible with DefaultValue which is set as default to 0, change them or give to the DefaultValue another number")
            else:
                cmds.addAttr(obj, longName=name_attr, attributeType='double', maxValue=max_val, defaultValue=def_val)
                cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
        else:
            cmds.addAttr(obj, longName=name_attr, attributeType='double', defaultValue=def_val)
            cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
    else:
        cmds.warning("You should declare a #--- Name ---# for the attribute you want to add") 

# boolean attr   
def add_boolean_attr(obj, name_attr, keyable=True, lock=False):
    """
    Args:

    Returns:
    
    """
    if name_attr != None:
        cmds.addAttr(obj, longName=name_attr, attributeType='bool')
        cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
    else:
        cmds.warning("You should declare a #--- Name ---# for the attribute you want to add")
            
# enum attr    
def add_enum_attr(obj, name_attr, enum_values, keyable=True, lock=False):
    """
    Args:

    Returns:
    
    """
    if name_attr != None:
        if enum_values != None or enum_values != '':
            cmds.addAttr(obj, longName=name_attr, attributeType='enum', enumName=enum_values)
            cmds.setAttr("{}.{}".format(obj, name_attr), keyable=keyable, lock=lock)
        else:
            cmds.warning("You should declare the enum values you want to put inside the attribute")
    else:
        cmds.warning("You should declare a #--- Name ---# for the attribute you want to add")
'''
def add_attribute(
                obj, 
                name_attr, 
                attr_type, 
                def_val=0, 
                enum_val=None, 
                min_val=None, 
                max_val=None, 
                keyable=True, 
                lock=False
                ):
    """
    Args:

    Returns:
    
    """                
    switcher =  {
                'vector' : add_vector_attr(obj, name_attr, keyable, lock),
                'integer' : add_integer_attr(obj, name_attr, def_val, min_val, max_val, keyable, lock),
                'string' : add_string_attr(obj, name_attr, keyable, lock),
                'float' : add_float_attr(obj, name_attr, min_val, max_val, def_val, keyable, lock),
                'bool' : add_boolean_attr(obj, name_attr, keyable, lock),
                'enum' : add_enum_attr(obj, name_attr, enum_val, keyable, lock)
                }
    func = switcher.get(attr_type, 'Invalid type of attribute')
    return func()
'''
