import maya.cmds as cmds
## @package voxelMesher
#  Mesh voxelization UI class
#
#  Takes user input and uses it in mesh voxelization

## Main mesh voxelization class
#
#  Handles input parsing and general user interface
class voxelMesher():
    
    ## Constructor of voxelMesher class
    def __init__(self) :
        
        filePath = cmds.file('voxelize.png', q=True, loc=True)
        
        self.mainWindow = cmds.window(title = 'Mesh Voxelizer', width=300, height=430, sizeable=False, menuBar=True)
        self.windowForm = cmds.formLayout(numberOfDivisions=100)
        self.helpMenu = cmds.menu(l='Help', helpMenu=True, p=self.mainWindow)
        self.helpMenuItem = cmds.menuItem(l='Voxelizer Help', c=self.printHelp)
        self.aboutMenuItem = cmds.menuItem(l='About Voxelizer', c=self.printAbout)
        self.windowImg = cmds.image(h=125, w=280, i=filePath, p=self.windowForm)
        self.meshInputTxt = cmds.text(l='Mesh to Voxelize: ', width=100,height=25, p=self.windowForm)
        self.meshInput = cmds.textField(w=95, h=25, p=self.windowForm)
        self.meshInputButton = cmds.button(label='Load',width=40,height=25 , command=self.loadSelected, p=self.windowForm)
        self.voxelResTxt = cmds.text(l='Voxel Resolution: ', width=100,height=25, p=self.windowForm)
        self.voxelResSlider = cmds.intSliderGrp( field=True, minValue=10, maxValue=50, value=10, p=self.windowForm)
        self.animatedTxt = cmds.text(l='Animated: ', width=70, height=25, p=self.windowForm)
        self.animatedCheck = cmds.checkBox(l='On', width=50, height=25)
        self.meshVoxelButton = cmds.button(label='Voxelize',width=100,height=25, command=self.toVoxel, p=self.windowForm)
        self.renderText = cmds.text(l='Render Options:', width = 100, height = 25, p=self.windowForm)
        self.framesText = cmds.text(l='Frames: ', width = 60, height=25, p=self.windowForm)
        self.renderFrames = cmds.intFieldGrp(nf=2, w=200, h=25, p=self.windowForm)
        self.renderButton = cmds.button(label='Render',width=100,height=25, command=self.renderScene, p=self.windowForm)
        self.cameraInputTxt = cmds.text(l='Camera: ', width=100,height=25, p=self.windowForm)
        self.cameraInput = cmds.textField(w=70, h=25,tx='persp', p=self.windowForm)
        self.cameraInputButton1 = cmds.button(label='Load',width=40,height=25 , command=self.loadCamera, p=self.windowForm)
        self.cameraInputButton2 = cmds.button(label='Default',width=50,height=25 , command=self.defaultCamera, p=self.windowForm)
        
        cmds.formLayout(self.windowForm, edit=True, attachForm=[(self.windowImg, 'top', 5), (self.windowImg, 'left', 10),
         (self.meshInputTxt, 'top', 150), (self.meshInputTxt, 'left', 25),
         (self.meshInput, 'top', 150), (self.meshInput, 'left', 140),
         (self.meshInputButton, 'top', 150), (self.meshInputButton, 'left', 235),
         (self.voxelResTxt, 'top', 180), (self.voxelResTxt, 'left', 25),
         (self.voxelResSlider, 'top', 200), (self.voxelResSlider, 'left', 30),
         (self.animatedTxt, 'top', 230), (self.animatedTxt, 'left', 25),
         (self.animatedCheck, 'top', 230), (self.animatedCheck, 'left', 180),
         (self.renderText, 'top', 260), (self.renderText, 'left', 25),
         (self.framesText, 'top', 290), (self.framesText, 'left', 25),
         (self.renderFrames, 'top', 290), (self.renderFrames, 'left', 110),
         (self.cameraInputTxt, 'top', 320), (self.cameraInputTxt, 'left', 5),
         (self.cameraInput, 'top', 320), (self.cameraInput, 'left', 110),
         (self.cameraInputButton1, 'top', 320), (self.cameraInputButton1, 'left', 185),
         (self.cameraInputButton2, 'top', 320), (self.cameraInputButton2, 'left', 225),
         (self.meshVoxelButton, 'top', 370), (self.meshVoxelButton, 'left', 30),
         (self.renderButton, 'top', 370), (self.renderButton, 'left', 175)])
        cmds.showWindow(self.mainWindow)
    
    ## Loads the selected mesh to the 'mesh to voxelize' text field in the UI  
    #  @param self The pointer to the UI elements  
    def loadSelected(self, *args) :
        obj = cmds.ls(sl=True)
        if len(obj) > 0:
            cmds.textField(self.meshInput,e=True, tx=obj[0])
    
    ## Loads the selected object to the 'render camera' text field in the UI
    #  @param self The pointer to the UI elements
    def loadCamera(self, *args) :
        obj = cmds.ls(sl=True)
        if len(obj) > 0:
            cmds.textField(self.cameraInput,e=True, tx=obj[0])
            
    ## Resets the 'render camera' text field in the UI to 'persp' for perspective camera rendering
    #  @param self The pointer to the UI elements
    def defaultCamera(self,*args):
        cmds.textField(self.cameraInput,e=True, tx='persp')
    
    ## Main voxelization function
    #  @param self The pointer to the UI elements
    #
    #  Checks the validity of the input mesh and camera text fields of the UI, throwing respective error messages for invalid input
    #  Calls custom voxelMesh command to voxelize the mesh from user input parameters
    def toVoxel(self, *args):
        meshName = cmds.textField(self.meshInput, q=True, tx=True)
        if len(meshName) == 0:
           cmds.confirmDialog(title='Error', message='No mesh loaded to voxelize.', button=['OK'], defaultButton = 'OK')
        else:
            resolution = cmds.intSliderGrp(self.voxelResSlider, q=True, v=True)
            
            animationOn = cmds.checkBox(self.animatedCheck, q=True, v=True)
            
            if animationOn == False:
                
                skinned = False
                checkSkinning = cmds.ls(meshName, dag=True)
                for i in range (0,len(checkSkinning)):
                    if checkSkinning[i] == meshName+'Shape1Orig' or checkSkinning[i] == meshName+'ShapeOrig':
                        skinned = True

                meshDuplicate = cmds.duplicate(meshName)
                print meshDuplicate[0]                  
                meshBbox = cmds.exactWorldBoundingBox(meshName)
                                
                if skinned == True:
                    cmds.showHidden(meshName)
                    
                    voxelGroupName = meshName+'1VoxelGroup'
                    if cmds.objExists(voxelGroupName):
                        cmds.delete(voxelGroupName)
                    skinDuplicateName = meshName+'1'
                    cmds.rename(meshDuplicate[0], skinDuplicateName)
                    
                    cmds.voxelMesh(skinDuplicateName, meshBbox, resolution)
                    cmds.delete(skinDuplicateName)
                    
                    cmds.hide(meshName)
                    
                else:
                    cmds.showHidden(meshName)
                    
                    voxelGroupName = meshName+'VoxelGroup'
                    if cmds.objExists(voxelGroupName):
                        cmds.delete(voxelGroupName)
                    
                    cmds.makeIdentity(meshDuplicate[0], a=True, t=True, r=True, s=True, n=0)
                    meshBbox = cmds.exactWorldBoundingBox(meshDuplicate[0])
                    
                    cmds.voxelMesh(meshName, meshBbox, resolution)
                    cmds.delete(meshDuplicate)
                    
                    cmds.hide(meshName)

            else:
                
                skinned = False
                checkSkinning = cmds.ls(meshName, dag=True)
                for i in range (0,len(checkSkinning)):
                    if checkSkinning[i] == meshName+'Shape1Orig' or checkSkinning[i] == meshName+'ShapeOrig':
                        skinned = True
                
                if skinned == False:
                    expressionCmd = 'python(\"vox.animatedVoxelization(\'' + meshName + '\',' + str(resolution) + ')\");'
                    cmds.expression(s=expressionCmd)
                else:
                    expressionCmdSkinned = 'python(\"vox.animatedSkinnedVoxelization(\'' + meshName + '\',' + str(resolution) + ')\");'
                    cmds.expression(s=expressionCmdSkinned)
    
    ## Updates the current frame and voxelizes the mesh
    #  @param self The pointer to the UI elements
    #  @param name The name of the mesh to voxelize
    #  @param res The resolution for voxelization
    #
    #  This function is called in the expression editor for voxelization of animated meshes
    def animatedVoxelization(self, name, res):
        
        time = cmds.currentTime(q=True)
        cmds.currentTime(time, e=True, u=False)
        cmds.currentTime(time, e=True, u=True)
        
        cmds.showHidden(name)
        
        voxelGroupName = name+'VoxelGroup'
        if cmds.objExists(voxelGroupName):
            cmds.delete(voxelGroupName)
        
        meshDuplicate = cmds.duplicate(name) 
        cmds.makeIdentity(meshDuplicate[0], a=True, t=True, r=True, s=True, n=0)
        meshBbox = cmds.exactWorldBoundingBox(meshDuplicate[0])
        cmds.delete(meshDuplicate)
        
        cmds.voxelMesh(name, meshBbox, res)
        
        cmds.hide(name)
    
    ## Updates the current frame and voxelizes the skinned mesh
    #  @param self The pointer to the UI elements
    #  @param name The name of the mesh to voxelize
    #  @param res The resolution for voxelization
    #
    #  This function is called in the expression editor for voxelization of animated skinned meshes
    def animatedSkinnedVoxelization(self, name, res):
        
        time = cmds.currentTime(q=True)
        cmds.currentTime(time, e=True, u=False)
        cmds.currentTime(time, e=True, u=True)
        
        cmds.showHidden(name)
        voxelGroupName = name+'1VoxelGroup'
        if cmds.objExists(voxelGroupName):
            cmds.delete(voxelGroupName)
        
        meshDuplicate = cmds.duplicate(name) 
        meshBbox = cmds.exactWorldBoundingBox(meshDuplicate[0])
            
        skinDuplicateName = name+'1'
        cmds.rename(meshDuplicate[0], skinDuplicateName)
        
        cmds.voxelMesh(skinDuplicateName, meshBbox, res)
        
        cmds.delete(skinDuplicateName)
        cmds.hide(name)
        
    ## Batch renders the scene using input parameters
    #  @param self The pointer to the UI elements
    #
    #  The function checks the validity of the input camera before render and renders using the set render settings defined in Maya
    def renderScene(self,*args):
        minFrame = cmds.intFieldGrp(self.renderFrames, q=True, value1=True)
        maxFrame = cmds.intFieldGrp(self.renderFrames, q=True, value2=True)
        
        if minFrame < 0 or maxFrame <= 0:
            cmds.confirmDialog(title='Error', message='Please enter a valid frame range.', button=['OK'], defaultButton='OK')
        else:
            cameraName = cmds.textField(self.cameraInput, q=True, tx=True)
            camList = cmds.ls(cameras=True)
            validCam = False
            for obj in camList:
                cam = obj[:-5]
                if cameraName == cam:
                    validCam=True
                    break
            if validCam == True:
                for i in range (minFrame,maxFrame+1):
                    cmds.currentTime(i, e=True, u=False)
                    cmds.currentTime(i, e=True, u=True)
                    cmds.render(cameraName)
            else:
                cmds.confirmDialog(title='Error', message='Please load valid camera or use default.', button=['OK'], defaultButton='OK')
                
    ## Prints the help menu
    #  @param self The pointer to the UI elements
    def printHelp(self, *args):
        helpText = "Mesh Voxelizer Help:"
        text1 = "\n\nLoad -\nLoads the currently selected mesh"
        text2 = "\n\nVoxel Resolution -\nDensity of voxelization"
        text3 = "\n\nVoxelize -\nVoxelizes loaded mesh based on resolution"
        text4 = "\n\nAnimeted -\nSelect if mesh to voxelize is intended for animation"
        text5 = "\n\nFrames -\nIndicate start/end frames to render"
        text6 = "\n\nCamera -\nSelect and load selected camera to use in rendering\n\'Default\' will reset the selected camera to perspective"
        text7 = "\n\nRender -\nRender the scene using indicated start/end frames and loaded camera"
        text8 = "\n\n\nPlease note that this plugin works on closed meshes only\nRender works based on render settings for the scene"
        text9 = "\n\nFor more information, please consult the User Documentation"
        helpText = helpText + text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9
        cmds.confirmDialog(title='Help', message=helpText, button=['OK'], defaultButton = 'OK')
    
    ## Prints information about the mesh voxelizer tool
    #  @param self The pointer to the UI elements
    def printAbout(self, *args):
        aboutText = "About Mesh Voxelizer:"
        text1 = "\n\nAuthor:\tRamesh Balachandran"
        text2 = "\nVersion:\tMesh Voxelizer Version 1.0 2014"
        aboutText = aboutText + text1 + text2
        cmds.confirmDialog(title='About', message=aboutText, button=['OK'], defaultButton = 'OK')
        
                      
vox = voxelMesher()