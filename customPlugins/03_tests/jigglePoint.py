import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math
VERSION = '1.0'

## @brief A node that triggers shapes from of an orientation
class JigglePoint(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00001234)

    aOutput = OpenMaya.MObject()
    aTime = OpenMaya.MObject()
    aJiggleAmount = OpenMaya.MObject()
    aDamping = OpenMaya.MObject()
    aStiffness = OpenMaya.MObject()
    aParentInverse = OpenMaya.MObject()
    aGoal = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        self._initialized = False
        self._currentPosition = OpenMaya.MPoint()
        self._previousPosition = OpenMaya.MPoint()
        self._previousTime = OpenMaya.MTime()


    def compute(self, plug, data):
        if plug != JigglePoint.aOutput:
            return OpenMaya.kUnknownParameter

        # Get the inputs
        damping = data.inputValue(self.aDamping).asFloat()
        stiffness = data.inputValue(self.aStiffness).asFloat()
        goal = OpenMaya.MPoint(data.inputValue(self.aGoal).asFloatVector())
        parentInverse = data.inputValue(self.aParentInverse).asMatrix()
        currentTime = data.inputValue(self.aTime).asTime()
        jiggleAmount = data.inputValue(self.aJiggleAmount).asFloat()

        # Initialize the data
        if not self._initialized:
            self._previousTime = currentTime
            self._currentPosition = goal
            self._previousPosition = goal
            self._initialized = True

        # Check if the timestep is just 1 frame since we want a stable simulation
        timeDifference = currentTime.value() - self._previousTime.value()
        if timeDifference > 1.0 or timeDifference < 0.0:
            self._initialized = False
            self._previousTime = currentTime
            return

        # Calculate the output position
        #stiffness *= 1.0 - jiggleAmount
        #damping *= jiggleAmount
        #if damping > 1.0:
        #    damping = 1.0
        #if stiffness > 1.0:
        #    stiffness = 1.0
        #if stiffness <= 0.0:
        #    stiffness = 0.001
        velocity = (self._currentPosition - self._previousPosition) * (1.0 - damping)
        newPosition = self._currentPosition + velocity
        goalForce = (goal - newPosition) * stiffness
        newPosition += goalForce

        # Store the states for the next computation
        self._previousPosition = OpenMaya.MPoint(self._currentPosition)
        self._currentPosition = OpenMaya.MPoint(newPosition)
        self._previousTime = OpenMaya.MTime(currentTime)

        newPosition = goal + ((newPosition - goal) * jiggleAmount)

        # Put in the output local space
        newPosition *= parentInverse

        hOutput = data.outputValue(JigglePoint.aOutput)
        outVector = OpenMaya.MFloatVector(newPosition.x, newPosition.y, newPosition.z)
        hOutput.setMFloatVector(outVector)
        hOutput.setClean()
        data.setClean(plug)


## @brief Creates the object for Maya.
def creator():
    return OpenMayaMPx.asMPxPtr(JigglePoint())


## @brief Creates the node attributes.
#
def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()
    uAttr = OpenMaya.MFnUnitAttribute()

    JigglePoint.aOutput = nAttr.createPoint('output', 'out')
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    JigglePoint.addAttribute(JigglePoint.aOutput)

    JigglePoint.aGoal = nAttr.createPoint('goal', 'goal')
    JigglePoint.addAttribute(JigglePoint.aGoal)
    JigglePoint.attributeAffects(JigglePoint.aGoal, JigglePoint.aOutput)

    JigglePoint.aTime = uAttr.create('time', 'time', OpenMaya.MFnUnitAttribute.kTime, 0.0)
    JigglePoint.addAttribute(JigglePoint.aTime)
    JigglePoint.attributeAffects(JigglePoint.aTime, JigglePoint.aOutput)

    JigglePoint.aJiggleAmount = nAttr.create('jiggle', 'jiggle', OpenMaya.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    JigglePoint.addAttribute(JigglePoint.aJiggleAmount)
    JigglePoint.attributeAffects(JigglePoint.aJiggleAmount, JigglePoint.aOutput)

    JigglePoint.aStiffness = nAttr.create('stiffness', 'stiffness', OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    JigglePoint.addAttribute(JigglePoint.aStiffness)
    JigglePoint.attributeAffects(JigglePoint.aStiffness, JigglePoint.aOutput)

    JigglePoint.aDamping = nAttr.create('damping', 'damping', OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    JigglePoint.addAttribute(JigglePoint.aDamping)
    JigglePoint.attributeAffects(JigglePoint.aDamping, JigglePoint.aOutput)

    JigglePoint.aParentInverse = mAttr.create('parentInverse', 'parentInverse')
    JigglePoint.addAttribute(JigglePoint.aParentInverse)


## @brief Initializes the plug-in in Maya.
#
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Chad Vernon', VERSION, 'Any')
    plugin.registerNode('jigglePoint', JigglePoint.kPluginNodeId, creator, initialize)


## @brief Uninitializes the plug-in in Maya.
#
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    plugin.deregisterNode(JigglePoint.kPluginNodeId)

