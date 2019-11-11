/*
Copyright (c) 2012 Chad Vernon

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
#ifndef CVJIGGLE_CVJIGGLECMD_H
#define CVJIGGLE_CVJIGGLECMD_H

#include <maya/MSelectionList.h>
#include <maya/MPointArray.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MString.h>
#include <maya/MStringArray.h>
#include <maya/MGlobal.h>
#include <maya/MSyntax.h>
#include <maya/MString.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>
#include <maya/MObject.h>
#include <maya/MObjectArray.h>
#include <maya/MDGModifier.h>

#include <maya/MItDependencyGraph.h>
#include <maya/MItGeometry.h>
#include <maya/MItSelectionList.h>

#include <maya/MFnDagNode.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnMesh.h>
#include <maya/MFnTransform.h>
#include <maya/MPxCommand.h>

#include <vector>
#include <sstream>


class cvJiggleCmd : public MPxCommand  {              
 public:                              
  cvJiggleCmd();
  virtual ~cvJiggleCmd();
  virtual MStatus doIt(const MArgList& argList);
  virtual MStatus redoIt();
  virtual MStatus undoIt();
  virtual bool isUndoable() const;
  static void* creator();
  static MSyntax newSyntax();

  static const char* kNameShort;
  static const char* kNameLong;
  static const char* kDampingShort;
  static const char* kDampingLong;
  static const char* kStiffnessShort;
  static const char* kStiffnessLong;

 private:
  MStatus GetShapeNode(MDagPath& path);
  MStatus GetJiggleDeformer(MDagPath& pathGeo, MObject& oDeformer);
  MDGModifier dgMod_;
  MString name_;
  MSelectionList selection_;
  float damping_;
  float stiffness_;
};  

#endif
