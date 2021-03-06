#pragma once

#include <maya/MPxCommand.h>
#include <maya/MGlobal.h>
#include <maya/MObject.h>

class SampleCmd : public MPxCommand
{
	public:
		SampleCmd();
		virtual MStatus doIt(const MArgList& argList);
		static void* creator();
};
