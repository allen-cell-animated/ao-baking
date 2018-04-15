import c4d
import upy
import os
import time
import thread
from c4d import utils

from upy import uiadaptor

upy.setUIClass()

# get the helperClass for modeling
helperClass = upy.getHelperClass()

from c4d import documents, plugins
#Welcome to the world of Python
#1: cell membrane
#2: dna
#3: structure
settings = [
    None,
    {
        'polygonReduction': .99,
        'smoothStrength': 1.0,

    },
    {
        'polygonReduction': .95,
        'smoothStrength': 1.0,

    },
    {
        'polygonReduction': .90,
        'smoothStrength': 0.2,
    },
]

inputStructures = [
    "ACTB",
    "ACTN1",
    "CENT2",
    "DSP",
    "FBL",
    "LAMP1",
    "LMNB1",
    "MYH10",
    "PMP34",
    "SEC61B",
    "ST6GAL1",
    "TJP1",
    "TOMM20",
    "TUBA1B"
]
inputStages = [
    'Int',
    'M1',
    'M3',
    'M5',
    'M6',
    'M7'
]

outputStructures = {
    "ACTB": "actin-filaments",
    "ACTN1": "sarcomeres",
    "CENT2": "centrosomes",
    "DSP": "desomsomes",
    "FBL": "nucleoli",
    "LAMP1": "lysosomes",
    "LMNB1": "nuclear-envelope",
    "MYH10": "actomyosin-bundles",
    "PMP34": "peroxisomes",
    "SEC61B": "endoplasmic-recticulum",
    "ST6GAL1": "golgi-apparatus",
    "TJP1": "tight-junctions",
    "TOMM20": "mitochondria",
    "TUBA1B": "microtubules",
}

outputStages = {
    "Int": "interphase",
    "M1": "prophase",
    "M3": "prometaphase",
    "M5": "metaphase",
    "M6": "anaphase",
    "M7": "cytokinesis-telophase"
}

inputfilenames = ['%s-%s' % (x,y) for x in inputStructures for y in inputStages]

# add to this list to process a cell.
#inputfilenames = [
  # 'TOMM20-Int',
  # 'TOMM20-M7',
  # 'TUBA1B-Int',
  # 'SEC61B-M3',
  # 'SEC61B-M6',
  # 'LMNB1-M1',
  # 'ACTB-Int',
  # 'ACTB-M1',
  # 'ACTB-M5',
  # 'DSP-M1',
  # 'DSP-M3',
  # 'DSP-M6',
  # 'FBL-Int',
  # 'FBL-M3',
  # 'FBL-M5',
  # 'FBL-M6',
  # 'FBL-M7',
  # 'TJP1-Int',
  # 'TJP1-M1',
  # 'TJP1-M3',
  # 'TJP1-M6',
  # 'LAMP1-M3',
  # 'LAMP1-M6',
  # 'SEC61B-M5',
  # 'SEC61B-M7',
  # 'SEC61B-M6',
  # 'TOMM20-M1'
  # 'ST6GAL1-M5',
  # 'ST6GAL1-M6',
  # 'SEC61B-M6',
                  #  'TUBA1B-M1',
                  #  'TUBA1B-M3',
                  #   'TUBA1B-M5',
                  # 'TUBA1B-M6',
                  #  'TUBA1B-M7'
#]

print("inputfilenames = ", inputfilenames)
#loadpath = "/Users/meganr/Dropbox/visual_cell_maker_files/objs-to-process"
#outputBasePath = "/Users/meganr/Dropbox/Structures_for_Visual_Cell"
#loadpath = "/Users/grahamj/Desktop/ao-baking-master/Input-OBJs"
loadpath = "/Volumes/aics/animated-cell/Allen-Cell-Explorer/3d-Vis-Summary-data_1.0.1/objs-to-process"
outputBasePath = "/Volumes/aics/animated-cell/Allen-Cell-Explorer/3d-Vis-Summary-data_1.0.1/Structures_for_Visual_Cell"

fileNames = [None, 'membrane', 'nucleus', 'structure']
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

class BakeOneObj:
    def __init__(self, outputbmp, outputfilepath):
        self.outputbmp = outputbmp
        self.outputfilepath = outputfilepath
        self.done = False

    def onbakeprogress(self, dict):
        state = dict['state']
        if state == c4d.BAKE_STATE_COMPLETE:
            print("bake done " + self.outputfilepath)
            self.outputbmp.Save( self.outputfilepath, c4d.FILTER_JPG)
            self.done = True

    def wait(self):
        while(self.done == False):
            time.sleep(4)
            c4d.EventAdd()


def do_one_file(inputfile):
    helper = helperClass()

    inputStructure = inputfile.split('-')[0]
    inputStage = inputfile.split('-')[1]
    print('inputStructure ' + inputStructure)
    print('inputStage ' + inputStage)

    outputDirectory = os.path.join(outputBasePath, outputStructures[inputStructure], outputStages[inputStage])
    print(outputDirectory)
    inputfile = inputfile + '.obj'

    c4d.documents.LoadFile(os.path.join(current_dir, 'base-visual-cell-maker-file_2.c4d'))
    doc = helper.getCurrentScene()

    filename = inputfile
    file_to_load = os.path.join(loadpath, filename)

    # Import without dialogs
    c4d.documents.MergeDocument(doc, file_to_load, c4d.SCENEFILTER_OBJECTS, None)
    c4d.EventAdd()

    # get the main object
    target_obj = helper.getObject(filename)
    print(target_obj.GetName())


    tp = target_obj.GetDown()
    while tp is not None:
        print("tp name = ", tp.GetName())
        i = int(tp.GetName()[-1])
        doc.SetSelection(tp)

        # getting rid of tags that came from chimera
        tp.KillTag(c4d.Tnormal)
        tp.KillTag(c4d.Ttexture)
        tp.KillTag(c4d.Tphong)
        tp.MakeTag(c4d.Tphong)

        c4d.CallCommand(14039, 14039) # Optimize
        c4d.CallCommand(14039, 14039) # Optimize

        # doc.InsertObject(smoothing_deformer)
#        reducer = c4d.BaseObject(1001253) # Polgyon reduction
#        reducer[c4d.POLYREDUCTIONOBJECT_STRENGTH] = settings[i]['polygonReduction']
#        helper.setName(reducer, "Polygon_Reduction_"+tp.GetName())
#        helper.AddObject(reducer, parent=tp)

#     displacer = helper.getObject("displacer_" + str(i))
#       helper.reParent(displacer, tp)
        if i == 1:
            CellMembraneHolster = helper.getObject("Holster_1")
            while CellMembraneHolster.GetDown() is not None: # tp is not None:
                helper.reParent(CellMembraneHolster.GetDown(), tp)
        if i == 2:
            DNAHolster = helper.getObject("Holster_2")
            while DNAHolster.GetDown() is not None: # tp is not None:
                helper.reParent(DNAHolster.GetDown(), tp)
        if i == 3:
            StructureHolster = helper.getObject("Holster_3")
            while StructureHolster.GetDown() is not None: # tp is not None:
                helper.reParent(StructureHolster.GetDown(), tp)

#        smoothing_deformer = c4d.BaseObject(1024529) # smoothing deformer
#        smoothing_deformer[c4d.ID_CA_SMOOTHING_DEFORMER_OBJECT_STRENGTH] = settings[i]['smoothStrength']
#        helper.setName(smoothing_deformer, "Smoothing_"+tp.GetName())
#        helper.AddObject(smoothing_deformer, parent=tp)

        tp = tp.GetNext()

    res = utils.SendModelingCommand(command = c4d.MCOMMAND_CURRENTSTATETOOBJECT,
                                list = [target_obj],
                                doc = doc,
                                # flags = c4d.MODELINGCOMMANDFLAGS_CREATEUNDO
                                )
    res = res[0]
    helper.setName(res, helper.getName(res) + '_reduced')
    print("created reduced object")
    helper.AddObject(res)

    doc.SetSelection(target_obj)
    target_obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1
    c4d.EventAdd()

    # return

#   c4d.documents.SaveDocument(doc, os.path.join(current_dir, 'gj.c4d'), c4d.SAVEDOCUMENTFLAGS_0, c4d.FORMAT_C4DEXPORT)
    c4d.documents.SaveDocument(doc, os.path.join(outputDirectory, inputStructure + '_prebake' + '.c4d'), c4d.SAVEDOCUMENTFLAGS_0, c4d.FORMAT_C4DEXPORT)


    print("deleting original target object")
    target_obj.Remove()
    c4d.EventAdd()

    material = doc.GetFirstMaterial()
    tp = res.GetDown()

    # enter polygon edit mode
    c4d.CallCommand(12187) # Polygons

    while tp is not None:
        print("make texture tag")
        texture = tp.MakeTag(c4d.Ttexture)
        texture[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_SPHERICAL
        texture[c4d.TEXTURETAG_MATERIAL] = material

        doc.SetSelection(texture)

        # makes a uvw tag on the object
        c4d.CallCommand(12235, 12235) # Generate UVW Coordinates
        print("generate uvw coords")
        doc.SetSelection(tp.GetTag(c4d.Tuvw))

        uvsettings = c4d.BaseContainer()
        uvsettings.SetBool(c4d.OPTIMALMAPPING_PRESERVEORIENTATION, False)
        uvsettings.SetBool(c4d.OPTIMALMAPPING_STRETCHTOFIT, True)
        uvsettings.SetFloat(c4d.OPTIMALMAPPING_DISTORTION, 0.01)
        uvsettings.SetInt32(c4d.OPTIMALMAPPING_RELAXCOUNT, 0)
        uvsettings.SetFloat(c4d.OPTIMALMAPPING_SPACING, 0.01)

        print("get active uv set")

        uvset = c4d.modules.bodypaint.GetActiveUVSet(doc, c4d.GETACTIVEUVSET_ALL)

        uvw = uvset.GetUVW()

      #  if tp.GetName()[-2:] == '_2': #switch these ifs for expensive structures during debugging
        if 1 == 1:
            uv_ok = c4d.modules.bodypaint.CallUVCommand(uvset.GetPoints(),
                uvset.GetPointCount(),
                uvset.GetPolys(),
                uvset.GetPolyCount(),
                uvw,
                uvset.GetPolySel(),
                uvset.GetUVPointSel(),
                tp, c4d.Mpolygons, c4d.UVCOMMAND_OPTIMALMAPPING, uvsettings)
            print("call uv command:", uv_ok)

        uvset.SetUVWFromTextureView(uvw, True, True, True)
        c4d.modules.bodypaint.FreeActiveUVSet(uvset)

        tp = tp.GetNext()


    subdiv = helper.getObject("Subdivision Surface")


    tp = res.GetDown()
    i = 0
    membraneobj = None
    while i < 3:
        if tp.GetName()[-2:] == '_1':
            membraneobj = tp
            break
        tp = tp.GetNext()
        i = i + 1

    children = []
    tp = res.GetDown()
    while tp is not None: # tp is not None:
        children.append(tp)
        tp = tp.GetNext()

    for tp in children: # tp is not None:
        if tp.GetName() == membraneobj.GetName():
            # switch object on
            membraneobj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER]=2
        else:
            # switch object off
            membraneobj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER]=1

        if tp.GetName()[-2:] != '_2': # do not subdivide the nucleus before baking
            print("reparent to subdiv for baking")
            helper.reParent(tp, subdiv)


        bake = c4d.BaseContainer()
        bake.SetBool(c4d.BAKE_TEX_AMBIENT_OCCLUSION, True)
        bake.SetInt32(c4d.BAKE_TEX_WIDTH, 1024)
        bake.SetInt32(c4d.BAKE_TEX_HEIGHT, 1024)
        bake.SetInt32(c4d.BAKE_TEX_PIXELBORDER, 3)
        bake.SetInt32(c4d.BAKE_TEX_SUPERSAMPLING, 0)
        (bakedoc, result) = c4d.utils.InitBakeTexture(doc, tp.GetTag(c4d.Ttexture), tp.GetTag(c4d.Tuvw), None, bake)
        if result != c4d.BAKE_TEX_ERR_NONE:
            print("InitBakeTexture error")
        else:
            output_bmp = c4d.bitmaps.MultipassBitmap(1024, 1024, c4d.COLORMODE_ARGB)
            bakeobj = BakeOneObj(output_bmp, os.path.join(outputDirectory, fileNames[int(tp.GetName()[-1:])] + '_ao.jpg'))
            print("BakeTexture " + fileNames[int(tp.GetName()[-1:])])
            c4d.utils.BakeTexture(bakedoc, bake, output_bmp, None, bakeobj.onbakeprogress)
            bakeobj.wait()
            print("done baking, reparenting to done")
            helper.reParent(tp, helper.getObject('done'))

        c4d.EventAdd()

        # print(fileNames[int(tp.GetName()[-1:])] + '_ao')

        # print("reparent to done")
        # helper.reParent(tp, res)


    # done with "res" since everything is reparented to "done"
    doc.SetSelection(res)
    res[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1
    c4d.EventAdd()
    res.Remove()
    c4d.EventAdd()

    tp = helper.getObject('done').GetDown()
    # while tp is not None: # tp is not None:
    for tp in children:
        # rotate by 90 degrees
        tp.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), 0))
        newdoc = c4d.documents.IsolateObjects(doc, [tp])
        c4d.documents.SaveDocument(newdoc, os.path.join(outputDirectory, fileNames[int(tp.GetName()[-1:])] + '.obj'), c4d.SAVEDOCUMENTFLAGS_0, c4d.FORMAT_OBJ2EXPORT)
        print(fileNames[int(tp.GetName()[-1:])] + '.obj')
        c4d.EventAdd()
        c4d.documents.KillDocument(newdoc)
        c4d.EventAdd()

    doc.SetDocumentName('tmp')
    c4d.documents.SaveDocument(doc, os.path.join(current_dir, 'tmp.c4d'), c4d.SAVEDOCUMENTFLAGS_0, c4d.FORMAT_C4DEXPORT)
    c4d.EventAdd()
    c4d.documents.KillDocument(doc)
    c4d.documents.CloseAllDocuments()

def main():
    # Get OBJ import plugin, 1030177 is its ID
    plug = plugins.FindPlugin(1030177, c4d.PLUGINTYPE_SCENELOADER)
    if plug is None:
        print("fatal error can't find obj import plugin")
        return

    ischecked = c4d.IsCommandChecked(170009)
    print("showuvmesh checked:", ischecked)
    if ischecked == False:
        c4d.CallCommand(170009, 170009) # Show UV Mesh
    for structure in inputfilenames:
        do_one_file(structure)
        print("structure = ", structure)

if __name__=='__main__':
    main()
    c4d.EventAdd()
