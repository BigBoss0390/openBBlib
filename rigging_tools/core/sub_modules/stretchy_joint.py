from ..utils import attributes_utils, joints_utils, dag_node, transforms_utils
from . import twist_chain

reload(attributes_utils)
reload(joints_utils)
reload(dag_node)
reload(transforms_utils)
reload(twist_chain)

try:
    from maya import cmds, mel
    from maya.api import OpenMaya as newOM
    from maya import OpenMaya as OM
except ImportError:
    import traceback
    traceback.print_exc()

DEBUG_MODE = True

class StretchyJoint():
    def __init__(
                    self, 
                    name, 
                    start_trf, 
                    end_trf, 
                    up_trf = "", 
                    start_driver = "", 
                    end_driver = "", 
                    up_driver = "",
                    side = "C", 
                    make_twist_chain = False, 
                    numb_twist_jnt = 5, 
                    twist_start_up_vector = "",
                    twist_end_up_vector = "",
                    start_axis_up_vector = [0, 1, 0],
                    start_axis_world_up_vector = [0, 1, 0],
                    end_axis_up_vector = [0, 1, 0],
                    end_axis_world_up_vector = [0, 1, 0],
                    delete_main_trf = False
                ):
        """
        Constructor class

        Args:

        Returns:
      
        """
        self.name = name
        self.start_trf = start_trf
        self.end_trf = end_trf
        self.up_trf = up_trf
        self.start_driver = start_driver
        self.end_driver = end_driver
        self.up_driver = up_driver
        self.side = side
        self.make_twist_chain = make_twist_chain
        self.numb_twist_jnt = numb_twist_jnt
        
        self.twist_start_up_vector = twist_start_up_vector
        self.twist_end_up_vector = twist_end_up_vector

        self.start_axis_up_vector = start_axis_up_vector
        self.start_axis_world_up_vector = start_axis_world_up_vector
        self.end_axis_up_vector = end_axis_up_vector
        self.end_axis_world_up_vector = end_axis_world_up_vector

        self.delete_main_trf = delete_main_trf

        self.start_loc = None
        self.end_loc = None
        self.up_loc = None

        self.start_jnt = None
        self.end_jnt = None

        self.twist_jnts_chain = None
        self.start_twist_grp = None

        self.module_stretchy_objs = []
        self.module_twist_objs = []

        self.main_grp = "{}_{}_stretchySystem_GRP".format(self.side, self.name)

    def stretchy_system(self):
        """
        building up the stretchy system

        Args:

        Returns:
      
        """

        joint_chain = joints_utils.related_clean_joint_chain([self.start_trf, self.end_trf], self.side, self.name, False)
        self.start_jnt = joint_chain[0]
        self.end_jnt = joint_chain[1]

        if DEBUG_MODE:
            print self.start_trf
            print self.end_trf
            print self.start_jnt
            print self.end_jnt

        # re-orient the last joint as his father
        cmds.joint(self.end_jnt, edit=True, orientJoint="none", children=True, zeroScaleOrient=True)

        cmds.joint(self.start_jnt, edit=True, orientJoint="xyz", secondaryAxisOrient="zdown", children=True, zeroScaleOrient=True)
        cmds.joint(self.end_jnt, edit=True, orientJoint="none", children=True, zeroScaleOrient=True)
        
        # start loc
        self.start_loc = cmds.spaceLocator(name="{}_{}_start_LOC".format(self.side, self.name))
        start_loc_offset_grp = transforms_utils.offset_grps_hierarchy(self.start_loc[0])
        transforms_utils.align_objs(self.start_trf, start_loc_offset_grp[0], True, False)
        transforms_utils.align_objs(self.start_jnt, start_loc_offset_grp[0], False, True)

        # end loc
        self.end_loc = cmds.spaceLocator(name="{}_{}_end_LOC".format(self.side, self.name))
        end_loc_offset_grp = transforms_utils.offset_grps_hierarchy(self.end_loc[0])
        transforms_utils.align_objs(self.end_trf, end_loc_offset_grp[0], True, False)
        transforms_utils.align_objs(self.end_jnt, end_loc_offset_grp[0], False, True)

        # up loc
        if self.up_trf == "":
            self.up_loc = cmds.spaceLocator(name="{}_{}_up_LOC".format(self.side, self.name))
            up_loc_offset_grp = transforms_utils.offset_grps_hierarchy(self.up_loc[0])
            transforms_utils.align_objs(self.start_trf, up_loc_offset_grp[0])
            cmds.setAttr("{}.translateY".format(up_loc_offset_grp[1]), 10)
        else:
            self.up_loc = cmds.spaceLocator(name="{}_{}_up_LOC".format(self.side, self.name))
            up_loc_offset_grp = transforms_utils.offset_grps_hierarchy(self.up_loc[0])
            transforms_utils.align_objs(self.up_trf, up_loc_offset_grp[0], True, False)
            transforms_utils.align_objs(self.start_jnt, up_loc_offset_grp[0], False, True)
        
        #Driver connection
        if self.start_driver:
            cmds.parentConstraint(self.start_driver, start_loc_offset_grp[0], maintainOffset=True)
        else:
            cmds.parentConstraint(self.start_trf, start_loc_offset_grp[0], maintainOffset=True)
            
        if self.end_driver:
            cmds.parentConstraint(self.end_driver, end_loc_offset_grp[0], maintainOffset=True)
        else:
            cmds.parentConstraint(self.end_trf, end_loc_offset_grp[0], maintainOffset=True)

        if self.up_driver:
            cmds.parentConstraint(self.up_driver, up_loc_offset_grp[0], maintainOffset=True)
        else:
            if self.up_trf == "" or self.up_trf == None:
                cmds.parentConstraint(self.start_loc, up_loc_offset_grp[0], maintainOffset=True)
            else:
                cmds.parentConstraint(self.up_trf, up_loc_offset_grp[0], maintainOffset=True)

        
        self.module_stretchy_objs.extend([self.start_jnt, start_loc_offset_grp[0], end_loc_offset_grp[0], up_loc_offset_grp[0]])

        # building Ik system
        ik_handle_stretchy = cmds.ikHandle(name="{}_{}_stretchy_IKH".format(self.side, self.name), solver="ikRPsolver", startJoint=self.start_jnt, endEffector=self.end_jnt)
        cmds.poleVectorConstraint(self.up_loc, ik_handle_stretchy[0])
        cmds.parentConstraint(self.start_loc, self.start_jnt, maintainOffset=True)
        cmds.parentConstraint(self.end_loc, ik_handle_stretchy[0], maintainOffset=True)

        self.module_stretchy_objs.append(ik_handle_stretchy[0])

        # building the stretchy behaviour
        distance_node = cmds.createNode("distanceBetween", name="{}_{}_dsb".format(self.side, self.name))
        cmds.connectAttr("{}Shape.worldPosition[0]".format(self.start_loc[0]), "{}.point1".format(distance_node), force=True)
        cmds.connectAttr("{}Shape.worldPosition[0]".format(self.end_loc[0]), "{}.point2".format(distance_node), force=True)

        # self.module_stretchy_objs.append(distance_node)

        stretchy_mld_node = cmds.createNode("multiplyDivide", name="{}_{}_mld".format(self.side, self.name))
        cmds.setAttr("{}.operation".format(stretchy_mld_node), 2)
        self.module_stretchy_objs.append(stretchy_mld_node)
        
        cmds.connectAttr("{}.distance".format(distance_node), "{}.input1X".format(stretchy_mld_node), force=True)
        actual_distance_attr = "actualDistanceValue"
        attributes_utils.add_float_attr(self.start_jnt, actual_distance_attr)
        start_distance_attr = "startDistanceValue"
        attributes_utils.add_float_attr(self.start_jnt, start_distance_attr)

        cmds.connectAttr("{}.distance".format(distance_node), "{}.{}".format(self.start_jnt, actual_distance_attr), force=True)
        cmds.connectAttr("{}.distance".format(distance_node), "{}.{}".format(self.start_jnt, start_distance_attr), force=True)
        cmds.disconnectAttr("{}.distance".format(distance_node), "{}.{}".format(self.start_jnt, start_distance_attr))

        cmds.connectAttr("{}.{}".format(self.start_jnt, start_distance_attr), "{}.input2X".format(stretchy_mld_node), force=True)
        cmds.connectAttr("{}.outputX".format(stretchy_mld_node), "{}.scaleX".format(self.start_jnt), force=True)

        # clean scene
        if self.delete_main_trf:
            if self.up_trf == "":
                cmds.delete([self.start_trf, self.end_trf])
            else:
                cmds.delete([self.start_trf, self.end_trf, self.up_trf])
        
        stretchy_grp = cmds.group(self.module_stretchy_objs, name="{}_{}_stretchy_GRP".format(self.side, self.name))
        # cmds.setAttr("{}.visibility".format(stretchy_grp), 0)
        self.module_main_grp(stretchy_grp)

        return True

    def twist_chain(self):
        """
        building up a twist chain of joints between the start and the end joint of the stretchy system

        Args:

        Returns:

        """
        name_bit_twist_system = self.start_jnt[2 : len(self.start_jnt)-4]
        stretchy_twist = twist_chain.TwistChain(
                                                    "{}_{}_stretchy".format(self.name, name_bit_twist_system),
                                                    self.start_jnt,
                                                    self.end_jnt,
                                                    self.side,
                                                    self.numb_twist_jnt,
                                                    self.twist_start_up_vector,
                                                    self.twist_end_up_vector,
                                                    self.start_axis_up_vector,
                                                    self.start_axis_world_up_vector,
                                                    self.end_axis_up_vector,
                                                    self.end_axis_world_up_vector
                                                )
        stretchy_twist.run()

        return True

    def module_main_grp(self, list_objs):
        """
        building up the main group for the sub-module which will contain all the parts built before

        Args:

        Returns:
        
        """
        if cmds.objExists(self.main_grp):
            cmds.parent(list_objs, self.main_grp)
        else:
            cmds.group(list_objs, name=self.main_grp)

        cmds.setAttr("{}.visibility".format(self.main_grp), 0)
        
        return self.main_grp 

    def run(self):
        """
        Method that run the entire more for building up it

        Args:

        Returns:
      
        """
        if self.make_twist_chain:
            print("###--- Module StretchyJoint --- TwistChain --- START ---###")
        else:
            print("###--- Module StretchyJoint --- START ---###")

        self.stretchy_system()

        if self.make_twist_chain:
            self.twist_chain()

        # Temporary stuff
        master_grp = "stretchySystems_GRP"
        if not cmds.objExists(master_grp):
            cmds.group(empty=True, name=master_grp)
            cmds.parent(self.main_grp, master_grp)
        else:
            cmds.parent(self.main_grp, master_grp)
        
        try:
            if cmds.objExists("rig_GRP"):
                cmds.parent(master_grp, "rig_GRP")
        except:
            print "{} already child of rig_GRP".format(master_grp)

        return [self.start_jnt, self.end_jnt]

    def get_name(self):
        """
        function for retrieving the name of the limb

        Args:

        Returns:
        
        """
        return self.name
        
    def get_side(self):
        """
        function for retrieving the side of the limb

        Args:

        Returns:
        
        """
        return self.side
        
    def get_start_trf(self):
        """
        function for retrieving the main_chain which are used for building the module

        Args:

        Returns:
        
        """
        return self.start_trf

    def get_end_trf(self):
        """
        function for retrieving the children/obj constrained to the root joint of the module

        Args:

        Returns:
        
        """
        return self.end_trf

    def get_up_trf(self):
        """
        function for retrieving the children/obj constrained to the root joint of the module

        Args:

        Returns:
        
        """
        return self.up_trf

    def set_name(self, name):
        """
        function for set the name of the limb

        Args:

        Returns:
        
        """
        self.name = name
        return self.name
        
    def set_side(self, side):
        """
        function for set the side of the limb

        Args:

        Returns:
        
        """
        self.side = side
        return self.side

    def set_start_trf(self, transform):
        """
        function for set the children/obj constrained to the root joint of the module

        Args:

        Returns:
        
        """
        self.start_trf = transform 
        return self.start_trf

    def set_end_trf(self, transform):
        """
        function for set the children/obj constrained to the end joint of the module

        Args:

        Returns:
        
        """
        self.end_trf = transform
        return self.end_trf

    def set_up_trf(self, transform):
        """
        function for set the children/obj constrained to the end joint of the module

        Args:

        Returns:
        
        """
        self.up_trf = transform
        return self.up_trf
