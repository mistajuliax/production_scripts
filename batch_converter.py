import bpy
from os import listdir
from os.path import join, isdir, isfile

tifDir = "C:/Users/TLOUSKY/Google Drive/PlatFORM/PQ_shades_app/FaceModels/images/depth"
pngDir = "C:/Users/TLOUSKY/Google Drive/PlatFORM/PQ_shades_app/FaceModels/images/depth/png"

class match_rotation(bpy.types.Operator):
    bl_idname      = "render.batch_convert"
    bl_label       = "Batch Convert"
    bl_description = "Batch convert source images to destination format"
    bl_options     = {'REGISTER', 'UNDO'}

    @classmethod
    def poll( self, context ):
        ''' Make sure both source and destination folders are valid '''
        props = context.scene.batch_convertor_properties
        sourceDirValid      = isdir( props.source_folder )
        destinationDirValid = isdir( props.destination_folder )
        return sourceDirValid and destinationDirValid

    def execute(self, context):
        C = bpy.context
        S = C.scene
        props = context.scene.batch_convertor_properties

        S.use_nodes = True
        t = S.node_tree

        # Clear node tree
        for n in t.nodes:
            t.nodes.remove( n )

        # Generate nodes
        for ntype in [ 'CompositorNodeImage', 'CompositorNodeComposite' ]:
            t.nodes.new( ntype )

        imgNode = t.nodes["Image"]
        img = t.nodes["Image"].image

        # Connect nodes


        source     = props.source_folder
        sourceImgs = [
            f for f in listdir( source ) if isfile( join( source, f ) )
        ]

        extension = S.render.file_extension

        destination = props.source_folder
        for f in sourceImgs:
            img.filepath      = join( source, f )
            S.render.filepath = join( destination, f[:-4] + extension )
            bpy.ops.render.render( write_still = True )

        return {'FINISHED'}

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label       = "Layout Demo"
    bl_idname      = "SCENE_PT_layout"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "scene"

    def draw(self, context):
        layout = self.layout
        col    = layout.column()

        S = context.scene
        P = S.batch_convertor_properties

        b  = col.box()
        bc = b.column()

        bc.label(
            text = "Warning: pressing 'Batch Convert'\nwill replace your node setup!"
        )

        b  = col.box()
        bc = b.column()
        bc.prop( P, "source_folder"      )
        bc.prop( P, "destination_folder" )

        col.operator( 'render.batch_convert' )

class batchConverterProps( bpy.types.PropertyGroup ):
    source_folder = bpy.props.StringProperty(
        description = "Folder of source files",
        name        = "Source folder",
        subtype     = 'FILE_PATH'
    )

    destination_folder = bpy.props.StringProperty(
        description = "Folder of destination files",
        name        = "Destination folder",
        subtype     = 'FILE_PATH'
    )

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.batch_convertor_properties = bpy.props.PointerProperty(
        type = batchConverterProps
    )

def unregister():
    bpy.utils.unregister_module(__name__)