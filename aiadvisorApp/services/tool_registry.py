from .tools.greenhouse_tool import GreenhouseTool
from .tools.harvest_tool import HarvestTool
from .tools.general_agriculture_tool import GeneralAgricultureTool
from .tools.analysis_tool import AnalysisTool
from .tools.crop_tool import CropTool
from .tools.greenhouse_crop_tool import GreenhouseCropTool

class ToolRegistry:

    TOOLS = {
        "analysis": AnalysisTool,
        "crop": CropTool,

        "general": GeneralAgricultureTool,
        "greenhouse_crop": GreenhouseCropTool,

        "greenhouse": GreenhouseTool,

        "harvest": HarvestTool,
        }

    @classmethod
    def get_tool(cls, intent):
        return cls.TOOLS.get(intent, GeneralAgricultureTool)